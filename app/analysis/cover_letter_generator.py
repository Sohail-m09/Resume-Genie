from schemas.cover_letter import CoverLetter
from llm.gemini import get_gemini_model


def generate_cover_letter(
    prompt: str,
) -> CoverLetter:
    """
    Generate a structured, evidence-grounded cover letter.
    """

    model = get_gemini_model().with_structured_output(
        CoverLetter
    )

    return model.invoke(prompt)