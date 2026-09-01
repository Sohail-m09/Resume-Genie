from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    File,
    Header,
    HTTPException,
    UploadFile,
)

from sqlalchemy.orm import Session

from backend.services.db_dependency import (
    get_db,
)

from database.services.guest_session import (
    get_or_create_guest_user,
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
    session_id: str = Header(
        ...,
        alias="X-Session-ID",
    ),
    db: Session = Depends(get_db),
):
    """
    Upload and process a resume PDF for a guest session.
    """

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF resume files are supported.",
        )

    upload_directory = Path(
        "data/uploads"
    )

    upload_directory.mkdir(
        parents=True,
        exist_ok=True,
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

        user = get_or_create_guest_user(
            db=db,
            session_id=session_id,
        )

        result = process_uploaded_resume(
            db=db,
            file_path=str(file_path),
            user_id=user.id,
        )

        return {
            "filename": safe_filename,
            "user_id": user.id,
            "resume_id": result["resume_id"],
            "chunk_count": result["chunk_count"],
            "resume": (
                result["resume"].model_dump()
            ),
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Resume processing failed.",
        )

    finally:

        cleanup_file(
            str(file_path)
        )