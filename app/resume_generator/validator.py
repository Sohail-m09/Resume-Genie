from schemas.resume import Resume
from resume_generator.tailoring import TailoredResume


def validate_tailored_resume(
    original_resume: Resume,
    tailored_resume: TailoredResume,
) -> dict:
    """
    Validate that the tailored resume does not introduce
    unsupported projects, experience, metrics, or other
    factual content.

    This is a deterministic validation layer.
    """

    original_project_names = {
        project.name.lower()
        for project in original_resume.projects
    }

    tailored_project_names = {
        project.name.lower()
        for project in tailored_resume.projects
    }

    unsupported_projects = sorted(
        tailored_project_names - original_project_names
    )

    original_experience = bool(
        original_resume.experience
    )

    tailored_experience = bool(
        tailored_resume.experience
    )

    experience_violation = (
        not original_experience
        and tailored_experience
    )

    original_certifications = {
        str(certification).lower()
        for certification in original_resume.certifications
    }

    tailored_certifications = {
        str(certification).lower()
        for certification in tailored_resume.certifications
    }

    unsupported_certifications = sorted(
        tailored_certifications - original_certifications
    )

    return {
        "valid": (
            not unsupported_projects
            and not experience_violation
            and not unsupported_certifications
        ),
        "unsupported_projects": unsupported_projects,
        "experience_violation": experience_violation,
        "unsupported_certifications": (
            unsupported_certifications
        ),
    }