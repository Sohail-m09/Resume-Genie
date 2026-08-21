from services.matching_engine import semantic_skill_match


tests = [
    ("Python", "Python programming"),
    ("Docker", "Containerization"),
    ("FastAPI", "Backend API development"),
    ("Docker", "Accounting"),
]


for resume_skill, job_skill in tests:

    result = semantic_skill_match(
        resume_skill,
        job_skill,
    )

    print(result)