from datetime import datetime, timezone

from sqlalchemy import (
    DateTime,
    ForeignKey,
    JSON,
    Float,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from database.base.base import Base


class Application(Base):
    """
    Represents one resume-to-job application attempt.
    """

    __tablename__ = "applications"

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

    resume_id: Mapped[int] = mapped_column(
        ForeignKey(
            "resumes.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    job_id: Mapped[int] = mapped_column(
        ForeignKey(
            "jobs.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    match_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    ats_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    analysis_result: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    tailored_resume: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )