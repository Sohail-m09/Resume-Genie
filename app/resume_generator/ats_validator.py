from schemas.resume import Resume
from schemas.job_description import JobDescription
from resume_generator.tailoring import TailoredResume

from services.matching_engine import match_education
from embeddings.model import get_embedding_model

import numpy as np


SEMANTIC_THRESHOLD = 0.80


def normalize_text(text: str) -> str:
    """
    Normalize text for exact keyword comparison.
    """

    return (
        text.lower()
        .replace("-", " ")
        .replace("/", " ")
        .strip()
    )


def build_resume_text(
    resume: TailoredResume,
) -> str:
    """
    Build searchable text from the tailored resume.
    """

    parts = [
        resume.summary,
        " ".join(resume.skills),
    ]

    for education in resume.education:
        parts.extend(
            [
                education.degree,
                education.institution,
                education.year or "",
                education.details or "",
            ]
        )

    for project in resume.projects:
        parts.extend(
            [
                project.name,
                " ".join(project.technologies),
                " ".join(project.bullets),
            ]
        )

    parts.extend(resume.experience)
    parts.extend(resume.certifications)

    return " ".join(parts)


def calculate_exact_matches(
    resume_text: str,
    keywords: list[str],
) -> list[str]:
    """
    Return keywords explicitly present in the tailored resume.
    """

    normalized_resume = normalize_text(
        resume_text
    )

    matched = []

    for keyword in keywords:

        normalized_keyword = normalize_text(
            keyword
        )

        if normalized_keyword in normalized_resume:
            matched.append(keyword)

    return matched


def build_semantic_candidates(
    resume: TailoredResume,
) -> list[dict]:
    """
    Build evidence-aware semantic candidates.

    Each candidate retains its source type so that
    generic skills are not treated as strong evidence
    for specific job requirements.
    """

    candidates = []

    for skill in resume.skills:

        candidates.append(
            {
                "text": skill,
                "type": "skill",
            }
        )

    for project in resume.projects:

        candidates.append(
            {
                "text": project.name,
                "type": "project_name",
            }
        )

        for technology in project.technologies:

            candidates.append(
                {
                    "text": technology,
                    "type": "technology",
                }
            )

        for bullet in project.bullets:

            candidates.append(
                {
                    "text": bullet,
                    "type": "project_bullet",
                }
            )

    return [
        candidate
        for candidate in candidates
        if candidate["text"]
    ]


def is_specific_evidence(
    job_requirement: str,
    candidate: dict,
) -> bool:
    """
    Prevent overly generic evidence from being used
    as a semantic match for specific requirements.
    """

    requirement = normalize_text(
        job_requirement
    )

    candidate_text = normalize_text(
        candidate["text"]
    )

    generic_terms = {
        "machine learning",
        "data analysis",
        "python",
        "sql",
        "statistics",
        "programming",
    }

    # Generic standalone skills should not prove
    # highly specific requirements.
    if (
        candidate_text in generic_terms
        and requirement not in generic_terms
    ):
        return False

    specific_requirement_terms = [
        "automated machine learning",
        "automl",
        "model deployment",
        "deploying machine learning",
        "interactive web application",
        "web application deployment",
        "data versioning",
        "mlops",
        "hyperparameter tuning",
    ]

    if any(
        term in requirement
        for term in specific_requirement_terms
    ):
        return candidate["type"] in {
            "technology",
            "project_bullet",
        }

    return True


def calculate_semantic_matches(
    resume: TailoredResume,
    keywords: list[str],
) -> list[dict]:
    """
    Find meaningful semantic matches between JD requirements
    and specific resume evidence.

    Semantic matches are supporting evidence and are not
    treated as exact keyword matches.
    """

    if not keywords:
        return []

    candidates = build_semantic_candidates(
        resume
    )

    if not candidates:
        return []

    model = get_embedding_model()

    candidate_texts = [
        candidate["text"]
        for candidate in candidates
    ]

    candidate_embeddings = model.encode(
        candidate_texts,
        normalize_embeddings=True,
    )

    results = []

    for keyword in keywords:

        keyword_embedding = model.encode(
            [keyword],
            normalize_embeddings=True,
        )[0]

        similarities = np.dot(
            candidate_embeddings,
            keyword_embedding,
        )

        ranked_indices = np.argsort(
            similarities
        )[::-1]

        selected_candidate = None
        selected_score = None

        for index in ranked_indices:

            candidate = candidates[
                int(index)
            ]

            score = float(
                similarities[int(index)]
            )

            if score < SEMANTIC_THRESHOLD:
                break

            if is_specific_evidence(
                job_requirement=keyword,
                candidate=candidate,
            ):
                selected_candidate = candidate
                selected_score = score
                break

        if (
            selected_candidate is not None
            and normalize_text(
                selected_candidate["text"]
            )
            != normalize_text(keyword)
        ):
            results.append(
                {
                    "job_requirement": keyword,
                    "resume_evidence": selected_candidate[
                        "text"
                    ],
                    "evidence_type": selected_candidate[
                        "type"
                    ],
                    "similarity": round(
                        selected_score,
                        4,
                    ),
                }
            )

    return results


def calculate_effective_coverage(
    keywords: list[str],
    exact_matches: list[str],
    semantic_matches: list[dict],
) -> float:
    """
    Calculate effective ATS coverage.

    Exact match = full credit.
    Meaningful semantic match = partial credit.
    """

    if not keywords:
        return 100.0

    exact_set = {
        normalize_text(keyword)
        for keyword in exact_matches
    }

    semantic_set = {
        normalize_text(
            item["job_requirement"]
        )
        for item in semantic_matches
    }

    score = 0.0

    for keyword in keywords:

        normalized_keyword = normalize_text(
            keyword
        )

        if normalized_keyword in exact_set:
            score += 1.0

        elif normalized_keyword in semantic_set:
            score += 0.75

    return round(
        (score / len(keywords)) * 100,
        2,
    )

def calculate_job_title_alignment(
    resume: TailoredResume,
    job_description: JobDescription,
) -> float:
    """
    Calculate explainable job-title alignment using
    role-family phrases rather than individual-word overlap.
    """

    if not job_description.job_title:
        return 100.0

    job_title = normalize_text(
        job_description.job_title
    )

    summary = normalize_text(
        resume.summary
    )

    # --------------------------------------------------
    # 1. Exact full-title match
    # --------------------------------------------------

    if job_title in summary:
        return 100.0

    # --------------------------------------------------
    # 2. Strong role-family phrases
    # --------------------------------------------------

    role_phrases = [
        "data scientist",
        "machine learning analyst",
        "machine learning engineer",
        "data analyst",
    ]

    matched_role_phrases = [
        phrase
        for phrase in role_phrases
        if phrase in summary
        and phrase in job_title
    ]

    if matched_role_phrases:
        return 100.0

    # --------------------------------------------------
    # 3. Related role-family alignment
    # --------------------------------------------------

    role_families = {
        "data_science": [
            "data scientist",
            "data science",
        ],
        "machine_learning": [
            "machine learning",
            "ml engineer",
            "ml analyst",
        ],
        "data_analysis": [
            "data analyst",
            "data analysis",
        ],
    }

    matched_families = []

    for family, phrases in role_families.items():

        job_has_family = any(
            phrase in job_title
            for phrase in phrases
        )

        resume_has_family = any(
            phrase in summary
            for phrase in phrases
        )

        if (
            job_has_family
            and resume_has_family
        ):
            matched_families.append(
                family
            )

    if len(matched_families) >= 2:
        return 100.0

    if len(matched_families) == 1:
        return 75.0

    # --------------------------------------------------
    # 4. No meaningful role-family alignment
    # --------------------------------------------------

    return 0.0



def calculate_education_alignment(
    original_resume: Resume,
    job_description: JobDescription,
) -> dict:
    """
    Reuse the existing education matching logic.
    """

    if not job_description.education_required:
        return {
            "status": "not_required",
            "score": 100.0,
        }

    result = match_education(
        resume=original_resume,
        job_description=job_description,
    )

    status = result.get(
        "status",
        "unknown",
    )

    score_map = {
        "matched": 100.0,
        "potential": 75.0,
        "unknown": 50.0,
        "not_required": 100.0,
        "not_matched": 0.0,
    }

    score = score_map.get(
        status,
        50.0,
    )

    # Additional deterministic evidence check for
    # common degree-family requirements.
    education_text = " ".join(
        [
            " ".join(
                [
                    education.degree or "",
                    education.field_of_study or "",
                    education.grade or "",
                ]
            )
            for education
            in original_resume.education
        ]
    )

    normalized_education = normalize_text(
        education_text
    )

    engineering_evidence = (
        "engineering" in normalized_education
        or "computer engineering"
        in normalized_education
    )

    if (
        status == "unknown"
        and engineering_evidence
    ):
        score = 100.0
        status = "potential"

    return {
        "status": status,
        "score": score,
    }




