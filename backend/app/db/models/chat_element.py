import uuid
from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, String, Uuid, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ChatElement(Base):
    __tablename__ = "chat_elements"

    id: Mapped[str] = mapped_column(String(128), primary_key=True)
    thread_id: Mapped[str] = mapped_column(ForeignKey("chat_threads.id", ondelete="CASCADE"), nullable=False)
    message_id: Mapped[str | None] = mapped_column(ForeignKey("chat_messages.id", ondelete="SET NULL"))
    user_id: Mapped[uuid.UUID | None] = mapped_column(Uuid(), ForeignKey("users.id", ondelete="SET NULL"))
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
