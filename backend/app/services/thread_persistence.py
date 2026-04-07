from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.chat_element import ChatElement
from app.db.models.chat_message import ChatMessage
from app.db.models.chat_thread import ChatThread


def _to_uuid(value: str | UUID) -> UUID:
    return value if isinstance(value, UUID) else UUID(str(value))


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


class ThreadPersistenceService:
    def __init__(self, db: Session):
        self.db = db

    def upsert_thread_snapshot(
        self,
        *,
        user_id: str | UUID,
        thread_id: str,
        title: str,
        profile_key: str,
        messages: list[dict],
        artifacts: list[str],
    ) -> None:
        thread = self.db.get(ChatThread, thread_id)
        if thread is None:
            thread = ChatThread(id=thread_id, user_id=_to_uuid(user_id), title=title, profile_key=profile_key, metadata_json={})
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
                    user_id=_to_uuid(user_id),
                    role=infer_role(message),
                    content=message.get("content", []),
                    text_content=text_from_content(message.get("content")),
                    message_index=index,
                    metadata_json={"raw_type": message.get("type")},
                )
            )
        self.db.commit()

    def get_thread(self, thread_id: str) -> ChatThread | None:
        return self.db.get(ChatThread, thread_id)

    def get_messages(self, thread_id: str) -> list[ChatMessage]:
        return self.db.query(ChatMessage).filter(ChatMessage.thread_id == thread_id).order_by(ChatMessage.message_index).all()

    def get_elements(self, thread_id: str) -> list[ChatElement]:
        return self.db.query(ChatElement).filter(ChatElement.thread_id == thread_id).all()

    def register_element(
        self,
        *,
        thread_id: str,
        user_id: str | UUID,
        element_id: str,
        name: str,
        mime: str | None,
        size: int | None,
        source: str,
        storage_provider: str,
        object_key: str | None,
    ) -> None:
        element = ChatElement(
            id=element_id,
            thread_id=thread_id,
            user_id=_to_uuid(user_id),
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

    def list_threads_for_user(self, user_id: str | UUID) -> list[ChatThread]:
        return self.db.query(ChatThread).filter(ChatThread.user_id == _to_uuid(user_id)).order_by(ChatThread.updated_at.desc()).all()

    def list_all_threads(self) -> list[ChatThread]:
        return self.db.query(ChatThread).order_by(ChatThread.updated_at.desc()).all()
