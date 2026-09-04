from pydantic import BaseModel, Field


class CoverLetterRequest(BaseModel):
    """
    Request body for generating a cover letter
    from a selected saved resume and job description.
    """

    resume_id: int = Field(
        description="ID of the selected saved resume.",
    )

    job_id: int = Field(
        description="ID of the selected saved job description.",
    )