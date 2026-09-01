from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import User


def create_user(
    db: Session,
    name: str | None,
    email: str,
) -> User:
    """
    Create and persist a new user.
    """

    user = User(
        name=name,
        email=email,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user_by_id(
    db: Session,
    user_id: int,
) -> User | None:
    """
    Retrieve a user by primary key.
    """

    statement = select(User).where(
        User.id == user_id
    )

    return db.scalar(statement)


def get_user_by_email(
    db: Session,
    email: str,
) -> User | None:
    """
    Retrieve a user by email.
    """

    statement = select(User).where(
        User.email == email
    )

    return db.scalar(statement)
