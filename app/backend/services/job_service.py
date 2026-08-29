from pathlib import Path

from application.job_input import (
    process_job_description_input,
)


def process_job_text(
    job_text: str,
):
    """
    Process pasted job-description text.
    """

    return process_job_description_input(
        job_text=job_text,
    )


def process_job_pdf(
    file_path: str,
):
    """
    Process a job-description PDF.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Job description file not found: {file_path}"
        )

    return process_job_description_input(
        pdf_path=str(path),
    )

