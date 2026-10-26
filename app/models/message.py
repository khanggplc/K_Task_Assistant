import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Text, DateTime, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from app.db.database import Base


class MessageSource(str, enum.Enum):
    GMAIL = "gmail"
    ZALO = "zalo"
    MANUAL = "manual"


class MessageStatus(str, enum.Enum):
    PENDING = "pending"
    PARSED = "parsed"
    IGNORED = "ignored"
    FAILED = "failed"


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), index=True, nullable=False)
    source: Mapped[MessageSource] = mapped_column(SqlEnum(MessageSource), default=MessageSource.MANUAL)
    external_id: Mapped[str] = mapped_column(String(255), index=True, nullable=True)  # e.g., Gmail msg ID or Zalo msg ID
    sender: Mapped[str] = mapped_column(String(255), nullable=True)
    recipient: Mapped[str] = mapped_column(String(255), nullable=True)
    subject: Mapped[str] = mapped_column(String(500), nullable=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[MessageStatus] = mapped_column(SqlEnum(MessageStatus), default=MessageStatus.PENDING)
    raw_payload: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    user = relationship("User", back_populates="messages")
    tasks = relationship("Task", back_populates="source_message")
