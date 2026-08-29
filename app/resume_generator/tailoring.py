
from pydantic import BaseModel, Field
from schemas.resume import Resume
from schemas.job_description import JobDescription
from llm.gemini import get_gemini_model


class ProjectTailoring(BaseModel):
    project_name: str

    priority: int = Field(
        description="Priority of the project for the target job. 1 is highest."
    )

    reason: str = Field(
        description="Why this project is relevant to the target job."
    )

    changes: list[str] = Field(
        description="Specific changes that should be made using existing evidence."
    )


class ResumeSectionConfig(BaseModel):
    section_order: list[str] = Field(
        description=(
            "Final order of resume sections. "
            "Allowed sections: summary, skills, education, "
            "projects, experience, certifications."
        )
    )

    removed_sections: list[str] = Field(
        description=(
            "Sections intentionally removed from the tailored resume."
        )
    )

    removed_projects: list[str] = Field(
        description=(
            "Existing projects intentionally removed from the tailored resume."
        )
    )


class ResumeTailoringPlan(BaseModel):
    summary_changes: list[str] = Field(
        description="Changes to improve the professional summary using only existing evidence."
    )

    skills_to_prioritize: list[str] = Field(
        description="Existing resume skills that should be prioritized for the target job."
    )

    skills_to_deprioritize: list[str] = Field(
        description="Existing resume skills that are less relevant to the target job."
    )

    project_tailoring: list[ProjectTailoring] = Field(
        description="Project prioritization and evidence-based improvement instructions."
    )

    experience_changes: list[str] = Field(
        description="Changes to existing professional experience, if experience exists."
    )

    unsupported_requirements: list[str] = Field(
        description="JD requirements that are not supported by the current resume and must not be added as claims."
    )

    section_config: ResumeSectionConfig = Field(
        description=(
            "Configuration controlling section ordering and "
            "intentional removal of sections or projects."
        )
    )


class TailoredProject(BaseModel):
    name: str
    technologies: list[str]
    bullets: list[str]


class TailoredEducation(BaseModel):
    degree: str
    institution: str
    year: str | None = None
    details: str | None = None


class TailoredResume(BaseModel):
    summary: str
    skills: list[str]
    projects: list[TailoredProject]
    experience: list[str]
    education: list[TailoredEducation]
    certifications: list[str]

    section_order: list[str] = Field(
        description=(
            "Final ordered list of resume sections."
        )
    )


def generate_tailoring_plan(
    resume: Resume,
    job_description: JobDescription,
    analysis_context: str,
):
    """
    Generate a job-specific tailoring plan using only
    existing resume evidence.
    """

    model = get_gemini_model()

    prompt = f"""
You are a professional resume optimization assistant.

Create a tailoring plan for the candidate's existing resume
based on the target job description and the provided analysis.

The goal is to improve relevance and presentation without
creating false claims.

Candidate Resume:
{resume.model_dump_json(indent=2)}

Job Description:
{job_description.model_dump_json(indent=2)}

Existing Analysis:
{analysis_context}

Rules:
1. Use only information supported by the resume and provided analysis.
2. Do not invent skills, experience, projects, achievements,
   certifications, technologies, metrics, employers, or responsibilities.
3. Do not add a missing JD requirement as if the candidate already has it.
4. Treat explicitly matched skills as supported resume evidence.
5. Treat strong semantic evidence as supporting evidence, not as an exact match.
6. If a JD requirement is marked as missing by exact matching but has
   strong semantic evidence, do NOT automatically classify it as an
   unsupported requirement.
7. Preserve the distinction between:
   - exact match,
   - semantic/potential match,
   - unsupported requirement.
8. Do not claim that semantic evidence is equivalent to direct experience.
9. Prioritize existing skills that are relevant to the target role.
10. Prioritize the most relevant existing projects.
11. Recommend stronger ordering and presentation of existing evidence.
12. Do not fabricate professional experience.
13. Do not add skills merely because they appear in the job description.
14. If a requirement has no exact match and no meaningful semantic evidence,
    it may be included in unsupported_requirements.
15. Existing skills and project evidence should be preserved when supported,
    even if the JD uses different terminology.
16. Do not treat an existing resume skill as unsupported merely because
    the exact JD wording is different.
17. The section_config must specify the final section order.
18. The section_config may remove a section only when it is empty,
    irrelevant, or explicitly requested for removal.
19. The section_config may remove an existing project only when
    explicitly requested or when the project is intentionally excluded
    from the tailored version.
20. Never replace a removed project or section with invented content.
21. Preserve Education when it is supported by the original resume
    unless it is explicitly requested to be removed.
22. Preserve truthful resume content even when its section is reordered.
23. Use only these section names:
    summary, skills, education, projects, experience, certifications.

Return the tailoring plan according to the ResumeTailoringPlan schema.
"""

    structured_model = model.with_structured_output(
        ResumeTailoringPlan
    )

    return structured_model.invoke(prompt)


def generate_tailored_resume(
    resume: Resume,
    job_description: JobDescription,
    tailoring_plan: ResumeTailoringPlan,
) -> TailoredResume:
    """
    Generate a job-tailored structured resume.

    Only existing resume evidence may be used.
    """

    model = get_gemini_model().with_structured_output(
        TailoredResume
    )

    prompt = f"""
You are a professional resume optimization assistant.

Create a tailored version of the candidate's existing resume
for the provided job description.

Use the tailoring plan as the instructions for prioritization
and presentation.

ORIGINAL RESUME:
{resume.model_dump_json(indent=2)}

JOB DESCRIPTION:
{job_description.model_dump_json(indent=2)}

TAILORING PLAN:
{tailoring_plan.model_dump_json(indent=2)}

Rules:
1. Use ONLY facts present in the original resume.
2. Do not invent skills, technologies, experience, employers,
   achievements, certifications, responsibilities, or metrics.
3. Do not add unsupported job requirements to the resume.
4. Do not create new projects.
5. Do not create professional experience when none exists.
6. Reorder and prioritize existing skills according to the
   tailoring plan.
7. Reorder existing projects according to the approved priority.
8. Rewrite project descriptions into concise resume bullet points
   while preserving only existing evidence.
9. Each bullet should communicate a clear action, technical method,
   result, or impact when supported by the original resume.
10. Do not create new metrics or technical claims.
11. Do not remove truthful resume content merely because it is
    not required by the target job unless it is explicitly
    identified as low priority.
12. Keep the resume concise and professional.
13. Preserve the education information from the original resume.
14. Do not invent, rename, or enhance degrees, institutions,
    dates, grades, or academic details.
15. Follow section_config.section_order for the final section order.
16. Follow section_config.removed_sections and
    section_config.removed_projects when producing the tailored resume.
17. Never replace removed content with invented content.
18. Return only the structured TailoredResume object.
"""

    return model.invoke(prompt)

