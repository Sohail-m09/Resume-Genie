# Resume Genie 🚀

### AI-Powered Resume Analysis & Career Suite

Resume Genie is an AI-powered career assistant that analyzes a candidate's resume against a job description and provides personalized, evidence-grounded career assistance.

The application combines **LLM-based structured extraction, semantic search, Retrieval-Augmented Generation (RAG), ATS analysis, tailored resume generation, cover-letter generation, and an AI Career Coach** into a single Streamlit application backed by a FastAPI API.

---

## 🎯 Problem Statement

Traditional resume tools usually provide only basic keyword matching or generic resume suggestions.

Candidates often struggle to answer questions such as:

- Does my resume actually match this job?
- Which skills from the job description do I already have?
- Why might my resume fail ATS screening?
- Which parts of my resume should be improved?
- How can I tailor my resume for a specific job?
- How can I write a cover letter based on my actual experience?
- Can I ask questions about my resume and get answers based on my actual information?

Resume Genie was designed to solve these problems through an integrated AI-powered workflow.

---

## 💡 What Resume Genie Solves

The project provides a complete resume-to-job analysis workflow.

### 1. Resume Understanding

The system converts an uploaded PDF resume into structured information such as:

- Personal information
- Summary
- Skills
- Education
- Experience
- Projects
- Certifications and other available resume information

### 2. Job Description Understanding

A job description can be provided as:

- Text
- PDF

The system extracts structured job information including:

- Job title
- Company
- Required skills
- Preferred skills
- Responsibilities
- Qualifications
- Education requirements
- Experience requirements

### 3. Resume–Job Analysis

The system compares the candidate's resume with the target job and generates an analysis of the application.

### 4. ATS Analysis

The system evaluates the resume against the job requirements and identifies areas that can affect ATS compatibility.

### 5. Tailored Resume

The system can generate a job-specific version of the resume while working from the candidate's existing information.

### 6. Grounded Cover Letter

The system generates a job-specific cover letter using evidence selected from the candidate's actual resume.

### 7. RAG-Powered AI Career Coach

The candidate can ask questions about their resume and target job.

The Career Coach retrieves relevant resume information from the vector database before generating an answer.

This helps keep answers grounded in the candidate's actual information instead of relying only on the LLM's general knowledge.

---

## 🏗️ Overall Architecture

```
                    Streamlit
                       ↓
                 Upload Resume
                       ↓
              Resume Processing
                       ↓
              Structured Resume
                       ↓
              Store Resume Data
                ↙           ↘
          PostgreSQL       ChromaDB
                              ↓
                         BGE Embeddings

                       ↓
               Add Job Description
                       ↓
                Job Processing
                       ↓
             Structured Job Data
                       ↓
                  PostgreSQL

                       ↓
              Select Resume + Job
                       ↓
          ┌────────────┼────────────┐
          ↓            ↓            ↓
       Analysis       ATS      Tailored Resume
          ↓            ↓            ↓
          └────────────┼────────────┘
                       ↓
              Career Coach
                       ↓
              Cover Letter
                       ↓
                 Final Output
```

---

## 🔄 Complete Processing Pipeline

### Step 1 — Resume Upload

The user uploads a resume PDF through the Streamlit interface.

```
Streamlit
   ↓
Resume PDF
   ↓
FastAPI
   ↓
Resume Processing Pipeline
```

The backend validates the uploaded file and passes it into the application layer.

---

### Step 2 — PDF Loading

The PDF is loaded using the PDF ingestion layer.

```
PDF
 ↓
PyPDFLoader
 ↓
Documents
```

The document structure, including page information, is preserved where available.

---

### Step 3 — Text Cleaning

Extracted document content is cleaned before further processing.

```
Raw PDF Content
      ↓
Text Cleaning
      ↓
Clean Documents
```

This helps reduce extraction noise before sending the content to the LLM.

---

### Step 4 — Text Extraction

The cleaned documents are converted into usable text.

```
Clean Documents
      ↓
Text Extraction
      ↓
Resume Text
```

---

### Step 5 — Text Chunking

The extracted resume text is split into smaller chunks using a recursive text splitter.

```
Resume Text
     ↓
Recursive Character Text Splitter
     ↓
Resume Chunks
```

Chunking is important because the entire document does not need to be retrieved for every question.

It allows the RAG system to retrieve only the most relevant portions of the resume.

---

### Step 6 — Structured Resume Extraction

The extracted resume text is passed to Gemini using LangChain structured output.

```
Resume Text
     ↓
Gemini
     ↓
Structured Output
     ↓
Pydantic Resume Schema
```

Instead of treating the LLM response as unstructured text, Resume Genie converts the result into a strongly typed `Resume` object.

This provides predictable fields that can be used by the rest of the application.

---

### Step 7 — Resume Persistence

The structured resume is persisted in PostgreSQL.

```
Structured Resume
       ↓
PostgreSQL
       ↓
Resume Record
```

The database stores information such as:

- Resume ID
- User ID
- Filename
- Resume summary
- Storage path
- Creation timestamp

This allows previously uploaded resumes to be selected later.

---

### Step 8 — Resume Vector Storage

The resume chunks are also stored in ChromaDB for semantic retrieval.

```
Resume Chunks
      ↓
BGE Embeddings
      ↓
ChromaDB
```

The project uses the BGE embedding model:

```
BAAI/bge-small-en-v1.5
```

Each chunk is stored with metadata such as:

- Source filename
- Page
- Page label
- User ID
- Resume ID

This metadata becomes important for retrieving only the correct user's resume and selected resume.

---

### Step 9 — Job Description Input

The user can provide a job description either through text or a PDF.

```
Job Description
      ↓
 ┌────┴────┐
 ↓         ↓
Text      PDF
 └────┬────┘
      ↓
Job Processing Pipeline
```

---

### Step 10 — Job Description Extraction

The job description is converted into a structured `JobDescription` object.

```
Job Description Text
        ↓
       Gemini
        ↓
Structured Output
        ↓
JobDescription
```

The system extracts:

- Job Title
- Company
- Required Skills
- Preferred Skills
- Responsibilities
- Qualifications
- Education Requirements
- Experience Requirements

The extraction prompt specifically instructs the model to distinguish between mandatory and preferred skills.

---

### Step 11 — Job Persistence

The structured job description is stored in PostgreSQL.

```
JobDescription
      ↓
PostgreSQL
      ↓
Job Record
```

This allows users to select saved job descriptions together with saved resumes.

---

### Step 12 — Resume + Job Selection

The Streamlit application allows the user to select:

```
Resume
   +
Job Description
```

These selections determine the target application being analyzed.

```
Selected Resume
      +
Selected Job
      ↓
Application Analysis
```

---

### Step 13 — Resume–Job Analysis

The resume and job description are passed through the application analysis pipeline.

```
Resume
   +
JobDescription
   ↓
Application Analysis
   ↓
Analysis Result
```

The analysis identifies how the candidate's existing profile relates to the target role.

The analysis result is also used by downstream features such as the Career Coach.

---

### Step 14 — ATS Analysis

The ATS component evaluates the resume against the job requirements.

```
Resume
   +
Job Description
   ↓
ATS Analysis
   ↓
ATS Result
```

The goal is to identify potential gaps between the resume and the target job and provide actionable information for improving alignment.

---

### Step 15 — Tailored Resume

The project also supports generating a tailored version of the resume.

```
Resume
   +
Job Description
   ↓
Tailoring Pipeline
   ↓
Job-Specific Resume
   ↓
PDF Output
```

The purpose is to adapt the presentation of the candidate's existing qualifications to the target role rather than generating unsupported information.

---

## 🤖 RAG Pipeline

One of the major components of Resume Genie is the RAG-powered Career Coach.

The RAG pipeline follows this architecture:

