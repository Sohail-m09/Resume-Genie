from pathlib import Path
from ingestion.pdf_loader import load_pdf
from processing.text_cleaner import clean_documents
from processing.text_splitter import split_documents
from extraction.resume_extractor import extract_resume 
from processing.text_extractor import extract_text
from schemas.resume import Resume
from validation.resume_validator import validate_resume_extraction
from langchain_core.documents import Document
from extraction.job_extractor import extract_job_description
from schemas.job_description import JobDescription
from vectorstore.chroma_store import store_resume_chunks
from rag.context_builder import build_resume_context
from retrieval.chroma_retriever import retrieve_resume_context
from rag.prompt_builder import build_resume_prompt
from rag.generator import generate_resume_answer
from llm.gemini import get_gemini_model
from rag.resume_rag import ask_resume
from analysis.resume_analyzer import analyze_resume
from analysis.skill_gap_analyzer import detect_skill_gaps, explain_skill_gaps
from analysis.semantic_evidence import find_semantic_skill_evidence
from services.keyword_optimizer import find_keyword_gaps
from analysis.project_strengthener import strengthen_projects
from analysis.final_analysis import build_final_analysis
from analysis.cover_letter_service import create_cover_letter
from analysis.career_coach import answer_resume_question
from analysis.career_coach import answer_job_question
from resume_generator.tailoring import generate_tailoring_plan, generate_tailored_resume
from analysis.improvement_recommendations import (
    generate_improvement_recommendations,
)
from analysis.cover_letter_evidence import (
    select_cover_letter_evidence,
)
from analysis.cover_letter_prompt import (
    build_cover_letter_prompt,
)
from analysis.cover_letter_generator import (
    generate_cover_letter,
)
from analysis.career_coach_prompt import (
    build_career_coach_prompt,
)
from analysis.career_coach import (
    answer_with_resume_rag,
)
from analysis.career_coach_service import (
    ask_career_coach,
)
from resume_generator.prioritization import (
    prioritize_resume_content,
)
from resume_generator.tailoring import (
    generate_tailored_resume,
)
from resume_generator.validator import (
    validate_tailored_resume,
)
from resume_generator.latex_generator import (
    generate_latex,
)
from resume_generator.pdf_builder import (
    build_pdf,
)
from resume_generator.ats_validator import (
    calculate_ats_score,
)
from resume_generator.customization import (
    apply_resume_customization,
)
from application.job_input import (
    process_job_description_input,
)
from application.resume_input import (
    process_resume_input,
)
from application.pipeline import (
    prepare_application,
    analyze_application,
)
from application.pipeline import run_resume_genie

def process_resume(file_path: str) -> tuple[Resume  ,list[Document]]:
    """
    Complete resume document-processing pipeline.

    Args:
        file_path: Path to the resume PDF.

    Returns:
        Processed resume chunks.
    """
    documents = load_pdf(file_path)
    cleaned_documents = clean_documents(documents)
    resume_text = extract_text(cleaned_documents)
    resume = extract_resume(resume_text)
    chunks = split_documents(cleaned_documents)

    return resume, chunks


def process_job_description(file_path: str) -> JobDescription:
    documents = load_pdf(file_path)
    cleaned_documents = clean_documents(documents)

    job_text = extract_text(cleaned_documents)

    job_description = extract_job_description(job_text)

    return job_description


