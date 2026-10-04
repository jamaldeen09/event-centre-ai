import uuid

from sqlalchemy import PrimaryKeyConstraint, Index, ForeignKey, ForeignKeyConstraint, func, DateTime, String, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship
from fastapi_users_db_sqlalchemy import UUID_ID
from fastapi_users_db_sqlalchemy.generics import GUID
from datetime import datetime

from .base import Base

class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[UUID_ID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)  
    channel_id: Mapped[UUID_ID | None] = mapped_column(ForeignKey("channels.id", ondelete="SET NULL"), nullable=True)
    channel_identifier: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False,
    )
    phone_number: Mapped[str | None] = mapped_column(String, nullable=True)
    email: Mapped[str | None] = mapped_column(String, nullable=True)
    name: Mapped[str | None] = mapped_column(String, nullable=True)

    conversations = relationship(
        "Conversation",
        back_populates="customer",
        cascade="save-update, merge"
    )

    __table_args__ = (
        PrimaryKeyConstraint("id", name="customers_pkey"),
        ForeignKeyConstraint(
            columns=["channel_id"],
            refcolumns=["channels.id"],
            name="fk_customers_channel_id",
            ondelete="SET NULL",
        ),
        UniqueConstraint("channel_id", "channel_identifier", name="uq_customers_channel_id_channel_identifier"),

        Index("idx_customers_channel_id_channel_identifier", "channel_id", "channel_identifier", unique=True),
    )



