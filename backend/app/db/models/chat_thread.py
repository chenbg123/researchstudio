import uuid
from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, Index, String, Uuid, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ChatThread(Base):
    __tablename__ = "chat_threads"
    __table_args__ = (Index("ix_chat_threads_user_updated", "user_id", "updated_at"),)

    id: Mapped[str] = mapped_column(String(128), primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), default="New Chat")
    profile_key: Mapped[str] = mapped_column(String(100), default="default")
    agent_key: Mapped[str | None] = mapped_column(String(100))
    metadata_json: Mapped[dict] = mapped_column("metadata", JSONB().with_variant(JSON(), "sqlite"), default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
