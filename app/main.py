from pathlib import Path
from ingestion.pdf_loader import load_pdf
from processing.text_cleaner import clean_documents
from processing.text_splitter import split_documents
from extraction.resume_extractor import extract_resume 
from processing.text_extractor import extract_text
from schemas.resume import Resume
from validation.resume_validator import validate_resume_extraction
from langchain_core.documents import Document
from extraction.job_extractor import extract_job_description
from schemas.job_description import JobDescription
from vectorstore.chroma_store import store_resume_chunks
from rag.context_builder import build_resume_context
from retrieval.chroma_retriever import retrieve_resume_context
from rag.prompt_builder import build_resume_prompt
from rag.generator import generate_resume_answer
from llm.gemini import get_gemini_model
from rag.resume_rag import ask_resume
from analysis.resume_analyzer import analyze_resume
from analysis.skill_gap_analyzer import detect_skill_gaps, explain_skill_gaps
from analysis.semantic_evidence import find_semantic_skill_evidence
from services.keyword_optimizer import find_keyword_gaps
from analysis.project_strengthener import strengthen_projects
from analysis.final_analysis import build_final_analysis
from analysis.cover_letter_service import create_cover_letter
from analysis.improvement_recommendations import (
    generate_improvement_recommendations,
)
from analysis.cover_letter_evidence import (
    select_cover_letter_evidence,
)
from analysis.cover_letter_prompt import (
    build_cover_letter_prompt,
)
from analysis.cover_letter_generator import (
    generate_cover_letter,
)
from analysis.career_coach_prompt import (
    build_career_coach_prompt,
)


def process_resume(file_path: str) -> tuple[Resume  ,list[Document]]:
    """
    Complete resume document-processing pipeline.

    Args:
        file_path: Path to the resume PDF.

    Returns:
        Processed resume chunks.
    """
    documents = load_pdf(file_path)
    cleaned_documents = clean_documents(documents)
    resume_text = extract_text(cleaned_documents)
    resume = extract_resume(resume_text)
    chunks = split_documents(cleaned_documents)

    return resume, chunks


def process_job_description(file_path: str) -> JobDescription:
    documents = load_pdf(file_path)
    cleaned_documents = clean_documents(documents)

    job_text = extract_text(cleaned_documents)

    job_description = extract_job_description(job_text)

    return job_description


