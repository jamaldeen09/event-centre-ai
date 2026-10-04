import uuid

from sqlalchemy import PrimaryKeyConstraint, Index, String, ForeignKey, ForeignKeyConstraint, func,DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from fastapi_users_db_sqlalchemy import UUID_ID
from fastapi_users_db_sqlalchemy.generics import GUID
from enum import Enum
from datetime import datetime

from ..models import Base

class MessageRole(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"
    SYSTEM = "system"

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[UUID_ID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)  
    conversation_id: Mapped[UUID_ID] = mapped_column(ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)
    role: Mapped[MessageRole] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False,
    )

    conversation = relationship("Conversation", back_populates="messages")

    __table_args__ = (
        PrimaryKeyConstraint("id", name="messages_pkey"),
        ForeignKeyConstraint(
            columns=["conversation_id"],
            refcolumns=["conversations.id"],
            name="fk_messages_conversation_id",
            ondelete="CASCADE",
        ),

        Index("idx_messages_conversation_id_created_at", "conversation_id", "created_at"),
    )
