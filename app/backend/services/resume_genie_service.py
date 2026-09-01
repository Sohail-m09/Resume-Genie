from pathlib import Path

from sqlalchemy.orm import Session

from application.pipeline import (
    run_resume_genie,
)

from database.repositories import (
    create_resume,
    create_job,
    create_application,
)


def run_complete_resume_genie(
    db: Session,
    user_id: int,
    resume_path: str,
    job_text: str | None = None,
    job_pdf_path: str | None = None,
    section_order: list[str] | None = None,
    removed_sections: list[str] | None = None,
    removed_projects: list[str] | None = None,
):
    """
    Run the complete Resume Genie workflow and persist
    the resulting Resume, Job, and Application records.
    """

    # --------------------------------------------------
    # 1. Run the existing Resume Genie pipeline
    # --------------------------------------------------

    result = run_resume_genie(
        resume_path=resume_path,
        job_text=job_text,
        job_pdf_path=job_pdf_path,
        section_order=section_order,
        removed_sections=removed_sections,
        removed_projects=removed_projects,
    )

    resume = result["analysis"]
    tailored_resume = result["tailored_resume"]

    # --------------------------------------------------
    # 2. Create Resume database record
    # --------------------------------------------------

    original_resume = None

    # The pipeline does not expose the original Resume
    # directly in its returned dictionary, so we extract
    # the basic persisted metadata from the input file.

    resume_file = Path(
        resume_path
    )

    resume_record = create_resume(
        db=db,
        user_id=user_id,
        filename=resume_file.name,
        summary=None,
        storage_path=str(resume_file),
    )

    # --------------------------------------------------
    # 3. Extract JobDescription data
    # --------------------------------------------------

    # The pipeline does not return the JobDescription
    # separately, so process the JD structure from the
    # same input using the existing application layer.

    from application.job_input import (
        process_job_description_input,
    )

    job_description = (
        process_job_description_input(
            job_text=job_text,
            pdf_path=job_pdf_path,
        )
    )

    job_data = (
        job_description.model_dump()
    )

    source_type = (
        "pdf"
        if job_pdf_path is not None
        else "text"
    )

    # --------------------------------------------------
    # 4. Create Job database record
    # --------------------------------------------------

    job_record = create_job(
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

    # --------------------------------------------------
    # 5. Prepare Application result
    # --------------------------------------------------

    analysis_data = (
        result["analysis"].model_dump()
    )

    tailored_resume_data = (
        tailored_resume.model_dump()
    )

    ats_result = result["ats"]

    ats_score = None

    if ats_result is not None:
        ats_score = ats_result.get(
            "ats_score"
        )

    match_score = (
        analysis_data.get(
            "overall_score"
        )
    )

    # --------------------------------------------------
    # 6. Create Application record
    # --------------------------------------------------

    application_record = (
        create_application(
            db=db,
            user_id=user_id,
            resume_id=resume_record.id,
            job_id=job_record.id,
            match_score=match_score,
            ats_score=ats_score,
            analysis_result=analysis_data,
            tailored_resume=tailored_resume_data,
        )
    )

    # --------------------------------------------------
    # 7. Return complete result + database IDs
    # --------------------------------------------------

    return {
        **result,
        "user_id": user_id,
        "resume_id": resume_record.id,
        "job_id": job_record.id,
        "application_id": (
            application_record.id
        ),
    }