from pathlib import Path

from fastapi import (
    APIRouter,
    File,
    HTTPException,
    UploadFile,
)

from backend.schemas.requests import (
    JobTextRequest,
)

from backend.services.job_service import (
    process_job_text,
    process_job_pdf,
)

from backend.services.file_service import (
    validate_pdf_file,
    sanitize_filename,
    cleanup_file,
)


router = APIRouter(
    prefix="/api/job",
    tags=["Job Description"],
)


@router.post("/text")
def upload_job_text(
    request: JobTextRequest,
):
    """
    Process a pasted job description.
    """

    try:

        job_description = process_job_text(
            request.job_text
        )

        return {
            "job_description": (
                job_description.model_dump()
            )
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


@router.post("/pdf")
async def upload_job_pdf(
    file: UploadFile = File(...),
):
    """
    Upload and process a job-description PDF.
    """

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail=(
                "Only PDF job-description files "
                "are supported."
            ),
        )

    upload_directory = Path(
        "data/uploads"
    )

    upload_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path = (
        upload_directory / file.filename
    )

    content = await file.read()

    validate_pdf_file(
        filename=file.filename,
        content_type=file.content_type,
        content=content,
    )

    safe_filename = sanitize_filename(
        file.filename
    )

    file_path = (
        upload_directory / safe_filename
    )

    file_path.write_bytes(
        content
    )

    try:

        job_description = process_job_pdf(
            str(file_path)
        )

        return {
            "filename": safe_filename,
            "job_description": (
                job_description.model_dump()
            ),
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Job description processing failed.",
        )

    finally:

        cleanup_file(
            str(file_path)
        )