if __name__ == "__main__":
    resume_path = Path(r"D:\Resume-Genie\data\Sohail_Momin.pdf")
    job_path = Path(r"D:\Resume-Genie\data\Data_Scientist_JD.pdf")

    ## Resume processing
    resume, chunks = process_resume(str(resume_path))

    ## Job description processing
    job_description = process_job_description(str(job_path))

    ## Store resume chunks in chromaDB
    stored_count = store_resume_chunks(
        chunks
    )

    validate_resume_extraction(resume)

    '''print("===== STRUCTURED RESUME =====")
    print(resume.model_dump())

    print("\n===== STRUCTURED JOB DESCRIPTION =====")
    print(job_description.model_dump())

    ## Vector Store Information.
    print("\n===== VECTOR STORE =====")
    print(f"Chunks stored in ChromaDB: {stored_count}")'''

    query = "Have I used python and it's libraries in the project?"

    ## Retrieve relevant resume chunks from ChromaDB
    retrieved_chunks = retrieve_resume_context(query)
    
    print("\n===== RETRIEVED CHUNKS =====")
    for i, chunk in enumerate(retrieved_chunks, start=1):
        print(f"\n--- Retrieved Chunk {i} ---")
        print("Text:", chunk["text"])
        print("Metadata:", chunk["metadata"])
        print("Distance:", chunk["distance"])
    
    ## Convert retrieved chunks into LLM-ready context
    resume_context = build_resume_context(retrieved_chunks)
    
    print("\n===== RESUME CONTEXT =====")
    print(resume_context)

    ## Prompt Grounding
    '''model = get_gemini_model()
    grounded_prompt = build_resume_prompt(
    context=resume_context,
    question=query,
    )

    print("\n===== GROUNDED PROMPT =====")
    print(grounded_prompt)

    answer = generate_resume_answer(
    model = model,
    prompt=grounded_prompt,
    )

    print("\n===== RAG ANSWER =====")
    print(answer)'''

    '''query = "How many years of AWS experience do I have?"

    answer = ask_resume(query)

    print("\n===== RAG ANSWER =====")
    print(answer) ## We can use this also in the place of that big code.

    ## Structured resume output
    resume_analysis = analyze_resume(resume)

    print("\n===== RESUME ANALYSIS =====")
    print(resume_analysis.model_dump())'''

    '''## Showing skill gaps
    skill_gaps = detect_skill_gaps(
    resume=resume,
    job_description=job_description,
    )

    print("\n===== SKILL GAPS =====")
    print(skill_gaps)

    ## Explaining the skill gaps
    skill_gap_analysis = explain_skill_gaps(
    resume=resume,
    job_description=job_description,
    )

    print("\n===== SKILL GAP ANALYSIS =====")
    print(skill_gap_analysis.model_dump())


    ## Imporovement Recommendation
    improvement_recommendations = (
    generate_improvement_recommendations(
        skill_gaps
    )
    )
    print("\n===== IMPROVEMENT RECOMMENDATIONS =====")
    print(
    improvement_recommendations.model_dump()
    )

    ## Skills matching with semantic meaning
    semantic_evidence = find_semantic_skill_evidence(
    resume=resume,
    job_description=job_description,
    )

    print("\n===== SEMANTIC EVIDENCE =====")
    print(semantic_evidence)

    keyword_gaps = find_keyword_gaps(
    resume,
    job_description,
    )

    print("\n===== KEYWORD GAPS =====")
    print(keyword_gaps)'''

    '''## Strengtning the Project
    project_strengthening = strengthen_projects(
    resume=resume,
    job_description=job_description,
    )

    print("\n===== PROJECT STRENGTHENING =====")
    print(project_strengthening.model_dump())'''

    final_analysis = build_final_analysis(
    resume=resume,
    job_description=job_description,
    )

    print("\n===== FINAL RESUME ANALYSIS =====")
    print(final_analysis.model_dump())


    '''## Cover Letter Evidence
    cover_letter_evidence = select_cover_letter_evidence(
    resume=resume,
    job_description=job_description,
    )

    print("\n===== COVER LETTER EVIDENCE =====")
    print(cover_letter_evidence.model_dump())

    ## Cover Letter Prompt
    cover_letter_prompt = build_cover_letter_prompt(
    evidence=cover_letter_evidence,
    job_description=job_description,
    )

    print("\n===== COVER LETTER PROMPT =====")
    print(cover_letter_prompt)

    ## Cover letter generation
    cover_letter = generate_cover_letter(
    prompt=cover_letter_prompt,
    )

    print("\n===== GENERATED COVER LETTER =====")
    print(cover_letter.model_dump())'''

    '''## Cover letter generation for all resumes 
    cover_letter = create_cover_letter(
    resume=resume,
    job_description=job_description,
    )

    print("\n===== COVER LETTER =====")
    print(cover_letter.model_dump())'''

    ## CHecking the CAREER COACH Prompt
    question = "Why is my match score low?"

    coach_prompt = build_career_coach_prompt(
    question=question,
    resume_context=resume_context,
    job_context=job_description.model_dump_json(indent=2),
    analysis_context=final_analysis.model_dump_json(indent=2),
    )

    print("\n===== CAREER COACH PROMPT =====")
    print(coach_prompt)

''' ## Going with the structured resume format
    print("\n***** Resume Skills *****")
    print(resume.skills)

    print("\n***** Resume Education *****")
    print(resume.education)

    print("\n***** RESUME PROJECTS *****")
    for project in resume.projects:
        print(project)

    print("\n***** RESUME CERTIFICATIONS *****")
    print(resume.certifications)

    print("\n***** CHUNK INFORMATION *****")
    print(f"Number of chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks, start=1):
        print(f"\n===== CHUNK {i} =====")
        print(chunk.page_content)
        print("Metadata:", chunk.metadata) '''
