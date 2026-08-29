from fastapi import (
    APIRouter,
    File,
    HTTPException,
    UploadFile,
)

from backend.services.resume_service import (
    process_uploaded_resume,
)
from backend.services.file_service import (
    validate_pdf_file,
    sanitize_filename,
    cleanup_file,
)


router = APIRouter(
    prefix="/api/resume",
    tags=["Resume"],
)


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
):
    """
    Upload and process a resume PDF.
    """

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF resume files are supported.",
        )

    upload_directory = "data/uploads"

    from pathlib import Path

    directory = Path(
        upload_directory
    )

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_path = (
        directory / file.filename
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
        directory / safe_filename
    )

    file_path.write_bytes(
        content
    )

    try:

        result = process_uploaded_resume(
            str(file_path)
        )

        return {
            "filename": safe_filename,
            "chunk_count": result[
                "chunk_count"
            ],
            "resume": (
                result["resume"].model_dump()
            ),
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Resume processing failed.",
        )

    finally:

        cleanup_file(
            str(file_path)
        )

