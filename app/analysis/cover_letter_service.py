from schemas.resume import Resume
from schemas.job_description import JobDescription
from schemas.cover_letter import CoverLetter

from analysis.cover_letter_evidence import (
    select_cover_letter_evidence,
)

from analysis.cover_letter_prompt import (
    build_cover_letter_prompt,
)

from analysis.cover_letter_generator import (
    generate_cover_letter,
)


def create_cover_letter(
    resume: Resume,
    job_description: JobDescription,
) -> CoverLetter:
    """
    Generate a job-specific, evidence-grounded cover letter.

    Flow:
        Resume + JD
        → Evidence Selection
        → Grounded Prompt
        → Gemini
        → Structured CoverLetter
    """

    # 1. Select relevant resume evidence
    evidence = select_cover_letter_evidence(
        resume=resume,
        job_description=job_description,
    )

    # 2. Build grounded prompt
    prompt = build_cover_letter_prompt(
        evidence=evidence,
        job_description=job_description,
    )

    # 3. Generate structured cover letter
    cover_letter = generate_cover_letter(
        prompt=prompt,
    )

    return cover_letter