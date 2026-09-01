from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import Application


def create_application(
    db: Session,
    user_id: int,
    resume_id: int,
    job_id: int,
    match_score: float | None = None,
    ats_score: float | None = None,
    analysis_result: dict | None = None,
    tailored_resume: dict | None = None,
) -> Application:
    """
    Create and persist an application record.
    """

    application = Application(
        user_id=user_id,
        resume_id=resume_id,
        job_id=job_id,
        match_score=match_score,
        ats_score=ats_score,
        analysis_result=analysis_result,
        tailored_resume=tailored_resume,
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return application


def get_application_by_id(
    db: Session,
    application_id: int,
) -> Application | None:
    """
    Retrieve an application by ID.
    """

    statement = select(Application).where(
        Application.id == application_id
    )

    return db.scalar(statement)


def get_applications_by_user(
    db: Session,
    user_id: int,
) -> list[Application]:
    """
    Retrieve all applications belonging to a user.
    """

    statement = (
        select(Application)
        .where(
            Application.user_id == user_id
        )
        .order_by(
            Application.created_at.desc()
        )
    )

    return list(
        db.scalars(statement)
    )

def update_application_analysis(
    db: Session,
    application_id: int,
    match_score: float | None,
    analysis_result: dict | None,
) -> Application | None:
    """
    Update an application with Resume Genie analysis results.
    """

    application = get_application_by_id(
        db=db,
        application_id=application_id,
    )

    if application is None:
        return None

    application.match_score = match_score
    application.analysis_result = analysis_result

    db.commit()
    db.refresh(application)

    return application

def update_tailored_resume(
    db: Session,
    application_id: int,
    tailored_resume: dict,
) -> Application | None:
    """
    Persist the generated tailored resume for an application.
    """

    application = get_application_by_id(
        db=db,
        application_id=application_id,
    )

    if application is None:
        return None

    application.tailored_resume = (
        tailored_resume
    )

    db.commit()
    db.refresh(application)

    return application


def update_ats_score(
    db: Session,
    application_id: int,
    ats_score: float | None,
) -> Application | None:
    """
    Persist the ATS-oriented score for an application.
    """

    application = get_application_by_id(
        db=db,
        application_id=application_id,
    )

    if application is None:
        return None

    application.ats_score = ats_score

    db.commit()
    db.refresh(application)

    return application