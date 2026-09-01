from database.config.database import SessionLocal

from database.models import (
    User,
    Job,
)


db = SessionLocal()

try:

    user = User(
        name="Job Test User",
        email="job-test@example.com",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    job = Job(
        user_id=user.id,
        job_title="Junior Data Scientist",
        company="Test Company",
        source_type="text",
        required_skills=[
            "Python",
            "SQL",
            "Machine Learning",
        ],
        preferred_skills=[
            "MLOps",
            "Data Versioning",
        ],
        responsibilities=[
            "Build machine learning models.",
            "Perform exploratory data analysis.",
        ],
        qualifications=[
            "Bachelor's degree in Engineering.",
        ],
        education_required=(
            "Bachelor's degree in Computer Science, "
            "Engineering, Mathematics, or related field."
        ),
        experience_required=None,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    print("Job created successfully:")

    print(
        {
            "id": job.id,
            "user_id": job.user_id,
            "job_title": job.job_title,
            "source_type": job.source_type,
        }
    )

finally:

    db.close()
