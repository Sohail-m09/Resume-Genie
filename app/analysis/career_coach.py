from llm.gemini import get_gemini_model
from retrieval.chroma_retriever import retrieve_resume_context
from rag.context_builder import build_resume_context
from analysis.career_coach_prompt import (
    build_career_coach_prompt,
)


def answer_resume_question(
    question: str,
    resume_context: str,
) -> str:
    """
    Answer a resume-related question using the
    Career Coach grounding policy.
    """

    prompt = build_career_coach_prompt(
        question=question,
        resume_context=resume_context,
    )

    model = get_gemini_model()

    response = model.invoke(prompt)

    return response.content

def answer_job_question(
    question: str,
    job_context: str,
    resume_context: str | None = None,
) -> str:
    """
    Answer a job-related question using job description context
    and optional resume context.
    """

    prompt = build_career_coach_prompt(
        question=question,
        resume_context=resume_context,
        job_context=job_context,
    )

    model = get_gemini_model()

    response = model.invoke(prompt)

    if isinstance(response.content, str):
        return response.content

    return str(response.content)

def answer_with_resume_rag(
    question: str,
    job_context: str | None = None,
    analysis_context: str | None = None,
) -> str:
    """
    Answer a Career Coach question using dynamically retrieved
    resume context plus optional JD and analysis context.
    """

    # 1. Retrieve relevant resume chunks
    retrieved_chunks = retrieve_resume_context(
        question
    )

    # 2. Build resume context
    resume_context = build_resume_context(
        retrieved_chunks
    )

    # 3. Build Career Coach prompt
    prompt = build_career_coach_prompt(
        question=question,
        resume_context=resume_context,
        job_context=job_context,
        analysis_context=analysis_context,
    )

    # 4. Generate answer
    model = get_gemini_model()

    response = model.invoke(prompt)

    if isinstance(response.content, str):
        return response.content

    return str(response.content)