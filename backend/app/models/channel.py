import uuid

from sqlalchemy import PrimaryKeyConstraint, Index, ForeignKey, ForeignKeyConstraint, func, DateTime, Boolean, text, String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from fastapi_users_db_sqlalchemy import UUID_ID
from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from enum import Enum

from .base import Base

class ChannelType (Enum):
    WEB = "web"

class Channel(Base):
    __tablename__ = "channels"

    id: Mapped[UUID_ID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)  
    venue_id: Mapped[UUID_ID] = mapped_column(ForeignKey("venues.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False,
    )
    channel_type: Mapped[ChannelType] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    config: Mapped[dict] = mapped_column(JSONB, server_default="{}", nullable=False)

    venue = relationship("Venue", back_populates="blocked_dates")
    customers = relationship(
        "Customer",
        back_populates="channel",
        cascade="save-update, merge",
    )

    __table_args__ = (
        PrimaryKeyConstraint("id", name="channels_pkey"),
        ForeignKeyConstraint(
            columns=["venue_id"],
            refcolumns=["venues.id"],
            name="fk_channels_venue_id",
            ondelete="CASCADE",
        ),

        Index("idx_channels_config.web.slug", text("(config->'web'->>'slug')"), unique=True),
    )



