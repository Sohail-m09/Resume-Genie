from sqlalchemy.orm import Session

from application.pipeline import run_resume_genie

from database.repositories.resume_repository import (
    get_resume_by_id,
)

from database.repositories.job_repository import (
    get_job_by_id,
)

from database.repositories.application_repository import (
    create_application,
)


def run_complete_resume_genie(
    db: Session,
    user_id: int,
    resume_id: int,
    job_id: int,
    section_order: list[str] | None = None,
    removed_sections: list[str] | None = None,
    removed_projects: list[str] | None = None,
):
    """
    Run the complete Resume Genie workflow using
    already-persisted Resume and Job records.
    """

    # --------------------------------------------------
    # 1. Retrieve existing Resume
    # --------------------------------------------------

    resume_record = get_resume_by_id(
        db=db,
        resume_id=resume_id,
    )

    if resume_record is None:
        raise ValueError(
            f"Resume with ID {resume_id} was not found."
        )

    # --------------------------------------------------
    # 2. Verify Resume belongs to current user
    # --------------------------------------------------

    if resume_record.user_id != user_id:
        raise ValueError(
            "Resume does not belong to the current user."
        )

    # --------------------------------------------------
    # 3. Retrieve existing Job
    # --------------------------------------------------

    job_record = get_job_by_id(
        db=db,
        job_id=job_id,
    )

    if job_record is None:
        raise ValueError(
            f"Job with ID {job_id} was not found."
        )

    # --------------------------------------------------
    # 4. Verify Job belongs to current user
    # --------------------------------------------------

    if job_record.user_id != user_id:
        raise ValueError(
            "Job does not belong to the current user."
        )

    # --------------------------------------------------
    # 5. Validate Resume storage path
    # --------------------------------------------------

    if not resume_record.storage_path:
        raise ValueError(
            "Stored resume does not have a valid storage path."
        )

    # --------------------------------------------------
    # 6. Determine Job input
    # --------------------------------------------------
    #
    # The existing pipeline still expects either:
    #   - job_text
    #   - job_pdf_path
    #
    # At this stage, the database Job record contains
    # structured JD information, but does not currently
    # expose the original JD text/PDF path.
    #
    # Therefore, we reconstruct a job text representation
    # from the persisted structured fields.
    # --------------------------------------------------

    job_parts = []

    if job_record.job_title:
        job_parts.append(
            f"Job Title: {job_record.job_title}"
        )

    if job_record.company:
        job_parts.append(
            f"Company: {job_record.company}"
        )

    if job_record.required_skills:
        job_parts.append(
            "Required Skills: "
            + ", ".join(
                str(skill)
                for skill in job_record.required_skills
            )
        )

    if job_record.preferred_skills:
        job_parts.append(
            "Preferred Skills: "
            + ", ".join(
                str(skill)
                for skill in job_record.preferred_skills
            )
        )

    if job_record.responsibilities:
        job_parts.append(
            "Responsibilities:\n"
            + "\n".join(
                f"- {item}"
                for item in job_record.responsibilities
            )
        )

    if job_record.qualifications:
        job_parts.append(
            "Qualifications:\n"
            + "\n".join(
                f"- {item}"
                for item in job_record.qualifications
            )
        )

    if job_record.education_required:
        job_parts.append(
            f"Education Required: "
            f"{job_record.education_required}"
        )

    if job_record.experience_required:
        job_parts.append(
            f"Experience Required: "
            f"{job_record.experience_required}"
        )

    job_text = "\n\n".join(job_parts)

    if not job_text:
        raise ValueError(
            "Stored job description does not contain "
            "enough information to run Resume Genie."
        )

    # --------------------------------------------------
    # 7. Run existing Resume Genie pipeline
    # --------------------------------------------------

    result = run_resume_genie(
        resume_path=resume_record.storage_path,
        job_text=job_text,
        job_pdf_path=None,
        section_order=section_order,
        removed_sections=removed_sections,
        removed_projects=removed_projects,
    )

    # --------------------------------------------------
    # 8. Prepare Application data
    # --------------------------------------------------

    analysis_data = (
        result["analysis"].model_dump()
    )

    tailored_resume_data = (
        result["tailored_resume"].model_dump()
    )

    ats_result = result.get("ats")

    ats_score = None

    if ats_result is not None:
        ats_score = ats_result.get(
            "ats_score"
        )

    match_score = analysis_data.get(
        "overall_score"
    )

    # --------------------------------------------------
    # 9. Create Application using EXISTING IDs
    # --------------------------------------------------

    application_record = create_application(
        db=db,
        user_id=user_id,
        resume_id=resume_record.id,
        job_id=job_record.id,
        match_score=match_score,
        ats_score=ats_score,
        analysis_result=analysis_data,
        tailored_resume=tailored_resume_data,
    )

    # --------------------------------------------------
    # 10. Return complete result
    # --------------------------------------------------

    return {
        **result,
        "user_id": user_id,
        "resume_id": resume_record.id,
        "job_id": job_record.id,
        "application_id": application_record.id,
    }