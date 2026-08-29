from embeddings.similarity import semantic_similarity
from config import SEMANTIC_SKILL_THRESHOLD


test_cases = [
    {
        "resume_skill": "Python",
        "job_requirement": "Python",
        "expected": "exact",
    },
    {
        "resume_skill": "Docker",
        "job_requirement": "Containerization",
        "expected": "semantic",
    },
    {
        "resume_skill": "FastAPI",
        "job_requirement": "Backend API development",
        "expected": "borderline",
    },
    {
        "resume_skill": "Python",
        "job_requirement": "Docker",
        "expected": "none",
    },
    {
        "resume_skill": "SQL",
        "job_requirement": "Photoshop",
        "expected": "none",
    },
]


print("===== FINAL SEMANTIC EVALUATION =====")
print(f"Provisional threshold: {SEMANTIC_SKILL_THRESHOLD}")
print()


for case in test_cases:

    resume_skill = case["resume_skill"]
    job_requirement = case["job_requirement"]

    # Exact comparison
    is_exact = (
        resume_skill.strip().lower()
        == job_requirement.strip().lower()
    )

    # Semantic comparison
    similarity = semantic_similarity(
        resume_skill,
        job_requirement,
    )

    if is_exact:
        actual = "exact"

    elif similarity >= SEMANTIC_SKILL_THRESHOLD:
        actual = "semantic"

    else:
        actual = "none"

    print(
        f"Resume: {resume_skill:15} | "
        f"JD: {job_requirement:30} | "
        f"Similarity: {similarity:.4f} | "
        f"Expected: {case['expected']:10} | "
        f"Actual: {actual}"
    )