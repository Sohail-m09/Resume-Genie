from pathlib import Path
import re

from fastapi import HTTPException


MAX_FILE_SIZE = 5 * 1024 * 1024


def validate_pdf_file(
    filename: str | None,
    content_type: str | None,
    content: bytes,
) -> None:
    """
    Validate an uploaded PDF file.
    """

    if not filename:
        raise HTTPException(
            status_code=400,
            detail="A filename is required.",
        )

    if content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    if not content.startswith(b"%PDF"):
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is not a valid PDF.",
        )

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size exceeds the 5 MB limit.",
        )


def sanitize_filename(
    filename: str,
) -> str:
    """
    Remove unsafe characters from uploaded filenames.
    """

    safe_name = Path(
        filename
    ).name

    safe_name = re.sub(
        r"[^a-zA-Z0-9._-]",
        "_",
        safe_name,
    )

    return safe_name


def cleanup_file(
    file_path: str,
) -> None:
    """
    Remove a temporary uploaded file if it exists.
    """

    path = Path(file_path)

    if path.exists():
        path.unlink()

