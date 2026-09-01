from database.config.database import SessionLocal

from database.models import (
    User,
    Resume,
    Job,
    Application,
)

from database.services.resume_result_persistence import (
    persist_tailored_resume,
    persist_ats_result,
)

from resume_generator.tailoring import (
    TailoredResume,
    TailoredProject,
    TailoredEducation,
)


db = SessionLocal()

try:

    # -----------------------------------------------
    # Create test user
    # -----------------------------------------------

    user = User(
        name="Result Test User",
        email="result-test@example.com",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # -----------------------------------------------
    # Create resume
    # -----------------------------------------------

    resume = Resume(
        user_id=user.id,
        filename="result_test_resume.pdf",
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
        company="Result Test Company",
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
    # Tailored resume result
    # -----------------------------------------------

    tailored_resume = TailoredResume(
        summary=(
            "Junior Data Scientist with "
            "Python and SQL."
        ),
        skills=[
            "Python",
            "SQL",
        ],
        projects=[],
        experience=[],
        education=[],
        certifications=[],
        section_order=[
            "summary",
            "skills",
            "projects",
            "education",
            "certifications",
        ],
    )

    updated_application = (
        persist_tailored_resume(
            db=db,
            application_id=application.id,
            tailored_resume=tailored_resume,
        )
    )

    # -----------------------------------------------
    # ATS result
    # -----------------------------------------------

    ats_result = {
        "ats_score": 82.5,
        "components": {
            "required_keyword_coverage": {
                "score": 80.0,
                "weight": 40.0,
            }
        },
    }

    updated_application = (
        persist_ats_result(
            db=db,
            application_id=application.id,
            ats_result=ats_result,
        )
    )

    print(
        "Resume and ATS results persisted successfully:"
    )

    print(
        {
            "application_id": (
                updated_application.id
            ),
            "ats_score": (
                updated_application.ats_score
            ),
            "tailored_resume": (
                updated_application.tailored_resume
            ),
        }
    )

finally:

    db.close()