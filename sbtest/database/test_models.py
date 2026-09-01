from app.database.models import (
    User,
    Resume,
    Job,
    Application,
)


def test_user_table_name():
    assert User.__tablename__ == "users"


def test_resume_table_name():
    assert Resume.__tablename__ == "resumes"


def test_job_table_name():
    assert Job.__tablename__ == "jobs"


def test_application_table_name():
    assert Application.__tablename__ == "applications"