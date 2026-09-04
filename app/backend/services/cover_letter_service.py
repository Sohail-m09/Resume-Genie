from sqlalchemy.orm import Session

from database.repositories.resume_repository import (
    get_resume_by_id,
)

from database.repositories.job_repository import (
    get_job_by_id,
)

from application.resume_input import (
    process_resume_input,
)

from schemas.job_description import (
    JobDescription,
)

from analysis.cover_letter_service import (
    create_cover_letter,
)


def generate_cover_letter(
    db: Session,
    user_id: int,
    resume_id: int,
    job_id: int,
):
    """
    Generate a cover letter using a saved resume and
    saved job description belonging to the current user.
    """

    # --------------------------------------------------
    # 1. Load selected resume
    # --------------------------------------------------

    resume_record = get_resume_by_id(
        db=db,
        resume_id=resume_id,
    )

    if resume_record is None:
        raise ValueError(
            "Resume not found."
        )

    if resume_record.user_id != user_id:
        raise ValueError(
            "Resume does not belong to the current user."
        )

    # --------------------------------------------------
    # 2. Load selected job
    # --------------------------------------------------

    job_record = get_job_by_id(
        db=db,
        job_id=job_id,
    )

    if job_record is None:
        raise ValueError(
            "Job not found."
        )

    if job_record.user_id != user_id:
        raise ValueError(
            "Job does not belong to the current user."
        )

    # --------------------------------------------------
    # 3. Reconstruct the structured resume
    #    from the original stored PDF
    # --------------------------------------------------

    resume, _ = process_resume_input(
        resume_record.storage_path
    )

    # --------------------------------------------------
    # 4. Reconstruct JobDescription from PostgreSQL
    # --------------------------------------------------

    job_description = JobDescription(
        job_title=job_record.job_title,
        company=job_record.company,
        required_skills=job_record.required_skills or [],
        preferred_skills=job_record.preferred_skills or [],
        responsibilities=job_record.responsibilities or [],
        experience_required=job_record.experience_required,
        education_required=job_record.education_required,
        qualifications=job_record.qualifications or [],
    )

    # --------------------------------------------------
    # 5. Generate grounded structured cover letter
    # --------------------------------------------------

    cover_letter = create_cover_letter(
        resume=resume,
        job_description=job_description,
    )

    return cover_letter