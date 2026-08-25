def generate_resume_answer(model, prompt: str) -> str:
    """
    Generate a resume-grounded answer using the provided LLM.
    """

    response = model.invoke(prompt)

    return response.content