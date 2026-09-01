from datetime import datetime, timezone

from sqlalchemy import (
    String,
    DateTime,
    ForeignKey,
    Text,
    JSON,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from database.base.base import Base


class Job(Base):
    """
    Represents a job description submitted by a user.
    """

    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    job_title: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    company: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    source_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    required_skills: Mapped[list | None] = mapped_column(
        JSON,
        nullable=True,
    )

    preferred_skills: Mapped[list | None] = mapped_column(
        JSON,
        nullable=True,
    )

    responsibilities: Mapped[list | None] = mapped_column(
        JSON,
        nullable=True,
    )

    qualifications: Mapped[list | None] = mapped_column(
        JSON,
        nullable=True,
    )

    education_required: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    experience_required: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
