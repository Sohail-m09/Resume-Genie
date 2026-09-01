from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import Job


def create_job(
    db: Session,
    user_id: int,
    job_title: str | None,
    company: str | None,
    source_type: str,
    required_skills: list | None = None,
    preferred_skills: list | None = None,
    responsibilities: list | None = None,
    qualifications: list | None = None,
    education_required: str | None = None,
    experience_required: str | None = None,
) -> Job:
    """
    Create and persist a job record.
    """

    job = Job(
        user_id=user_id,
        job_title=job_title,
        company=company,
        source_type=source_type,
        required_skills=required_skills,
        preferred_skills=preferred_skills,
        responsibilities=responsibilities,
        qualifications=qualifications,
        education_required=education_required,
        experience_required=experience_required,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


def get_job_by_id(
    db: Session,
    job_id: int,
) -> Job | None:
    """
    Retrieve a job by ID.
    """

    statement = select(Job).where(
        Job.id == job_id
    )

    return db.scalar(statement)


def get_jobs_by_user(
    db: Session,
    user_id: int,
) -> list[Job]:
    """
    Retrieve all jobs belonging to a user.
    """

    statement = (
        select(Job)
        .where(
            Job.user_id == user_id
        )
        .order_by(
            Job.created_at.desc()
        )
    )

    return list(
        db.scalars(statement)
    )