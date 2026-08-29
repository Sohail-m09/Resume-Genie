from fastapi import (
    APIRouter,
    HTTPException,
)

from backend.services.analysis_service import (
    analyze_resume_for_job,
)

from application.resume_input import (
    process_resume_input,
)

from application.job_input import (
    process_job_description_input,
)

from backend.services.request_validation import (
    validate_job_input,
)


router = APIRouter(
    prefix="/api/analysis",
    tags=["Analysis"],
)


@router.post("/run")
def run_analysis(
    resume_path: str,
    job_text: str | None = None,
    job_pdf_path: str | None = None,
):
    """
    Run Resume Genie resume-vs-job analysis.

    The current development version accepts
    paths for the already-uploaded files.
    """

    validate_job_input(
        job_text=job_text,
        job_pdf_path=job_pdf_path,
    )

    try:

        resume, _ = process_resume_input(
            resume_path
        )

        job_description = (
            process_job_description_input(
                job_text=job_text,
                pdf_path=job_pdf_path,
            )
        )

        result = analyze_resume_for_job(
            resume=resume,
            job_description=job_description,
        )

        return {
            "analysis": result.model_dump()
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )
