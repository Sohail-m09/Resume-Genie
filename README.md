# Resume Genie 🚀

### AI-Powered Resume Analysis & Career Suite

Resume Genie is an AI-powered career assistant that analyzes a candidate's resume against a job description and provides personalized, evidence-grounded career assistance.

The application combines **LLM-based structured extraction, semantic search, Retrieval-Augmented Generation (RAG), ATS analysis, tailored resume generation, cover-letter generation, and an AI Career Coach** into a single Streamlit application backed by a FastAPI API.

---

## 🎯 Problem Statement

Traditional resume tools provide only basic keyword matching or generic suggestions. Candidates struggle with questions like:

- Does my resume match this job?
- Which skills from the JD do I already have?
- Why might my resume fail ATS screening?
- How can I tailor my resume or write a cover letter based on my actual experience?

Resume Genie solves these through an integrated AI-powered workflow.

---

## 💡 What Resume Genie Solves

| Feature | Description |
|---------|-------------|
| **Resume Understanding** | Extracts structured info (skills, education, experience, projects) from PDF |
| **Job Description Understanding** | Extracts structured JD info from text or PDF |
| **Resume–Job Analysis** | Compares resume against job requirements |
| **ATS Analysis** | Evaluates ATS compatibility and identifies gaps |
| **Tailored Resume** | Generates job-specific resume version |
| **Grounded Cover Letter** | Generates evidence-based cover letter from actual resume data |
| **AI Career Coach** | RAG-powered Q&A grounded in candidate's actual information |

---

## 🏗️ Architecture Overview

```
Streamlit → Resume Upload → Processing → PostgreSQL + ChromaDB → Analysis → Career Coach → Cover Letter → Output
```

**Key Components:**
- **Frontend:** Streamlit
- **Backend:** FastAPI
- **LLM:** Google Gemini (via LangChain)
- **Database:** PostgreSQL (structured data) + ChromaDB (vector embeddings)
- **Embeddings:** BAAI/bge-small-en-v1.5
- **RAG:** Semantic retrieval with user/resume-aware filtering

---

## 🔄 Processing Pipeline (Summary)

1. **Resume Upload** → PDF ingestion via PyPDFLoader
2. **Text Cleaning & Extraction** → Remove noise, extract clean text
3. **Chunking** → Split into smaller chunks for RAG retrieval
4. **Structured Extraction** → Gemini + Pydantic outputs `Resume` object
5. **Persistence** → Store in PostgreSQL + ChromaDB (with metadata)
6. **Job Description Input** → Text or PDF → Structured `JobDescription` object
7. **Analysis** → Resume–JD match + ATS evaluation
8. **Tailored Resume** → Job-specific version generation
9. **Career Coach** → RAG-powered Q&A with grounding rules
10. **Cover Letter** → Evidence-based generation from actual resume data

---

## 🛠️ Technology Stack

| Category | Technology |
| -------- | ---------- |
| Frontend | Streamlit |
| Backend | FastAPI |
| LLM | Google Gemini |
| LLM Framework | LangChain |
| Structured Output | Pydantic |
| PDF Processing | PyPDFLoader |
| Embeddings | BAAI/bge-small-en-v1.5 |
| Vector DB | ChromaDB |
| Relational DB | PostgreSQL |
| ORM | SQLAlchemy |
| Migrations | Alembic |

---

## ✅ Key Problems Solved

| Problem | Solution |
|---------|----------|
| Unreliable PDF extraction | Dedicated cleaning pipeline |
| Unstructured LLM responses | Pydantic structured schemas |
| Pydantic validation errors | Debugged schemas & extraction |
| RAG without user isolation | Metadata filtering (user_id, resume_id) |
| Hallucination risk | Grounded prompts with explicit rules |
| Cover Letter hallucination | Evidence-selection layer before generation |
| Frontend/backend coupling | Separate FastAPI + Streamlit architecture |

---

## 📁 Project Structure

```
Resume-Genie/
├── app/
│   ├── analysis/          # Career Coach, Cover Letter
│   ├── application/       # Resume/JD input pipelines
│   ├── backend/           # FastAPI routes, services
│   ├── database/          # PostgreSQL models, repositories
│   ├── extraction/        # Resume/JD extractors
│   ├── ingestion/         # PDF loader
│   ├── llm/               # Gemini integration
│   ├── processing/        # Text cleaning, splitting
│   ├── rag/               # Context builder
│   ├── retrieval/         # ChromaDB retriever
│   ├── schemas/           # Pydantic models
│   ├── vectorstore/       # ChromaDB store
│   └── frontend/          # Streamlit app + API client
├── data/                  # Uploads & ChromaDB
├── .env
├── requirements.txt
└── README.md
```

---

## ▶️ Running the Project

### 1. Setup

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure `.env`

```env
GEMINI_API_KEY=your_gemini_api_key
```

### 3. Start Services

**🔗 FastAPI Backend:**
```powershell
$env:PYTHONPATH="app"
python -m uvicorn backend.main:app --reload
```

**🔗 Streamlit Frontend:**
```powershell
$env:PYTHONPATH="app"
python -m streamlit run app/frontend/app.py
```

---

## 🧪 Current Status

- [x] Resume PDF ingestion & extraction
- [x] Structured resume & JD extraction
- [x] PostgreSQL + ChromaDB persistence
- [x] Resume–JD analysis & ATS evaluation
- [x] Tailored resume generation
- [x] RAG-powered Career Coach
- [x] Evidence-based Cover Letter generation
- [x] FastAPI backend + Streamlit frontend

---

## 🔮 Future Improvements

- RAG evaluation (RAGAS)
- End-to-end testing
- Docker containerization
- Cloud deployment (AWS)
- Production-grade authentication

---

## 📌 Key Takeaway

Resume Genie combines **document processing, structured LLM extraction, PostgreSQL, ChromaDB, RAG, grounded generation, ATS analysis, tailored resumes, cover letters, AI Career Coach, FastAPI, and Streamlit** into a complete end-to-end AI application.

The project demonstrates how GenAI components can work alongside traditional software engineering to build practical, production-ready career assistance tools.
