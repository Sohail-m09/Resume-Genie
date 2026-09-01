from database.config.database import SessionLocal

from database.models import (
    User,
    Resume,
    Job,
    Application,
)

from database.services.analysis_persistence import (
    persist_analysis_result,
)

from types import SimpleNamespace


db = SessionLocal()

try:

    # -----------------------------------------------
    # Create test user
    # -----------------------------------------------

    user = User(
        name="Analysis Test User",
        email="analysis-test@example.com",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # -----------------------------------------------
    # Create test resume
    # -----------------------------------------------

    resume = Resume(
        user_id=user.id,
        filename="analysis_test_resume.pdf",
        summary="Python and SQL candidate.",
        storage_path="data/analysis_test_resume.pdf",
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    # -----------------------------------------------
    # Create test job
    # -----------------------------------------------

    job = Job(
        user_id=user.id,
        job_title="Junior Data Scientist",
        company="Analysis Test Company",
        source_type="text",
        required_skills=[
            "Python",
            "SQL",
        ],
        preferred_skills=[
            "MLOps",
        ],
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
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    # -----------------------------------------------
    # Mock analysis object
    # -----------------------------------------------

    analysis_result = SimpleNamespace(
        model_dump=lambda: {
            "overall_score": 72.5,
            "matched_required_skills": [
                "Python",
                "SQL",
            ],
            "missing_required_skills": [],
        }
    )

    # -----------------------------------------------
    # Persist analysis
    # -----------------------------------------------

    updated_application = (
        persist_analysis_result(
            db=db,
            application_id=application.id,
            analysis_result=analysis_result,
        )
    )

    print(
        "Analysis persisted successfully:"
    )

    print(
        {
            "application_id": (
                updated_application.id
            ),
            "match_score": (
                updated_application.match_score
            ),
            "analysis_result": (
                updated_application.analysis_result
            ),
        }
    )

finally:

    db.close()