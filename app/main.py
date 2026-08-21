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

    resume, chunks = process_resume(str(resume_path))
    job_description = process_job_description(str(job_path))

    

    validate_resume_extraction(resume)

    print("===== STRUCTURED RESUME =====")
    print(resume.model_dump())

    print("\n===== STRUCTURED JOB DESCRIPTION =====")
    print(job_description.model_dump())

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
