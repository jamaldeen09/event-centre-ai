import uuid

from sqlalchemy import PrimaryKeyConstraint, Index, String, ForeignKey, ForeignKeyConstraint, Integer, Text, CheckConstraint, func, text
from sqlalchemy.orm import mapped_column, Mapped, relationship
from fastapi_users_db_sqlalchemy import UUID_ID
from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy.dialects.postgresql import ARRAY, JSONB

from ..models import Base

class Space(Base):
    __tablename__ = "spaces"

    id: Mapped[UUID_ID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)  
    venue_id: Mapped[UUID_ID] = mapped_column(ForeignKey("venues.id", ondelete="CASCADE"), nullable=False)
    max_capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    amenities: Mapped[list[str]] = mapped_column(ARRAY(Text), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    policies: Mapped[dict] = mapped_column(JSONB, server_default="{}", nullable=False)
    gallery: Mapped[list[str]] = mapped_column(ARRAY(Text), nullable=False)

    venue = relationship("Venue", back_populates="spaces")

    __table_args__ = (
        PrimaryKeyConstraint("id", name="spaces_pkey"),
        ForeignKeyConstraint(
            columns=["venue_id"],
            refcolumns=["venues.id"],
            name="fk_spaces_venue_id",
            ondelete="CASCADE",
        ),
        CheckConstraint("amenities > 0", name="ck_spaces_amenities_not_empty"),
        CheckConstraint("gallery > 0", name="ck_spaces_gallery_not_empty"),

        Index("idx_spaces_venue_id", "venue_id"),
        Index(
            "idx_spaces_venue_id_name", 
            "venue_id", 
            func.lower(text("name")), 
            unique=True
        ),
    )



