from pathlib import Path

from sqlalchemy.orm import Session

from application.resume_input import (
    process_resume_input,
)

from database.repositories import (
    create_resume,
    get_user_by_id,
)

from vectorstore.chroma_store import (
    store_resume_chunks,
)


def process_uploaded_resume(
    db: Session,
    file_path: str,
    user_id: int,
):
    """
    Process an uploaded resume, persist its metadata
    for the user, and store its chunks in ChromaDB
    using both user_id and resume_id.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Resume file not found: {file_path}"
        )

    user = get_user_by_id(
        db=db,
        user_id=user_id,
    )

    if user is None:
        raise ValueError(
            "User does not exist."
        )

    resume, chunks = process_resume_input(
        str(path)
    )

    filename = path.name

    # Create the database record first
    # so that we have the canonical resume_id.
    resume_record = create_resume(
        db=db,
        user_id=user_id,
        filename=filename,
        summary=resume.summary,
        storage_path=str(path),
    )

    # Store the chunks using both user_id
    # and the specific resume_id.
    stored_chunks = store_resume_chunks(
        chunks=chunks,
        user_id=user_id,
        resume_id=resume_record.id,
        filename=filename,
    )

    return {
        "resume": resume,
        "chunk_count": stored_chunks,
        "resume_id": resume_record.id,
    }