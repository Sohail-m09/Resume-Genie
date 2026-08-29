from application.resume_input import (
    process_resume_input,
)

from application.job_input import (
    process_job_description_input,
)

from application.pipeline import (
    analyze_application,
)

from resume_generator.tailoring import (
    generate_tailoring_plan,
    generate_tailored_resume,
)

from resume_generator.validator import (
    validate_tailored_resume,
)

from resume_generator.ats_validator import (
    calculate_ats_score,
)


def calculate_ats_for_application(
    resume_path: str,
    job_text: str | None = None,
    job_pdf_path: str | None = None,
):
    """
    Generate a tailored resume and calculate its
    ATS-oriented optimization score.
    """

    resume, _ = process_resume_input(
        resume_path
    )

    job_description = (
        process_job_description_input(
            job_text=job_text,
            pdf_path=job_pdf_path,
        )
    )

    analysis = analyze_application(
        resume=resume,
        job_description=job_description,
    )

    tailoring_plan = generate_tailoring_plan(
        resume=resume,
        job_description=job_description,
        analysis_context=(
            analysis.model_dump_json(
                indent=2
            )
        ),
    )

    tailored_resume = generate_tailored_resume(
        resume=resume,
        job_description=job_description,
        tailoring_plan=tailoring_plan,
    )

    validation = validate_tailored_resume(
        original_resume=resume,
        tailored_resume=tailored_resume,
    )

    if not validation["valid"]:
        return {
            "validation": validation,
            "ats": None,
        }

    ats = calculate_ats_score(
        original_resume=resume,
        tailored_resume=tailored_resume,
        job_description=job_description,
    )

    return {
        "validation": validation,
        "ats": ats,
    }
