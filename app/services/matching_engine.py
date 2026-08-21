from schemas.resume import Resume
from schemas.job_description import JobDescription
from embeddings.similarity import semantic_similarity
from config import SEMANTIC_SKILL_THRESHOLD
import re


def normalize_skill(skill: str) -> str:
    """
    Normalize a skill for comparison.

    Args:
        skill: Skill name.

    Returns:
        Normalized skill.
    """
    return skill.strip().lower()


def match_skills(
    resume: Resume,
    job_description: JobDescription,
) -> dict:
    """
    Match resume skills against required and preferred job skills.

    Args:
        resume: Structured Resume object.
        job_description: Structured JobDescription object.

    Returns:
        A dictionary containing matched and missing
        required and preferred skills.
    """

    resume_skills = {
        normalize_skill(skill)
        for skill in resume.skills
    }

    required_skills = {
        normalize_skill(skill)
        for skill in job_description.required_skills
    }

    preferred_skills = {
        normalize_skill(skill)
        for skill in job_description.preferred_skills
    }

    matched_required = sorted(
        resume_skills.intersection(required_skills)
    )

    missing_required = sorted(
        required_skills.difference(resume_skills)
    )

    matched_preferred = sorted(
        resume_skills.intersection(preferred_skills)
    )

    missing_preferred = sorted(
        preferred_skills.difference(resume_skills)
    )

    return {
        "required": {
            "matched": matched_required,
            "missing": missing_required,
        },
        "preferred": {
            "matched": matched_preferred,
            "missing": missing_preferred,
        },
    }

def calculate_skill_coverage(
    matched_skills: list[str],
    total_skills: list[str],
) -> float | None:
    """
    Calculate the percentage of skills that were matched.

    Args:
        matched_skills: Skills matched by the candidate.
        total_skills: Total skills being evaluated.

    Returns:
        Coverage percentage, or None when there are no skills to evaluate.
    """

    if not total_skills:
        return None

    return round(
        (len(matched_skills) / len(total_skills)) * 100,
        2,
    )

def extract_required_years(experience_required: str | None) -> float | None:
    """
    Extract the minimum required years from common JD experience text.
    """

    if not experience_required:
        return None

    text = experience_required.lower().strip()

    range_match = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:-|to)\s*(\d+(?:\.\d+)?)\s*years?",
        text,
    )

    if range_match:
        return float(range_match.group(1))

    plus_match = re.search(
        r"(\d+(?:\.\d+)?)\s*\+?\s*years?",
        text,
    )

    if plus_match:
        return float(plus_match.group(1))

    return None

def match_experience(
    resume: Resume,
    job_description: JobDescription,
) -> dict:
    """
    Perform a conservative experience comparison.

    Returns:
        Experience matching result.
    """

    required_years = extract_required_years(
        job_description.experience_required
    )

    if required_years is None:
        return {
            "status": "unknown",
            "required_experience": job_description.experience_required,
            "required_years": None,
            "candidate_evidence": [],
        }

    if not resume.experience:
        return {
            "status": "unknown",
            "required_experience": job_description.experience_required,
            "required_years": required_years,
            "candidate_evidence": [],
        }

    evidence = []

    for experience in resume.experience:
        evidence.append(
            {
                "role": experience.role,
                "company": experience.company,
                "start_date": experience.start_date,
                "end_date": experience.end_date,
            }
        )

    return {
        "status": "unknown",
        "required_experience": job_description.experience_required,
        "required_years": required_years,
        "candidate_evidence": evidence,
    }


def normalize_education(text: str | None) -> str:
    """
    Normalize education text for basic comparison.

    Args:
        text: Education requirement/text.

    Returns:
        Normalized education text.
    """
    if not text:
        return ""

    return " ".join(text.lower().split())


def match_education(
    resume: Resume,
    job_description: JobDescription,
) -> dict:
    """
    Perform a conservative education comparison.

    Returns:
        Education matching result.
    """

    required = normalize_education(
        job_description.education_required
    )

    if not required:
        return {
            "status": "not_required",
            "requirement": None,
            "candidate_education": [],
        }

    if not resume.education:
        return {
            "status": "unknown",
            "requirement": required,
            "candidate_education": [],
        }

    for education in resume.education:
        degree = normalize_education(education.degree)
        field = normalize_education(education.field_of_study)

        candidate_text = f"{degree} {field}".strip()

        # Strong exact/near-exact evidence
        if (
            candidate_text == required
            or degree == required
            or field == required
        ):
            return {
                "status": "exact_match",
                "requirement": required,
                "candidate_education": [
                    {
                        "degree": education.degree,
                        "field_of_study": education.field_of_study,
                        "institution": education.institution,
                        "grade": education.grade,
                    }
                ],
            }

    # We do not have enough deterministic evidence
    # to claim a related-field match.
    return {
        "status": "unknown",
        "requirement": required,
        "candidate_education": [
            {
                "degree": education.degree,
                "field_of_study": education.field_of_study,
                "institution": education.institution,
                "grade": education.grade,
            }
            for education in resume.education
        ],
    }

