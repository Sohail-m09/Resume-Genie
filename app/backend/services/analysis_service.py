from application.pipeline import (
    analyze_application,
)


def analyze_resume_for_job(
    resume,
    job_description,
):
    """
    Run the existing Resume Genie analysis engine.
    """

    return analyze_application(
        resume=resume,
        job_description=job_description,
    )