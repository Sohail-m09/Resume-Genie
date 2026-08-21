from schemas.job_description import JobDescription


job = JobDescription(
    job_title="Machine Learning Engineer",
    company="Example Technologies",
    required_skills=[
        "Python",
        "SQL",
        "Machine Learning",
        "FastAPI",
    ],
    preferred_skills=[
        "Docker",
        "AWS",
    ],
    responsibilities=[
        "Develop machine learning models.",
        "Build backend APIs.",
        "Deploy ML applications.",
    ],
    experience_required="1-3 years of experience",
    education_required="Bachelor's degree in Computer Science or related field",
    qualifications=[
        "Strong problem-solving skills.",
        "Good communication skills.",
    ],
)

print("===== JOB DESCRIPTION =====")
print(job)

print("\n===== AS DICTIONARY =====")
print(job.model_dump())