from fastapi import (
    APIRouter,
    HTTPException,
)

from backend.schemas.tailored_resume import (
    TailoredResumeRequest,
)

from backend.services.tailored_resume_service import (
    generate_tailored_resume_for_application,
)

from backend.services.request_validation import (
    validate_job_input,
)


router = APIRouter(
    prefix="/api/tailored-resume",
    tags=["Tailored Resume"],
)


@router.post("/generate")
def generate_tailored_resume_endpoint(
    request: TailoredResumeRequest,
):
    """
    Generate a validated job-tailored resume.
    """

    validate_job_input(
        job_text=request.job_text,
        job_pdf_path=request.job_pdf_path,
    )

    try:

        result = (
            generate_tailored_resume_for_application(
                resume_path=request.resume_path,
                job_text=request.job_text,
                job_pdf_path=request.job_pdf_path,
                section_order=request.section_order,
                removed_sections=request.removed_sections,
                removed_projects=request.removed_projects,
            )
        )

        if not result["validation"]["valid"]:
            raise HTTPException(
                status_code=422,
                detail={
                    "message": (
                        "Tailored resume failed "
                        "validation."
                    ),
                    "validation": result[
                        "validation"
                    ],
                },
            )

        return {
            "tailored_resume": (
                result["tailored_resume"].model_dump()
            ),
            "validation": result[
                "validation"
            ],
        }

    except HTTPException:
        raise

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )

