from schemas.resume import Resume
from schemas.job_description import JobDescription


def find_keyword_gaps(
    resume: Resume,
    job_description: JobDescription,
) -> dict:
    """
    Identify important JD keywords that are not explicitly
    represented in the resume.

    This function does not add or invent resume skills.
    """

    resume_text = " ".join(
        [
            str(resume.summary or ""),
            " ".join(str(skill) for skill in resume.skills),
            " ".join(
                str(project)
                for project in resume.projects
            ),
            " ".join(
                str(experience)
                for experience in resume.experience
            ),
            " ".join(
                str(certification)
                for certification in resume.certifications
            ),
        ]
    ).lower()

    jd_keywords = (
        list(job_description.required_skills)
        + list(job_description.preferred_skills)
    )

    missing_keywords = []

    for keyword in jd_keywords:
        keyword_lower = keyword.lower()

        if keyword_lower not in resume_text:
            missing_keywords.append(keyword)

    return {
        "missing_keywords": sorted(
            set(missing_keywords),
            key=str.lower,
        )
    }