```
Resume PDF
    ↓
Text Extraction
    ↓
Cleaning
    ↓
Chunking
    ↓
BGE Embeddings
    ↓
ChromaDB
```

When the user asks a question:

```
User Question
      ↓
Query Embedding
      ↓
ChromaDB Retrieval
      ↓
Relevant Resume Chunks
      ↓
Context Builder
      ↓
Grounded Prompt
      ↓
Gemini
      ↓
Career Coach Answer
```

---

## 🔎 Retrieval Filtering

Resume Genie does not simply search the entire vector database.

Retrieved chunks can be filtered using:

- User ID
- Resume ID
- Source

This is important for maintaining separation between different users and different saved resumes.

For example:

```
User
 ↓
Selected Resume
 ↓
Selected Resume Chunks
 ↓
Relevant Context
```

This prevents the Career Coach from accidentally retrieving information belonging to another resume.

---

## 🧠 Career Coach

The AI Career Coach allows the user to ask questions related to:

- Resume
- Job description
- Resume–job alignment
- Skills
- Missing requirements
- Projects
- Career preparation

The Career Coach uses:

```
Resume RAG Context
+
Job Context
+
Analysis Context
+
User Question
        ↓
     Gemini
        ↓
Grounded Answer
```

The prompt contains explicit grounding rules.

The model is instructed not to invent:

- Skills
- Experience
- Projects
- Certifications
- Achievements
- Job requirements
- Metrics

This makes the Career Coach more reliable for resume-specific questions.

---

## ✉️ Cover Letter Generator

The Cover Letter Generator follows an evidence-based generation pipeline.

```
Resume
   +
Job Description
   ↓
Evidence Selection
   ↓
Grounded Prompt
   ↓
Gemini
   ↓
Structured CoverLetter
   ↓
Streamlit
```

Before generating the letter, the system selects relevant evidence from the resume.

For example:

```
Resume Skills
      ↓
Relevant Job Skills
```

and:

```
Resume Projects
      ↓
Projects Relevant to Job
```

The generator then creates structured sections:

```
Opening
Relevant Experience
Relevant Projects
Motivation
Closing
```

The prompt explicitly prevents the model from fabricating candidate information.

---

## 🧩 Structured Output

Structured output is used throughout the project to make LLM responses predictable.

Examples include:

- `Resume`
- `JobDescription`
- `CoverLetter`
- `CoverLetterEvidence`

Instead of depending on free-form LLM responses, the application uses Pydantic models.

This makes the generated information easier to:

- Validate
- Store
- Process
- Pass between components
- Display in the frontend

---

## 🗄️ Database Architecture

PostgreSQL is used for application-level persistence.

The database stores entities such as:

```
User
 │
 ├── Resumes
 │
 └── Jobs
```

Resume records contain information such as:

- Resume ID
- User ID
- Filename
- Summary
- Storage Path
- Created At

Job records contain information such as:

- Job ID
- User ID
- Job Title
- Company
- Required Skills
- Preferred Skills
- Responsibilities
- Qualifications
- Education
- Experience
- Created At

SQLAlchemy is used as the ORM layer and Alembic is used for database migrations.

---

## 🧠 Vector Database Architecture

ChromaDB is used specifically for semantic retrieval.

```
PostgreSQL
    ↓
Structured Application Data

ChromaDB
    ↓
Semantic Resume Chunks
```

This separation allows each database to perform the task it is best suited for.

### PostgreSQL

Used for:

- Users
- Resumes
- Jobs
- Application records
- Persistent structured information

### ChromaDB

Used for:

- Resume chunks
- Embeddings
- Semantic retrieval
- RAG context

---

## 🔐 User Isolation

The backend uses a session-based user identification mechanism.

The frontend sends:

```
X-Session-ID
```

with API requests.

The backend uses this session to identify the current user and associate resumes and jobs with that user.

This allows the application to support multiple user sessions without mixing their stored data.

---

## ⚙️ Backend Architecture

FastAPI acts as the backend API layer.