def find_project_evidence(
        resume : Resume,
        skill : str,
) -> list[dict]:
    normalized_skill = normalize_skill(skill)
    evidence = []

    for project in resume.projects:
        project_technologies = {
            normalize_skill(technology)
            for technology in project.technologies
        }

        if normalized_skill in project_technologies:
            evidence.append(
                {
                    "project_name" : project.name,
                    "description" : project.description, 
                }
            )
    return evidence

def match_project_relevance(
        resume : Resume,
        job_description : JobDescription, 
) -> dict:

    required_project_evidance = {}
    preferred_project_evidance = {}

    for skill in job_description.required_skills:
        evidence = find_project_evidence(resume, skill)

        if evidence:
            required_project_evidance[
                normalize_skill(skill)
            ] = evidence

    for skill in job_description.preferred_skills:
        evidence = find_project_evidence(resume, skill)

        if evidence:
            preferred_project_evidance[
                normalize_skill(skill)
            ] = evidence

    return {
        "required" : required_project_evidance,
        "preferred" : preferred_project_evidance
    }

def status_to_score(status: str) -> float | None:     
    if status in {"meets", "exact_match"}:
        return 100.0

    if status in {"does_not_meet", "does_not_match"}:
        return 0.0

    return None


def calculate_match_score(
    skill_result: dict,
    experience_result: dict,
    education_result: dict,
) -> dict:
    required_matched = skill_result["required"]["matched"]
    required_missing = skill_result["required"]["missing"]

    preferred_matched = skill_result["preferred"]["matched"]
    preferred_missing = skill_result["preferred"]["missing"]

    required_total = len(required_matched) + len(required_missing)
    preferred_total = len(preferred_matched) + len(preferred_missing)

    required_coverage = (
        (len(required_matched) / required_total) * 100
        if required_total
        else None
    )

    preferred_coverage = (
        (len(preferred_matched) / preferred_total) * 100
        if preferred_total
        else None
    )

    components = []

    if required_coverage is not None:
        components.append(
            ("required_skills", required_coverage, 50.0)
        )

    if preferred_coverage is not None:
        components.append(
            ("preferred_skills", preferred_coverage, 15.0)
        )

    experience_score = status_to_score(
        experience_result["status"]
    )

    if experience_score is not None:
        components.append(
            ("experience", experience_score, 20.0)
        )

    education_score = status_to_score(
        education_result["status"]
    )

    if education_score is not None:
        components.append(
            ("education", education_score, 15.0)
        )

    if not components:
        return {
            "overall_score": None,
            "components": {},
        }

    total_weight = sum(
        weight for _, _, weight in components
    )

    weighted_score = sum(
        score * weight
        for _, score, weight in components
    )

    overall_score = round(
        weighted_score / total_weight,
        2,
    )

    component_results = {
        name: {
            "score": round(score, 2),
            "weight": weight,
        }
        for name, score, weight in components
    }

    return {
        "overall_score": overall_score,
        "components": component_results,
    }

def build_match_analysis(
    skill_result: dict,
    experience_result: dict,
    education_result: dict,
    project_result: dict,
) -> dict:
    """
    Build an explainable Resume-JD analysis.
    """

    score_result = calculate_match_score(
        skill_result=skill_result,
        experience_result=experience_result,
        education_result=education_result,
    )

    return {
        "overall_score": score_result["overall_score"],
        "score_breakdown": score_result["components"],
        "skills": skill_result,
        "experience": experience_result,
        "education": education_result,
        "project_evidence": project_result,
    }

def semantic_skill_match(
    resume_skill: str,
    job_skill: str,
) -> dict:
    """
    Compare a resume skill and job skill semantically.

    Args:
        resume_skill: Skill from the resume.
        job_skill: Requirement from the JD.

    Returns:
        Explainable semantic comparison result.
    """

    score = semantic_similarity(
        resume_skill,
        job_skill,
    )

    return {
        "resume_skill": resume_skill,
        "job_requirement": job_skill,
        "similarity": round(score, 4),
    }

def semantic_education_match(
    resume: Resume,
    job_description: JobDescription,
) -> dict:
    """
    Compare job education requirements with candidate education
    using semantic similarity.

    Args:
        resume: Structured Resume object.
        job_description: Structured JobDescription object.

    Returns:
        Semantic education evidence.
    """

    requirement = job_description.education_required

    if not requirement:
        return {
            "status": "not_required",
            "requirement": None,
            "candidates": [],
        }

    if not resume.education:
        return {
            "status": "unknown",
            "requirement": requirement,
            "candidates": [],
        }

    candidates = []

    for education in resume.education:
        candidate_text = " ".join(
            value
            for value in [
                education.degree,
                education.field_of_study,
            ]
            if value
        )

        score = semantic_similarity(
            requirement,
            candidate_text,
        )

        candidates.append(
            {
                "degree": education.degree,
                "field_of_study": education.field_of_study,
                "similarity": round(score, 4),
            }
        )

    candidates.sort(
        key=lambda item: item["similarity"],
        reverse=True,
    )

    return {
        "status": "semantic_evidence",
        "requirement": requirement,
        "candidates": candidates,
    }

