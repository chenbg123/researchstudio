from dataclasses import dataclass
from datetime import datetime, timezone

from hashlib import pbkdf2_hmac
import secrets
import base64

from sqlalchemy.orm import Session

from app.db.models.user import User


def _hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    dk = pbkdf2_hmac("sha256", password.encode(), salt, 260000)
    return base64.b64encode(salt + dk).decode()


def _verify_password(password: str, stored_hash: str) -> bool:
    raw = base64.b64decode(stored_hash)
    salt, dk = raw[:16], raw[16:]
    new_dk = pbkdf2_hmac("sha256", password.encode(), salt, 260000)
    return secrets.compare_digest(dk, new_dk)


@dataclass
class HeaderIdentity:
    identifier: str
    display_name: str
    email: str | None = None


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def create_local_user(self, *, username: str, password: str, display_name: str, role: str) -> User:
        user = User(
            provider="local",
            identifier=username,
            password_hash=_hash_password(password),
            display_name=display_name,
            role=role,
            status="active",
            metadata_json={},
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def verify_local_password(self, user: User, password: str) -> bool:
        return bool(user.password_hash and _verify_password(password, user.password_hash))

    def upsert_header_user(self, identity: HeaderIdentity) -> User:
        user = self.db.query(User).filter_by(provider="oa-header", identifier=identity.identifier).one_or_none()
        if user is None:
            user = User(
                provider="oa-header",
                identifier=identity.identifier,
                display_name=identity.display_name,
                email=identity.email,
                role="user",
                status="active",
                metadata_json={},
            )
            self.db.add(user)
        else:
            user.display_name = identity.display_name
            user.email = identity.email
        user.last_login_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(user)
        return user
