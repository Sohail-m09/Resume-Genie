from pathlib import Path

from ingestion.pdf_loader import load_pdf
from processing.text_cleaner import clean_documents
from processing.text_splitter import split_documents
from processing.text_extractor import extract_text
from extraction.resume_extractor import extract_resume

from schemas.resume import Resume
from langchain_core.documents import Document


def process_resume_input(
    file_path: str,
) -> tuple[Resume, list[Document]]:
    """
    Process a resume PDF into a structured Resume object
    and processed document chunks.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Resume PDF not found: {file_path}"
        )

    documents = load_pdf(
        str(path)
    )

    cleaned_documents = clean_documents(
        documents
    )

    resume_text = extract_text(
        cleaned_documents
    )

    resume = extract_resume(
        resume_text
    )

    chunks = split_documents(
        cleaned_documents
    )

    return resume, chunks

