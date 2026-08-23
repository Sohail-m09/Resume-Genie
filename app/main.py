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
    job_path = Path(r"D:\Resume-Genie\data\Sample_Job_Description.pdf")

    ## Resume processing
    resume, chunks = process_resume(str(resume_path))

    ## Job description processing
    job_description = process_job_description(str(job_path))

    ## Store resume chunks in chromaDB
    stored_count = store_resume_chunks(
        chunks
    )

    validate_resume_extraction(resume)

    print("===== STRUCTURED RESUME =====")
    print(resume.model_dump())

    print("\n===== STRUCTURED JOB DESCRIPTION =====")
    print(job_description.model_dump())

    ## Vector Store Information.
    print("\n===== VECTOR STORE =====")
    print(f"Chunks stored in ChromaDB: {stored_count}")

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
    
    grounded_prompt = build_resume_prompt(
    context=resume_context,
    question=query,
    )

    print("\n===== GROUNDED PROMPT =====")
    print(grounded_prompt)

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