The architecture is divided into layers rather than placing all logic inside the routes.

```
Streamlit
    ↓
FastAPI Routes
    ↓
Services
    ↓
Application / Analysis Logic
    ↓
Databases / LLM / RAG
```

This separation makes the application easier to maintain and extend.

Major backend responsibilities include:

- Resume upload
- Job processing
- Resume listing
- Job listing
- Resume analysis
- ATS analysis
- Tailored resume generation
- Career Coach
- Cover Letter generation
- PDF generation
- History

---

## 🖥️ Streamlit Frontend

Streamlit acts as the user-facing application.

The frontend provides functionality for:

### Resume

- Upload resume
- View saved resumes
- Select resume

### Job Description

- Add job description as text
- Upload job description PDF
- View saved jobs
- Select job

### Analysis

- Run Resume Genie analysis
- View analysis results
- View ATS results
- Generate tailored resume

### Career Coach

- Ask questions
- Retrieve resume-specific context
- Display grounded answers

### Cover Letter

- Generate job-specific cover letter
- Display structured sections

---

## 🔌 Frontend–Backend Communication

The Streamlit frontend communicates with FastAPI through an API client layer.

```
Streamlit UI
     ↓
api_client.py
     ↓
HTTP Request
     ↓
FastAPI
     ↓
Backend Service
     ↓
Result
     ↓
Streamlit UI
```

This keeps the frontend separate from the backend implementation.

---

## 🛠️ Technology Stack

| Category | Technology |
| -------- | ---------- |
| Frontend | Streamlit |
| Backend | FastAPI |
| Programming Language | Python |
| LLM | Google Gemini |
| LLM Framework | LangChain |
| Structured Output | Pydantic |
| PDF Processing | PyPDFLoader |
| Text Splitting | Recursive Character Text Splitter |
| Embeddings | BAAI/bge-small-en-v1.5 |
| Vector Database | ChromaDB |
| Relational Database | PostgreSQL |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| API Communication | Requests |
| Environment Management | python-dotenv |
| Version Control | Git / GitHub |

---

## ✅ Problems We Solved

Building Resume Genie involved several practical problems that occur in real GenAI applications.

### 1. Unreliable PDF Text Extraction

Resume PDFs did not always produce clean text.

Examples of extraction problems included words getting joined together, such as:

```
recordsusing
riskby
forecasted28-day
```

#### Solution

A dedicated processing pipeline was created:

```
PDF
 ↓
Load
 ↓
Clean
 ↓
Extract
 ↓
Split
```

This separated document ingestion from downstream AI processing.

---

### 2. Unstructured LLM Responses

Initially, relying on free-form LLM responses created problems when application code expected specific fields.

#### Solution

Pydantic structured schemas were introduced.

```
LLM
 ↓
Structured Output
 ↓
Pydantic Model
```

This made the data predictable and easier to validate.

---

### 3. Pydantic Validation Errors

During resume extraction, incorrect data types could be returned.

For example, a field expected a string but received an integer.

#### Solution

The schemas and structured-output pipeline were debugged so that extracted resume information conforms to the expected data structures.

---

### 4. Structured Output Return-Type Confusion

There were cases where the code expected a Pydantic object but received a list or another response representation.

This resulted in errors such as:

```
AttributeError:
'list' object has no attribute 'model_dump'
```

#### Solution

The actual return type of structured generation was traced and the downstream code was aligned with the returned object structure.

---

### 5. RAG Retrieval Without User Isolation

A vector database becomes problematic if retrieved information is not associated with the correct user and resume.

#### Solution

Metadata was added to ChromaDB chunks:

```
user_id
resume_id
source
page
page_label
```

Retrieval was then filtered using the selected user and resume.

---

### 6. Resume Chunk Identification

A simple chunk identifier is not enough when multiple users and resumes are stored.

#### Solution

Chunk IDs were designed around both user and resume:

```
user_{user_id}_resume_{resume_id}_chunk{i}
```

This gives each stored chunk a more meaningful identity.

