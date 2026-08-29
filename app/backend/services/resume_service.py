from pathlib import Path

from application.resume_input import (
    process_resume_input,
)


def process_uploaded_resume(
    file_path: str,
) -> dict:
    """
    Process an uploaded resume PDF and return
    structured resume information.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Resume file not found: {file_path}"
        )

    resume, chunks = process_resume_input(
        str(path)
    )

    return {
        "resume": resume,
        "chunk_count": len(chunks),
    }
