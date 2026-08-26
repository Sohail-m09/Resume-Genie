from schemas.cover_letter import CoverLetterEvidence
from schemas.job_description import JobDescription


def build_cover_letter_prompt(
    evidence: CoverLetterEvidence,
    job_description: JobDescription,
) -> str:
    """
    Build a grounded prompt for cover-letter generation.

    The prompt restricts Gemini to evidence selected
    from the candidate's actual resume.
    """

    prompt = f"""
You are a professional cover-letter writer.

Generate a job-specific cover letter using ONLY the
provided candidate evidence and job description.

Candidate Evidence:
{evidence.model_dump_json(indent=2)}

Job Description:
{job_description.model_dump_json(indent=2)}

Rules:
1. Do not invent skills, experience, projects, achievements,
   certifications, employers, responsibilities, or metrics.
2. Use only facts explicitly present in the candidate evidence.
3. Do not claim that the candidate has a missing skill.
4. Do not exaggerate the candidate's qualifications.
5. Do not mention information that is absent from the evidence.
6. Connect the candidate's actual projects and skills to the
   requirements of the target job.
7. Keep the tone professional and natural.
8. Do not make unsupported claims about years of experience.
9. If professional experience is unavailable, do not fabricate it.
10. The motivation section must remain general unless personal
    motivation is explicitly provided.
11. Return the result using the CoverLetter schema.
12. Keep the cover letter concise and suitable for a typical
    one-page job application.
13. Prefer 3-5 concise paragraphs.
14. Do not mention every project if fewer projects provide
    stronger evidence for the target role.
15. Prioritize the most relevant evidence instead of listing
    all available technologies and metrics.

The cover letter should contain:
- A professional opening
- Relevant experience, only when evidence exists
- Relevant projects
- A grounded motivation for the role
- A professional closing
"""

    return prompt.strip()