from pydantic import BaseModel, Field


class ResumeGenieRequest(BaseModel):
    """
    Request body for the complete Resume Genie workflow.
    Uses already-persisted Resume and Job records.
    """

    resume_id: int = Field(
        gt=0,
        description="ID of the already uploaded resume.",
    )

    job_id: int = Field(
        gt=0,
        description="ID of the already uploaded job description.",
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