---

### 7. Hallucination Risk

A Career Coach can potentially generate information that does not exist in the candidate's resume.

For a career application, this is a serious problem.

#### Solution

The Career Coach uses:

```
Retrieved Resume Context
+
Job Context
+
Analysis Context
```

and explicit grounding rules.

The model is instructed not to fabricate candidate information.

---

### 8. Raw Gemini Response Metadata

At one point, Gemini responses could contain content-block structures and metadata instead of clean text.

This created unwanted output in the Career Coach.

#### Solution

The response handling logic was updated to extract only the actual text content before displaying it.

---

### 9. Long / Unnecessary Career Coach Responses

The Career Coach initially had the possibility of producing overly long responses.

#### Solution

Response-style instructions were added:

```
Answer directly.
Focus on relevant information.
Prefer 3–5 concise bullet points.
Avoid unnecessary explanations.
Do not expose internal metadata.
```

---

### 10. Cover Letter Hallucination Risk

A generic LLM could easily create:

- Fake experience
- Fake achievements
- Fake metrics
- Fake certifications

#### Solution

A separate evidence-selection layer was introduced.

```
Resume
   +
Job Description
   ↓
Evidence Selection
   ↓
Grounded Prompt
   ↓
Gemini
```

The generator is explicitly instructed to use only the supplied evidence.

---

### 11. Separating Application Data from RAG Data

Not all information belongs in a vector database.

#### Solution

The project uses a hybrid persistence architecture:

```
PostgreSQL
   ↓
Structured application data

ChromaDB
   ↓
Semantic retrieval data
```

This gives the application both reliable structured storage and semantic search.

---

### 12. Frontend and Backend Separation

Putting all processing directly inside Streamlit would make the application harder to maintain and deploy.

#### Solution

The project separates:

```
Streamlit
   ↓
FastAPI
   ↓
Services
   ↓
Application Logic
```

This also makes it easier to expose the same backend to other clients in the future.

---

## 📊 Project Outcomes

By the end of the implemented Streamlit phase, Resume Genie provides an integrated workflow where a user can:

```
Upload Resume
      ↓
Process Resume
      ↓
Store Resume
      ↓
Add Job Description
      ↓
Store Job
      ↓
Select Resume + Job
      ↓
Run Analysis
      ↓
View ATS Analysis
      ↓
Generate Tailored Resume
      ↓
Ask Career Coach Questions
      ↓
Generate Grounded Cover Letter
      ↓
View Final Results in Streamlit
```

The project therefore evolved from a simple resume analyzer into a broader **AI-powered career suite**.

---

## 🎓 What This Project Demonstrates

Resume Genie demonstrates practical implementation of several modern GenAI concepts:

- LLM-based information extraction
- Structured LLM output
- Pydantic validation
- Prompt engineering
- RAG architecture
- Semantic search
- Vector databases
- Embeddings
- Metadata filtering
- Grounded generation
- Hallucination control
- Evidence-based generation
- Resume–JD matching
- ATS analysis
- LLM-powered career assistance
- API-based application architecture
- Database persistence
- Frontend/backend separation
- Session-based user isolation

---

## 📁 High-Level Project Structure

