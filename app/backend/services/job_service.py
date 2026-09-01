from pathlib import Path

from sqlalchemy.orm import Session

from application.job_input import (
    process_job_description_input,
)

from database.repositories import (
    create_job,
)


def _persist_job(
    db: Session,
    user_id: int,
    job_description,
    source_type: str,
):
    """
    Persist a structured job description for a user.
    """

    job_data = job_description.model_dump()

    job = create_job(
        db=db,
        user_id=user_id,
        job_title=job_data.get(
            "job_title"
        ),
        company=job_data.get(
            "company"
        ),
        source_type=source_type,
        required_skills=job_data.get(
            "required_skills"
        ),
        preferred_skills=job_data.get(
            "preferred_skills"
        ),
        responsibilities=job_data.get(
            "responsibilities"
        ),
        qualifications=job_data.get(
            "qualifications"
        ),
        education_required=job_data.get(
            "education_required"
        ),
        experience_required=job_data.get(
            "experience_required"
        ),
    )

    return job


def process_job_text(
    db: Session,
    user_id: int,
    job_text: str,
):
    """
    Process and persist a pasted job description.
    """

    job_description = (
        process_job_description_input(
            job_text=job_text,
        )
    )

    job = _persist_job(
        db=db,
        user_id=user_id,
        job_description=job_description,
        source_type="text",
    )

    return {
        "job": job,
        "job_description": job_description,
    }


def process_job_pdf(
    db: Session,
    user_id: int,
    file_path: str,
):
    """
    Process and persist a job-description PDF.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Job description file not found: {file_path}"
        )

    job_description = (
        process_job_description_input(
            pdf_path=str(path),
        )
    )

    job = _persist_job(
        db=db,
        user_id=user_id,
        job_description=job_description,
        source_type="pdf",
    )

    return {
        "job": job,
        "job_description": job_description,
    }