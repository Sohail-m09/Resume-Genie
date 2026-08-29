from fastapi import (
    APIRouter,
    HTTPException,
)

from backend.schemas.career_coach import (
    CareerCoachRequest,
)

from backend.services.career_coach_service import (
    ask_career_coach_for_application,
)

from backend.services.request_validation import (
    validate_job_input,
)

router = APIRouter(
    prefix="/api/career-coach",
    tags=["Career Coach"],
)


@router.post("/ask")
def ask_career_coach_endpoint(
    request: CareerCoachRequest,
):
    """
    Ask the Resume Genie Career Coach.
    """

    validate_job_input(
        job_text=request.job_text, 
        job_pdf_path=request.job_pdf_path,
    )

    try:

        answer = ask_career_coach_for_application(
            question=request.question,
            resume_path=request.resume_path,
            job_text=request.job_text,
            job_pdf_path=request.job_pdf_path,
        )

        return {
            "question": request.question,
            "answer": answer,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )
