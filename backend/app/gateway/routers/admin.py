from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.models.admin_visibility import AdminVisibility
from app.db.models.user import User
from app.db.session import get_db_session
from app.services.auth import AuthService, _hash_password
from app.services.visibility import VisibilityService

router = APIRouter(prefix="/api/admin", tags=["admin"])


# --- Request/Response schemas ---


class CreateUserRequest(BaseModel):
    username: str
    password: str
    display_name: str
    role: str = "user"


class ResetPasswordRequest(BaseModel):
    password: str


class UserResponse(BaseModel):
    id: UUID
    provider: str
    identifier: str
    display_name: str
    role: str
    status: str

    model_config = {"from_attributes": True}


class UsersListResponse(BaseModel):
    users: list[UserResponse]


class VisibilityUpdateRequest(BaseModel):
    enabled: bool


class VisibilityRuleResponse(BaseModel):
    category: str
    key: str
    enabled: bool

    model_config = {"from_attributes": True}


class VisibilityRulesResponse(BaseModel):
    rules: list[VisibilityRuleResponse]


# --- Dependencies ---


def require_admin():
    # Placeholder: will be replaced with real auth check in Task 5
    return {"id": "admin-placeholder", "role": "admin"}


# --- Endpoints ---


@router.post("/users", status_code=201)
def create_user(request: CreateUserRequest, db: Session = Depends(get_db_session), _admin=Depends(require_admin)) -> UserResponse:
    service = AuthService(db)
    user = service.create_local_user(
        username=request.username,
        password=request.password,
        display_name=request.display_name,
        role=request.role,
    )
    return UserResponse.model_validate(user)


@router.get("/users")
def list_users(db: Session = Depends(get_db_session), _admin=Depends(require_admin)) -> UsersListResponse:
    users = db.query(User).order_by(User.created_at.desc()).all()
    return UsersListResponse(users=[UserResponse.model_validate(user) for user in users])


@router.post("/users/{user_id}/disable")
def disable_user(user_id: UUID, db: Session = Depends(get_db_session), _admin=Depends(require_admin)) -> UserResponse:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.status = "disabled"
    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user)


@router.post("/users/{user_id}/reset-password")
def reset_password(user_id: UUID, request: ResetPasswordRequest, db: Session = Depends(get_db_session), _admin=Depends(require_admin)) -> UserResponse:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.password_hash = _hash_password(request.password)
    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user)


# --- Visibility endpoints ---


@router.put("/visibility/{category}/{key}")
def update_visibility(category: str, key: str, request: VisibilityUpdateRequest, db: Session = Depends(get_db_session), _admin=Depends(require_admin)) -> VisibilityRuleResponse:
    rule = VisibilityService(db).set_rule(category=category, key=key, enabled=request.enabled)
    return VisibilityRuleResponse.model_validate(rule)


@router.get("/visibility")
def list_visibility_rules(db: Session = Depends(get_db_session), _admin=Depends(require_admin)) -> VisibilityRulesResponse:
    rules = db.query(AdminVisibility).all()
    return VisibilityRulesResponse(rules=[VisibilityRuleResponse.model_validate(rule) for rule in rules])
