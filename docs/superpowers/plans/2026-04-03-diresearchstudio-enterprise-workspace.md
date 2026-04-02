# DiResearchStudio Enterprise Workspace Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn DeerFlow into a PostgreSQL-backed multi-user enterprise workspace named DiResearchStudio with local login, future trusted-header SSO, database-backed conversation persistence, admin management, enterprise workspace UI, and admin visibility controls for modes/profiles, skills, and MCP.

**Architecture:** Keep the existing LangGraph runtime and gateway split, but add an application persistence layer in the FastAPI gateway backed by PostgreSQL for users, threads, messages, and elements. Use Better Auth in the Next.js app for session handling, with one unified local user model that supports both local password login and future trusted-header auto-provisioning. Preserve the current workspace information architecture while replacing the landing page with login, adding admin surfaces, and redesigning the workspace shell into a production-oriented enterprise layout.

**Tech Stack:** FastAPI, PostgreSQL, SQLAlchemy + Alembic, Better Auth, Next.js 16 App Router, React 19, TypeScript 5.8, TanStack Query, Tailwind CSS 4, pnpm, pytest, ruff, TypeScript typecheck

---

## File Structure

### Backend application persistence and auth
- Create: `backend/app/db/__init__.py`
- Create: `backend/app/db/base.py`
- Create: `backend/app/db/session.py`
- Create: `backend/app/db/models/__init__.py`
- Create: `backend/app/db/models/user.py`
- Create: `backend/app/db/models/chat_thread.py`
- Create: `backend/app/db/models/chat_message.py`
- Create: `backend/app/db/models/chat_element.py`
- Create: `backend/app/db/models/admin_visibility.py`
- Create: `backend/app/db/repositories/users.py`
- Create: `backend/app/db/repositories/threads.py`
- Create: `backend/app/db/repositories/messages.py`
- Create: `backend/app/db/repositories/elements.py`
- Create: `backend/app/db/repositories/visibility.py`
- Create: `backend/app/db/alembic.ini`
- Create: `backend/app/db/alembic/env.py`
- Create: `backend/app/db/alembic/versions/<timestamp>_init_diresearchstudio_schema.py`
- Create: `backend/app/services/auth.py`
- Create: `backend/app/services/thread_persistence.py`
- Create: `backend/app/services/visibility.py`
- Modify: `backend/app/gateway/deps.py`
- Modify: `backend/app/gateway/app.py`
- Modify: `backend/app/gateway/routers/threads.py`
- Modify: `backend/app/gateway/routers/uploads.py`
- Modify: `backend/app/gateway/routers/artifacts.py`
- Modify: `backend/app/gateway/routers/mcp.py`
- Modify: `backend/app/gateway/routers/skills.py`
- Modify: `backend/app/gateway/routers/agents.py`
- Create: `backend/app/gateway/routers/admin.py`
- Modify: `backend/app/gateway/routers/__init__.py`
- Modify: `backend/app/gateway/config.py`

### Frontend auth, admin, and enterprise workspace
- Create: `frontend/src/server/auth-schema.ts`
- Modify: `frontend/src/server/better-auth/config.ts`
- Modify: `frontend/src/server/better-auth/client.ts`
- Modify: `frontend/src/server/better-auth/server.ts`
- Modify: `frontend/src/app/api/auth/[...all]/route.ts`
- Create: `frontend/src/app/login/page.tsx`
- Modify: `frontend/src/app/page.tsx`
- Modify: `frontend/src/app/layout.tsx`
- Create: `frontend/src/app/workspace/admin/page.tsx`
- Create: `frontend/src/app/workspace/admin/users/page.tsx`
- Create: `frontend/src/app/workspace/admin/conversations/page.tsx`
- Create: `frontend/src/app/workspace/admin/capabilities/page.tsx`
- Modify: `frontend/src/app/workspace/layout.tsx`
- Modify: `frontend/src/app/workspace/page.tsx`
- Modify: `frontend/src/app/workspace/chats/page.tsx`
- Modify: `frontend/src/app/workspace/chats/[thread_id]/page.tsx`
- Modify: `frontend/src/components/workspace/workspace-sidebar.tsx`
- Modify: `frontend/src/components/workspace/workspace-header.tsx`
- Modify: `frontend/src/components/workspace/workspace-nav-chat-list.tsx`
- Modify: `frontend/src/components/workspace/recent-chat-list.tsx`
- Modify: `frontend/src/components/workspace/chats/chat-box.tsx`
- Modify: `frontend/src/components/workspace/input-box.tsx`
- Modify: `frontend/src/components/workspace/messages/message-list.tsx`
- Modify: `frontend/src/components/workspace/workspace-container.tsx`
- Create: `frontend/src/components/workspace/admin/admin-shell.tsx`
- Create: `frontend/src/components/workspace/admin/user-table.tsx`
- Create: `frontend/src/components/workspace/admin/conversation-table.tsx`
- Create: `frontend/src/components/workspace/admin/capability-visibility-panel.tsx`
- Create: `frontend/src/core/auth/api.ts`
- Create: `frontend/src/core/auth/hooks.ts`
- Create: `frontend/src/core/auth/types.ts`
- Modify: `frontend/src/core/threads/hooks.ts`
- Modify: `frontend/src/core/threads/types.ts`
- Modify: `frontend/src/core/skills/api.ts`
- Modify: `frontend/src/core/mcp/api.ts`
- Create: `frontend/src/core/admin/api.ts`
- Create: `frontend/src/core/admin/hooks.ts`
- Create: `frontend/src/core/admin/types.ts`
- Modify: `frontend/src/env.js`

### Config and docs
- Modify: `config.example.yaml`
- Modify: `backend/pyproject.toml`
- Modify: `frontend/package.json`
- Modify: `README.md`
- Modify: `README_zh.md`
- Modify: `backend/CLAUDE.md`
- Modify: `frontend/CLAUDE.md`

