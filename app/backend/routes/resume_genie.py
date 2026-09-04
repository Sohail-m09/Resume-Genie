from fastapi import (
    APIRouter,
    Depends,
    Header,
    HTTPException,
)

from sqlalchemy.orm import Session

from backend.schemas.resume_genie import (
    ResumeGenieRequest,
)

from backend.services.resume_genie_service import (
    run_complete_resume_genie,
)

from backend.services.db_dependency import (
    get_db,
)


router = APIRouter(
    prefix="/api/resume-genie",
    tags=["Resume Genie"],
)


@router.post("/run")
def run_resume_genie_endpoint(
    request: ResumeGenieRequest,
    session_id: str = Header(
        ...,
        alias="X-Session-ID",
    ),
    db: Session = Depends(get_db),
):
    """
    Run the complete Resume Genie workflow
    using existing Resume and Job records,
    and persist the resulting application.
    """

    try:

        from database.repositories import (
            get_user_by_session_id,
        )

        user = get_user_by_session_id(
            db=db,
            session_id=session_id,
        )

        if user is None:
            raise HTTPException(
                status_code=404,
                detail="Session not found.",
            )

        result = (
            run_complete_resume_genie(
                db=db,
                user_id=user.id,
                resume_id=request.resume_id,
                job_id=request.job_id,
                section_order=request.section_order,
                removed_sections=request.removed_sections,
                removed_projects=request.removed_projects,
            )
        )

        return {
            "user_id": result[
                "user_id"
            ],
            "application_id": result[
                "application_id"
            ],
            "resume_id": result[
                "resume_id"
            ],
            "job_id": result[
                "job_id"
            ],
            "analysis": (
                result[
                    "analysis"
                ].model_dump()
            ),
            "tailored_resume": (
                result[
                    "tailored_resume"
                ].model_dump()
            ),
            "validation": result[
                "validation"
            ],
            "ats": result[
                "ats"
            ],
            "pdf": result[
                "pdf"
            ],
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
            detail="Resume Genie workflow failed.",
        )