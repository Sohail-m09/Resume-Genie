from schemas.resume import Resume
from schemas.job_description import JobDescription
from schemas.resume_analysis import ExperienceStrengthening
from llm.gemini import get_gemini_model


def strengthen_experience(
    resume: Resume,
    job_description: JobDescription,
) -> ExperienceStrengthening:
    """
    Analyze existing professional experience against the JD.

    If no professional experience exists, return an explicit
    no-experience result instead of generating fictional content.
    """

    if not resume.experience:
        return ExperienceStrengthening(
            improvements=[],
            note=(
                "No professional experience is available in the "
                "structured resume data for analysis."
            ),
        )

    model = get_gemini_model().with_structured_output(
        ExperienceStrengthening
    )

    prompt = f"""
You are a professional resume optimization assistant.

Analyze the candidate's EXISTING professional experience
against the target job description.

Rules:
1. Use only information present in the resume and job description.
2. Do not invent responsibilities, technologies, achievements,
   metrics, or employment history.
3. Do not create fictional experience.
4. Identify genuine strengths of existing experience.
5. Identify weaknesses in how the experience is presented.
6. Suggest how existing evidence could be presented more clearly.
7. Focus on responsibilities, technologies, measurable impact,
   ownership, and relevance to the target role.
8. If experience does not provide evidence for a JD requirement,
   state that clearly.

Structured Resume:
{resume.model_dump_json(indent=2)}

Structured Job Description:
{job_description.model_dump_json(indent=2)}

Return the result using the ExperienceStrengthening schema.
"""

    return model.invoke(prompt)