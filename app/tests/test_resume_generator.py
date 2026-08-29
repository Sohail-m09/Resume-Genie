from resume_generator.validator import (
    validate_tailored_resume,
)
from resume_generator.customization import (
    apply_resume_customization,
)

from resume_generator.tailoring import (
    TailoredResume,
    TailoredProject,
    TailoredEducation,
    ResumeTailoringPlan,
)

from schemas.resume import (
    Resume,
    PersonalInformation,
    Education,
    Project,
)

def build_test_resume() -> Resume:
    """
    Create a minimal resume fixture for testing.
    """

    return Resume(
        personal_information=PersonalInformation(
            name="Test Candidate",
            email="test@example.com",
            phone="1234567890",
            location="India",
        ),

        summary="Python and machine learning candidate.",

        skills=[
            "Python",
            "SQL",
            "Machine Learning",
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

        experience=[],

        projects=[
            Project(
                name="Phishing Prediction Model",
                description="Machine learning project.",
                technologies=[
                    "Python",
                    "Streamlit",
                ],
            )
        ],

        certifications=[
            "Python Essentials",
        ],
    )


def build_valid_tailored_resume() -> TailoredResume:
    """
    Create a valid tailored resume fixture.
    """

    return TailoredResume(
        summary=(
            "Junior Data Scientist with a foundation "
            "in Python and SQL."
        ),

        skills=[
            "Python",
            "SQL",
            "Machine Learning",
        ],

        projects=[
            TailoredProject(
                name="Phishing Prediction Model",
                technologies=[
                    "Python",
                    "Streamlit",
                ],
                bullets=[
                    "Built a machine learning solution."
                ],
            )
        ],

        experience=[],

        education=[
            TailoredEducation(
                degree="B.E.",
                institution="University of Mumbai",
                year="2021 - 2025",
                details="Computer Engineering",
            )
        ],

        certifications=[
            "Python Essentials",
        ],

        section_order=[
            "summary",
            "skills",
            "projects",
            "education",
            "certifications",
        ],
    )

def test_valid_tailored_resume():
    original_resume = build_test_resume()
    tailored_resume = build_valid_tailored_resume()

    result = validate_tailored_resume(
        original_resume=original_resume,
        tailored_resume=tailored_resume,
    )

    assert result["valid"] is True
    assert result["unsupported_projects"] == []
    assert result["experience_violation"] is False

def test_hallucinated_project_is_rejected():
    original_resume = build_test_resume()

    tailored_resume = build_valid_tailored_resume()

    tailored_resume.projects.append(
        TailoredProject(
            name="AWS Cloud Deployment",
            technologies=["AWS"],
            bullets=[
                "Deployed machine learning models to AWS."
            ],
        )
    )

    result = validate_tailored_resume(
        original_resume=original_resume,
        tailored_resume=tailored_resume,
    )

    assert result["valid"] is False
    assert "aws cloud deployment" in (
        result["unsupported_projects"]
    )

def test_fabricated_experience_is_rejected():
    original_resume = build_test_resume()

    tailored_resume = build_valid_tailored_resume()

    tailored_resume.experience = [
        "Machine Learning Intern at XYZ Company"
    ]

    result = validate_tailored_resume(
        original_resume=original_resume,
        tailored_resume=tailored_resume,
    )

    assert result["valid"] is False
    assert result["experience_violation"] is True

def test_invalid_section_is_rejected():
    original_resume = build_test_resume()

    tailored_resume = build_valid_tailored_resume()

    tailored_resume.section_order = [
        "summary",
        "skills",
        "projects",
        "aws_experience",
    ]

    result = validate_tailored_resume(
        original_resume=original_resume,
        tailored_resume=tailored_resume,
    )

    assert result["valid"] is False
    assert "aws_experience" in (
        result["invalid_sections"]
    )

def test_duplicate_sections_are_rejected():
    original_resume = build_test_resume()

    tailored_resume = build_valid_tailored_resume()

    tailored_resume.section_order = [
        "summary",
        "skills",
        "projects",
        "education",
        "education",
        "certifications",
    ]

    result = validate_tailored_resume(
        original_resume=original_resume,
        tailored_resume=tailored_resume,
    )

    assert result["valid"] is False
    assert result["duplicate_sections"] is True


def test_section_reordering():
    plan = ResumeTailoringPlan(
        summary_changes=[],
        skills_to_prioritize=[],
        skills_to_deprioritize=[],
        project_tailoring=[],
        experience_changes=[],
        unsupported_requirements=[],
        section_config={
            "section_order": [
                "summary",
                "skills",
                "projects",
                "education",
                "certifications",
            ],
            "removed_sections": [],
            "removed_projects": [],
        },
    )

    updated_plan = apply_resume_customization(
        tailoring_plan=plan,
        section_order=[
            "summary",
            "education",
            "skills",
            "projects",
            "certifications",
        ],
    )

    assert updated_plan.section_config.section_order == [
        "summary",
        "education",
        "skills",
        "projects",
        "certifications",
    ]

def test_project_removal():
    plan = ResumeTailoringPlan(
        summary_changes=[],
        skills_to_prioritize=[],
        skills_to_deprioritize=[],
        project_tailoring=[],
        experience_changes=[],
        unsupported_requirements=[],
        section_config={
            "section_order": [
                "summary",
                "skills",
                "projects",
                "education",
                "certifications",
            ],
            "removed_sections": [],
            "removed_projects": [],
        },
    )

    updated_plan = apply_resume_customization(
        tailoring_plan=plan,
        removed_projects=[
            "Bank Loan Prediction",
        ],
    )

    assert (
        "Bank Loan Prediction"
        in updated_plan.section_config.removed_projects
    )
