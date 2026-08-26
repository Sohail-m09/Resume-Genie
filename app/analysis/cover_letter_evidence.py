from schemas.resume import Resume
from schemas.job_description import JobDescription
from schemas.cover_letter import CoverLetterEvidence


def select_cover_letter_evidence(
    resume: Resume,
    job_description: JobDescription,
) -> CoverLetterEvidence:
    """
    Select resume evidence relevant to the target job.

    This layer only selects existing evidence.
    It does not invent or rewrite resume information.
    """

    relevant_skills = [
        skill
        for skill in resume.skills
        if skill.lower() in {
            jd_skill.lower()
            for jd_skill in (
                job_description.required_skills
                + job_description.preferred_skills
            )
        }
    ]

    relevant_projects = []

    job_skill_text = " ".join(
        job_description.required_skills
        + job_description.preferred_skills
    ).lower()

    for project in resume.projects:
        project_text = (
            f"{project.name} "
            f"{project.description} "
            f"{' '.join(project.technologies)}"
        ).lower()

        if any(
            skill.lower() in project_text
            for skill in job_description.required_skills
            + job_description.preferred_skills
        ):
            relevant_projects.append(project.name)

    relevant_experience = []

    for experience in resume.experience:
        relevant_experience.append(
            str(experience)
        )

    supporting_evidence = []

    for project in resume.projects:
        if project.name in relevant_projects:
            supporting_evidence.append(
                f"{project.name}: {project.description}"
            )

    return CoverLetterEvidence(
        relevant_skills=relevant_skills,
        relevant_projects=relevant_projects,
        relevant_experience=relevant_experience,
        supporting_evidence=supporting_evidence,
    )