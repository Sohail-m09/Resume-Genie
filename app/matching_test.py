from schemas.resume import Resume, PersonalInformation
from schemas.job_description import JobDescription
from services.matching_engine import match_skills
from services.matching_engine import (
    match_skills,
    calculate_skill_coverage,
    match_experience,
    match_education,
    match_project_relevance,
    build_match_analysis,
    select_best_semantic_matches,
    integrate_semantic_skill_evidence,
)
from schemas.resume import (
    Resume,
    PersonalInformation,
    Education,
    Project,
)

from services.matching_engine import (
    semantic_education_match,
    find_semantic_skill_candidates,
    classify_semantic_skill_candidates,
)

from services.matching_engine import match_project_relevance
from services.matching_engine import build_match_analysis


resume = Resume(
    personal_information=PersonalInformation(
        name="Test Candidate"
    ),
    skills=[
        "Python",
        "SQL",
    ],
    education=[
        Education(
            degree="B.E.",
            institution="University of Mumbai",
            field_of_study="Computer Engineering",
            start_date="2021",
            end_date="2025",
            grade="7.01/10.0",
        )
    ],
    projects=[
        Project(
            name="Resume Genie",
            description="Built an AI-powered resume analysis application.",
            technologies=[
                "Python",
                "FastAPI",
                "Docker",
            ],
            url=None,
        )
    ],
)

job = JobDescription(
    job_title="Backend Engineer",
    required_skills=[
        "Python",
        "SQL",
        "FastAPI",
        "Docker",
    ],
    preferred_skills=[
        "AWS",
        "Kubernetes",
    ],
    experience_required="2+ years of experience",
    education_required="B.E. Computer Engineering",
)

projects=[
    Project(
        name="Resume Genie",
        description="Built an AI-powered resume analysis application.",
        technologies=[
            "Python",
            "LangChain",
            "FastAPI",
            "Docker",
        ],
        url=None,
    )
]


# ---------------------------------------------------------
# 1. Skill matching
# ---------------------------------------------------------

skill_result = match_skills(
    resume,
    job,
)

print("===== MATCHING RESULT =====")
print(skill_result)


# ---------------------------------------------------------
# 2. Skill coverage
# ---------------------------------------------------------

required_coverage = calculate_skill_coverage(
    skill_result["required"]["matched"],
    job.required_skills,
)

preferred_coverage = calculate_skill_coverage(
    skill_result["preferred"]["matched"],
    job.preferred_skills,
)

print("\n===== SKILL COVERAGE =====")
print(f"Required Skill Coverage: {required_coverage}%")
print(f"Preferred Skill Coverage: {preferred_coverage}%")


# ---------------------------------------------------------
# 3. Experience matching
# ---------------------------------------------------------

experience_result = match_experience(
    resume,
    job,
)

print("\n===== EXPERIENCE MATCH =====")
print(experience_result)


# ---------------------------------------------------------
# 4. Education matching
# ---------------------------------------------------------

education_result = match_education(
    resume,
    job,
)

print("\n===== EDUCATION MATCH =====")
print(education_result)


# ---------------------------------------------------------
# 5. Project relevance
# ---------------------------------------------------------

project_result = match_project_relevance(
    resume,
    job,
)

print("\n===== PROJECT RELEVANCE =====")
print(project_result)


# ---------------------------------------------------------
# 6. Complete analysis
# ---------------------------------------------------------

analysis = build_match_analysis(
    skill_result=skill_result,
    experience_result=experience_result,
    education_result=education_result,
    project_result=project_result,
)

print("\n===== COMPLETE MATCH ANALYSIS =====")
print(analysis)

semantic_education_result = semantic_education_match(
    resume,
    job,
)

print("\n===== SEMANTIC EDUCATION MATCH =====")
print(semantic_education_result)

semantic_candidates = find_semantic_skill_candidates(
    resume,
    job,
)

classified_candidates = classify_semantic_skill_candidates(
    semantic_candidates
)

print("\n===== SEMANTIC SKILL CANDIDATES =====")
print(classified_candidates)

best_semantic_matches = select_best_semantic_matches(
    semantic_candidates
)

print("\n===== BEST SEMANTIC MATCHES =====")
print(best_semantic_matches)

combined_skill_result = integrate_semantic_skill_evidence(
    skill_result=skill_result,
    semantic_matches=best_semantic_matches,
)

print("\n===== COMBINED SKILL ANALYSIS =====")
print(combined_skill_result)