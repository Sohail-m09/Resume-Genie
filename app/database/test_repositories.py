from database.config.database import SessionLocal

from database.models import (
    User,
)

from database.repositories import (
    create_user,
    get_user_by_email,
)


db = SessionLocal()

try:

    email = "repository-test@example.com"

    user = create_user(
        db=db,
        name="Repository Test User",
        email=email,
    )

    print(
        "User created through repository:"
    )

    print(
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        }
    )

    retrieved_user = get_user_by_email(
        db=db,
        email=email,
    )

    print(
        "\nUser retrieved through repository:"
    )

    print(
        {
            "id": retrieved_user.id,
            "name": retrieved_user.name,
            "email": retrieved_user.email,
        }
        if retrieved_user
        else None
    )

finally:

    db.close()