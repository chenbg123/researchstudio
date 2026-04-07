from app.db.models import AdminVisibility, ChatElement, ChatMessage, ChatThread, User


def test_models_expose_expected_tables():
    assert User.__tablename__ == "users"
    assert ChatThread.__tablename__ == "chat_threads"
    assert ChatMessage.__tablename__ == "chat_messages"
    assert ChatElement.__tablename__ == "chat_elements"
    assert AdminVisibility.__tablename__ == "admin_visibility_rules"
