import uuid

from sqlalchemy import PrimaryKeyConstraint, Index, String, ForeignKey, ForeignKeyConstraint, func, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from fastapi_users_db_sqlalchemy import UUID_ID
from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy.dialects.postgresql import ExcludeConstraint
from datetime import datetime

from .base import Base

class BlockedDate(Base):
    __tablename__ = "blocked_dates"

    id: Mapped[UUID_ID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)  
    venue_id: Mapped[UUID_ID] = mapped_column(ForeignKey("venues.id", ondelete="CASCADE"), nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    reason: Mapped[str | None] = mapped_column(String, nullable=True)
    space_id: Mapped[str | None] = mapped_column(ForeignKey("spaces.id", ondelete="SET NULL"), nullable=True)

    venue = relationship("Venue", back_populates="blocked_dates")

    __table_args__ = (
        PrimaryKeyConstraint("id", name="blocked_dates_pkey"),
        ForeignKeyConstraint(
            columns=["venue_id"],
            refcolumns=["venues.id"],
            name="fk_blocked_dates_venue_id",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            columns=["space_id"],
            refcolumns=["spaces.id"],
            name="fk_blocked_dates_space_id",
            ondelete="SET NULL",
        ),
        ExcludeConstraint(
            ("venue_id", "="),
            (func.daterange(start_date, end_date, "[]"), "&&"),
            name="no_overlapping_blocked_dates",
            using="gist",
        ),

        Index("idx_blocked_dates_venue_range", "venue_id", "start_date", "end_date"),
        Index("idx_blocked_dates_space_range", "space_id", "start_date", "end_date"),
    )