def semantic_project_match(
    project_description: str | None,
    job_requirement: str,
) -> dict:
    """
    Compare a project description with a job requirement
    using semantic similarity.

    Args:
        project_description: Description of the candidate project.
        job_requirement: Requirement from the JD.

    Returns:
        Semantic project evidence.
    """

    if not project_description:
        return {
            "project_description": None,
            "job_requirement": job_requirement,
            "similarity": None,
        }

    score = semantic_similarity(
        project_description,
        job_requirement,
    )

    return {
        "project_description": project_description,
        "job_requirement": job_requirement,
        "similarity": round(score, 4),
    }

def find_semantic_project_evidence(
    resume: Resume,
    job_description: JobDescription,
) -> dict:
    """
    Find semantic evidence between project descriptions
    and job requirements.
    """

    required_evidence = []
    preferred_evidence = []

    for project in resume.projects:

        for requirement in job_description.required_skills:

            result = semantic_project_match(
                project.description,
                requirement,
            )

            if result["similarity"] is not None:
                required_evidence.append(
                    {
                        "project_name": project.name,
                        "job_requirement": requirement,
                        "similarity": result["similarity"],
                    }
                )

        for requirement in job_description.preferred_skills:

            result = semantic_project_match(
                project.description,
                requirement,
            )

            if result["similarity"] is not None:
                preferred_evidence.append(
                    {
                        "project_name": project.name,
                        "job_requirement": requirement,
                        "similarity": result["similarity"],
                    }
                )

    return {
        "required": required_evidence,
        "preferred": preferred_evidence,
    }

def find_semantic_skill_candidates(
    resume: Resume,
    job_description: JobDescription,
) -> dict:
    """
    Find semantic candidates for JD skills that were not
    matched exactly.

    Returns semantic similarity evidence without making
    a final match/no-match decision.
    """

    resume_skills = resume.skills

    required_candidates = []
    preferred_candidates = []

    # Required skills
    for job_skill in job_description.required_skills:

        exact_match = any(
            normalize_skill(job_skill) == normalize_skill(resume_skill)
            for resume_skill in resume_skills
        )

        if exact_match:
            continue

        for resume_skill in resume_skills:
            result = semantic_skill_match(
                resume_skill,
                job_skill,
            )

            required_candidates.append(result)

    # Preferred skills
    for job_skill in job_description.preferred_skills:

        exact_match = any(
            normalize_skill(job_skill) == normalize_skill(resume_skill)
            for resume_skill in resume_skills
        )

        if exact_match:
            continue

        for resume_skill in resume_skills:
            result = semantic_skill_match(
                resume_skill,
                job_skill,
            )

            preferred_candidates.append(result)

    return {
        "required": required_candidates,
        "preferred": preferred_candidates,
    }

def classify_semantic_skill_match(
    similarity: float,
) -> str:
    """
    Classify semantic similarity for experimentation.

    Returns:
        'potential_match' when similarity meets the configured
        threshold, otherwise 'weak_match'.
    """

    if similarity >= SEMANTIC_SKILL_THRESHOLD:
        return "potential_match"

    return "weak_match"

def classify_semantic_skill_candidates(
    semantic_candidates: dict,
) -> dict:
    """
    Add experimental classifications to semantic candidates.
    """

    classified = {
        "required": [],
        "preferred": [],
    }

    for category in ["required", "preferred"]:

        for candidate in semantic_candidates[category]:

            classification = classify_semantic_skill_match(
                candidate["similarity"]
            )

            classified[category].append(
                {
                    **candidate,
                    "classification": classification,
                }
            )

    return classified

def select_best_semantic_matches(
    semantic_candidates: dict,
) -> dict:
    """
    Select the highest-similarity resume skill for each
    job requirement and keep it only when it meets the
    provisional semantic threshold.

    Args:
        semantic_candidates:
            Output from find_semantic_skill_candidates().

    Returns:
        Best semantic candidates that pass the threshold.
    """

    best_matches = {
        "required": {},
        "preferred": {},
    }

    for category in ["required", "preferred"]:

        for candidate in semantic_candidates[category]:

            requirement = candidate["job_requirement"]
            current_best = best_matches[category].get(requirement)

            if (
                current_best is None
                or candidate["similarity"]
                > current_best["similarity"]
            ):
                best_matches[category][requirement] = candidate

    filtered_matches = {
        "required": {},
        "preferred": {},
    }

    for category in ["required", "preferred"]:

        for requirement, candidate in best_matches[category].items():

            if candidate["similarity"] >= SEMANTIC_SKILL_THRESHOLD:
                filtered_matches[category][requirement] = {
                    **candidate,
                    "classification": "potential_match",
                }

    return filtered_matches