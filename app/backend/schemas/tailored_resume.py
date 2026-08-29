from pydantic import BaseModel, Field


class TailoredResumeRequest(BaseModel):
    """
    Request body for generating a tailored resume.
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

    section_order: list[str] | None = Field(
        default=None,
        description="Optional custom order for resume sections.",
    )

    removed_sections: list[str] | None = Field(
        default=None,
        description="Optional sections to remove.",
    )

    removed_projects: list[str] | None = Field(
        default=None,
        description="Optional projects to remove.",
    )

