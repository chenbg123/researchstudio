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


def test_verify_local_password(fake_session):
    service = AuthService(fake_session)
    user = service.create_local_user(username="bob", password="p@ssword1", display_name="Bob", role="user")

    assert service.verify_local_password(user, "p@ssword1") is True
    assert service.verify_local_password(user, "wrong") is False


def test_upsert_header_user_creates_new(fake_session):
    from app.services.auth import HeaderIdentity

    service = AuthService(fake_session)
    identity = HeaderIdentity(identifier="ext-user-1", display_name="External User", email="ext@example.com")

    user = service.upsert_header_user(identity)
    assert user.provider == "oa-header"
    assert user.identifier == "ext-user-1"
    assert user.display_name == "External User"


def test_upsert_header_user_updates_existing(fake_session):
    from app.services.auth import HeaderIdentity

    service = AuthService(fake_session)
    identity = HeaderIdentity(identifier="ext-user-2", display_name="Old Name")
    service.upsert_header_user(identity)

    identity2 = HeaderIdentity(identifier="ext-user-2", display_name="New Name", email="new@example.com")
    user = service.upsert_header_user(identity2)
    assert user.display_name == "New Name"
    assert user.email == "new@example.com"
