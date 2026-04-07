import uuid
from unittest.mock import MagicMock, patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.db.models.user import User
from app.db.session import get_db_session


def _make_app():
    """Create a test app with admin router."""
    from app.gateway.routers import admin

    app = FastAPI()
    app.include_router(admin.router)
    return app, admin


def test_admin_can_create_user():
    app, admin_mod = _make_app()

    fake_user = User(
        id=uuid.uuid4(),
        provider="local",
        identifier="bob",
        password_hash="hashed",
        display_name="Bob",
        role="user",
        status="active",
        metadata_json={},
    )

    mock_session = MagicMock()
    app.dependency_overrides[get_db_session] = lambda: mock_session
    app.dependency_overrides[admin_mod.require_admin] = lambda: {"id": "admin-1", "role": "admin"}

    with patch("app.gateway.routers.admin.AuthService") as mock_auth:
        mock_auth.return_value.create_local_user.return_value = fake_user

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


def test_admin_can_list_users():
    app, admin_mod = _make_app()

    fake_user = User(
        id=uuid.uuid4(),
        provider="local",
        identifier="alice",
        password_hash="hashed",
        display_name="Alice",
        role="user",
        status="active",
        metadata_json={},
    )

    mock_session = MagicMock()
    mock_session.query.return_value.order_by.return_value.all.return_value = [fake_user]
    app.dependency_overrides[get_db_session] = lambda: mock_session
    app.dependency_overrides[admin_mod.require_admin] = lambda: {"id": "admin-1", "role": "admin"}

    with TestClient(app) as client:
        response = client.get("/api/admin/users")

    assert response.status_code == 200
    assert len(response.json()["users"]) == 1
