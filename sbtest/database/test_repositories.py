from uuid import uuid4

from app.database.config.database import SessionLocal

from app.database.repositories import (
    create_user,
    get_user_by_id,
    get_user_by_email,
)


def test_user_repository_crud():
    db = SessionLocal()

    email = (
        f"repository-test-{uuid4()}@example.com"
    )

    try:
        # Create
        user = create_user(
            db=db,
            name="Repository Test User",
            email=email,
        )

        assert user.id is not None
        assert user.name == "Repository Test User"
        assert user.email == email

        # Get by ID
        retrieved_by_id = get_user_by_id(
            db=db,
            user_id=user.id,
        )

        assert retrieved_by_id is not None
        assert retrieved_by_id.id == user.id

        # Get by email
        retrieved_by_email = get_user_by_email(
            db=db,
            email=email,
        )

        assert retrieved_by_email is not None
        assert retrieved_by_email.id == user.id

    finally:
        # Cleanup test user
        test_user = get_user_by_email(
            db=db,
            email=email,
        )

        if test_user is not None:
            db.delete(test_user)
            db.commit()

        db.close()