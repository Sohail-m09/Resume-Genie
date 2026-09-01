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

from database.repositories import (
    get_user_by_session_id,
)

from database.services.application_history import (
    get_user_application_history,
    get_user_application_detail,
)


router = APIRouter(
    prefix="/api/history",
    tags=["Application History"],
)


@router.get("/applications")
def get_application_history(
    session_id: str = Header(
        ...,
        alias="X-Session-ID",
    ),
    db: Session = Depends(get_db),
):
    """
    Return the existing guest session's
    application history.
    """

    try:

        user = get_user_by_session_id(
            db=db,
            session_id=session_id,
        )

        if user is None:
            return {
                "count": 0,
                "applications": [],
            }

        applications = (
            get_user_application_history(
                db=db,
                user_id=user.id,
            )
        )

        return {
            "user_id": user.id,
            "count": len(applications),
            "applications": [
                {
                    "application_id": (
                        application.id
                    ),
                    "resume_id": (
                        application.resume_id
                    ),
                    "job_id": (
                        application.job_id
                    ),
                    "match_score": (
                        application.match_score
                    ),
                    "ats_score": (
                        application.ats_score
                    ),
                    "created_at": (
                        application.created_at
                    ),
                }
                for application in applications
            ],
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Application history retrieval failed.",
        )


@router.get(
    "/applications/{application_id}"
)
def get_application_detail(
    application_id: int,
    session_id: str = Header(
        ...,
        alias="X-Session-ID",
    ),
    db: Session = Depends(get_db),
):
    """
    Return one application belonging to
    the current guest session.
    """

    try:

        user = get_user_by_session_id(
            db=db,
            session_id=session_id,
        )

        if user is None:
            raise HTTPException(
                status_code=404,
                detail="Application not found.",
            )

        application = (
            get_user_application_detail(
                db=db,
                user_id=user.id,
                application_id=application_id,
            )
        )

        if application is None:
            raise HTTPException(
                status_code=404,
                detail="Application not found.",
            )

        return {
            "application_id": (
                application.id
            ),
            "user_id": (
                application.user_id
            ),
            "resume_id": (
                application.resume_id
            ),
            "job_id": (
                application.job_id
            ),
            "match_score": (
                application.match_score
            ),
            "ats_score": (
                application.ats_score
            ),
            "analysis_result": (
                application.analysis_result
            ),
            "tailored_resume": (
                application.tailored_resume
            ),
            "created_at": (
                application.created_at
            ),
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Application retrieval failed.",
        )