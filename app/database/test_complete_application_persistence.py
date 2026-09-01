from sqlalchemy.orm import Session

from database.config.database import (
    SessionLocal,
)

from database.models import (
    User,
    Resume,
    Job,
    Application,
)

from database.services.complete_application_persistence import (
    persist_tailored_and_ats,
)

from resume_generator.tailoring import (
    TailoredResume,
)


db: Session = SessionLocal()

try:

    # -----------------------------------------------
    # Create user
    # -----------------------------------------------

    user = User(
        name="Complete Result Test User",
        email="complete-result-test@example.com",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # -----------------------------------------------
    # Create resume
    # -----------------------------------------------

    resume = Resume(
        user_id=user.id,
        filename="complete_result_resume.pdf",
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
        company="Complete Result Test Company",
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
        match_score=78.5,
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    # -----------------------------------------------
    # Tailored resume
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

    # -----------------------------------------------
    # ATS result
    # -----------------------------------------------

    ats_result = {
        "ats_score": 84.0,
        "components": {
            "required_keyword_coverage": {
                "score": 80.0,
                "weight": 40.0,
            }
        },
    }

    # -----------------------------------------------
    # Persist
    # -----------------------------------------------

    updated_application = (
        persist_tailored_and_ats(
            db=db,
            application_id=application.id,
            tailored_resume=tailored_resume,
            ats_result=ats_result,
        )
    )

    print(
        "Complete application result persisted successfully:"
    )

    print(
        {
            "application_id": (
                updated_application.id
            ),
            "user_id": (
                updated_application.user_id
            ),
            "resume_id": (
                updated_application.resume_id
            ),
            "job_id": (
                updated_application.job_id
            ),
            "match_score": (
                updated_application.match_score
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