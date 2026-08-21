from pydantic import BaseModel, Field

class JobDescription(BaseModel):
    job_title : str | None = None
    company : str | None = None
    required_skills : list[str] = Field(default_factory = list)
    preferred_skills: list[str] = Field(default_factory=list)
    responsibilities: list[str] = Field(default_factory=list)
    experience_required: str | None = None
    education_required: str | None = None
    qualifications: list[str] = Field(default_factory=list)