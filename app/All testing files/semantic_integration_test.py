from schemas.resume import Resume, PersonalInformation
from schemas.job_description import JobDescription

from services.matching_engine import (
    match_skills,
    find_semantic_skill_candidates,
    select_best_semantic_matches,
    integrate_semantic_skill_evidence,
)


resume = Resume(
    personal_information=PersonalInformation(
        name="Semantic Test Candidate"
    ),
    skills=[
        "Python",
        "SQL",
        "Docker",
    ],
)


job = JobDescription(
    job_title="Platform Engineer",
    required_skills=[
        "Containerization",
    ],
)


# 1. Deterministic matching
skill_result = match_skills(
    resume,
    job,
)


# 2. Semantic candidate generation
semantic_candidates = find_semantic_skill_candidates(
    resume,
    job,
)


# 3. Select best semantic candidate
best_semantic_matches = select_best_semantic_matches(
    semantic_candidates
)


# 4. Integrate deterministic + semantic evidence
combined_result = integrate_semantic_skill_evidence(
    skill_result=skill_result,
    semantic_matches=best_semantic_matches,
)


print("===== DETERMINISTIC RESULT =====")
print(skill_result)

print("\n===== SEMANTIC CANDIDATES =====")
print(semantic_candidates)

print("\n===== BEST SEMANTIC MATCHES =====")
print(best_semantic_matches)

print("\n===== COMBINED RESULT =====")
print(combined_result)