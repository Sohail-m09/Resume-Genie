from pydantic import BaseModel, Field


class CoverLetter(BaseModel):
    opening: str = Field(
        description="Opening paragraph introducing the candidate and interest in the role."
    )

    relevant_experience: str = Field(
        description="Evidence-based paragraph connecting the candidate's actual background to the job."
    )

    relevant_projects: str = Field(
        description="Evidence-based discussion of relevant projects and technologies."
    )

    motivation: str = Field(
        description="Why the candidate is interested in the role, without inventing personal information."
    )

    closing: str = Field(
        description="Professional closing paragraph."
    )

class CoverLetterEvidence(BaseModel):
    relevant_skills: list[str] = Field(
        description="Resume skills directly relevant to the target job."
    )

    relevant_projects: list[str] = Field(
        description="Existing resume project names relevant to the target job."
    )

    relevant_experience: list[str] = Field(
        description="Existing professional experience relevant to the target job."
    )

    supporting_evidence: list[str] = Field(
        description="Specific resume facts, technologies, achievements, or metrics that can safely support the cover letter."
    )