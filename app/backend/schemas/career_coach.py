from pydantic import BaseModel, Field


class CareerCoachRequest(BaseModel):
    """
    Request body for the Career Coach.
    """

    question: str = Field(
        min_length=3,
        description="Career-related question asked by the user.",
    )

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

