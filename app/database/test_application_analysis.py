from types import SimpleNamespace

from database.config.database import (
    SessionLocal,
)

from database.models import (
    User,
    Resume,
    Job,
)

from database.services.application_service import (
    create_application_from_analysis,
)


db = SessionLocal()

try:

    # -----------------------------------------------
    # Create user
    # -----------------------------------------------

    user = User(
        name="API Integration Test User",
        email="api-analysis-test@example.com",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # -----------------------------------------------
    # Create resume
    # -----------------------------------------------

    resume = Resume(
        user_id=user.id,
        filename="api_analysis_resume.pdf",
        summary="Python and SQL candidate.",
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
        company="API Analysis Test Company",
        source_type="text",
        required_skills=[
            "Python",
            "SQL",
        ],
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    # -----------------------------------------------
    # Mock Resume Genie analysis
    # -----------------------------------------------

    analysis_result = SimpleNamespace(
        model_dump=lambda: {
            "overall_score": 78.5,
            "matched_required_skills": [
                "Python",
                "SQL",
            ],
            "missing_required_skills": [
                "Hyperparameter Tuning",
            ],
        }
    )

    # -----------------------------------------------
    # Create application
    # -----------------------------------------------

    application = (
        create_application_from_analysis(
            db=db,
            user_id=user.id,
            resume_id=resume.id,
            job_id=job.id,
            analysis_result=analysis_result,
        )
    )

    print(
        "Application created from analysis:"
    )

    print(
        {
            "application_id": application.id,
            "user_id": application.user_id,
            "resume_id": application.resume_id,
            "job_id": application.job_id,
            "match_score": application.match_score,
            "analysis_result": application.analysis_result,
        }
    )

finally:

    db.close()