from datetime import datetime, timezone
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from database.base.base import Base
from sqlalchemy import String


class User(Base):
    """
    Represents a Resume Genie application user.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique = True,
        nullable = True,
        index = True,
    )
    session_id: Mapped[str | None] = mapped_column(
        String(128),
        unique=True,
        nullable=True,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