### Tests
- Create: `backend/tests/db/test_models.py`
- Create: `backend/tests/services/test_auth_service.py`
- Create: `backend/tests/services/test_thread_persistence.py`
- Create: `backend/tests/routers/test_admin_router.py`
- Modify: `backend/tests/test_threads_router.py`
- Create: `frontend/src/core/auth/__tests__/auth-schema.test.ts` *(only if a frontend test runner is added in Task 9; otherwise skip and rely on `pnpm check` + manual verification)*

---

### Task 1: Add PostgreSQL persistence foundation

**Files:**
- Create: `backend/app/db/base.py`
- Create: `backend/app/db/session.py`
- Create: `backend/app/db/models/__init__.py`
- Create: `backend/app/db/models/user.py`
- Create: `backend/app/db/models/chat_thread.py`
- Create: `backend/app/db/models/chat_message.py`
- Create: `backend/app/db/models/chat_element.py`
- Create: `backend/app/db/models/admin_visibility.py`
- Create: `backend/app/db/alembic/env.py`
- Create: `backend/app/db/alembic/versions/<timestamp>_init_diresearchstudio_schema.py`
- Modify: `backend/pyproject.toml`
- Modify: `config.example.yaml`
- Test: `backend/tests/db/test_models.py`

- [ ] **Step 1: Write the failing backend model test**

```python
from app.db.models import AdminVisibility, ChatElement, ChatMessage, ChatThread, User


def test_models_expose_expected_tables():
    assert User.__tablename__ == "users"
    assert ChatThread.__tablename__ == "chat_threads"
    assert ChatMessage.__tablename__ == "chat_messages"
    assert ChatElement.__tablename__ == "chat_elements"
    assert AdminVisibility.__tablename__ == "admin_visibility_rules"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /home/jetson/deer-flow/backend && pytest tests/db/test_models.py -q`
Expected: FAIL with `ModuleNotFoundError` or missing model/table definitions.

- [ ] **Step 3: Add database dependencies**

```toml
[project]
dependencies = [
    "deerflow-harness",
    "fastapi>=0.115.0",
    "sqlalchemy>=2.0.40",
    "alembic>=1.15.2",
    "psycopg[binary]>=3.2.6",
    "python-multipart>=0.0.20",
]

[dependency-groups]
dev = ["pytest>=8.0.0", "ruff>=0.14.11"]
```

- [ ] **Step 4: Create the shared declarative base**

```python
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
```

- [ ] **Step 5: Create the DB session factory**

```python
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.gateway.config import get_gateway_settings

_settings = get_gateway_settings()
_engine = create_engine(_settings.database_url, future=True, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=_engine, autoflush=False, autocommit=False, class_=Session)


def get_db_session() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

- [ ] **Step 6: Implement the core ORM models**

```python
import uuid
from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, Index, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("provider", "identifier", name="uq_users_provider_identifier"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    identifier: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str | None] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(32), default="user")
    status: Mapped[str] = mapped_column(String(32), default="active")
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255))
    metadata_json: Mapped[dict] = mapped_column("metadata", JSONB().with_variant(JSON(), "sqlite"), default=dict)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
