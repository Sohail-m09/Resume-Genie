from sqlalchemy.orm import Session

from database.repositories import (
    update_tailored_resume,
    update_ats_score,
)


def persist_tailored_resume(
    db: Session,
    application_id: int,
    tailored_resume,
):
    """
    Persist the generated tailored resume.
    """

    result = tailored_resume.model_dump()

    return update_tailored_resume(
        db=db,
        application_id=application_id,
        tailored_resume=result,
    )


def persist_ats_result(
    db: Session,
    application_id: int,
    ats_result: dict,
):
    """
    Persist the ATS-oriented score.
    """

    ats_score = ats_result.get(
        "ats_score"
    )

    return update_ats_score(
        db=db,
        application_id=application_id,
        ats_score=ats_score,
    )