from schemas.resume import Resume
from resume_generator.tailoring import TailoredResume
import re


def normalize_certification(
    certification: str,
) -> str:
    """
    Normalize certification text for
    format-tolerant comparison.
    """

    return re.sub(
        r"[^a-z0-9]+",
        " ",
        certification.lower(),
    ).strip()


def certification_is_supported(
    tailored_certification: str,
    original_certifications: set[str],
) -> bool:
    """
    Check whether a tailored certification is
    supported by an original certification despite
    harmless formatting differences.
    """

    tailored = normalize_certification(
        tailored_certification
    )

    for original in original_certifications:

        normalized_original = normalize_certification(
            original
        )

        if tailored == normalized_original:
            return True

        if (
            tailored in normalized_original
            or normalized_original in tailored
        ):
            return True

    return False



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
        str(certification)
        for certification in original_resume.certifications 
    }

    tailored_certifications = {
        str(certification).lower()
        for certification in tailored_resume.certifications
    }

    unsupported_certifications = [ 
        certification 
        for certification in tailored_resume.certifications 
        if not certification_is_supported( 
            certification, 
            original_certifications, 
        ) 
    ]
    
    allowed_sections = {
        "summary",
        "skills",
        "education",
        "projects",
        "experience",
        "certifications",
    }

    invalid_sections = [
        section
        for section in tailored_resume.section_order
        if section not in allowed_sections
    ]

    duplicate_sections = (
        len(tailored_resume.section_order)
        != len(set(tailored_resume.section_order))
    )

    return {
        "valid": (
            not unsupported_projects
            and not experience_violation
            and not unsupported_certifications
            and not invalid_sections
            and not duplicate_sections
        ),
        "unsupported_projects": unsupported_projects,
        "experience_violation": experience_violation,
        "invalid_sections": invalid_sections,
        "duplicate_sections": duplicate_sections,
        "unsupported_certifications": (
            unsupported_certifications
        ),
    }