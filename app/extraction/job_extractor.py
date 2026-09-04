from schemas.job_description import JobDescription
from llm.gemini import get_gemini_model

def extract_job_description(job_text: str) -> JobDescription:
    model = get_gemini_model()

    structured_model = model.with_structured_output(
        JobDescription,
        method = 'json_schema',
    )

    prompt = f'''

You are an expert job-description information extraction system.

Extract information from the job description below.

Rules:
- Extract only information explicitly present in the job description.
- Do not invent requirements, skills, experience, education, or qualifications.
- Separate mandatory/required skills from preferred/nice-to-have skills.
- Extract responsibilities as separate items.
- Preserve the meaning of the original job description.
- If information is missing, leave the corresponding field empty.
- Keep technologies as separate skill items even if the source uses
  separators such as '|', commas, bullets, or similar formatting.

Job Description:
{job_text}
'''
    '''return structured_model.invoke(prompt)'''
    import time

    start_time = time.perf_counter()

    print("Starting Gemini JD extraction...")

    response = structured_model.invoke(prompt)

    elapsed_time = time.perf_counter() - start_time

    print(
        f"Gemini JD extraction completed in "
        f"{elapsed_time:.2f} seconds."
    )

    return response