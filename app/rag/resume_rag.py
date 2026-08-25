from llm.gemini import get_gemini_model
from retrieval.chroma_retriever import retrieve_resume_context
from rag.context_builder import build_resume_context
from rag.prompt_builder import build_resume_prompt
from rag.generator import generate_resume_answer


def ask_resume(question: str) -> str:
    """
    Answer a question using the resume through
    the complete RAG pipeline.

    Flow:
        Question
        → Retrieval
        → Context Construction
        → Prompt Grounding
        → Gemini Generation
    """

    # 1. Retrieve relevant resume chunks
    retrieved_chunks = retrieve_resume_context(question)

    # 2. Build clean resume context
    resume_context = build_resume_context(
        retrieved_chunks
    )

    # 3. Build grounded prompt
    grounded_prompt = build_resume_prompt(
        context=resume_context,
        question=question,
    )

    # 4. Get Gemini model
    model = get_gemini_model()

    # 5. Generate grounded answer
    answer = generate_resume_answer(
        model=model,
        prompt=grounded_prompt,
    )

    return answer