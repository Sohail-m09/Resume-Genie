from pydantic import BaseModel, Field


class CareerCoachRequest(BaseModel):
    """
    Request body for the Resume Genie Career Coach.
    """

    question: str = Field(
        min_length=3,
        description="Career-related question asked by the user.",
    )

    resume_id: int = Field(
        description="ID of the selected saved resume.",
    )

    job_id: int = Field(
        description="ID of the selected saved job.",
    )