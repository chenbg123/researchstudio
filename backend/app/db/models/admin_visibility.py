import uuid

from sqlalchemy import String, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AdminVisibility(Base):
    __tablename__ = "admin_visibility_rules"
    __table_args__ = (UniqueConstraint("category", "key", name="uq_visibility_category_key"),)

    id: Mapped[uuid.UUID] = mapped_column(Uuid(), primary_key=True, default=uuid.uuid4)
    category: Mapped[str] = mapped_column(String(32), nullable=False)
    key: Mapped[str] = mapped_column(String(255), nullable=False)
    enabled: Mapped[bool] = mapped_column(default=True)
