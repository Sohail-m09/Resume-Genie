from fastapi import (
    APIRouter,
    HTTPException,
)

from backend.schemas.ats import (
    ATSRequest,
)

from backend.services.ats_service import (
    calculate_ats_for_application,
)

from backend.services.request_validation import (
    validate_job_input,
)


router = APIRouter(
    prefix="/api/ats",
    tags=["ATS"],
)


@router.post("/score")
def calculate_ats_endpoint(
    request: ATSRequest,
):
    """
    Calculate the ATS-oriented optimization score
    for a job-tailored resume.
    """

    validate_job_input(
        job_text=request.job_text,
        job_pdf_path=request.job_pdf_path,
    )

    try:

        result = calculate_ats_for_application(
            resume_path=request.resume_path,
            job_text=request.job_text,
            job_pdf_path=request.job_pdf_path,
        )

        if result["ats"] is None:
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
            "ats": result["ats"],
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