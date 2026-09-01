from database.config.database import (
    SessionLocal,
)

from database.models import User


db = SessionLocal()

try:

    user = User(
        name="Resume Genie Test User",
        email="resume-genie-test@example.com",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    print(
        "User created successfully:"
    )

    print(
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at,
        }
    )

finally:

    db.close()