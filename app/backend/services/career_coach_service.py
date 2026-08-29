from application.resume_input import (
    process_resume_input,
)

from application.job_input import (
    process_job_description_input,
)

from application.pipeline import (
    analyze_application,
)

from analysis.career_coach import (
    answer_with_resume_rag,
)


def ask_career_coach_for_application(
    question: str,
    resume_path: str,
    job_text: str | None = None,
    job_pdf_path: str | None = None,
):
    """
    Prepare resume and job context, run the existing
    analysis pipeline, and ask the existing Career Coach.
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

    job_context = (
        job_description.model_dump_json(
            indent=2
        )
    )

    analysis_context = (
        analysis.model_dump_json(
            indent=2
        )
    )

    answer = answer_with_resume_rag(
        question=question,
        job_context=job_context,
        analysis_context=analysis_context,
    )

    return answer
