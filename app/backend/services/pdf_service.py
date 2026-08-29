from application.pipeline import (
    run_resume_genie,
)


def generate_resume_pdf(
    resume_path: str,
    job_text: str | None = None,
    job_pdf_path: str | None = None,
    section_order: list[str] | None = None,
    removed_sections: list[str] | None = None,
    removed_projects: list[str] | None = None,
):
    """
    Run the complete Resume Genie pipeline
    and return the generated PDF path.
    """

    result = run_resume_genie(
        resume_path=resume_path,
        job_text=job_text,
        job_pdf_path=job_pdf_path,
        section_order=section_order,
        removed_sections=removed_sections,
        removed_projects=removed_projects,
    )

    return result