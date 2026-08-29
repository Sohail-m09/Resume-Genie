from pydantic import BaseModel

from schemas.resume import Resume
from schemas.job_description import JobDescription

from application.resume_input import (
    process_resume_input,
)

from application.job_input import (
    process_job_description_input,
)
from analysis.final_analysis import (
    build_final_analysis,
)
from resume_generator.tailoring import (
    generate_tailoring_plan,
    generate_tailored_resume,
)

from resume_generator.customization import (
    apply_resume_customization,
)

from resume_generator.validator import (
    validate_tailored_resume,
)

from resume_generator.latex_generator import (
    generate_latex,
)

from resume_generator.pdf_builder import (
    build_pdf,
)

from resume_generator.ats_validator import (
    calculate_ats_score,
)


class ApplicationInputs(BaseModel):
    resume: Resume
    job_description: JobDescription


def prepare_application(
    resume_path: str,
    job_text: str | None = None,
    job_pdf_path: str | None = None,
) -> ApplicationInputs:
    """
    Prepare the structured inputs required by Resume Genie.
    """

    resume, _ = process_resume_input(
        resume_path
    )

    job_description = process_job_description_input(
        job_text=job_text,
        pdf_path=job_pdf_path,
    )

    return ApplicationInputs(
        resume=resume,
        job_description=job_description,
    )

def analyze_application(
    resume: Resume,
    job_description: JobDescription,
):
    """
    Run the existing Resume Genie analysis engine
    for a structured resume and job description.
    """

    return build_final_analysis(
        resume=resume,
        job_description=job_description,
    )

def run_resume_genie(
    resume_path: str,
    job_text: str | None = None,
    job_pdf_path: str | None = None,
    section_order: list[str] | None = None,
    removed_sections: list[str] | None = None,
    removed_projects: list[str] | None = None,
    analysis_context: str = "",
) -> dict:
    """
    Run the complete Resume Genie tailored-resume pipeline.
    """

    # --------------------------------------------------
    # 1. Prepare inputs
    # --------------------------------------------------

    application_inputs = prepare_application(
        resume_path=resume_path,
        job_text=job_text,
        job_pdf_path=job_pdf_path,
    )

    resume = application_inputs.resume
    job_description = application_inputs.job_description

    # --------------------------------------------------
    # 2. Analyze resume against JD
    # --------------------------------------------------

    analysis = analyze_application(
        resume=resume,
        job_description=job_description,
    )

    # --------------------------------------------------
    # 3. Generate tailoring plan
    # --------------------------------------------------

    tailoring_plan = generate_tailoring_plan(
        resume=resume,
        job_description=job_description,
        analysis_context=(
            analysis_context
            if analysis_context
            else analysis.model_dump_json(indent=2)
        ),
    )

    # --------------------------------------------------
    # 4. Apply optional user customization
    # --------------------------------------------------

    if (
        section_order is not None
        or removed_sections is not None
        or removed_projects is not None
    ):

        tailoring_plan = apply_resume_customization(
            tailoring_plan=tailoring_plan,
            section_order=section_order,
            removed_sections=removed_sections,
            removed_projects=removed_projects,
        )

    # --------------------------------------------------
    # 5. Generate tailored structured resume
    # --------------------------------------------------

    tailored_resume = generate_tailored_resume(
        resume=resume,
        job_description=job_description,
        tailoring_plan=tailoring_plan,
    )

    # --------------------------------------------------
    # 6. Validate tailored resume
    # --------------------------------------------------

    validation = validate_tailored_resume(
        original_resume=resume,
        tailored_resume=tailored_resume,
    )

    if not validation["valid"]:
        return {
            "analysis": analysis,
            "tailoring_plan": tailoring_plan,
            "tailored_resume": tailored_resume,
            "validation": validation,
            "ats": None,
            "latex": None,
            "pdf": None,
        }

    # --------------------------------------------------
    # 7. ATS-oriented score
    # --------------------------------------------------

    ats = calculate_ats_score(
        original_resume=resume,
        tailored_resume=tailored_resume,
        job_description=job_description,
    )

    # --------------------------------------------------
    # 8. Generate LaTeX
    # --------------------------------------------------

    latex = generate_latex(
        tailored_resume=tailored_resume,
        original_resume=resume,
    )

    # --------------------------------------------------
    # 9. Generate PDF
    # --------------------------------------------------

    pdf = build_pdf(
        latex_source=latex,
        filename="tailored_resume",
    )

    # --------------------------------------------------
    # 10. Return complete application result
    # --------------------------------------------------

    return {
        "analysis": analysis,
        "tailoring_plan": tailoring_plan,
        "tailored_resume": tailored_resume,
        "validation": validation,
        "ats": ats,
        "latex": latex,
        "pdf": str(pdf),
    }
