from pydantic import BaseModel, Field


class ResumeImprovement(BaseModel):
    section: str = Field(
        description="Resume section that needs improvement."
    )

    issue: str = Field(
        description="Specific weakness identified in the resume."
    )

    suggestion: str = Field(
        description="Actionable suggestion to improve the section."
    )


class ResumeAnalysis(BaseModel):
    overall_assessment: str = Field(
        description="Concise overall assessment of the resume."
    )

    improvements: list[ResumeImprovement] = Field(
        description="Actionable resume improvement suggestions."
    )

class ImprovementRecommendation(BaseModel):
    skill: str
    category: str
    reason: str
    recommendation: str


class ImprovementRecommendations(BaseModel):
    recommendations: list[ImprovementRecommendation]

class ProjectImprovement(BaseModel):
    project_name: str
    strength: str
    weakness: str
    recommendation: str


class ProjectStrengthening(BaseModel):
    improvements: list[ProjectImprovement]



class ExperienceImprovement(BaseModel):
    role: str
    strength: str
    weakness: str
    recommendation: str



class ExperienceStrengthening(BaseModel):
    improvements: list[ExperienceImprovement]
    note: str | None = None

class FinalResumeAnalysis(BaseModel):
    overall_score: float | None
    score_components: dict

    matched_required_skills: list[str]
    missing_required_skills: list[str]

    matched_preferred_skills: list[str]
    missing_preferred_skills: list[str]

    semantic_evidence: list[dict]

    improvement_recommendations: list[ImprovementRecommendation]

    project_improvements: list[ProjectImprovement]
    experience_improvements: list[ExperienceImprovement]
    experience_note: str | None = None