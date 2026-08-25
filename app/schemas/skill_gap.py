from pydantic import BaseModel, Field


class MissingSkill(BaseModel):
    skill: str = Field(
        description="Skill required by the job description but not explicitly found in the resume."
    )

    importance: str = Field(
        description="Why this skill is relevant to the job."
    )

    explanation: str = Field(
        description="Explanation of the skill gap based only on the job description and resume evidence."
    )

    recommendation: str = Field(
        description="Actionable recommendation for addressing the skill gap."
    )


class SkillGapAnalysis(BaseModel):
    missing_skills: list[MissingSkill] = Field(
        description="Skills required or preferred by the job description that are missing from the resume."
    )