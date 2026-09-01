from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import Resume


def create_resume(
    db: Session,
    user_id: int,
    filename: str,
    summary: str | None = None,
    storage_path: str | None = None,
) -> Resume:
    """
    Create and persist a resume record.
    """

    resume = Resume(
        user_id=user_id,
        filename=filename,
        summary=summary,
        storage_path=storage_path,
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return resume


def get_resume_by_id(
    db: Session,
    resume_id: int,
) -> Resume | None:
    """
    Retrieve a resume by ID.
    """

    statement = select(Resume).where(
        Resume.id == resume_id
    )

    return db.scalar(statement)


def get_resumes_by_user(
    db: Session,
    user_id: int,
) -> list[Resume]:
    """
    Retrieve all resumes belonging to a user.
    """

    statement = (
        select(Resume)
        .where(
            Resume.user_id == user_id
        )
        .order_by(
            Resume.created_at.desc()
        )
    )

    return list(
        db.scalars(statement)
    )
