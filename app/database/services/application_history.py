from sqlalchemy.orm import Session

from database.repositories import (
    get_applications_by_user,
    get_application_by_id,
)


def get_user_application_history(
    db: Session,
    user_id: int,
):
    """
    Retrieve all application records belonging
    to a specific user.
    """

    return get_applications_by_user(
        db=db,
        user_id=user_id,
    )


def get_user_application_detail(
    db: Session,
    user_id: int,
    application_id: int,
):
    """
    Retrieve one application only if it belongs
    to the requested user.
    """

    application = get_application_by_id(
        db=db,
        application_id=application_id,
    )

    if application is None:
        return None

    if application.user_id != user_id:
        return None

    return application

