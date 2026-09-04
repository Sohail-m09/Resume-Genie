from fastapi import (
    APIRouter,
    Depends,
    Header,
    HTTPException,
)

from sqlalchemy.orm import Session

from backend.services.db_dependency import (
    get_db,
)

from backend.schemas.cover_letter import (
    CoverLetterRequest,
)

from backend.services.cover_letter_service import (
    generate_cover_letter,
)

from database.repositories import (
    get_user_by_session_id,
)


router = APIRouter(
    prefix="/api/cover-letter",
    tags=["Cover Letter"],
)


@router.post("/generate")
def generate_cover_letter_endpoint(
    request: CoverLetterRequest,
    session_id: str = Header(
        ...,
        alias="X-Session-ID",
    ),
    db: Session = Depends(get_db),
):
    """
    Generate a grounded cover letter using
    a selected saved resume and job description.
    """

    try:

        # --------------------------------------------------
        # 1. Resolve the current guest user
        # --------------------------------------------------

        user = get_user_by_session_id(
            db=db,
            session_id=session_id,
        )

        if user is None:
            raise HTTPException(
                status_code=404,
                detail="Session not found.",
            )

        # --------------------------------------------------
        # 2. Generate Cover Letter
        # --------------------------------------------------

        cover_letter = generate_cover_letter(
            db=db,
            user_id=user.id,
            resume_id=request.resume_id,
            job_id=request.job_id,
        )

        # --------------------------------------------------
        # 3. Return structured CoverLetter
        # --------------------------------------------------

        return {
            "resume_id": request.resume_id,
            "job_id": request.job_id,
            "cover_letter": (
                cover_letter.model_dump()
            ),
        }

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Cover Letter generation failed.",
        )