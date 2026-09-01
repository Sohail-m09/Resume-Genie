from database.config.database import SessionLocal

from database.models import (
    User,
    Resume,
    Job,
    Application,
)


db = SessionLocal()

try:

    # -----------------------------------------------
    # Create user
    # -----------------------------------------------

    user = User(
        name="Application Test User",
        email="application-test@example.com",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # -----------------------------------------------
    # Create resume
    # -----------------------------------------------

    resume = Resume(
        user_id=user.id,
        filename="application_test_resume.pdf",
        summary="Python and SQL candidate.",
        storage_path="data/application_test_resume.pdf",
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    # -----------------------------------------------
    # Create job
    # -----------------------------------------------

    job = Job(
        user_id=user.id,
        job_title="Junior Data Scientist",
        company="Application Test Company",
        source_type="text",
        required_skills=[
            "Python",
            "SQL",
        ],
        preferred_skills=[
            "MLOps",
        ],
        responsibilities=[
            "Build machine learning models.",
        ],
        qualifications=[
            "Bachelor's degree in Engineering.",
        ],
        education_required=(
            "Bachelor's degree in Engineering."
        ),
        experience_required=None,
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    # -----------------------------------------------
    # Create application
    # -----------------------------------------------

    application = Application(
        user_id=user.id,
        resume_id=resume.id,
        job_id=job.id,
        match_score=75.0,
        ats_score=82.5,
        analysis_result={
            "matched_skills": [
                "Python",
                "SQL",
            ]
        },
        tailored_resume={
            "summary": (
                "Junior Data Scientist with "
                "Python and SQL."
            )
        },
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    print("Application created successfully:")

    print(
        {
            "application_id": application.id,
            "user_id": application.user_id,
            "resume_id": application.resume_id,
            "job_id": application.job_id,
            "match_score": application.match_score,
            "ats_score": application.ats_score,
        }
    )

finally:

    db.close()