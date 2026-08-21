from schemas.resume import Resume
from llm.gemini import get_gemini_model


def extract_resume(resume_text: str) -> Resume:
    """
    Extract structured information from resume text.

    Args:
        resume_text: Cleaned full resume text.

    Returns:
        Structured and validated Resume object.
    """

    model = get_gemini_model()

    structured_model = model.with_structured_output(
        Resume,
        method="json_schema",
    )

    prompt = f"""
You are an expert resume information extraction system.

Extract information from the resume text below.

Rules:
- Extract only information explicitly present in the resume.
- Do not invent skills, experience, education, certifications,
  achievements, dates, URLs, or other information.
- If optional information is missing, leave it empty.
- Preserve the meaning of the original resume.
- Separate individual skills when the resume uses separators
  such as '|', commas, bullets, or similar formatting.
- Keep project technologies separate from the project description.

Resume:
{resume_text}
"""

    return structured_model.invoke(prompt)