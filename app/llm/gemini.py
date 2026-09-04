import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_groq import ChatGroq
load_dotenv()


def get_gemini_model() -> ChatGoogleGenerativeAI:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set.")
    return ChatGoogleGenerativeAI(
        model = "gemini-3.1-flash-lite",
        google_api_key=api_key,
    ) 

'''def get_huggingface_model() -> ChatHuggingFace:
    api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    
    if not api_key:
        raise ValueError("HUGGINGFACEHUB_API_TOKEN is not set in the .env file.")

    # 1. Initialize the LLM Endpoint
    llm = HuggingFaceEndpoint(
        repo_id = "deepseek-ai/DeepSeek-V4-Flash-0731", 
        task = "text-generation",
        max_new_tokens = 2048,
        huggingfacehub_api_token = api_key
    )
    
    # 2. Wrap it so it behaves like the Gemini Chat Model
    model = ChatHuggingFace(llm = llm)
    
    return model '''

'''def get_groq_model() -> ChatGroq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set in the .env file.")

    # We use Llama 3.3 70B, which is incredibly smart for extraction tasks
    model = ChatGroq(
        model="qwen3-32b", 
        temperature=0.0, # Keep temperature at 0 for strict data extraction
        groq_api_key=api_key,
    )
    return model'''