```

- [ ] **Step 7: Implement the thread/message/element/admin visibility models**

```python
class ChatThread(Base):
    __tablename__ = "chat_threads"
    __table_args__ = (Index("ix_chat_threads_user_updated", "user_id", "updated_at"),)

    id: Mapped[str] = mapped_column(String(128), primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), default="New Chat")
    profile_key: Mapped[str] = mapped_column(String(100), default="default")
    agent_key: Mapped[str | None] = mapped_column(String(100))
    metadata_json: Mapped[dict] = mapped_column("metadata", JSONB().with_variant(JSON(), "sqlite"), default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    __table_args__ = (Index("ix_chat_messages_thread_index", "thread_id", "message_index"),)

    id: Mapped[str] = mapped_column(String(128), primary_key=True)
    thread_id: Mapped[str] = mapped_column(ForeignKey("chat_threads.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    role: Mapped[str] = mapped_column(String(32), nullable=False)
    content: Mapped[list[dict] | dict] = mapped_column(JSONB().with_variant(JSON(), "sqlite"), nullable=False)
    text_content: Mapped[str | None] = mapped_column(Text)
    message_index: Mapped[int] = mapped_column(nullable=False)
    metadata_json: Mapped[dict] = mapped_column("metadata", JSONB().with_variant(JSON(), "sqlite"), default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ChatElement(Base):
    __tablename__ = "chat_elements"

    id: Mapped[str] = mapped_column(String(128), primary_key=True)
    thread_id: Mapped[str] = mapped_column(ForeignKey("chat_threads.id", ondelete="CASCADE"), nullable=False)
    message_id: Mapped[str | None] = mapped_column(ForeignKey("chat_messages.id", ondelete="SET NULL"))
    user_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    mime: Mapped[str | None] = mapped_column(String(255))
    size: Mapped[int | None]
    storage_provider: Mapped[str] = mapped_column(String(32), default="local")
    object_key: Mapped[str | None] = mapped_column(String(500))
    url: Mapped[str | None] = mapped_column(String(1000))
    source: Mapped[str] = mapped_column(String(50), default="generated")
    metadata_json: Mapped[dict] = mapped_column("metadata", JSONB().with_variant(JSON(), "sqlite"), default=dict)
    props: Mapped[dict] = mapped_column(JSONB().with_variant(JSON(), "sqlite"), default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class AdminVisibility(Base):
    __tablename__ = "admin_visibility_rules"
    __table_args__ = (UniqueConstraint("category", "key", name="uq_visibility_category_key"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category: Mapped[str] = mapped_column(String(32), nullable=False)
    key: Mapped[str] = mapped_column(String(255), nullable=False)
    enabled: Mapped[bool] = mapped_column(default=True)
```

- [ ] **Step 8: Create the initial Alembic migration**

```python
def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("provider", sa.String(length=50), nullable=False),
        sa.Column("identifier", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255)),
        sa.Column("role", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("display_name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255)),
        sa.Column("metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("last_login_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("provider", "identifier", name="uq_users_provider_identifier"),
    )
```

- [ ] **Step 9: Add config entries for the application database**

```yaml
gateway:
  database_url: postgresql+psycopg://postgres:postgres@localhost:5432/diresearchstudio
  trusted_header_auth_enabled: false
  trusted_header_user_id: X-User-Id
  trusted_header_display_name: X-User-Name
  trusted_header_email: X-User-Email
```

- [ ] **Step 10: Run the model test and migration smoke check**

Run: `cd /home/jetson/deer-flow/backend && pytest tests/db/test_models.py -q`
Expected: PASS

Run: `cd /home/jetson/deer-flow/backend && alembic -c app/db/alembic.ini upgrade head`
Expected: migration applies cleanly.

- [ ] **Step 11: Commit**

```bash
git add backend/app/db backend/pyproject.toml config.example.yaml backend/tests/db/test_models.py
git commit -m "feat: add postgres persistence foundation"
```

### Task 2: Add backend auth services and admin user management

**Files:**
- Create: `backend/app/services/auth.py`
- Create: `backend/app/db/repositories/users.py`
- Create: `backend/app/gateway/routers/admin.py`
- Modify: `backend/app/gateway/deps.py`
- Modify: `backend/app/gateway/app.py`
- Modify: `backend/app/gateway/routers/__init__.py`
- Test: `backend/tests/services/test_auth_service.py`
- Test: `backend/tests/routers/test_admin_router.py`

- [ ] **Step 1: Write the failing auth service test**

```python
from app.services.auth import AuthService


def test_create_local_user_hashes_password(fake_session):
    service = AuthService(fake_session)

    user = service.create_local_user(
        username="alice",
        password="s3cret123",
        display_name="Alice",
        role="user",
    )

    assert user.identifier == "alice"
    assert user.provider == "local"
    assert user.password_hash is not None
    assert user.password_hash != "s3cret123"
```

- [ ] **Step 2: Write the failing admin router test**

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.gateway.routers import admin


def test_admin_can_create_user(monkeypatch):
    app = FastAPI()
    app.include_router(admin.router, prefix="/api/admin")

    monkeypatch.setattr(admin, "require_admin", lambda: {"id": "admin-1", "role": "admin"})

    with TestClient(app) as client:
        response = client.post(
            "/api/admin/users",
            json={
                "username": "bob",
                "password": "12345678",
                "display_name": "Bob",
                "role": "user",
            },
        )

    assert response.status_code == 201
    assert response.json()["identifier"] == "bob"
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `cd /home/jetson/deer-flow/backend && pytest tests/services/test_auth_service.py tests/routers/test_admin_router.py -q`
Expected: FAIL with missing service/router implementations.

- [ ] **Step 4: Implement the auth service**

```python
from dataclasses import dataclass
from datetime import datetime, timezone

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.db.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
            password_hash=pwd_context.hash(password),
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
        return bool(user.password_hash and pwd_context.verify(password, user.password_hash))

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
```

- [ ] **Step 5: Implement the admin router contracts**

```python
@router.post("/users", status_code=201)
def create_user(request: CreateUserRequest, db: Session = Depends(get_db)) -> UserResponse:
    user = AuthService(db).create_local_user(
        username=request.username,
        password=request.password,
        display_name=request.display_name,
        role=request.role,
    )
    return UserResponse.model_validate(user)


@router.get("/users")
def list_users(db: Session = Depends(get_db)) -> UsersListResponse:
    users = db.query(User).order_by(User.created_at.desc()).all()
    return UsersListResponse(users=[UserResponse.model_validate(user) for user in users])
```

- [ ] **Step 6: Add disable/reset-password admin endpoints**

```python
@router.post("/users/{user_id}/disable")
def disable_user(user_id: UUID, db: Session = Depends(get_db)) -> UserResponse:
    user = db.get(User, user_id)
    user.status = "disabled"
    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user)


@router.post("/users/{user_id}/reset-password")
def reset_password(user_id: UUID, request: ResetPasswordRequest, db: Session = Depends(get_db)) -> UserResponse:
    user = db.get(User, user_id)
    user.password_hash = pwd_context.hash(request.password)
    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user)
```

- [ ] **Step 7: Wire the router into the FastAPI app**

```python
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
```

- [ ] **Step 8: Run tests to verify they pass**

Run: `cd /home/jetson/deer-flow/backend && pytest tests/services/test_auth_service.py tests/routers/test_admin_router.py -q`
Expected: PASS

- [ ] **Step 9: Commit**

```bash
git add backend/app/services/auth.py backend/app/db/repositories/users.py backend/app/gateway/routers/admin.py backend/app/gateway/app.py backend/tests/services/test_auth_service.py backend/tests/routers/test_admin_router.py
git commit -m "feat: add admin-managed user auth services"
```

### Task 3: Persist threads, full messages, and elements in PostgreSQL

**Files:**
- Create: `backend/app/services/thread_persistence.py`
- Create: `backend/app/db/repositories/threads.py`
- Create: `backend/app/db/repositories/messages.py`
- Create: `backend/app/db/repositories/elements.py`
- Modify: `backend/app/gateway/routers/threads.py`
- Modify: `backend/app/gateway/routers/uploads.py`
- Modify: `backend/app/gateway/routers/artifacts.py`
- Test: `backend/tests/services/test_thread_persistence.py`
- Modify: `backend/tests/test_threads_router.py`

- [ ] **Step 1: Write the failing persistence service test**

```python
from app.services.thread_persistence import ThreadPersistenceService


def test_upsert_thread_snapshot_persists_messages(fake_session):
    service = ThreadPersistenceService(fake_session)

    service.upsert_thread_snapshot(
        user_id="00000000-0000-0000-0000-000000000001",
        thread_id="thread-1",
        title="Quarterly Research",
        profile_key="default",
        messages=[
            {"id": "m1", "type": "human", "content": [{"type": "text", "text": "hello"}]},
            {"id": "m2", "type": "ai", "content": [{"type": "text", "text": "world"}]},
        ],
        artifacts=[],
    )

    snapshot = service.get_thread("thread-1")
    assert snapshot.title == "Quarterly Research"
    assert len(snapshot.messages) == 2
    assert snapshot.messages[0].text_content == "hello"
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `cd /home/jetson/deer-flow/backend && pytest tests/services/test_thread_persistence.py -q`
Expected: FAIL because the persistence service does not exist yet.

- [ ] **Step 3: Implement message normalization helpers**

```python
def infer_role(message: dict) -> str:
    message_type = message.get("type")
    return {
        "human": "user",
        "ai": "assistant",
        "tool": "tool",
        "system": "system",
    }.get(message_type, "assistant")


def text_from_content(content: object) -> str | None:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = [block.get("text", "") for block in content if isinstance(block, dict) and block.get("type") == "text"]
        return "\n".join(part for part in parts if part) or None
    return None
```

- [ ] **Step 4: Implement thread snapshot upsert logic**

```python
class ThreadPersistenceService:
    def __init__(self, db: Session):
        self.db = db

    def upsert_thread_snapshot(self, *, user_id: UUID, thread_id: str, title: str, profile_key: str, messages: list[dict], artifacts: list[str]) -> None:
        thread = self.db.get(ChatThread, thread_id)
        if thread is None:
            thread = ChatThread(id=thread_id, user_id=user_id, title=title, profile_key=profile_key, metadata_json={})
            self.db.add(thread)
        else:
            thread.title = title
            thread.profile_key = profile_key

        self.db.query(ChatMessage).filter(ChatMessage.thread_id == thread_id).delete()
        for index, message in enumerate(messages):
            self.db.add(
                ChatMessage(
                    id=message.get("id", f"{thread_id}-{index}"),
                    thread_id=thread_id,
                    user_id=user_id,
                    role=infer_role(message),
                    content=message.get("content", []),
                    text_content=text_from_content(message.get("content")),
                    message_index=index,
                    metadata_json={"raw_type": message.get("type")},
                )
            )
        self.db.commit()
```

- [ ] **Step 5: Add element persistence for uploads and generated artifacts**

```python
def register_element(self, *, thread_id: str, user_id: UUID, element_id: str, name: str, mime: str | None, size: int | None, source: str, storage_provider: str, object_key: str | None) -> None:
    element = ChatElement(
        id=element_id,
        thread_id=thread_id,
        user_id=user_id,
        type="file",
        name=name,
        mime=mime,
        size=size,
        source=source,
        storage_provider=storage_provider,
        object_key=object_key,
        metadata_json={},
        props={},
    )
    self.db.merge(element)
    self.db.commit()
```

- [ ] **Step 6: Update the threads router to scope by current user**

```python
@router.get("/search", response_model=list[ThreadResponse])
async def search_threads(request: Request, db: Session = Depends(get_db), current_user: CurrentUser = Depends(require_user)) -> list[ThreadResponse]:
    query = db.query(ChatThread)
    if current_user.role != "admin":
        query = query.filter(ChatThread.user_id == current_user.id)
    threads = query.order_by(ChatThread.updated_at.desc()).all()
    return [to_thread_response(thread) for thread in threads]
```

- [ ] **Step 7: Update upload handling to create `chat_elements` records**

```python
for uploaded in saved_files:
    persistence.register_element(
        thread_id=thread_id,
        user_id=current_user.id,
        element_id=f"upload-{thread_id}-{uploaded.filename}",
        name=uploaded.filename,
        mime=uploaded.content_type,
        size=uploaded.size,
        source="upload",
        storage_provider="local",
        object_key=str(uploaded.virtual_path),
    )
```

- [ ] **Step 8: Keep artifact serving backend-mediated and ownership-checked**

```python
if current_user.role != "admin" and thread.user_id != current_user.id:
    raise HTTPException(status_code=403, detail="Forbidden")
return FileResponse(path, filename=path.name, media_type=media_type)
```

- [ ] **Step 9: Run the tests**

Run: `cd /home/jetson/deer-flow/backend && pytest tests/services/test_thread_persistence.py tests/test_threads_router.py -q`
Expected: PASS

- [ ] **Step 10: Commit**

```bash
git add backend/app/services/thread_persistence.py backend/app/db/repositories/threads.py backend/app/db/repositories/messages.py backend/app/db/repositories/elements.py backend/app/gateway/routers/threads.py backend/app/gateway/routers/uploads.py backend/app/gateway/routers/artifacts.py backend/tests/services/test_thread_persistence.py backend/tests/test_threads_router.py
git commit -m "feat: persist chat threads messages and elements"
```

### Task 4: Add admin visibility controls for modes/profiles, skills, and MCP

**Files:**
- Create: `backend/app/services/visibility.py`
- Create: `backend/app/db/repositories/visibility.py`
- Modify: `backend/app/gateway/routers/admin.py`
- Modify: `backend/app/gateway/routers/skills.py`
- Modify: `backend/app/gateway/routers/mcp.py`
- Modify: `backend/app/gateway/routers/agents.py`
- Test: `backend/tests/routers/test_admin_router.py`

- [ ] **Step 1: Write the failing visibility test**

```python
def test_admin_can_toggle_skill_visibility(client, admin_headers):
    response = client.put(
        "/api/admin/visibility/skills/research-pack",
        headers=admin_headers,
        json={"enabled": False},
    )

    assert response.status_code == 200
    assert response.json() == {
        "category": "skills",
        "key": "research-pack",
        "enabled": False,
    }
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `cd /home/jetson/deer-flow/backend && pytest tests/routers/test_admin_router.py -q`
Expected: FAIL with missing visibility endpoints.

- [ ] **Step 3: Implement the visibility service**

```python
class VisibilityService:
    def __init__(self, db: Session):
        self.db = db

    def set_rule(self, *, category: str, key: str, enabled: bool) -> AdminVisibility:
        rule = self.db.query(AdminVisibility).filter_by(category=category, key=key).one_or_none()
        if rule is None:
            rule = AdminVisibility(category=category, key=key, enabled=enabled)
            self.db.add(rule)
        else:
            rule.enabled = enabled
        self.db.commit()
        self.db.refresh(rule)
        return rule
```

- [ ] **Step 4: Add admin visibility endpoints**

```python
@router.put("/visibility/{category}/{key}")
def update_visibility(category: str, key: str, request: VisibilityUpdateRequest, db: Session = Depends(get_db)) -> VisibilityRuleResponse:
    rule = VisibilityService(db).set_rule(category=category, key=key, enabled=request.enabled)
    return VisibilityRuleResponse.model_validate(rule)


@router.get("/visibility")
def list_visibility_rules(db: Session = Depends(get_db)) -> VisibilityRulesResponse:
    rules = db.query(AdminVisibility).all()
    return VisibilityRulesResponse(rules=[VisibilityRuleResponse.model_validate(rule) for rule in rules])
```

- [ ] **Step 5: Apply visibility filtering to skills and MCP responses**

```python
rules = {rule.key: rule.enabled for rule in visibility_repo.list_enabled_map(category="skills")}
visible_skills = [skill for skill in skills if rules.get(skill.name, True)]
```

```python
rules = {rule.key: rule.enabled for rule in visibility_repo.list_enabled_map(category="mcp")}
visible_servers = {name: server for name, server in config.mcp_servers.items() if rules.get(name, True)}
```

- [ ] **Step 6: Treat modes/profiles as admin-controlled catalog items**

```python
DEFAULT_PROFILES = [
    {"key": "default", "label": "General Research", "enabled": True},
    {"key": "reporting", "label": "Report Drafting", "enabled": True},
]
```

- [ ] **Step 7: Run the admin router tests**

Run: `cd /home/jetson/deer-flow/backend && pytest tests/routers/test_admin_router.py -q`
Expected: PASS

- [ ] **Step 8: Commit**

```bash
git add backend/app/services/visibility.py backend/app/db/repositories/visibility.py backend/app/gateway/routers/admin.py backend/app/gateway/routers/skills.py backend/app/gateway/routers/mcp.py backend/app/gateway/routers/agents.py backend/tests/routers/test_admin_router.py
git commit -m "feat: add admin visibility controls for capabilities"
```

### Task 5: Wire Better Auth to local users and trusted-header SSO

**Files:**
- Create: `frontend/src/server/auth-schema.ts`
- Modify: `frontend/src/server/better-auth/config.ts`
- Modify: `frontend/src/server/better-auth/client.ts`
- Modify: `frontend/src/server/better-auth/server.ts`
- Modify: `frontend/src/app/api/auth/[...all]/route.ts`
- Modify: `frontend/src/env.js`
- Create: `frontend/src/core/auth/types.ts`
- Create: `frontend/src/core/auth/api.ts`
- Create: `frontend/src/core/auth/hooks.ts`

- [ ] **Step 1: Write the failing auth schema check**

```ts
export function assertLoginPayload(payload: unknown) {
  const result = loginSchema.safeParse(payload);
  if (!result.success) {
    throw new Error("invalid payload");
  }
  return result.data;
}
```

- [ ] **Step 2: Run typecheck to verify the auth modules do not exist yet**

Run: `cd /home/jetson/deer-flow/frontend && pnpm typecheck`
Expected: FAIL after temporarily importing the future auth helpers from one page.

- [ ] **Step 3: Define the login payload schema**

```ts
import { z } from "zod";

export const loginSchema = z.object({
  username: z.string().min(1),
  password: z.string().min(8),
});

export type LoginPayload = z.infer<typeof loginSchema>;
```

- [ ] **Step 4: Extend Better Auth config to use backend-backed credentials**

```ts
import { betterAuth } from "better-auth";

import { loginWithPassword, resolveTrustedHeaderUser } from "@/core/auth/api";
import { env } from "@/env";

export const auth = betterAuth({
  emailAndPassword: {
    enabled: true,
    async authorize(credentials) {
      return loginWithPassword(credentials.email, credentials.password);
    },
  },
  trustedOrigins: [env.NEXT_PUBLIC_BACKEND_BASE_URL ?? "http://localhost:3000"],
  hooks: {
    after: [
      {
        matcher: () => env.TRUSTED_HEADER_AUTH_ENABLED === "true",
        handler: async (ctx) => {
          await resolveTrustedHeaderUser(ctx.request);
        },
      },
    ],
  },
});
```

- [ ] **Step 5: Add frontend auth API helpers**

```ts
export async function loginWithPassword(username: string, password: string) {
  const response = await fetch(`${getBackendBaseURL()}/api/admin/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
    credentials: "include",
  });
  if (!response.ok) throw new Error("Login failed");
  return response.json() as Promise<AuthSession>;
}

export async function fetchSession() {
  const response = await fetch(`${getBackendBaseURL()}/api/admin/auth/session`, {
    credentials: "include",
  });
  if (!response.ok) return null;
  return response.json() as Promise<AuthSession>;
}
```

- [ ] **Step 6: Add environment variables for header auth**

```ts
server: {
  BETTER_AUTH_SECRET: z.string().optional(),
  TRUSTED_HEADER_AUTH_ENABLED: z.string().optional(),
  TRUSTED_HEADER_USER_ID: z.string().optional(),
  TRUSTED_HEADER_DISPLAY_NAME: z.string().optional(),
  TRUSTED_HEADER_EMAIL: z.string().optional(),
}
```

- [ ] **Step 7: Expose typed auth hooks**

```ts
export function useSession() {
  return useQuery({
    queryKey: ["auth", "session"],
    queryFn: fetchSession,
  });
}
```

- [ ] **Step 8: Run frontend typecheck**

Run: `cd /home/jetson/deer-flow/frontend && pnpm typecheck`
Expected: PASS

- [ ] **Step 9: Commit**

```bash
git add frontend/src/server/auth-schema.ts frontend/src/server/better-auth/config.ts frontend/src/server/better-auth/client.ts frontend/src/server/better-auth/server.ts frontend/src/core/auth frontend/src/env.js
git commit -m "feat: wire frontend auth to local and header sessions"
```

### Task 6: Replace landing with login and gate workspace access

**Files:**
- Create: `frontend/src/app/login/page.tsx`
- Modify: `frontend/src/app/page.tsx`
- Modify: `frontend/src/app/workspace/page.tsx`
- Modify: `frontend/src/app/layout.tsx`
- Modify: `frontend/src/app/workspace/layout.tsx`
- Modify: `frontend/src/components/workspace/workspace-header.tsx`

- [ ] **Step 1: Write the login page component**

```tsx
"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { useLogin } from "@/core/auth/hooks";

export default function LoginPage() {
  const router = useRouter();
  const login = useLogin();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-950 px-6">
      <form
        className="w-full max-w-md rounded-2xl border border-white/10 bg-white p-8 shadow-2xl"
        onSubmit={(e) => {
          e.preventDefault();
          login.mutate(
            { username, password },
            { onSuccess: () => router.push("/workspace") },
          );
        }}
      >
        <h1 className="text-2xl font-semibold text-slate-900">DiResearchStudio</h1>
        <p className="mt-2 text-sm text-slate-600">Sign in to continue to the research workspace.</p>
      </form>
    </main>
  );
}
```

- [ ] **Step 2: Replace `/` with a redirect to login or workspace**

```tsx
import { redirect } from "next/navigation";

import { getSession } from "@/server/better-auth/server";

export default async function HomePage() {
  const session = await getSession();
  redirect(session ? "/workspace" : "/login");
}
```

- [ ] **Step 3: Gate the workspace root**

```tsx
import { redirect } from "next/navigation";

import { getSession } from "@/server/better-auth/server";

export default async function WorkspacePage() {
  const session = await getSession();
  if (!session) redirect("/login");
  redirect("/workspace/chats/new");
}
```

- [ ] **Step 4: Update app metadata for the new product brand**

```tsx
export const metadata: Metadata = {
  title: "DiResearchStudio",
  description: "Enterprise AI research workspace powered by LangGraph and PostgreSQL.",
};
```

- [ ] **Step 5: Update visible workspace branding**

```tsx
<div className="text-primary ml-2 cursor-default font-serif">
  DiResearchStudio
</div>
```

- [ ] **Step 6: Run lint and typecheck**

Run: `cd /home/jetson/deer-flow/frontend && pnpm check`
Expected: PASS

- [ ] **Step 7: Commit**

```bash
git add frontend/src/app/login/page.tsx frontend/src/app/page.tsx frontend/src/app/workspace/page.tsx frontend/src/app/layout.tsx frontend/src/app/workspace/layout.tsx frontend/src/components/workspace/workspace-header.tsx
git commit -m "feat: replace landing page with authenticated login flow"
```

### Task 7: Redesign the workspace shell into an enterprise layout

**Files:**
- Modify: `frontend/src/app/workspace/layout.tsx`
- Modify: `frontend/src/app/workspace/chats/page.tsx`
- Modify: `frontend/src/app/workspace/chats/[thread_id]/page.tsx`
- Modify: `frontend/src/components/workspace/workspace-sidebar.tsx`
- Modify: `frontend/src/components/workspace/workspace-nav-chat-list.tsx`
- Modify: `frontend/src/components/workspace/recent-chat-list.tsx`
- Modify: `frontend/src/components/workspace/chats/chat-box.tsx`
- Modify: `frontend/src/components/workspace/input-box.tsx`
- Modify: `frontend/src/components/workspace/messages/message-list.tsx`
- Modify: `frontend/src/components/workspace/workspace-container.tsx`

- [ ] **Step 1: Refactor the workspace shell into a two-zone enterprise layout**

```tsx
<div className="flex h-screen bg-slate-100 text-slate-900">
  <WorkspaceSidebar />
  <SidebarInset className="min-w-0 bg-transparent">
    <div className="flex h-full min-w-0 flex-col">
      <div className="border-b border-slate-200 bg-white/90 px-6 py-3 backdrop-blur">
        <WorkspaceTopBar />
      </div>
      <div className="min-h-0 flex-1 p-4">{children}</div>
    </div>
  </SidebarInset>
</div>
```

- [ ] **Step 2: Upgrade the chat page header and content hierarchy**

```tsx
<header className="sticky top-0 z-20 flex items-center justify-between border-b border-slate-200 bg-white/95 px-6 py-4 backdrop-blur">
  <div>
    <ThreadTitle threadId={threadId} thread={thread} />
    <p className="mt-1 text-xs text-slate-500">Enterprise research workspace · persisted conversation</p>
  </div>
  <div className="flex items-center gap-2">
    <TokenUsageIndicator messages={thread.messages} />
    <ExportTrigger threadId={threadId} />
    <ArtifactTrigger />
  </div>
</header>
```

- [ ] **Step 3: Make the recent thread list denser and clearly business-oriented**

```tsx
<Link href={pathOfThread(thread)} className="group flex flex-col rounded-xl border border-transparent px-3 py-3 hover:border-slate-200 hover:bg-white">
  <span className="line-clamp-1 text-sm font-medium text-slate-900">{titleOfThread(thread)}</span>
  <span className="mt-1 text-xs text-slate-500">Updated {formatTimeAgo(thread.updated_at)}</span>
</Link>
```

- [ ] **Step 4: Add sidebar entry points for admin-only areas**

```tsx
{session?.user.role === "admin" ? (
  <SidebarMenuItem>
    <SidebarMenuButton isActive={pathname.startsWith("/workspace/admin")} asChild>
      <Link href="/workspace/admin/users">
        <ShieldCheck />
        <span>Admin Console</span>
      </Link>
    </SidebarMenuButton>
  </SidebarMenuItem>
) : null}
```

- [ ] **Step 5: Tighten the message list and input surface styling**

```tsx
<div className="mx-auto flex w-full max-w-5xl flex-1 flex-col gap-4 px-6 py-6">
  <MessageList />
  <div className="rounded-2xl border border-slate-200 bg-white p-3 shadow-sm">
    <InputBox />
  </div>
</div>
```

- [ ] **Step 6: Verify the workspace manually**

Run: `cd /home/jetson/deer-flow/frontend && pnpm dev`
Expected: `/login` renders first; after authentication, `/workspace/chats/new` shows the redesigned shell.

- [ ] **Step 7: Commit**

```bash
git add frontend/src/app/workspace/layout.tsx frontend/src/app/workspace/chats/page.tsx frontend/src/app/workspace/chats/[thread_id]/page.tsx frontend/src/components/workspace/workspace-sidebar.tsx frontend/src/components/workspace/workspace-nav-chat-list.tsx frontend/src/components/workspace/recent-chat-list.tsx frontend/src/components/workspace/chats/chat-box.tsx frontend/src/components/workspace/input-box.tsx frontend/src/components/workspace/messages/message-list.tsx frontend/src/components/workspace/workspace-container.tsx
git commit -m "feat: redesign workspace into enterprise chat layout"
```

### Task 8: Scope thread history and chat data to the logged-in user

**Files:**
- Modify: `frontend/src/core/threads/types.ts`
- Modify: `frontend/src/core/threads/hooks.ts`
- Modify: `frontend/src/components/workspace/recent-chat-list.tsx`
- Modify: `frontend/src/app/workspace/chats/page.tsx`
- Modify: `frontend/src/app/workspace/chats/[thread_id]/page.tsx`

- [ ] **Step 1: Extend the thread type with ownership-aware metadata**

```ts
export interface AgentThreadState extends Record<string, unknown> {
  title: string;
  messages: Message[];
  artifacts: string[];
  todos?: Todo[];
  owner_id?: string;
  profile_key?: string;
}
```

- [ ] **Step 2: Update thread queries to use authenticated backend endpoints**

```ts
export function useThreads() {
  return useQuery({
    queryKey: ["threads", "search"],
    queryFn: async () => {
      const response = await fetch(`${getBackendBaseURL()}/api/threads/search`, {
        credentials: "include",
      });
      if (!response.ok) throw new Error("Failed to load threads");
      return response.json() as Promise<Array<AgentThread>>;
    },
  });
}
```

- [ ] **Step 3: Ensure new thread creation carries the selected profile context**

```ts
const [thread, sendMessage, isUploading] = useThreadStream({
  threadId: isNewThread ? undefined : threadId,
  context: {
    ...settings.context,
    profile_key: settings.context.agent_name ?? "default",
  },
  isMock,
});
```

- [ ] **Step 4: Keep sidebar history consistent after delete/rename**

```ts
const { data: threads = [] } = useThreads();
const sortedThreads = useMemo(() => [...threads].sort((a, b) => Date.parse(b.updated_at) - Date.parse(a.updated_at)), [threads]);
```

- [ ] **Step 5: Verify user isolation manually**

Run: create two users, log into each in separate browser sessions.
Expected: each user only sees their own left-sidebar threads; admin can see all only in admin review pages, not the normal user sidebar.

- [ ] **Step 6: Commit**

```bash
git add frontend/src/core/threads/types.ts frontend/src/core/threads/hooks.ts frontend/src/components/workspace/recent-chat-list.tsx frontend/src/app/workspace/chats/page.tsx frontend/src/app/workspace/chats/[thread_id]/page.tsx
git commit -m "feat: scope workspace history to authenticated users"
```

### Task 9: Build the admin console for users, conversations, and capability visibility

**Files:**
- Create: `frontend/src/app/workspace/admin/page.tsx`
- Create: `frontend/src/app/workspace/admin/users/page.tsx`
- Create: `frontend/src/app/workspace/admin/conversations/page.tsx`
- Create: `frontend/src/app/workspace/admin/capabilities/page.tsx`
- Create: `frontend/src/components/workspace/admin/admin-shell.tsx`
- Create: `frontend/src/components/workspace/admin/user-table.tsx`
- Create: `frontend/src/components/workspace/admin/conversation-table.tsx`
- Create: `frontend/src/components/workspace/admin/capability-visibility-panel.tsx`
- Create: `frontend/src/core/admin/types.ts`
- Create: `frontend/src/core/admin/api.ts`
- Create: `frontend/src/core/admin/hooks.ts`
- Modify: `frontend/src/components/workspace/workspace-nav-chat-list.tsx`

- [ ] **Step 1: Add typed admin API contracts**

```ts
export interface AdminUser {
  id: string;
  identifier: string;
  display_name: string;
  role: "admin" | "user";
  status: "active" | "disabled";
  provider: string;
}

export interface VisibilityRule {
  category: "profiles" | "skills" | "mcp";
  key: string;
  enabled: boolean;
}
```

- [ ] **Step 2: Add admin API helpers**

```ts
export async function listUsers() {
  const response = await fetch(`${getBackendBaseURL()}/api/admin/users`, { credentials: "include" });
  if (!response.ok) throw new Error("Failed to list users");
  return response.json() as Promise<{ users: AdminUser[] }>;
}
```

- [ ] **Step 3: Build the admin shell layout**

```tsx
export function AdminShell({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="mx-auto flex w-full max-w-7xl flex-col gap-6 px-6 py-6">
      <div>
        <h1 className="text-2xl font-semibold text-slate-900">{title}</h1>
        <p className="mt-1 text-sm text-slate-500">Testing-stage administration for DiResearchStudio.</p>
      </div>
      <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">{children}</div>
    </div>
  );
}
```

- [ ] **Step 4: Implement the user management page**

```tsx
export default function AdminUsersPage() {
  const { data } = useAdminUsers();
  return (
    <AdminShell title="User Management">
      <UserTable users={data?.users ?? []} />
    </AdminShell>
  );
}
```

- [ ] **Step 5: Implement the conversation review page**

```tsx
export default function AdminConversationsPage() {
  const { data } = useAdminConversations();
  return (
    <AdminShell title="Conversation Review">
      <ConversationTable conversations={data?.threads ?? []} />
    </AdminShell>
  );
}
```

- [ ] **Step 6: Implement the capability visibility page**

```tsx
export default function AdminCapabilitiesPage() {
  const { data } = useVisibilityRules();
  return (
    <AdminShell title="Capability Visibility">
      <CapabilityVisibilityPanel rules={data?.rules ?? []} />
    </AdminShell>
  );
}
```

- [ ] **Step 7: Add navigation into the admin console**

```tsx
<Link href="/workspace/admin/users">
  <ShieldCheck />
  <span>Admin Console</span>
</Link>
```

- [ ] **Step 8: Run frontend checks**

Run: `cd /home/jetson/deer-flow/frontend && pnpm check`
Expected: PASS

- [ ] **Step 9: Manual verification**

Run: log in as admin.
Expected: admin can create/disable users, reset passwords, review conversations, and toggle profile/skill/MCP visibility.

- [ ] **Step 10: Commit**

```bash
git add frontend/src/app/workspace/admin frontend/src/components/workspace/admin frontend/src/core/admin frontend/src/components/workspace/workspace-nav-chat-list.tsx
git commit -m "feat: add admin console for users conversations and visibility"
```

### Task 10: Complete branding, config, and documentation updates

**Files:**
- Modify: `README.md`
- Modify: `README_zh.md`
- Modify: `backend/CLAUDE.md`
- Modify: `frontend/CLAUDE.md`
- Modify: `frontend/src/app/layout.tsx`
- Modify: `backend/app/gateway/app.py`
- Modify: `config.example.yaml`

- [ ] **Step 1: Replace remaining user-facing DeerFlow branding**

```python
app = FastAPI(
    title="DiResearchStudio API Gateway",
    description="""
## DiResearchStudio API Gateway

API Gateway for DiResearchStudio - an enterprise AI research workspace built on LangGraph.
""",
    version="0.1.0",
    lifespan=lifespan,
)
```

- [ ] **Step 2: Update the health response naming**

```python
@app.get("/health", tags=["health"])
async def health_check() -> dict:
    return {"status": "healthy", "service": "diresearchstudio-gateway"}
```

- [ ] **Step 3: Update README usage and setup sections**

```md
## DiResearchStudio

DiResearchStudio is an enterprise AI research workspace built on DeerFlow's LangGraph runtime. This deployment adds PostgreSQL persistence, authenticated multi-user access, admin-managed capabilities, and a production-oriented chat workspace.
```

- [ ] **Step 4: Update backend and frontend CLAUDE docs to reflect new architecture**

```md
- PostgreSQL-backed app persistence now stores users, chat threads, messages, and elements.
- Better Auth is used for frontend session handling with local accounts and optional trusted-header SSO.
- Admin APIs now manage users, visibility rules, and conversation review.
```

- [ ] **Step 5: Run the project checks**

Run: `cd /home/jetson/deer-flow/backend && make test && make lint`
Expected: PASS

Run: `cd /home/jetson/deer-flow/frontend && pnpm check`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add README.md README_zh.md backend/CLAUDE.md frontend/CLAUDE.md frontend/src/app/layout.tsx backend/app/gateway/app.py config.example.yaml
git commit -m "docs: rename product and document enterprise architecture"
```

### Task 11: End-to-end validation and rollout checklist

**Files:**
- Modify: `docs/superpowers/plans/2026-04-03-diresearchstudio-enterprise-workspace.md`

- [ ] **Step 1: Run backend validation**

Run: `cd /home/jetson/deer-flow/backend && alembic -c app/db/alembic.ini upgrade head && pytest -q && make lint`
Expected: all backend migrations, tests, and lint pass.

- [ ] **Step 2: Run frontend validation**

Run: `cd /home/jetson/deer-flow/frontend && pnpm install && pnpm check`
Expected: lint and typecheck pass.

- [ ] **Step 3: Run local integration validation**

Run:
```bash
cd /home/jetson/deer-flow && make dev
```
Expected:
- `/login` is the first screen.
- local admin account can sign in.
- admin can create a normal user.
- normal user can create threads and only see their own history.
- uploads create element metadata and remain downloadable.
- admin console can review all conversations and toggle capability visibility.

- [ ] **Step 4: Run trusted-header smoke test**

Run: send requests through a local reverse proxy that injects `X-User-Id`, `X-User-Name`, and optional `X-User-Email`.
Expected:
- unknown header user is auto-created.
- returning header user is matched.
- user is redirected into `/workspace` without password entry.

- [ ] **Step 5: Record final rollout notes in the plan file**

```md
- [ ] Database migration applied in target environment
- [ ] Initial admin account created
- [ ] Trusted header auth disabled by default outside production proxy
- [ ] OBS/object storage follow-up tracked separately if not implemented in phase 1
```

- [ ] **Step 6: Commit**

```bash
git add docs/superpowers/plans/2026-04-03-diresearchstudio-enterprise-workspace.md
git commit -m "chore: finalize diresearchstudio rollout checklist"
```

---

## Spec Coverage Self-Review

- PostgreSQL persistence: covered in Tasks 1, 3, 10, 11.
- Local login + password: covered in Tasks 2, 5, 6.
- Trusted-header SSO + auto-create: covered in Tasks 2, 5, 11.
- Full chat message persistence: covered in Task 3.
- Sidebar history isolation: covered in Tasks 3 and 8.
- Admin page for user management: covered in Tasks 2 and 9.
- Admin management for mode/profile, skills, MCP visibility: covered in Tasks 4 and 9.
- Admin conversation review: covered in Tasks 3, 4, and 9.
- Landing page replacement + direct workspace entry: covered in Tasks 5 and 6.
- Enterprise workspace redesign: covered in Task 7.
- Product rename to DiResearchStudio: covered in Tasks 6 and 10.
- File modeling with Chainlit-inspired `chat_elements`: covered in Tasks 1 and 3.
- Runtime sandbox preserved with secure access mediation: covered in Task 3.

No placeholder sections remain; each task names concrete files, code, commands, and verification.

---

Plan complete and saved to `docs/superpowers/plans/2026-04-03-diresearchstudio-enterprise-workspace.md`. Two execution options:

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**
