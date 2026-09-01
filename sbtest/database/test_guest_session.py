from uuid import uuid4

from app.database.config.database import (
    SessionLocal,
)

from app.database.services.guest_session import (
    get_or_create_guest_user,
)


def test_same_session_returns_same_user():
    db = SessionLocal()

    session_id = str(
        uuid4()
    )

    try:

        user_1 = get_or_create_guest_user(
            db=db,
            session_id=session_id,
        )

        user_2 = get_or_create_guest_user(
            db=db,
            session_id=session_id,
        )

        assert user_1.id == user_2.id
        assert (
            user_1.session_id
            == session_id
        )

    finally:

        db.delete(user_1)
        db.commit()
        db.close()