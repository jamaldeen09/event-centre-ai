import uuid

from sqlalchemy import PrimaryKeyConstraint, Index, ForeignKeyConstraint, text, String, Numeric, Integer, Boolean, ForeignKey, func, text
from sqlalchemy.orm import mapped_column, Mapped, relationship
from fastapi_users_db_sqlalchemy import UUID_ID
from fastapi_users_db_sqlalchemy.generics import GUID
from decimal import Decimal

from .base import Base


class EventType(Base):
    __tablename__ = "event_types"

    id: Mapped[UUID_ID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)  
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    price_multiplier: Mapped[Decimal] = mapped_column(
        Numeric(precision=3, scale=2),
        default=Decimal("1.00"),
        server_default=text("1.00"), 
        nullable=False,
    )
    buffer_hours_required: Mapped[int] = mapped_column(Integer, nullable=False)
    requires_special_permit: Mapped[bool] = mapped_column(Boolean, nullable=False)
    venue_id: Mapped[UUID_ID] = mapped_column(ForeignKey("venues.id", ondelete="CASCADE"), nullable=False)

    venue = relationship("Venue", back_populates="event_types")

    __table_args__ = (
        PrimaryKeyConstraint("id", name="event_types_pkey"),
        ForeignKeyConstraint(
            columns=["venue_id"],
            refcolumns=["venues.id"],
            name="fk_event_types_venue_id",
            ondelete="CASCADE",
        ),

        Index("idx_event_types_venue_id", "venue_id"),
        Index("idx_event_types_venue_id_name", "venue_id", func.lower(text("name")), unique=True),
    )


