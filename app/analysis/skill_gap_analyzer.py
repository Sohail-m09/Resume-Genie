from schemas.resume import Resume
from schemas.job_description import JobDescription
from schemas.skill_gap import SkillGapAnalysis
from services.matching_engine import match_skills
from llm.gemini import get_gemini_model


def detect_skill_gaps(
    resume: Resume,
    job_description: JobDescription,
) -> dict:
    """
    Detect missing required and preferred skills
    using the existing deterministic skill matcher.
    """

    skill_matches = match_skills(
        resume=resume,
        job_description=job_description,
    )

    return {
        "missing_required": skill_matches["required"]["missing"],
        "missing_preferred": skill_matches["preferred"]["missing"],
    }


def explain_skill_gaps(
    resume: Resume,
    job_description: JobDescription,
) -> SkillGapAnalysis:
    """
    Explain deterministic skill gaps using Gemini.

    Gemini does not determine whether a skill is missing.
    The deterministic matcher performs that task.
    """

    skill_gaps = detect_skill_gaps(
        resume=resume,
        job_description=job_description,
    )

    model = get_gemini_model().with_structured_output(
        SkillGapAnalysis
    )

    prompt = f"""
You are a professional resume and job-description analysis assistant.

Analyze the skill gaps identified between the candidate's resume
and the job description.

IMPORTANT:
The missing skills have already been determined by a deterministic
matching system. Do NOT add, remove, or reinterpret the missing skills.

Use ONLY the provided resume and job description.

Rules:
1. Do not invent candidate skills or experience.
2. Do not assume the candidate knows a skill unless the resume explicitly
   supports it.
3. Explain why each missing skill is relevant to the job.
4. Clearly distinguish required skills from preferred skills.
5. Recommendations must be realistic and actionable.
6. Do not claim that learning a skill guarantees getting shortlisted.
7. Do not invent projects or experience for the candidate.
8. If the resume provides no evidence about a missing skill, say so.
9. Keep explanations concise.

Structured Resume:
{resume.model_dump_json(indent=2)}

Structured Job Description:
{job_description.model_dump_json(indent=2)}

Deterministically Identified Skill Gaps:

Missing Required Skills:
{skill_gaps["missing_required"]}

Missing Preferred Skills:
{skill_gaps["missing_preferred"]}

Return the analysis using the provided SkillGapAnalysis schema.
"""

    return model.invoke(prompt)