```
Resume-Genie/
│
├── app/
│   │
│   ├── analysis/
│   │   ├── career_coach.py
│   │   ├── career_coach_prompt.py
│   │   ├── cover_letter_evidence.py
│   │   ├── cover_letter_generator.py
│   │   ├── cover_letter_prompt.py
│   │   └── cover_letter_service.py
│   │
│   ├── application/
│   │   ├── resume_input.py
│   │   ├── job_input.py
│   │   └── pipeline.py
│   │
│   ├── backend/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── schemas/
│   │   └── main.py
│   │
│   ├── database/
│   │   ├── models/
│   │   ├── repositories/
│   │   └── migrations/
│   │
│   ├── extraction/
│   │   ├── resume_extractor.py
│   │   └── job_extractor.py
│   │
│   ├── ingestion/
│   │   └── pdf_loader.py
│   │
│   ├── llm/
│   │   └── gemini.py
│   │
│   ├── processing/
│   │   ├── text_cleaner.py
│   │   ├── text_extractor.py
│   │   └── text_splitter.py
│   │
│   ├── rag/
│   │   └── context_builder.py
│   │
│   ├── retrieval/
│   │   └── chroma_retriever.py
│   │
│   ├── schemas/
│   │   ├── resume.py
│   │   ├── job_description.py
│   │   └── cover_letter.py
│   │
│   ├── vectorstore/
│   │   └── chroma_store.py
│   │
│   └── frontend/
│       ├── app.py
│       └── api_client.py
│
├── data/
│   ├── uploads/
│   └── chroma/
│
├── .env
├── requirements.txt
└── README.md
```

> The exact repository structure may evolve as additional modules are added.

---

## ▶️ Running the Project

### 1. Create and activate the virtual environment

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

---

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

---

### 3. Configure environment variables

Create a `.env` file and configure the required Gemini API key and database configuration.

Example:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Do not commit `.env` or API keys to GitHub.

---

## 🚀 Start the FastAPI Backend

From the project root:

```powershell
$env:PYTHONPATH="app"
python -m uvicorn backend.main:app --reload
```

The backend will start locally.

---

## 🖥️ Start the Streamlit Frontend

Open another terminal:

```powershell
$env:PYTHONPATH="app"
python -m streamlit run app/frontend/app.py
```

The Streamlit interface will then connect to the FastAPI backend.

---

## 🔗 Application Flow

Once both services are running:

```
Streamlit
    ↓
FastAPI
    ↓
Resume / Job Processing
    ↓
PostgreSQL + ChromaDB
    ↓
Analysis / ATS / Tailoring
    ↓
Career Coach / Cover Letter
    ↓
Streamlit Results
```

---

## 🧪 Current Project Status

### Completed

- [x] Resume PDF ingestion
- [x] Resume text extraction
- [x] Text cleaning
- [x] Text chunking
- [x] Structured resume extraction
- [x] Pydantic resume schema
- [x] Job description text processing
- [x] Job description PDF processing
- [x] Structured job extraction
- [x] PostgreSQL persistence
- [x] ChromaDB integration
- [x] BGE embeddings
- [x] Metadata-based retrieval
- [x] User/resume-aware retrieval
- [x] Resume–JD analysis
- [x] ATS analysis
- [x] Tailored resume generation
- [x] RAG-powered Career Coach
- [x] Grounded Career Coach responses
- [x] Evidence-based cover letter generation
- [x] FastAPI backend
- [x] Streamlit frontend
- [x] Frontend–backend integration

---

## 🔮 Future Improvements

The current implementation provides the core application. Future development can extend it with:

```
Evaluation
   ↓
RAG Evaluation / RAGAS
   ↓
End-to-End Testing
   ↓
Docker
   ↓
Cloud Deployment
   ↓
AWS
```

Additional improvements can include:

- Automated RAG evaluation
- Retrieval quality benchmarking
- Answer faithfulness evaluation
- Resume/JD matching evaluation
- Automated API testing
- Better PDF layout preservation
- Advanced document parsing
- Production-grade authentication
- Improved observability
- Cloud deployment
- Scalable vector/database infrastructure

---

## 📌 Key Takeaway

Resume Genie is not simply an LLM wrapper around a resume prompt.

It combines multiple components into a complete application:

```
Document Processing
       +
Structured LLM Extraction
       +
PostgreSQL
       +
Embeddings
       +
ChromaDB
       +
RAG
       +
Grounded Generation
       +
Resume–JD Analysis
       +
ATS
       +
Tailored Resume
       +
Cover Letter
       +
AI Career Coach
       +
FastAPI
       +
Streamlit
```

The project demonstrates how GenAI components can be combined with traditional software engineering, databases, APIs, and frontend development to build a practical end-to-end AI application.