if __name__ == "__main__":
    resume_path = Path(r"D:\Resume-Genie\data\Sohail_Momin.pdf")
    job_path = Path(r"D:\Resume-Genie\data\Data_Scientist_JD.pdf")

    ## Resume processing
    resume, chunks = process_resume(str(resume_path))

    ## Job description processing
    job_description = process_job_description(str(job_path))

    ## Store resume chunks in chromaDB
    stored_count = store_resume_chunks(
        chunks
    )

    validate_resume_extraction(resume)

    '''print("===== STRUCTURED RESUME =====")
    print(resume.model_dump())

    print("\n===== STRUCTURED JOB DESCRIPTION =====")
    print(job_description.model_dump())

    ## Vector Store Information.
    print("\n===== VECTOR STORE =====")
    print(f"Chunks stored in ChromaDB: {stored_count}")'''

    '''query = "Have I used python and it's libraries in the project?"

    ## Retrieve relevant resume chunks from ChromaDB
    retrieved_chunks = retrieve_resume_context(query)
    
    print("\n===== RETRIEVED CHUNKS =====")
    for i, chunk in enumerate(retrieved_chunks, start=1):
        print(f"\n--- Retrieved Chunk {i} ---")
        print("Text:", chunk["text"])
        print("Metadata:", chunk["metadata"])
        print("Distance:", chunk["distance"])
    
    ## Convert retrieved chunks into LLM-ready context
    resume_context = build_resume_context(retrieved_chunks)
    
    print("\n===== RESUME CONTEXT =====")
    print(resume_context)'''

    ## Prompt Grounding
    '''model = get_gemini_model()
    grounded_prompt = build_resume_prompt(
    context=resume_context,
    question=query,
    )

    print("\n===== GROUNDED PROMPT =====")
    print(grounded_prompt)

    answer = generate_resume_answer(
    model = model,
    prompt=grounded_prompt,
    )

    print("\n===== RAG ANSWER =====")
    print(answer)'''

    '''query = "How many years of AWS experience do I have?"

    answer = ask_resume(query)

    print("\n===== RAG ANSWER =====")
    print(answer) ## We can use this also in the place of that big code.

    ## Structured resume output
    resume_analysis = analyze_resume(resume)

    print("\n===== RESUME ANALYSIS =====")
    print(resume_analysis.model_dump())'''

    '''## Showing skill gaps
    skill_gaps = detect_skill_gaps(
    resume=resume,
    job_description=job_description,
    )

    print("\n===== SKILL GAPS =====")
    print(skill_gaps)

    ## Explaining the skill gaps
    skill_gap_analysis = explain_skill_gaps(
    resume=resume,
    job_description=job_description,
    )

    print("\n===== SKILL GAP ANALYSIS =====")
    print(skill_gap_analysis.model_dump())


    ## Imporovement Recommendation
    improvement_recommendations = (
    generate_improvement_recommendations(
        skill_gaps
    )
    )
    print("\n===== IMPROVEMENT RECOMMENDATIONS =====")
    print(
    improvement_recommendations.model_dump()
    )

    ## Skills matching with semantic meaning
    semantic_evidence = find_semantic_skill_evidence(
    resume=resume,
    job_description=job_description,
    )

    print("\n===== SEMANTIC EVIDENCE =====")
    print(semantic_evidence)

    keyword_gaps = find_keyword_gaps(
    resume,
    job_description,
    )

    print("\n===== KEYWORD GAPS =====")
    print(keyword_gaps)'''

    '''## Strengtning the Project
    project_strengthening = strengthen_projects(
    resume=resume,
    job_description=job_description,
    )

    print("\n===== PROJECT STRENGTHENING =====")
    print(project_strengthening.model_dump())'''

    '''final_analysis = build_final_analysis(
    resume=resume,
    job_description=job_description,
    )

    print("\n===== FINAL RESUME ANALYSIS =====")
    print(final_analysis.model_dump())'''


    '''## Cover Letter Evidence
    cover_letter_evidence = select_cover_letter_evidence(
    resume=resume,
    job_description=job_description,
    )

    print("\n===== COVER LETTER EVIDENCE =====")
    print(cover_letter_evidence.model_dump())

    ## Cover Letter Prompt
    cover_letter_prompt = build_cover_letter_prompt(
    evidence=cover_letter_evidence,
    job_description=job_description,
    )

    print("\n===== COVER LETTER PROMPT =====")
    print(cover_letter_prompt)

    ## Cover letter generation
    cover_letter = generate_cover_letter(
    prompt=cover_letter_prompt,
    )

    print("\n===== GENERATED COVER LETTER =====")
    print(cover_letter.model_dump())'''

    '''## Cover letter generation for all resumes 
    cover_letter = create_cover_letter(
    resume=resume,
    job_description=job_description,
    )

    print("\n===== COVER LETTER =====")
    print(cover_letter.model_dump())'''

    '''## CHecking the CAREER COACH Prompt
    question = "Why is my match score low?"

    coach_prompt = build_career_coach_prompt(
    question=question,
    resume_context=resume_context,
    job_context=job_description.model_dump_json(indent=2),
    analysis_context=final_analysis.model_dump_json(indent=2),
    )

    print("\n===== CAREER COACH PROMPT =====")
    print(coach_prompt)'''

    '''## Going with the structured resume format
    print("\n***** Resume Skills *****")
    print(resume.skills)

    print("\n***** Resume Education *****")
    print(resume.education)

    print("\n***** RESUME PROJECTS *****")
    for project in resume.projects:
        print(project)

    print("\n***** RESUME CERTIFICATIONS *****")
    print(resume.certifications)

    print("\n***** CHUNK INFORMATION *****")
    print(f"Number of chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks, start=1):
        print(f"\n===== CHUNK {i} =====")
        print(chunk.page_content)
        print("Metadata:", chunk.metadata)'''

    '''question = "What Python libraries have I used?"

    answer = answer_resume_question(
    question=question,
    resume_context=resume_context,
    )

    print("\n===== CAREER COACH ANSWER =====")
    print(answer)'''

    '''question = "What are the main required skills for this job?"

    job_context = job_description.model_dump_json(
        indent=2
    )

    answer = answer_job_question(
        question=question,
        job_context=job_context,
    )

    print("\n===== JOB-AWARE CAREER COACH =====")
    print(answer)'''

    # ==================================================
    # PHASE 9.5 — RAG-POWERED CAREER COACH
    # ==================================================

    '''question = (
    "Based on my resume, what area should I improve "
    "to become a stronger candidate for machine learning roles?"
    )

    answer = answer_with_resume_rag(
        question=question,
    )

    print("\n===== RAG-POWERED CAREER COACH =====")
    print(answer)'''

    # ==================================================
    # PHASE 9.6 — COMPLETE AI CAREER COACH
    # ==================================================

    question = "How can I become the most preferred candidate for this role?"

    analysis_context = """
    Overall score: 25.64

    Matched required skills:
    Python
    SQL

    Missing required skills:
    - automated machine learning (AutoML) frameworks
    - hyperparameter tuning
    - machine learning model packaging and deployment
    - model evaluation techniques

    Matched preferred skills:
    None

    Missing preferred skills:
    - cybersecurity data analytics
    - data versioning
    - financial risk modeling
    - MLOps

    Semantic evidence:
    model evaluation techniques → Model Evaluation → 0.9305
    """

    '''answer = ask_career_coach(
        question=question,
        resume=resume,
        job_description=job_description,
        analysis_context=analysis_context,
    )

    print("\n===== COMPLETE CAREER COACH =====")
    print(answer)'''

    '''# ==================================================
    # PHASE 10.2 — TAILORING PLAN
    # ==================================================

    tailoring_plan = generate_tailoring_plan(
        resume=resume,
        job_description=job_description,
        analysis_context=analysis_context,
    )

    print("\n===== RESUME TAILORING PLAN =====")
    print(tailoring_plan.model_dump())

    prioritized_resume = prioritize_resume_content(
        resume=resume,
        tailoring_plan=tailoring_plan,
    )

    tailored_resume = generate_tailored_resume(
    resume=resume,
    job_description=job_description,
    tailoring_plan=tailoring_plan,
    )

    print("\n===== TAILORED STRUCTURED RESUME =====")
    print(tailored_resume.model_dump())

    validation_result = validate_tailored_resume(
    original_resume=resume,
    tailored_resume=tailored_resume,
    )

    print("\n===== TAILORED RESUME VALIDATION =====")
    print(validation_result)

    # ==================================================
    # PHASE 10.8 — ATS VALIDATION
    # ==================================================

    ats_result = calculate_ats_score(
        original_resume=resume,
        tailored_resume=tailored_resume,
        job_description=job_description,
    )

    print("\n===== ATS RESUME SCORE =====")
    print(ats_result)'''

    '''# ==================================================
    # PHASE 10.5 — LATEX GENERATION
    # ==================================================

    if validation_result["valid"]:

        latex_source = generate_latex(
            tailored_resume=tailored_resume,
            original_resume=resume,
        )

        print("\n===== LATEX SOURCE =====")
        print(latex_source)

    else:

        print(
            "\nLaTeX generation skipped because "
            "tailored resume validation failed."
        )

    # ==================================================
    # PHASE 10.7 — PDF COMPILATION
    # ==================================================

    if validation_result["valid"]:

        pdf_path = build_pdf(
            latex_source=latex_source,
        )

        print("\n===== PDF CREATED =====")
        print(pdf_path)

    else:

        print(
            "\nPDF generation skipped because "
            "tailored resume validation failed."
        )'''

    '''# ==================================================
    # PHASE 10.3 — RESUME PRIORITIZATION
    # ==================================================

    prioritized_resume = prioritize_resume_content(
        resume=resume,
        tailoring_plan=tailoring_plan,
    )

    print("\n===== RESUME PRIORITIZATION =====")

    print(
        "Prioritized Skills:",
        prioritized_resume["prioritized_skills"],
    )

    print(
        "Deprioritized Skills:",
        prioritized_resume["deprioritized_skills"],
    )

    print("\nPrioritized Projects:")

    for item in prioritized_resume["prioritized_projects"]:

        project = item["project"]

        print(
            f"Priority: {item['priority']} | "
            f"Project: {project.name}"
        )

        print(
            f"Reason: {item['reason']}"
        )

    print(
        "\nUnsupported Requirements:",
        prioritized_resume["unsupported_requirements"],
    )

    # ==================================================
    # PHASE 10.9.3 — PROJECT REMOVAL INTEGRATION TEST
    # ==================================================

    customized_plan = apply_resume_customization(
        tailoring_plan=tailoring_plan,
        removed_projects=[
            "Bank Loan Prediction"
        ],
    )

    print("\n===== CUSTOMIZED TAILORING PLAN =====")
    print(
        customized_plan.model_dump()
    )'''


    '''customized_tailored_resume = generate_tailored_resume(
        resume=resume,
        job_description=job_description,
        tailoring_plan=customized_plan,
    )

    print("\n===== CUSTOMIZED TAILORED RESUME =====")
    print(
        customized_tailored_resume.model_dump()
    )

    customized_validation = validate_tailored_resume(
        original_resume=resume,
        tailored_resume=customized_tailored_resume,
    )

    print("\n===== CUSTOMIZED RESUME VALIDATION =====")
    print(customized_validation)'''


    '''customized_plan = apply_resume_customization(
        tailoring_plan=customized_plan,
        section_order=[
            "summary",
            "education",
            "skills",
            "projects",
            "certifications",
        ],
    )

    customized_tailored_resume = generate_tailored_resume(
        resume=resume,
        job_description=job_description,
        tailoring_plan=customized_plan,
    )

    print("\n===== REORDERED TAILORED RESUME =====")
    print(
        customized_tailored_resume.model_dump()
    )

    customized_validation = validate_tailored_resume(
        original_resume=resume,
        tailored_resume=customized_tailored_resume,
    )

    print("\n===== REORDERED RESUME VALIDATION =====")
    print(customized_validation)'''

    '''# ==================================================
    # PHASE 10.9.4 — FULL CUSTOMIZED END-TO-END TEST
    # ==================================================

    customized_tailored_resume = generate_tailored_resume(
        resume=resume,
        job_description=job_description,
        tailoring_plan=customized_plan,
    )

    print("\n===== FINAL CUSTOMIZED RESUME =====")
    print(
        customized_tailored_resume.model_dump()
    )


    customized_validation = validate_tailored_resume(
        original_resume=resume,
        tailored_resume=customized_tailored_resume,
    )

    print("\n===== FINAL CUSTOMIZED VALIDATION =====")
    print(customized_validation)


    if customized_validation["valid"]:

        customized_latex = generate_latex(
            tailored_resume=customized_tailored_resume,
            original_resume=resume,
        )

        print("\n===== FINAL CUSTOMIZED LATEX =====")
        print(customized_latex)


        customized_pdf_path = build_pdf(
            latex_source=customized_latex,
            filename="customized_tailored_resume",
        )

        print("\n===== FINAL CUSTOMIZED PDF =====")
        print(customized_pdf_path)


        customized_ats = calculate_ats_score(
            original_resume=resume,
            tailored_resume=customized_tailored_resume,
            job_description=job_description,
        )

        print("\n===== FINAL CUSTOMIZED ATS SCORE =====")
        print(customized_ats)

    else:

        print(
            "\nFinal PDF and ATS generation skipped "
            "because validation failed."
        )'''

    '''# ==================================================
    # PHASE 10.10.1 — PASTED JD INPUT TEST
    # ==================================================

    pasted_jd = """
    Junior Data Scientist / Machine Learning Analyst

    Required Skills:
    Python
    SQL
    Model Evaluation
    Hyperparameter Tuning
    Automated Machine Learning frameworks

    Preferred Skills:
    MLOps
    Data Versioning
    Financial Risk Modeling
    Cybersecurity Data Analytics

    Qualifications:
    Bachelor's degree in Computer Science, Engineering,
    Mathematics, or a related analytical field.

    Responsibilities:
    Design, train, and deploy machine learning models.
    Perform exploratory data analysis and feature engineering.
    Build data pipelines and dashboards.
    """

    job_description_from_text = process_job_description_input(
        job_text=pasted_jd,
    )

    print(
        "\n===== PASTED JD STRUCTURED OUTPUT ====="
    )

    print(
        job_description_from_text.model_dump()
    )

    from application.job_input import (
        process_job_description_input,
    )

    job_description_from_pdf = process_job_description_input(
        pdf_path=str(job_path),
    )

    print(
        "\n===== PDF JD STRUCTURED OUTPUT ====="
    )

    print(
        job_description_from_pdf.model_dump()
    )'''

    '''# ==================================================
    # PHASE 10.10.2a — RESUME INPUT TEST
    # ==================================================

    resume_from_input, chunks_from_input = (
        process_resume_input(
            str(resume_path)
        )
    )

    print("\n===== RESUME INPUT TEST =====")
    print(
        resume_from_input.model_dump()
    )

    print(
        "\nNumber of chunks:",
        len(chunks_from_input),
    )'''

    '''# ==================================================
    # PHASE 10.10.2b — APPLICATION INPUT PIPELINE
    # ==================================================

    resume_result, job_result = prepare_application_inputs(
        resume_path=str(resume_path),

        job_text="""
        Junior Data Scientist / Machine Learning Analyst

        Required Skills:
        Python
        SQL
        Model Evaluation
        Hyperparameter Tuning

        Preferred Skills:
        MLOps
        Data Versioning

        Responsibilities:
        Design, train, and deploy machine learning models.
        Perform exploratory data analysis and feature engineering.
        """,
    )

    print("\n===== APPLICATION INPUT PIPELINE =====")

    print("\n===== RESUME =====")
    print(
        resume_result.model_dump()
    )

    print("\n===== JOB DESCRIPTION =====")
    print(
        job_result.model_dump()
    )'''

    '''application_inputs = prepare_application(
        resume_path=str(resume_path),

        job_text="""
        Junior Data Scientist / Machine Learning Analyst

        Required Skills:
        Python
        SQL
        Model Evaluation
        Hyperparameter Tuning

        Preferred Skills:
        MLOps
        Data Versioning

        Responsibilities:
        Design, train, and deploy machine learning models.
        Perform exploratory data analysis and feature engineering.
        """,
    )

    print("\n===== APPLICATION INPUTS =====")
    print(
        application_inputs.model_dump()
    )

    # ==================================================
    # PHASE 10.10.3 — ANALYSIS ORCHESTRATION
    # ==================================================

    analysis_result = analyze_application(
        resume=application_inputs.resume,
        job_description=application_inputs.job_description,
    )

    print("\n===== APPLICATION ANALYSIS =====")
    print(
        analysis_result.model_dump()
    )'''

    result = run_resume_genie(
        resume_path=str(resume_path),

        job_text="""
        Junior Data Scientist / Machine Learning Analyst

        Required Skills:
        Python
        SQL
        Model Evaluation
        Hyperparameter Tuning

        Preferred Skills:
        MLOps
        Data Versioning

        Responsibilities:
        Design, train, and deploy machine learning models.
        Perform exploratory data analysis and feature engineering.
        """,

        section_order=[
            "summary",
            "education",
            "skills",
            "projects",
            "certifications",
        ],

        removed_projects=[
            "Bank Loan Prediction",
        ],
    )

    print("\n===== RESUME GENIE RESULT =====")

    print("\nAnalysis:")
    print(
        result["analysis"].model_dump()
    )

    print("\nValidation:")
    print(
        result["validation"]
    )

    print("\nATS:")
    print(
        result["ats"]
    )

    print("\nPDF:")
    print(
        result["pdf"]
    )