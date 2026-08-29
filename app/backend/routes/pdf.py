from pathlib import Path

from fastapi import (
    APIRouter,
    HTTPException,
)
from fastapi.responses import FileResponse

from backend.schemas.pdf import (
    PDFRequest,
)

from backend.services.pdf_service import (
    generate_resume_pdf,
)

from backend.services.request_validation import (
    validate_job_input,
)


router = APIRouter(
    prefix="/api/pdf",
    tags=["PDF"],
)


@router.post("/generate")
def generate_pdf_endpoint(
    request: PDFRequest,
):
    """
    Generate and return the tailored resume PDF.
    """

    validate_job_input(
        job_text=request.job_text,
        job_pdf_path=request.job_pdf_path,
    )

    try:

        result = generate_resume_pdf(
            resume_path=request.resume_path,
            job_text=request.job_text,
            job_pdf_path=request.job_pdf_path,
            section_order=request.section_order,
            removed_sections=request.removed_sections,
            removed_projects=request.removed_projects,
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

        pdf_path = Path(
            result["pdf"]
        )

        if not pdf_path.exists():
            raise HTTPException(
                status_code=500,
                detail="Generated PDF was not found.",
            )

        return FileResponse(
            path=pdf_path,
            media_type="application/pdf",
            filename="tailored_resume.pdf",
        )

    except HTTPException:
        raise

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )
