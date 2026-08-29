from fastapi import HTTPException


def validate_job_input(
    job_text: str | None,
    job_pdf_path: str | None,
) -> None:
    """
    Validate that exactly one job-description input
    is provided.
    """

    has_text = (
        job_text is not None
        and bool(job_text.strip())
    )

    has_pdf = (
        job_pdf_path is not None
        and bool(job_pdf_path.strip())
    )

    if has_text and has_pdf:
        raise HTTPException(
            status_code=400,
            detail=(
                "Provide either job_text or "
                "job_pdf_path, not both."
            ),
        )

    if not has_text and not has_pdf:
        raise HTTPException(
            status_code=400,
            detail=(
                "Provide either job_text or "
                "job_pdf_path."
            ),
        )