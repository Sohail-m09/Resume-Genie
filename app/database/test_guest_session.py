from uuid import uuid4

from database.config.database import (
    SessionLocal,
)

from database.services.guest_session import (
    get_or_create_guest_user,
)


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

    print(
        "Guest user created successfully:"
    )

    print(
        {
            "user_id": user_1.id,
            "session_id": user_1.session_id,
        }
    )

    print(
        "\nSame session returned same user:"
    )

    print(
        user_1.id == user_2.id
    )

finally:

    db.close()