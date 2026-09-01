from sqlalchemy.orm import Session

from database.repositories import (
    update_tailored_resume,
    update_ats_score,
)


def persist_tailored_and_ats(
    db: Session,
    application_id: int,
    tailored_resume,
    ats_result: dict,
):
    """
    Persist the tailored resume and ATS score
    for an existing application.
    """

    tailored_resume_data = (
        tailored_resume.model_dump()
    )

    application = update_tailored_resume(
        db=db,
        application_id=application_id,
        tailored_resume=tailored_resume_data,
    )

    if application is None:
        return None

    ats_score = ats_result.get(
        "ats_score"
    )

    application = update_ats_score(
        db=db,
        application_id=application_id,
        ats_score=ats_score,
    )

    return application