from resume_generator.tailoring import ResumeTailoringPlan


ALLOWED_SECTIONS = {
    "summary",
    "skills",
    "education",
    "projects",
    "experience",
    "certifications",
}


def apply_resume_customization(
    tailoring_plan: ResumeTailoringPlan,
    section_order: list[str] | None = None,
    removed_sections: list[str] | None = None,
    removed_projects: list[str] | None = None,
) -> ResumeTailoringPlan:
    """
    Apply explicit user customization to an existing
    resume tailoring plan.

    This function does not generate new content.
    """

    if section_order is not None:

        invalid_sections = [
            section
            for section in section_order
            if section not in ALLOWED_SECTIONS
        ]

        if invalid_sections:
            raise ValueError(
                "Invalid resume sections: "
                + ", ".join(invalid_sections)
            )

        if len(section_order) != len(
            set(section_order)
        ):
            raise ValueError(
                "section_order contains duplicate sections."
            )

        tailoring_plan.section_config.section_order = (
            section_order
        )

    if removed_sections is not None:

        invalid_sections = [
            section
            for section in removed_sections
            if section not in ALLOWED_SECTIONS
        ]

        if invalid_sections:
            raise ValueError(
                "Invalid sections for removal: "
                + ", ".join(invalid_sections)
            )

        tailoring_plan.section_config.removed_sections = (
            removed_sections
        )

        tailoring_plan.section_config.section_order = [
            section
            for section
            in tailoring_plan.section_config.section_order
            if section not in removed_sections
        ]

    if removed_projects is not None:

        tailoring_plan.section_config.removed_projects = (
            removed_projects
        )

    return tailoring_plan

