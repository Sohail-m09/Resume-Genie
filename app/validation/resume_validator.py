from schemas.resume import Resume


def validate_resume_extraction(resume: Resume) -> None:
    """
    Perform basic application-level checks on a structured Resume.

    Args:
        resume: Structured Resume object.

    Raises:
        ValueError: When a critical extraction condition fails.
    """

    if not resume.personal_information:
        raise ValueError("Personal information is missing.")

    if not resume.skills:
        print("Warning: No skills were extracted.")

    if not resume.education:
        print("Warning: No education records were extracted.")

    if not resume.experience:
        print("Info: No professional experience was extracted.")

    if not resume.projects:
        print("Info: No projects were extracted.")