from pydantic import BaseModel, Field


class ResumeGenieRequest(BaseModel):
    """
    Request body for the complete Resume Genie workflow.
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

    section_order: list[str] | None = Field(
        default=None,
        description="Optional custom section order.",
    )

    removed_sections: list[str] | None = Field(
        default=None,
        description="Optional sections to remove.",
    )

    removed_projects: list[str] | None = Field(
        default=None,
        description="Optional projects to remove.",
    )