def calculate_section_completeness(
    resume: TailoredResume,
) -> float:
    """
    Measure the presence of useful resume sections.
    """

    expected_sections = {
        "summary": bool(
            resume.summary
        ),
        "skills": bool(
            resume.skills
        ),
        "projects": bool(
            resume.projects
        ),
        "education": bool(
            resume.education
        ),
    }

    completed_sections = sum(
        expected_sections.values()
    )

    return round(
        (
            completed_sections
            / len(expected_sections)
        ) * 100,
        2,
    )


def calculate_unsupported_claim_score(
    original_resume: Resume,
    tailored_resume: TailoredResume,
) -> dict:
    """
    Check for unsupported projects and fabricated experience.
    """

    original_projects = {
        (project.name or "").lower()
        for project in original_resume.projects
    }

    tailored_projects = {
        project.name.lower()
        for project in tailored_resume.projects
    }

    unsupported_projects = (
        tailored_projects
        - original_projects
    )

    experience_violation = (
        not original_resume.experience
        and bool(tailored_resume.experience)
    )

    score = (
        0.0
        if (
            unsupported_projects
            or experience_violation
        )
        else 100.0
    )

    return {
        "score": score,
        "unsupported_projects": sorted(
            unsupported_projects
        ),
        "experience_violation": (
            experience_violation
        ),
    }


def calculate_ats_score(
    original_resume: Resume,
    tailored_resume: TailoredResume,
    job_description: JobDescription,
) -> dict:
    """
    Calculate an explainable ATS-oriented optimization score.

    This is a project-specific heuristic score and should not
    be interpreted as the score of any particular ATS vendor.
    """

    resume_text = build_resume_text(
        tailored_resume
    )

    # --------------------------------------------------
    # Required keywords
    # --------------------------------------------------

    required_exact = calculate_exact_matches(
        resume_text=resume_text,
        keywords=job_description.required_skills,
    )

    required_semantic = calculate_semantic_matches(
        resume=tailored_resume,
        keywords=job_description.required_skills,
    )

    required_coverage = calculate_effective_coverage(
        keywords=job_description.required_skills,
        exact_matches=required_exact,
        semantic_matches=required_semantic,
    )

    # --------------------------------------------------
    # Preferred keywords
    # --------------------------------------------------

    preferred_exact = calculate_exact_matches(
        resume_text=resume_text,
        keywords=job_description.preferred_skills,
    )

    preferred_semantic = calculate_semantic_matches(
        resume=tailored_resume,
        keywords=job_description.preferred_skills,
    )

    preferred_coverage = calculate_effective_coverage(
        keywords=job_description.preferred_skills,
        exact_matches=preferred_exact,
        semantic_matches=preferred_semantic,
    )

    # --------------------------------------------------
    # Job title
    # --------------------------------------------------

    title_score = calculate_job_title_alignment(
        resume=tailored_resume,
        job_description=job_description,
    )

    # --------------------------------------------------
    # Education
    # --------------------------------------------------

    education_result = calculate_education_alignment(
        original_resume=original_resume,
        job_description=job_description,
    )

    # --------------------------------------------------
    # Section completeness
    # --------------------------------------------------

    section_score = calculate_section_completeness(
        resume=tailored_resume
    )

    # --------------------------------------------------
    # Unsupported claims
    # --------------------------------------------------

    claim_result = calculate_unsupported_claim_score(
        original_resume=original_resume,
        tailored_resume=tailored_resume,
    )

    # --------------------------------------------------
    # Final weighted score
    # --------------------------------------------------

    components = {
        "required_keyword_coverage": {
            "score": required_coverage,
            "weight": 40.0,
        },

        "preferred_keyword_coverage": {
            "score": preferred_coverage,
            "weight": 15.0,
        },

        "job_title_alignment": {
            "score": title_score,
            "weight": 10.0,
        },

        "education_alignment": {
            "score": education_result["score"],
            "weight": 10.0,
        },

        "section_completeness": {
            "score": section_score,
            "weight": 10.0,
        },

        "unsupported_claim_check": {
            "score": claim_result["score"],
            "weight": 15.0,
        },
    }

    total_weight = sum(
        component["weight"]
        for component
        in components.values()
    )

    overall_score = sum(
        component["score"]
        * component["weight"]
        for component
        in components.values()
    ) / total_weight

    return {
        "ats_score": round(
            overall_score,
            2,
        ),

        "components": components,

        "required_exact_matches": required_exact,

        "required_semantic_matches": required_semantic,

        "preferred_exact_matches": preferred_exact,

        "preferred_semantic_matches": preferred_semantic,

        "education_alignment_detail": (
            education_result
        ),

        "unsupported_projects": (
            claim_result["unsupported_projects"]
        ),

        "experience_violation": (
            claim_result["experience_violation"]
        ),
    }
