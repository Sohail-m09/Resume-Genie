import re


def clean_text(text: str) -> str:
    """Normalize common whitespace issues in extracted document text."""

    # Replace tabs with spaces
    text = text.replace("\t", " ")

    # Collapse repeated spaces
    text = re.sub(r"[ ]+", " ", text)

    # Collapse 3+ consecutive newlines into 2
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove leading/trailing whitespace
    text = text.strip()

    return text