from schemas.resume import Resume
from schemas.job_description import JobDescription
from retrieval.chroma_retriever import retrieve_resume_context
from rag.context_builder import build_resume_context
from analysis.career_coach import (
    answer_with_resume_rag,
    answer_job_question,
)
from analysis.career_coach_prompt import (
    build_career_coach_prompt,
)
from llm.gemini import get_gemini_model

def _get_response_text(response) -> str:
    """
    Normalize Gemini's response content into plain text.
    """

    if isinstance(response.content, str):
        return response.content

    if isinstance(response.content, list):
        text_parts = []

        for item in response.content:
            if isinstance(item, dict) and item.get("type") == "text":
                text_parts.append(item.get("text", ""))

        if text_parts:
            return "\n".join(text_parts)

    return str(response.content)


def ask_career_coach(
    question: str,
    resume: Resume | None = None,
    job_description: JobDescription | None = None,
    analysis_context: str | None = None,
) -> str:
    """
    Single user-facing entry point for the AI Career Coach.

    The router determines whether the question requires:
    - Resume context
    - Job description context
    - Analysis context
    - A combination of contexts
    """

    question_lower = question.lower()

    # --------------------------------------------------
    # 1. Combined Resume + JD questions
    # --------------------------------------------------

    combined_terms = [
        "how can i become",
        "how can i improve",
        "how do i improve",
        "how can i better match",
        "how can i strengthen",
        "how can i increase",
        "what should i improve",
        "what should i learn",
        "what should i focus on",
        "what do i need to improve",
        "become a stronger candidate",
        "become the preferred candidate",
        "most preferred candidate",
        "better candidate",
        "stronger candidate",
    ]

    role_terms = [
        "for this role",
        "for the role",
        "for this job",
        "for the job",
        "for this position",
        "for the position",
    ]

    is_combined_question = (
        any(term in question_lower for term in combined_terms)
        or (
            any(term in question_lower for term in role_terms)
            and resume is not None
            and job_description is not None
        )
    )

    if is_combined_question:

        if resume is None and job_description is None:
            return (
                "Resume and job description information "
                "are not available."
            )

        # Retrieve resume evidence when a resume exists
        resume_context = None

        if resume is not None:
            retrieved_chunks = retrieve_resume_context(
                question
            )

            resume_context = build_resume_context(
                retrieved_chunks
            )

        prompt = build_career_coach_prompt(
            question=question,
            resume_context=resume_context,
            job_context=(
                job_description.model_dump_json(indent=2)
                if job_description
                else None
            ),
            analysis_context=analysis_context,
        )

        model = get_gemini_model()

        response = model.invoke(prompt)

        return _get_response_text(response)

    # --------------------------------------------------
    # 2. Resume-focused questions
    # --------------------------------------------------

    resume_terms = [
        "my resume",
        "my cv",
        "on my resume",
        "in my resume",
        "my skills",
        "my projects",
        "my experience",
    ]

    if any(term in question_lower for term in resume_terms):

        if resume is None:
            return "Resume information is not available."

        return answer_with_resume_rag(
            question=question,
            job_context=(
                job_description.model_dump_json(indent=2)
                if job_description
                else None
            ),
            analysis_context=analysis_context,
        )

    # --------------------------------------------------
    # 3. Job-focused questions
    # --------------------------------------------------

    job_terms = [
        "what does this job",
        "what does this role",
        "what are the requirements",
        "required skills",
        "preferred skills",
        "job description",
        "job requirements",
    ]

    if any(term in question_lower for term in job_terms):

        if job_description is None:
            return "Job description information is not available."

        job_context = job_description.model_dump_json(
            indent=2
        )

        return answer_job_question(
            question=question,
            job_context=job_context,
            resume_context=None,
        )

    # --------------------------------------------------
    # 4. Analysis-focused questions
    # --------------------------------------------------

    analysis_terms = [
        "match score",
        "why is my score",
        "why is my match",
        "missing skills",
        "skill gaps",
        "semantic match",
    ]

    if any(term in question_lower for term in analysis_terms):

        prompt = build_career_coach_prompt(
            question=question,
            resume_context=None,
            job_context=(
                job_description.model_dump_json(indent=2)
                if job_description
                else None
            ),
            analysis_context=analysis_context,
        )

        model = get_gemini_model()

        response = model.invoke(prompt)

        return _get_response_text(response)

    # --------------------------------------------------
    # 5. General career questions
    # --------------------------------------------------

    prompt = build_career_coach_prompt(
        question=question,
        resume_context=None,
        job_context=(
            job_description.model_dump_json(indent=2)
            if job_description
            else None
        ),
        analysis_context=analysis_context,
    )

    model = get_gemini_model()

    response = model.invoke(prompt)

    return _get_response_text(response)