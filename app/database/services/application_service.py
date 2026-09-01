from sqlalchemy.orm import Session

from database.repositories import (
    create_application,
)


def create_application_from_analysis(
    db: Session,
    user_id: int,
    resume_id: int,
    job_id: int,
    analysis_result,
):
    """
    Create an Application record from a Resume Genie
    Resume-JD analysis result.
    """

    analysis_data = analysis_result.model_dump()

    match_score = analysis_data.get(
        "overall_score"
    )

    return create_application(
        db=db,
        user_id=user_id,
        resume_id=resume_id,
        job_id=job_id,
        match_score=match_score,
        analysis_result=analysis_data,
    )
