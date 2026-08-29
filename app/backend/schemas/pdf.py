from pydantic import BaseModel, Field


class PDFRequest(BaseModel):
    """
    Request body for generating a tailored resume PDF.
    """

    resume_path: str = Field(
        min_length=1,
        description="Path to the original uploaded resume PDF.",
    )

    job_text: str | None = Field(
        default=None,
        description="Pasted job description text.",
    )

    job_pdf_path: str | None = Field(
        default=None,
        description="Path to the uploaded job description PDF.",
    )

    section_order: list[str] | None = None

    removed_sections: list[str] | None = None

    removed_projects: list[str] | None = None