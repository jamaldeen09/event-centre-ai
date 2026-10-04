import uuid

from sqlalchemy import PrimaryKeyConstraint, Index, ForeignKey, ForeignKeyConstraint, Integer, Boolean
from sqlalchemy.orm import mapped_column, Mapped
from fastapi_users_db_sqlalchemy import UUID_ID
from fastapi_users_db_sqlalchemy.generics import GUID

from .base import Base

class SpaceEventPermission(Base):
    __tablename__ = "space_event_permissions"

    id: Mapped[UUID_ID] = mapped_column(GUID, primary_key=True, default=uuid.uuid4)  
    space_id: Mapped[UUID_ID] = mapped_column(ForeignKey("spaces.id", ondelete="CASCADE"), nullable=False)
    event_type_id: Mapped[UUID_ID] = mapped_column(ForeignKey("event_types.id", ondelete="CASCADE"), nullable=False)
    max_capacity_for_type: Mapped[int] = mapped_column(Integer, nullable=False)
    is_allowed: Mapped[bool] = mapped_column(Boolean, nullable=False)


    __table_args__ = (
        PrimaryKeyConstraint("id", name="space_event_permissions_pkey"),
        ForeignKeyConstraint(
            columns=["space_id"],
            refcolumns=["spaces.id"],
            name="fk_space_event_permissions_space_id",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            columns=["event_type_id"],
            refcolumns=["event_types.id"],
            name="fk_space_event_permissions_event_type_id",
            ondelete="CASCADE",
        ),

        Index("idx_space_event_permissions_space_id_event_type_id", "space_id", "event_type_id", unique=True),
    )
