from schemas.resume import Resume
from resume_generator.tailoring import ResumeTailoringPlan


def prioritize_resume_content(
    resume: Resume,
    tailoring_plan: ResumeTailoringPlan,
) -> dict:
    """
    Create a verified priority order for existing resume content.

    No new content is generated.
    Only existing skills and projects are reordered/prioritized.
    """

    # --------------------------------------------------
    # 1. Verify prioritized skills against the resume
    # --------------------------------------------------

    existing_skills = {
        skill.lower(): skill
        for skill in resume.skills
    }

    prioritized_skills = []

    for skill in tailoring_plan.skills_to_prioritize:

        original_skill = existing_skills.get(
            skill.lower()
        )

        if original_skill:
            prioritized_skills.append(
                original_skill
            )

    # --------------------------------------------------
    # 2. Verify deprioritized skills against the resume
    # --------------------------------------------------

    deprioritized_skills = []

    for skill in tailoring_plan.skills_to_deprioritize:

        original_skill = existing_skills.get(
            skill.lower()
        )

        if original_skill:
            deprioritized_skills.append(
                original_skill
            )

    # --------------------------------------------------
    # 3. Prioritize existing projects
    # --------------------------------------------------

    existing_projects = {
        project.name.lower(): project
        for project in resume.projects
    }

    ranked_projects = []

    for project_plan in tailoring_plan.project_tailoring:

        project = existing_projects.get(
            project_plan.project_name.lower()
        )

        if project:
            ranked_projects.append(
                {
                    "project": project,
                    "priority": project_plan.priority,
                    "reason": project_plan.reason,
                }
            )

    ranked_projects.sort(
        key=lambda item: item["priority"]
    )

    # --------------------------------------------------
    # 4. Keep unranked existing projects
    # --------------------------------------------------

    ranked_project_names = {
        item["project"].name.lower()
        for item in ranked_projects
    }

    for project in resume.projects:

        if project.name.lower() not in ranked_project_names:

            ranked_projects.append(
                {
                    "project": project,
                    "priority": None,
                    "reason": (
                        "Existing project without an explicit "
                        "priority in the tailoring plan."
                    ),
                }
            )

    # --------------------------------------------------
    # 5. Return verified prioritization
    # --------------------------------------------------

    return {
        "prioritized_skills": prioritized_skills,
        "deprioritized_skills": deprioritized_skills,
        "prioritized_projects": ranked_projects,
        "unsupported_requirements": (
            tailoring_plan.unsupported_requirements
        ),
    }