from schemas.resume import Resume
from schemas.job_description import JobDescription
from services.matching_engine import semantic_skill_match


SEMANTIC_THRESHOLD = 0.80


def find_semantic_skill_evidence(
    resume: Resume,
    job_description: JobDescription,
) -> list[dict]:
    """
    Find potential semantic matches for JD skills that are not
    exact matches in the resume.

    Semantic evidence is supporting evidence only.
    It does not overwrite deterministic matching results.
    """

    resume_skills = resume.skills

    evidence = []

    # We only investigate skills that were not exact matches.
    from services.matching_engine import match_skills

    exact_matches = match_skills(
        resume=resume,
        job_description=job_description,
    )

    missing_required = exact_matches["required"]["missing"]
    missing_preferred = exact_matches["preferred"]["missing"]

    missing_skills = [
        (skill, "required")
        for skill in missing_required
    ] + [
        (skill, "preferred")
        for skill in missing_preferred
    ]

    for job_skill, category in missing_skills:

        best_match = None

        for resume_skill in resume_skills:

            result = semantic_skill_match(
                resume_skill=resume_skill,
                job_skill=job_skill,
            )

            if (
                best_match is None
                or result["similarity"] > best_match["similarity"]
            ):
                best_match = result

        if (
            best_match is not None
            and best_match["similarity"] >= SEMANTIC_THRESHOLD
        ):
            evidence.append(
                {
                    "job_requirement": job_skill,
                    "category": category,
                    "resume_skill": best_match["resume_skill"],
                    "similarity": best_match["similarity"],
                }
            )

    return evidence