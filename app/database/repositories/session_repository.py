from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import User


def get_user_by_session_id(
    db: Session,
    session_id: str,
) -> User | None:
    """
    Retrieve a guest user by session ID.
    """

    statement = select(User).where(
        User.session_id == session_id
    )

    return db.scalar(statement)


def create_guest_user(
    db: Session,
    session_id: str,
) -> User:
    """
    Create a guest user associated with a session ID.
    """

    user = User(
        session_id=session_id,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user