import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI  
from schemas.resume import Resume

load_dotenv()

model = ChatGoogleGenerativeAI(
    model = "gemini-3.6-flash",
    google_api_key = os.getenv("GEMINI_API_KEY"),
)

structured_model = model.with_structured_output(
    Resume,
    method = "json_schema"
)

resume_text = """
Sohail Momin
Email: example@gmail.com
Location: Mumbai

Summary:
Computer Engineer with experience in Python, SQL and machine learning.

Skills:
Python | SQL | Machine Learning | FastAPI | Docker

Education:
B.E. in Computer Engineering from ARMIET, 2021-2025, CGPA 7.01/10.

Projects:
Resume Genie
Built an AI-powered resume analysis application using Python, LangChain and Gemini.
"""

resume = structured_model.invoke(
    f"""
Extract the information from the following resume text
and return it according to the provided Resume schema.

Important rules:
- Extract only information present in the resume.
- Do not invent missing information.
- Keep missing optional fields empty.
- Preserve the meaning of the original information.

Resume:
{resume_text}
"""
)


print("===== STRUCTURED RESUME =====")
print(resume)

print("\n===== TYPE =====")
print(type(resume))

print("\n===== DICTIONARY =====")
print(resume.model_dump())
