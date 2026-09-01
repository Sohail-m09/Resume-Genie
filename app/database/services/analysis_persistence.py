from sqlalchemy.orm import Session

from database.repositories import (
    update_application_analysis,
)


def persist_analysis_result(
    db: Session,
    application_id: int,
    analysis_result,
):
    """
    Persist the Resume Genie analysis result
    for an existing application.
    """

    result_data = analysis_result.model_dump()

    overall_score = result_data.get(
        "overall_score"
    )

    application = update_application_analysis(
        db=db,
        application_id=application_id,
        match_score=overall_score,
        analysis_result=result_data,
    )

    return application