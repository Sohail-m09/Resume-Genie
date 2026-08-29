from pydantic import BaseModel, Field


class JobTextRequest(BaseModel):
    """
    Request body for a pasted job description.
    """

    job_text: str = Field(
        min_length=20,
        description="Job description pasted by the user.",
    )


class ResumeCustomizationRequest(BaseModel):
    """
    Optional user customization for tailored resumes.
    """

    section_order: list[str] | None = None

    removed_sections: list[str] | None = None

    removed_projects: list[str] | None
