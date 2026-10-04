import uuid

from sqlalchemy import PrimaryKeyConstraint, Index, String, DateTime, func, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship
from fastapi_users_db_sqlalchemy import UUID_ID
from fastapi_users_db_sqlalchemy.generics import GUID
from datetime import datetime
from sqlalchemy.dialects.postgresql.json import JSONB

from ..models import Base

class Venue (Base):
    __tablename__ = "venues"

    id: Mapped[UUID_ID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)    
    name: Mapped[str] = mapped_column(String, nullable=False)
    logo_url: Mapped[str | None] = mapped_column(String, nullable=True)
    owner_id: Mapped[UUID_ID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)
    timezone: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[str] = mapped_column(String, nullable=False)
    policies: Mapped[dict] = mapped_column(JSONB, server_default="{}", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False,
    )

    owner = relationship("User", back_populates="venues")
    spaces = relationship(
        "Space", 
        back_populates="venue", 
        cascade="all, delete-orphan"
    )
    blocked_dates = relationship(
        "BlockedDate",
        back_populates="venue",
        cascade="all, delete-orphan",
    )
    channels = relationship(
        "Channel",
        back_populates="venue",
        cascade="all, delete-orphan",
    )
    event_types = relationship(
        "EventType",
        back_populates="venue",
        cascade="all, delete-orphan",
    )
    
    __table_args__ = (
        PrimaryKeyConstraint("id", name="venues_pkey"),
        ForeignKeyConstraint(
            columns=["owner_id"], 
            refcolumns=["users.id"], 
            name="fk_venues_owner_id",
            ondelete="CASCADE",
        ),
    )


