import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an AI assistant helping with career and resume analysis."),
    ("human", "{question}")
])

chain = prompt | model

response = chain.invoke({
    "question": "What is RAG and why can it be useful in a resume analysis application?"
})

print(response.content)