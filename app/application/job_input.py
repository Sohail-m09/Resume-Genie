from pathlib import Path

from ingestion.pdf_loader import load_pdf
from processing.text_cleaner import clean_documents
from processing.text_extractor import extract_text
from extraction.job_extractor import extract_job_description
from schemas.job_description import JobDescription


def process_job_description_text(
    job_text: str,
) -> JobDescription:
    """
    Convert pasted job-description text into
    the structured JobDescription schema.
    """

    if not job_text.strip():
        raise ValueError(
            "Job description text cannot be empty."
        )

    job_description = extract_job_description(
        job_text
    )

    return job_description


def process_job_description_pdf(
    file_path: str,
) -> JobDescription:
    """
    Convert a job-description PDF into
    the structured JobDescription schema.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Job description PDF not found: {file_path}"
        )

    documents = load_pdf(
        str(path)
    )

    cleaned_documents = clean_documents(
        documents
    )

    job_text = extract_text(
        cleaned_documents
    )

    return extract_job_description(
        job_text
    )


def process_job_description_input(
    job_text: str | None = None,
    pdf_path: str | None = None,
) -> JobDescription:
    """
    Unified JD input handler.

    Exactly one input method must be provided:
    - pasted job-description text
    - PDF path
    """

    has_text = (
        job_text is not None
        and bool(job_text.strip())
    )

    has_pdf = (
        pdf_path is not None
    )

    if has_text and has_pdf:
        raise ValueError(
            "Provide either job_text or pdf_path, "
            "not both."
        )

    if not has_text and not has_pdf:
        raise ValueError(
            "A job description must be provided "
            "as text or PDF."
        )

    if has_text:
        return process_job_description_text(
            job_text
        )

    return process_job_description_pdf(
        pdf_path
    )
