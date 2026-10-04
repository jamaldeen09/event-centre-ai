import uuid

from sqlalchemy import PrimaryKeyConstraint, Index, ForeignKey, ForeignKeyConstraint, func, DateTime, String, Integer, Date, Time, text, Boolean, Numeric
from sqlalchemy.orm import mapped_column, Mapped, relationship
from fastapi_users_db_sqlalchemy import UUID_ID
from fastapi_users_db_sqlalchemy.generics import GUID
from datetime import datetime, date, time
from sqlalchemy.schema import Computed
from sqlalchemy.dialects.postgresql import ExcludeConstraint, TSRANGE
from decimal import Decimal
from enum import Enum

from .base import Base

class BookingStatus(Enum):
    HELD = "held"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"

class BookingPaymentStatus(Enum):
    UNPAID = "unpaid"
    DEPOSIT_PAID = "deposit_paid"
    FULLY_PAID = "fully_paid"

class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[UUID_ID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)  
    space_id: Mapped[UUID_ID] = mapped_column(ForeignKey("spaces.id", ondelete="SET NULL"), nullable=False)
    customer_id: Mapped[UUID_ID] = mapped_column(ForeignKey("customers.id", ondelete="SET NULL"), nullable=False)
    conversation_id: Mapped[UUID_ID] = mapped_column(ForeignKey("conversations.id", ondelete="SET NULL"), nullable=False)
    event_type_id: Mapped[UUID_ID] = mapped_column(ForeignKey("event_types.id", ondelete="SET NULL"), nullable=False)
    guest_count: Mapped[int] = mapped_column(Integer, nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    effective_start: Mapped[text] = mapped_column(
        Computed(
            "start_date + COALESCE(start_time, TIME '00:00')",
            persisted=True,
        ),
        type_=TSRANGE,
    )
    effective_end: Mapped[text] = mapped_column(
        Computed(
            "end_date + (INTERVAL '1 day' * (end_time IS NULL)::int) + COALESCE(end_time, TIME '00:00')",
            persisted=True,
        ),
        type_=TSRANGE,
    )
    status: Mapped[BookingStatus] = mapped_column(String, nullable=False)
    notes: Mapped[str] = mapped_column(String, nullable=True)
    is_archived: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    archived_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    payment_status: Mapped[BookingPaymentStatus] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False,
    )
    created_by: Mapped[str | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(precision=12, scale=2), 
        nullable=False
    )
    caution_deposit_amount: Mapped[Decimal] = mapped_column(
        Numeric(precision=12, scale=2), 
        nullable=False,
        default=Decimal("0.00")
    )

    conversation = relationship("Conversation", back_populates="bookings")
    event_type = relationship("EventType", back_populates="bookings")

    __table_args__ = (
        PrimaryKeyConstraint("id", name="bookings_pkey"),
        ExcludeConstraint(
            ("space_id", "="),
            (func.tsrange(text("effective_start"), text("effective_end")), "&&"),
            name="no_overlapping_bookings",
            using="gist",
            where=text(f"status != {BookingStatus.CANCELLED}"),
        ),
        ForeignKeyConstraint(
            columns=["space_id"],
            refcolumns=["spaces.id"],
            name="fk_bookings_space_id",
            ondelete="SET NULL",
        ),
        ForeignKeyConstraint(
            columns=["customer_id"],
            refcolumns=["customers.id"],
            name="fk_bookings_customer_id",
            ondelete="SET NULL",
        ),
        ForeignKeyConstraint(
            columns=["conversation_id"],
            refcolumns=["conversations.id"],
            name="fk_bookings_conversation_id",
            ondelete="SET NULL",
        ),
        ForeignKeyConstraint(
            columns=["event_type_id"],
            refcolumns=["event_types.id"],
            name="fk_bookings_event_type_id",
            ondelete="SET NULL",
        ),

        Index("idx_bookings_customer_id", "customer_id"),
        Index("idx_bookings_space_id_effective_start", "space_id", "effective_start"),
        Index("idx_bookings_space_id_status_is_archived", "space_id", "status", "is_archived"),
    )



