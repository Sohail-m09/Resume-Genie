from schemas.resume import (
    PersonalInformation,
    Education,
    Experience,
    Project,
    Resume,
)


resume = Resume(
    personal_information=PersonalInformation(
        name="Sohail Momin",
        email="example@gmail.com",
        phone=None,
        location="Mumbai",
        linkedin=None,
        github=None,
    ),
    summary="Computer Engineer with experience in Python and machine learning.",
    skills=[
        "Python",
        "SQL",
        "Machine Learning",
        "FastAPI",
    ],
    education=[
        Education(
            degree="B.E.",
            institution="ARMIET",
            field_of_study="Computer Engineering",
            start_date="2021",
            end_date="2025",
            grade="7.01/10",
        )
    ],
    experience=[],
    projects=[
        Project(
            name="Resume Genie",
            description="AI-powered resume analysis application.",
            technologies=["Python", "LangChain", "Gemini"],
            url=None,
        )
    ],
    certifications=[],
)

print(resume)
print("\n===== AS DICTIONARY =====")
print(resume.model_dump())