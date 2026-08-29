from pydantic import BaseModel, Field


class ATSRequest(BaseModel):
    """
    Request body for ATS-oriented resume scoring.
    """

    resume_path: str = Field(
        min_length=1,
        description="Path to the uploaded resume PDF.",
    )

    job_text: str | None = Field(
        default=None,
        description="Pasted job description text.",
    )

    job_pdf_path: str | None = Field(
        default=None,
        description="Path to the uploaded job description PDF.",
    )

