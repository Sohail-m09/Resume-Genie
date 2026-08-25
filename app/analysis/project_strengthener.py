from schemas.resume import Resume
from schemas.job_description import JobDescription
from schemas.resume_analysis import ProjectStrengthening
from llm.gemini import get_gemini_model


def strengthen_projects(
    resume: Resume,
    job_description: JobDescription,
) -> ProjectStrengthening:
    """
    Analyze existing resume projects against the target JD
    and provide evidence-based improvement suggestions.
    """

    model = get_gemini_model().with_structured_output(
        ProjectStrengthening
    )

    prompt = f"""
You are a professional resume optimization assistant.

Analyze the candidate's existing projects against the target
job description.

Your task is to identify how the EXISTING projects can be
presented more effectively for this job.

Rules:
1. Use ONLY information present in the resume and job description.
2. Do not invent technologies, responsibilities, metrics,
   deployment methods, or project achievements.
3. Do not create new projects.
4. Do not claim that a project used a technology unless the
   resume explicitly supports it.
5. Identify genuine strengths in each relevant project.
6. Identify weaknesses in how the existing project is presented.
7. Give actionable recommendations for improving the project
   description.
8. Recommendations should focus on clarity, technical depth,
   measurable impact, and relevance to the job.
9. If a project is not relevant to the job, explain that rather
   than forcing a connection.

Structured Resume:
{resume.model_dump_json(indent=2)}

Structured Job Description:
{job_description.model_dump_json(indent=2)}

Return the result using the ProjectStrengthening schema.
"""

    return model.invoke(prompt)