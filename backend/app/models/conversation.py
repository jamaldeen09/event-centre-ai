import uuid

from sqlalchemy import PrimaryKeyConstraint, Index, ForeignKey, ForeignKeyConstraint, DateTime, Boolean, String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from fastapi_users_db_sqlalchemy import UUID_ID
from fastapi_users_db_sqlalchemy.generics import GUID
from datetime import datetime
from enum import Enum

from .base import Base

class ConversationStatus(Enum):
    ACTIVE = "active"
    ESCALATED = "escalated"
    CLOSED = "closed"

class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[UUID_ID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)  
    status: Mapped[ConversationStatus] = mapped_column(String, nullable=False, default=ConversationStatus.ACTIVE)
    agent_paused: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    customer_id: Mapped[UUID_ID | None] = mapped_column(ForeignKey("customers.id", ondelete="SET NULL"), nullable=True)
    venue_id: Mapped[UUID_ID] = mapped_column(ForeignKey("venues.id", ondelete="CASCADE"), nullable=False)
    last_message_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    customer = relationship("Customer", back_populates="conversations")
    messages = relationship(
        "Message", 
        back_populates="conversation", 
        cascade="all, delete-orphan"
    )
    bookings = relationship(
        "Booking",
        back_populates="conversation",
        cascade="save-update, merge",
    )

    __table_args__ = (
        PrimaryKeyConstraint("id", name="conversations_pkey"),
        ForeignKeyConstraint(
            columns=["venue_id"],
            refcolumns=["venues.id"],
            name="fk_conversations_venue_id",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            columns=["customer_id"],
            refcolumns=["customers.id"],
            name="fk_conversations_customer_id",
            ondelete="SET NULL",
        ),

        Index("idx_conversations_customer_id", "customer_id"),
        Index("idx_conversations_venue_id_status", "venue_id", "status"),
        Index("idx_conversations_venue_id_last_message_at", "venue_id", "last_message_at"),
    )
