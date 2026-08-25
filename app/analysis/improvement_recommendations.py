from schemas.resume_analysis import ImprovementRecommendations
from llm.gemini import get_gemini_model


def generate_improvement_recommendations(
    skill_gaps: dict,
) -> ImprovementRecommendations:
    """
    Generate resume improvement recommendations
    based on identified skill gaps.

    Args:
        skill_gaps: Missing required and preferred skills.

    Returns:
        Structured improvement recommendations.
    """

    model = get_gemini_model()

    prompt = f"""
You are a resume improvement assistant.

Analyze the following skill gaps identified by a deterministic
resume-to-job-description matching system.

Skill gaps:
{skill_gaps}

For each missing skill, provide:

1. skill
2. category
3. reason
4. recommendation

Rules:

- Base recommendations only on the provided skill gaps.
- Do not invent skills or resume experience.
- Do not claim that the candidate has a skill that is missing.
- Do not recommend falsely adding a skill to the resume.
- If a skill is genuinely learned or used later, explain that
  the candidate can add the relevant evidence.
- Keep recommendations practical and concise.
"""

    structured_model = model.with_structured_output(
        ImprovementRecommendations
    )

    return structured_model.invoke(prompt)