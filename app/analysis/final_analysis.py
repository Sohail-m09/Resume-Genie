from schemas.resume import Resume
from schemas.job_description import JobDescription
from schemas.resume_analysis import FinalResumeAnalysis
from analysis.experience_strengthener import (
    strengthen_experience,
)

from services.matching_engine import (
    match_skills,
    match_experience,
    match_education,
    calculate_match_score,
)

from analysis.semantic_evidence import (
    find_semantic_skill_evidence,
)

from analysis.improvement_recommendations import (
    generate_improvement_recommendations,
)

from analysis.project_strengthener import (
    strengthen_projects,
)


def build_final_analysis(
    resume: Resume,
    job_description: JobDescription,
) -> FinalResumeAnalysis:
    """
    Combine existing deterministic matching, semantic evidence,
    and analysis outputs into one application-level result.

    The existing scoring formula is not modified.
    """

    # --------------------------------------------------
    # 1. Existing deterministic matching
    # --------------------------------------------------

    skill_result = match_skills(
        resume=resume,
        job_description=job_description,
    )

    experience_result = match_experience(
        resume=resume,
        job_description=job_description,
    )

    education_result = match_education(
        resume=resume,
        job_description=job_description,
    )

    # --------------------------------------------------
    # 2. Existing explainable score
    # --------------------------------------------------

    score_result = calculate_match_score(
        skill_result=skill_result,
        experience_result=experience_result,
        education_result=education_result,
    )

    # --------------------------------------------------
    # 3. Existing semantic evidence
    # --------------------------------------------------

    semantic_evidence = find_semantic_skill_evidence(
        resume=resume,
        job_description=job_description,
    )

    # --------------------------------------------------
    # 4. Existing improvement recommendations
    # --------------------------------------------------

    skill_gaps = {
        "missing_required": skill_result["required"]["missing"],
        "missing_preferred": skill_result["preferred"]["missing"],
    }

    recommendations = generate_improvement_recommendations(
        skill_gaps
    )

    # --------------------------------------------------
    # 5. Existing project strengthening
    # --------------------------------------------------

    project_strengthening = strengthen_projects(
        resume=resume,
        job_description=job_description,
    )

    experience_strengthening = strengthen_experience(
        resume=resume,
        job_description=job_description,
    )

    # --------------------------------------------------
    # 6. Final structured result
    # --------------------------------------------------

    return FinalResumeAnalysis(
        overall_score=score_result["overall_score"],
        score_components=score_result["components"],

        matched_required_skills=(
            skill_result["required"]["matched"]
        ),

        missing_required_skills=(
            skill_result["required"]["missing"]
        ),

        matched_preferred_skills=(
            skill_result["preferred"]["matched"]
        ),

        missing_preferred_skills=(
            skill_result["preferred"]["missing"]
        ),

        semantic_evidence=semantic_evidence,

        improvement_recommendations=(
            recommendations.recommendations
        ),

        project_improvements=(
            project_strengthening.improvements
        ),

        experience_improvements=(
            experience_strengthening.improvements
        ),

        experience_note=(
            experience_strengthening.note
        ),
    )