from database.config.database import SessionLocal

from database.models import (
    User,
    Resume,
)


db = SessionLocal()

try:

    user = User(
        name="Resume Test User",
        email="resume-test@example.com",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    resume = Resume(
        user_id=user.id,
        filename="sample_resume.pdf",
        summary="Python and SQL candidate.",
        storage_path="data/sample_resume.pdf",
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    print("User created:")
    print(
        {
            "id": user.id,
            "email": user.email,
        }
    )

    print("\nResume created:")
    print(
        {
            "id": resume.id,
            "user_id": resume.user_id,
            "filename": resume.filename,
        }
    )

finally:

    db.close()
