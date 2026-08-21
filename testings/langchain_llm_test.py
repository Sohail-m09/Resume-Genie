import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI  

load_dotenv()

model = ChatGoogleGenerativeAI(
    model = "gemini-3.6-flash",
    google_api_key = os.getenv("GEMINI_API_KEY")
)

response = model.invoke("Explain RAG in one simple sentence.")

print(response.content)