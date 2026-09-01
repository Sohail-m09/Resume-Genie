from sqlalchemy.orm import Session

from database.repositories import (
    get_user_by_session_id,
    create_guest_user,
)


def get_or_create_guest_user(
    db: Session,
    session_id: str,
):
    """
    Return the existing guest user for a session,
    or create one if it does not exist.
    """

    user = get_user_by_session_id(
        db=db,
        session_id=session_id,
    )

    if user is not None:
        return user

    return create_guest_user(
        db=db,
        session_id=session_id,
    )
