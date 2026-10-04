

from sqlalchemy import UniqueConstraint, PrimaryKeyConstraint, Index, String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from fastapi_users.db import SQLAlchemyBaseUserTableUUID

from ..models import Base

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"

    image_url: Mapped[str | None] = mapped_column(String, nullable=True)
    venues = relationship( 
        "Venue",
        back_populates="owner",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint("email", name="uq_users_email"),
        PrimaryKeyConstraint("id", name="users_pkey"),
    )



