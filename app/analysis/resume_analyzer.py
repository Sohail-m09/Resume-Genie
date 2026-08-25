from llm.gemini import get_gemini_model
from schemas.resume import Resume
from schemas.resume_analysis import ResumeAnalysis


def analyze_resume(resume: Resume) -> ResumeAnalysis:
    """
    Analyze a structured resume and generate
    actionable improvement suggestions.
    """

    model = get_gemini_model().with_structured_output(
        ResumeAnalysis
    )

    prompt = f"""
You are a professional resume analysis assistant.

Analyze the following structured resume.

Your task is to identify genuine weaknesses or areas
that could be improved.

Rules:
1. Use ONLY the information present in the provided resume.
2. Do not invent experience, skills, projects, or achievements.
3. Do not assume information that is not explicitly present.
4. Give actionable and specific suggestions.
5. Focus on improving clarity, impact, technical presentation,
   and evidence of achievements.
6. Do not rewrite the entire resume.
7. If a section is already strong, do not invent a problem.

Structured Resume:
{resume.model_dump_json(indent=2)}
"""

    return model.invoke(prompt)