'''from pathlib import Path
import requests
import streamlit as st
from session import get_session_id
from frontend.api_client import (
    upload_resume,
    process_job_text,
    upload_job_pdf,
    get_resumes,
    get_jobs,
    run_resume_genie,
    ask_career_coach,
    generate_cover_letter,
)


st.set_page_config(
    page_title="Resume Genie",
    page_icon="📄",
    layout="wide",
)


# =========================================================
# SESSION
# =========================================================

session_id = get_session_id()


# =========================================================
# STREAMLIT SESSION STATE
# =========================================================

if "resume_result" not in st.session_state:
    st.session_state["resume_result"] = None

if "job_result" not in st.session_state:
    st.session_state["job_result"] = None

if "resume_genie_result" not in st.session_state:
    st.session_state["resume_genie_result"] = None

if "resume_history" not in st.session_state:
    st.session_state["resume_history"] = []

if "job_history" not in st.session_state:
    st.session_state["job_history"] = []

if "history_loaded" not in st.session_state:
    st.session_state["history_loaded"] = False

if "career_coach_messages" not in st.session_state:
    st.session_state["career_coach_messages"] = []

if "cover_letter_result" not in st.session_state:
    st.session_state["cover_letter_result"] = None


st.title("Resume Genie")
st.subheader("AI-Powered Resume & Career Suite")

st.write(
    "Analyze your resume, match it against job descriptions, "
    "generate tailored resumes, check ATS compatibility, "
    "and get AI-powered career guidance."
)

st.caption(
    f"Session: {session_id}"
)

st.divider()


# =========================================================
# RESUME
# =========================================================

st.header("📄 Resume")

uploaded_resume = st.file_uploader(
    "Upload your resume in PDF format",
    type=["pdf"],
    key="resume_upload",
)


if uploaded_resume is not None:

    st.write(
        f"**Selected file:** {uploaded_resume.name}"
    )

    if st.button(
        "Process Resume",
        key="process_resume",
    ):

        with st.spinner(
            "Processing your resume..."
        ):

            try:

                result = upload_resume(
                    file_bytes=uploaded_resume.getvalue(),
                    filename=uploaded_resume.name,
                    session_id=session_id,
                )

                # Store the API response
                # in Streamlit session state.
                st.session_state["resume_result"] = result

                # Refresh saved history because a new resume was created.
                st.session_state["history_loaded"] = False

                st.success(
                    "Resume processed successfully."
                )   

            except requests.exceptions.RequestException as e:

                st.error(
                    f"Backend request failed: {e}"
                )

            except Exception as e:

                st.error(
                    f"Something went wrong: {e}"
                )


# =========================================================
# DISPLAY RESUME RESULT
# =========================================================

resume_result = st.session_state["resume_result"]


if resume_result is not None:

    st.success(
        "Resume is ready."
    )

    st.write(
        f"**Resume ID:** "
        f"{resume_result.get('resume_id')}"
    )

    st.write(
        f"**Chunk Count:** "
        f"{resume_result.get('chunk_count')}"
    )

    with st.expander(
        "View Structured Resume"
    ):

        st.json(
            resume_result.get("resume")
        )


st.divider()


# =========================================================
# JOB DESCRIPTION
# =========================================================

st.header("💼 Job Description")

job_input_method = st.radio(
    "How would you like to provide the job description?",
    options=[
        "Paste Text",
        "Upload PDF",
    ],
    horizontal=True,
)


# =========================================================
# JD TEXT
# =========================================================

if job_input_method == "Paste Text":

    job_text = st.text_area(
        "Paste the Job Description here",
        height=300,
        placeholder=(
            "Paste the complete job description here..."
        ),
        key="job_text",
    )

    if st.button(
        "Process Job Description",
        key="process_job_text",
    ):

        if not job_text.strip():

            st.warning(
                "Please paste a job description first."
            )

        else:

            with st.spinner(
                "Processing job description..."
            ):

                try:

                    result = process_job_text(
                        job_text=job_text,
                        session_id=session_id,
                    )

                    # Store the API response
                    # in Streamlit session state.
                    st.session_state["job_result"] = result

                    # Refresh saved history because a new job was created.
                    st.session_state["history_loaded"] = False

                    st.success(
                        "Job description processed successfully."
                     )

                except requests.exceptions.RequestException as e:

                    st.error(
                        f"Backend request failed: {e}"
                    )

                except Exception as e:

                    st.error(
                        f"Something went wrong: {e}"
                    )


# =========================================================
# JD PDF
# =========================================================

else:

    uploaded_job = st.file_uploader(
        "Upload the Job Description PDF",
        type=["pdf"],
        key="job_upload",
    )

    if uploaded_job is not None:

        st.write(
            f"**Selected file:** {uploaded_job.name}"
        )

        if st.button(
            "Process Job Description PDF",
            key="process_job_pdf",
        ):

            with st.spinner(
                "Processing job description..."
            ):

                try:

                    result = upload_job_pdf(
                        file_bytes=uploaded_job.getvalue(),
                        filename=uploaded_job.name,
                        session_id=session_id,
                    )

                    # Store the API response
                    # in Streamlit session state.
                    st.session_state["job_result"] = result

                    # Refresh saved history because a new job was created.
                    st.session_state["history_loaded"] = False

                    st.success(
                        "Job description processed successfully."
                    )
                except requests.exceptions.RequestException as e:

                    st.error(
                        f"Backend request failed: {e}"
                    )

                except Exception as e:

                    st.error(
                        f"Something went wrong: {e}"
                    )


# =========================================================
# DISPLAY JOB RESULT
# =========================================================

job_result = st.session_state["job_result"]


if job_result is not None:

    st.success(
        "Job description is ready."
    )

    st.write(
        f"**Job ID:** "
        f"{job_result.get('job_id')}"
    )

    with st.expander(
        "View Structured Job Description"
    ):

        st.json(
            job_result.get(
                "job_description"
            )
        )


st.divider()


# =========================================================
# ANALYSIS PREPARATION
# =========================================================

st.header("🎯 Resume–Job Analysis")


# =========================================================
# RESUME & JOB HISTORY
# =========================================================

st.subheader("📚 Your Saved Work")


# =========================================================
# LOAD SAVED HISTORY
# =========================================================

if not st.session_state["history_loaded"]:

    try:

        resume_history_result = get_resumes(
            session_id=session_id,
        )

        job_history_result = get_jobs(
            session_id=session_id,
        )

        st.session_state["resume_history"] = (
            resume_history_result.get(
                "resumes",
                [],
            )
        )

        st.session_state["job_history"] = (
            job_history_result.get(
                "jobs",
                [],
            )
        )

        st.session_state["history_loaded"] = True

    except requests.exceptions.RequestException:

        st.session_state["resume_history"] = []
        st.session_state["job_history"] = []
        st.session_state["history_loaded"] = True

    except Exception:

        st.session_state["resume_history"] = []
        st.session_state["job_history"] = []
        st.session_state["history_loaded"] = True


# =========================================================
# GET HISTORY FROM SESSION STATE
# =========================================================

resume_history = st.session_state.get(
    "resume_history",
    [],
)

job_history = st.session_state.get(
    "job_history",
    [],
)


# =========================================================
# DISPLAY SAVED RESUMES
# =========================================================

if resume_history:

    st.markdown("#### 📄 Saved Resumes")

    for resume in resume_history:

        st.write(
            f"**{resume.get('filename', 'Unknown Resume')}** "
            f"— Resume ID: `{resume.get('resume_id')}`"
        )

else:

    st.info(
        "No saved resumes yet."
    )


# =========================================================
# DISPLAY SAVED JOB DESCRIPTIONS
# =========================================================

if job_history:

    st.markdown("#### 💼 Saved Job Descriptions")

    for job in job_history:

        st.write(
            f"**{job.get('job_title') or 'Unknown Job'}** "
            f"- {job.get('company') or 'Unknown Company'} "
            f"— Job ID: `{job.get('job_id')}`"
        )

else:

    st.info(
        "No saved job descriptions yet."
    )


st.divider()


# =========================================================
# DETERMINE RESUME AND JOB IDs
# =========================================================

resume_id = None
job_id = None
selected_resume_id = None
selected_job_id = None

# ---------------------------------------------------------
# SAVED HISTORY AVAILABLE
# ---------------------------------------------------------

if len(resume_history) > 0 and len(job_history) > 0:

    st.subheader("📚 Select Resume & Job")

    resume_options = {
        (
            f"{resume.get('filename', 'Unknown Resume')} "
            f"(ID: {resume.get('resume_id')})"
        ): resume.get("resume_id")
        for resume in resume_history
    }

    job_options = {
        (
            f"{job.get('job_title') or 'Unknown Job'} "
            f"- {job.get('company') or 'Unknown Company'} "
            f"(ID: {job.get('job_id')})"
        ): job.get("job_id")
        for job in job_history
    }

    selected_resume_label = st.selectbox(
        "Select Resume",
        options=list(resume_options.keys()),
        key="selected_resume",
    )

    selected_job_label = st.selectbox(
        "Select Job Description",
        options=list(job_options.keys()),
        key="selected_job",
    )

    resume_id = resume_options[
        selected_resume_label
    ]

    job_id = job_options[
        selected_job_label
    ]

    selection_key = f"{resume_id}:{job_id}"

    if st.session_state.get(
        "career_coach_selection"
    ) != selection_key:

        st.session_state["career_coach_messages"] = []

        st.session_state[
        "cover_letter_result"
        ] = None

        st.session_state[
            "career_coach_selection"
        ] = selection_key

    st.success(
        f"Selected Resume ID: {resume_id} | "
        f"Selected Job ID: {job_id}"
    )


# ---------------------------------------------------------
# CURRENTLY PROCESSED RESUME + JOB
# ---------------------------------------------------------

elif resume_result is not None and job_result is not None:

    resume_id = resume_result.get(
        "resume_id"
    )

    job_id = job_result.get(
        "job_id"
    )

    st.subheader("✅ Current Resume & Job")

    st.info(
        "Using the Resume and Job Description you just processed."
    )

    st.write(
        f"Resume ID: `{resume_id}`"
    )

    st.write(
        f"Job ID: `{job_id}`"
    )


# ---------------------------------------------------------
# WAITING FOR RESUME / JOB
# ---------------------------------------------------------

else:

    if resume_result is None and job_result is None:

        st.info(
            "Process a resume and a job description to continue."
        )

    elif resume_result is None:

        st.info(
            "Resume is missing. Process your resume first."
        )

    else:

        st.info(
            "Job description is missing. Process a JD first."
        )


# =========================================================
# ANALYZE RESUME AGAINST JOB
# =========================================================

if resume_id is not None and job_id is not None:

    st.divider()

    st.subheader("🚀 Run Analysis")

    st.write(
        "Resume Genie will compare your resume against "
        "the selected job description and generate "
        "matching insights, recommendations, ATS analysis, "
        "and a tailored resume."
    )

    if st.button(
        "🔍 Analyze Resume Against Job",
        key="analyze_resume",
        type="primary",
    ):

        with st.spinner(
            "Running Resume Genie analysis..."
        ):

            try:

                result = run_resume_genie(
                    resume_id=resume_id,
                    job_id=job_id,
                    session_id=session_id,
                )

                st.session_state[
                    "resume_genie_result"
                ] = result

                st.success(
                    "Resume Genie analysis completed successfully."
                )

            except requests.exceptions.RequestException as e:

                st.error(
                    f"Backend request failed: {e}"
                )

            except Exception as e:

                st.error(
                    f"Something went wrong: {e}"
                )

# =========================================================
# DISPLAY RESUME GENIE RESULT
# =========================================================

resume_genie_result = st.session_state[
    "resume_genie_result"
]


if resume_genie_result is not None:

    st.divider()

    st.header("📊 Resume Genie Analysis")

    st.caption(
        "Your resume has been analyzed against the selected job description."
    )

    # -----------------------------------------------------
    # EXTRACT RESULTS
    # -----------------------------------------------------

    analysis = resume_genie_result.get(
        "analysis"
    )

    tailored_resume = resume_genie_result.get(
        "tailored_resume"
    )

    validation = resume_genie_result.get(
        "validation"
    )

    ats = resume_genie_result.get(
        "ats"
    )

    # -----------------------------------------------------
    # KEY SCORES
    # -----------------------------------------------------

    overall_score = None
    ats_score = None

    if isinstance(analysis, dict):

        overall_score = analysis.get(
            "overall_score"
        )

    if isinstance(ats, dict):

        ats_score = ats.get(
            "ats_score"
        )

    # -----------------------------------------------------
    # KEY SCORE DISPLAY
    # -----------------------------------------------------

    score_col1, score_col2 = st.columns(2)

    with score_col1:

        if overall_score is not None:

            st.metric(
                "🎯 Overall Match Score",
                f"{overall_score:.2f}",
            )

        else:

            st.metric(
                "🎯 Overall Match Score",
                "N/A",
            )

    with score_col2:

        if ats_score is not None:

            st.metric(
                "📋 ATS Score",
                f"{ats_score:.2f}",
            )

        else:

            st.metric(
                "📋 ATS Score",
                "N/A",
            )

    # -----------------------------------------------------
    # APPLICATION INFORMATION
    # -----------------------------------------------------

    st.markdown(
        "### 📌 Application Information"
    )

    info_col1, info_col2, info_col3 = st.columns(3)

    with info_col1:

        st.metric(
            "Application ID",
            resume_genie_result.get(
                "application_id",
                "N/A",
            ),
        )

    with info_col2:

        st.metric(
            "Resume ID",
            resume_genie_result.get(
                "resume_id",
                "N/A",
            ),
        )

    with info_col3:

        st.metric(
            "Job ID",
            resume_genie_result.get(
                "job_id",
                "N/A",
            ),
        )

    # -----------------------------------------------------
    # EXTRACT RESULTS
    # -----------------------------------------------------

    analysis = resume_genie_result.get(
        "analysis"
    )

    tailored_resume = resume_genie_result.get(
        "tailored_resume"
    )

    validation = resume_genie_result.get(
        "validation"
    )

    ats = resume_genie_result.get(
        "ats"
    )

    # -----------------------------------------------------
    # ANALYSIS SUMMARY
    # -----------------------------------------------------

    st.subheader("🎯 Match Analysis")

    if isinstance(analysis, dict):

        # -------------------------------------------------
        # SCORE BREAKDOWN
        # -------------------------------------------------

        score_components = analysis.get(
            "score_components"
        )

        if isinstance(score_components, dict) and score_components:

            st.markdown(
                "### 📊 Score Breakdown"
            )

            component_columns = st.columns(
                min(len(score_components), 4)
            )

            for column, (
                component_name,
                component_value,
            ) in zip(
                component_columns,
                score_components.items(),
            ):

                with column:

                    display_name = (
                        component_name
                        .replace("_", " ")
                        .title()
                    )

                    if isinstance(
                        component_value,
                        (int, float),
                    ):

                        st.metric(
                            display_name,
                            f"{component_value:.2f}",
                        )

                    else:

                        st.write(
                            f"**{display_name}**"
                        )

                        st.write(
                            component_value
                        )


        matched_required_skills = analysis.get(
            "matched_required_skills",
            [],
        )

        missing_required_skills = analysis.get(
            "missing_required_skills",
            [],
        )

        matched_preferred_skills = analysis.get(
            "matched_preferred_skills",
            [],
        )

        missing_preferred_skills = analysis.get(
            "missing_preferred_skills",
            [],
        )


        # -----------------------------------------------------
        # REQUIRED SKILLS
        # -----------------------------------------------------

        st.markdown(
            "### 🔴 Required Skills"
        )

        required_col1, required_col2 = st.columns(2)


        with required_col1:

            st.markdown(
                "#### ✅ Matched"
            )

            if matched_required_skills:

                for skill in matched_required_skills:

                    st.success(
                        skill
                    )

            else:

                st.info(
                    "No required skills matched."
                )


        with required_col2:

            st.markdown(
                "#### ⚠️ Missing"
            )

            if missing_required_skills:

                for skill in missing_required_skills:

                    st.warning(
                        skill
                    )

            else:

                st.success(
                    "No required skills are missing."
                )


        # -----------------------------------------------------
        # PREFERRED SKILLS
        # -----------------------------------------------------

        st.markdown(
            "### 🟡 Preferred Skills"
        )

        preferred_col1, preferred_col2 = st.columns(2)


        with preferred_col1:

            st.markdown(
                "#### ✅ Matched"
            )

            if matched_preferred_skills:

                for skill in matched_preferred_skills:

                    st.success(
                        skill
                    )

            else:

                st.info(
                    "No preferred skills matched."
                )


        with preferred_col2:

            st.markdown(
                "#### ⚠️ Missing"
            )

            if missing_preferred_skills:

                for skill in missing_preferred_skills:

                    st.warning(
                        skill
                    )

            else:

                st.success(
                    "No preferred skills are missing."
                )

        # -----------------------------------------------------
        # IMPROVEMENT RECOMMENDATIONS
        # -----------------------------------------------------

        recommendations = analysis.get(
            "improvement_recommendations",
            [],
        )

        st.markdown(
            "### 💡 Improvement Recommendations"
        )

        if recommendations:

            for recommendation in recommendations:

                skill = recommendation.get(
                    "skill",
                    "N/A",
                )

                category = recommendation.get(
                    "category",
                    "N/A",
                )

                reason = recommendation.get(
                    "reason",
                    "",
                )

                suggestion = recommendation.get(
                    "recommendation",
                    "",
                )

                with st.container(border=True):

                    st.markdown(
                        f"#### 🎯 {skill.title()}"
                    )

                    st.caption(
                        f"Category: {category.replace('_', ' ').title()}"
                    )

                    if reason:

                        st.markdown(
                            f"**Why it matters:** {reason}"
                        )

                    if suggestion:

                        st.markdown(
                            f"**What to improve:** {suggestion}"
                        )

        else:

            st.info(
                "No improvement recommendations were generated."
            )

        # -----------------------------------------------------
        # SEMANTIC EVIDENCE
        # -----------------------------------------------------

        st.markdown(
            "### 🔎 Semantic Evidence"
        )

        semantic_evidence = analysis.get(
            "semantic_evidence",
            []
        )

        if semantic_evidence:

            for evidence in semantic_evidence:

                job_requirement = evidence.get(
                    "job_requirement",
                    "N/A",
                )

                category = evidence.get(
                    "category",
                    "N/A",
                )

                resume_skill = evidence.get(
                    "resume_skill",
                    "N/A",
                )

                similarity = evidence.get(
                    "similarity"
                )

                with st.container(border=True):

                    st.markdown(
                        f"**Job Requirement:** {job_requirement}"
                    )

                    st.markdown(
                        f"**Resume Evidence:** {resume_skill}"
                    )

                    st.caption(
                        f"Category: "
                        f"{category.replace('_', ' ').title()}"
                    )

                    if similarity is not None:

                        st.metric(
                            "Semantic Similarity",
                            f"{similarity:.4f}",
                        )

        else:

            st.info(
                "No semantic evidence was generated."
            )

        # -----------------------------------------------------
        # PROJECT IMPROVEMENTS
        # -----------------------------------------------------

        st.markdown(
            "### 🛠 Project Improvements"
        )

        project_improvements = analysis.get(
            "project_improvements",
            []
        )

        if project_improvements:

            for project in project_improvements:

                project_name = project.get(
                    "project_name",
                    "Unknown Project",
                )

                strength = project.get(
                    "strength",
                    "",
                )

                weakness = project.get(
                    "weakness",
                    "",
                )

                recommendation = project.get(
                    "recommendation",
                    "",
                )

                with st.container(border=True):

                    st.markdown(
                        f"#### 📌 {project_name}"
                    )

                    if strength:

                        st.markdown(
                            f"**Strength:** {strength}"
                        )

                    if weakness:

                        st.markdown(
                            f"**Weakness:** {weakness}"
                        )

                    if recommendation:

                        st.markdown(
                            f"**Recommendation:** {recommendation}"
                        )

        else:

            st.info(
                "No project-specific improvements were generated."
            )


        # -----------------------------------------------------
        # EXPERIENCE INSIGHTS
        # -----------------------------------------------------

        st.markdown(
            "### 👔 Experience Insights"
        )

        experience_improvements = analysis.get(
            "experience_improvements",
            []
        )

        experience_note = analysis.get(
            "experience_note",
            ""
        )

        if experience_improvements:

            for experience in experience_improvements:

                with st.container(border=True):

                    st.markdown(
                        f"• {experience}"
                    )

        elif experience_note:

            st.info(
                experience_note
            )

        else:

            st.info(
                "No experience-specific insights were generated."
            )

    # -----------------------------------------------------
    # ATS SCORE
    # -----------------------------------------------------

    st.subheader("📋 ATS Compatibility")

    if isinstance(ats, dict):

        ats_score = ats.get(
            "ats_score"
        )

        if ats_score is not None:

            st.metric(
                "ATS Score",
                f"{ats_score:.2f}",
            )

        else:

            st.info(
                "ATS score is not available."
            )

    else:

        st.info(
            "ATS result is not available."
        )

    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    st.subheader("✅ Tailored Resume Validation")

    if isinstance(validation, dict):

        validation_status = validation.get(
            "valid"
        )

        if validation_status is True:

            st.success(
                "Tailored resume passed validation."
            )

        elif validation_status is False:

            st.error(
                "Tailored resume did not pass validation."
            )

        else:

            st.info(
                "Validation status is not available."
            )

    else:

        st.info(
            "Validation result is not available."
        )

    # -----------------------------------------------------
    # TAILORED RESUME
    # -----------------------------------------------------

    st.subheader("📝 Tailored Resume")

    if tailored_resume is not None:

        with st.expander(
            "View Tailored Resume Data"
        ):

            st.json(
                tailored_resume
            )

    else:

        st.info(
            "Tailored resume is not available."
        )

    # -----------------------------------------------------
    # RAW RESULTS
    # -----------------------------------------------------

    with st.expander(
        "🔍 View Raw Analysis JSON"
    ):

        st.json(
            analysis
        )

    with st.expander(
        "🔍 View Raw ATS JSON"
    ):

        st.json(
            ats
        )

    with st.expander(
        "🔍 View Raw Validation JSON"
    ):

        st.json(
            validation
        )

    # -----------------------------------------------------
    # PDF DOWNLOAD
    # -----------------------------------------------------

    st.subheader("📄 Download Tailored Resume")

    pdf_path = resume_genie_result.get(
        "pdf"
    )

    if pdf_path:

        pdf_file = Path(
            pdf_path
        )

        if pdf_file.exists():

            st.success(
                "Tailored resume PDF is ready."
            )

            with open(
                pdf_file,
                "rb",
            ) as file:

                st.download_button(
                    label="⬇️ Download Tailored Resume",
                    data=file,
                    file_name=pdf_file.name,
                    mime="application/pdf",
                    key="download_tailored_resume",
                )

        else:

            st.error(
                "The tailored resume PDF could not be found."
            )

    else:

        st.info(
            "No tailored PDF was generated."
        )


st.divider()

st.header("AI Career Coach")

st.write(
    "Ask questions about your selected resume, "
    "job description, match, skills, or career fit."
)

if resume_id is None or job_id is None:

    st.info(
        "Select a saved resume and job description above "
        "to use the AI Career Coach."
    )

else:

    # Display previous Career Coach messages
    for message in st.session_state["career_coach_messages"]:

        with st.chat_message(
            message["role"]
        ):
            st.markdown(
                message["content"]
            )

    question = st.chat_input(
        "Ask your Career Coach a question..."
    )

    if question:

        # Display user message immediately
        st.session_state["career_coach_messages"].append(
            {
                "role": "user",
                "content": question,
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        try:

            with st.chat_message("assistant"):

                with st.spinner(
                    "Career Coach is thinking..."
                ):

                    response = ask_career_coach(
                        question=question,
                        resume_id=resume_id,
                        job_id=job_id,
                        session_id=session_id,
                    )

                answer = response.get(
                    "answer",
                    "No answer was returned.",
                )

                st.markdown(answer)

            # Store assistant response
            st.session_state["career_coach_messages"].append(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )

        except Exception as exc:

            st.error(
                f"Career Coach request failed: {exc}"
            )

# =========================================================
# COVER LETTER GENERATOR
# =========================================================

st.divider()

st.header("✉️ Cover Letter Generator")

st.write(
    "Generate a job-specific, evidence-grounded cover letter "
    "using your selected resume and job description."
)

if resume_id is None or job_id is None:

    st.info(
        "Select a resume and job description above "
        "to generate a cover letter."
    )

else:

    if st.button(
        "✉️ Generate Cover Letter",
        key="generate_cover_letter",
        type="primary",
    ):

        with st.spinner(
            "Generating your cover letter..."
        ):

            try:

                response = generate_cover_letter(
                    resume_id=resume_id,
                    job_id=job_id,
                    session_id=session_id,
                )

                st.session_state[
                    "cover_letter_result"
                ] = response

                st.success(
                    "Cover letter generated successfully."
                )

            except requests.exceptions.RequestException as e:

                st.error(
                    f"Backend request failed: {e}"
                )

            except Exception as e:

                st.error(
                    f"Something went wrong: {e}"
                )


# =========================================================
# DISPLAY COVER LETTER
# =========================================================

cover_letter_result = st.session_state[
    "cover_letter_result"
]

if cover_letter_result is not None:

    cover_letter = cover_letter_result.get(
        "cover_letter"
    )

    if isinstance(cover_letter, dict):

        st.subheader("📄 Generated Cover Letter")

        st.markdown(
            cover_letter.get(
                "opening",
                ""
            )
        )

        st.markdown(
            cover_letter.get(
                "relevant_experience",
                ""
            )
        )

        st.markdown(
            cover_letter.get(
                "relevant_projects",
                ""
            )
        )

        st.markdown(
            cover_letter.get(
                "motivation",
                ""
            )
        )

        st.markdown(
            cover_letter.get(
                "closing",
                ""
            )
        )

    else:

        st.warning(
            "Cover letter content was not returned "
            "in the expected format."
        )
'''


from pathlib import Path
import requests
import streamlit as st
from session import get_session_id
from frontend.api_client import (
    upload_resume,
    process_job_text,
    upload_job_pdf,
    get_resumes,
    get_jobs,
    run_resume_genie,
    ask_career_coach,
    generate_cover_letter,
)


st.set_page_config(
    page_title="Resume Genie",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# UI STYLING
# =========================================================

st.markdown(
    """
    <style>
        /* ---------------------------------------------------------
           SAFE UI LAYER
           Only presentation is changed here. Streamlit's native
           theme is left in control of widgets so text/background
           contrast stays correct in light and dark modes.
        --------------------------------------------------------- */

        .block-container {
            max-width: 1280px;
            padding-top: 1.5rem;
            padding-bottom: 4rem;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background: #0f172a;
            border-right: 1px solid rgba(255,255,255,0.08);
        }

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] li,
        [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
            color: #e2e8f0 !important;
        }

        [data-testid="stSidebar"] hr {
            border-color: rgba(255,255,255,0.16) !important;
        }

        [data-testid="stSidebar"] [data-testid="stExpander"] {
            background: #111827;
            border: 1px solid #334155;
            border-radius: 12px;
            overflow: hidden;
        }

        [data-testid="stSidebar"] [data-testid="stExpander"] summary,
        [data-testid="stSidebar"] [data-testid="stExpander"] summary * {
            color: #f8fafc !important;
        }

        [data-testid="stSidebar"] [data-testid="stCodeBlock"],
        [data-testid="stSidebar"] pre,
        [data-testid="stSidebar"] code {
            background: #0b1220 !important;
            color: #f8fafc !important;
        }

        /* Brand / custom blocks */
        .rg-brand {
            padding: 0.75rem 0 1rem 0;
        }

        .rg-brand-title {
            font-size: 1.35rem;
            font-weight: 800;
            color: #ffffff !important;
            letter-spacing: -0.02em;
        }

        .rg-brand-subtitle {
            color: #94a3b8 !important;
            font-size: 0.88rem;
            margin-top: 0.2rem;
        }

        .rg-hero {
            padding: 2.2rem 2.35rem;
            border: 1px solid #e2e8f0;
            border-radius: 22px;
            background:
                radial-gradient(circle at top right, rgba(99,102,241,0.14), transparent 30%),
                linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            box-shadow: 0 12px 35px rgba(15, 23, 42, 0.06);
            margin-bottom: 1.5rem;
        }

        .rg-kicker {
            display: inline-block;
            padding: 0.38rem 0.72rem;
            border-radius: 999px;
            background: #eef2ff;
            color: #4338ca !important;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            margin-bottom: 0.9rem;
        }

        .rg-hero h1 {
            margin: 0;
            color: #0f172a !important;
            font-size: clamp(2.1rem, 4vw, 3.5rem);
            line-height: 1.05;
            letter-spacing: -0.04em;
        }

        .rg-hero p {
            max-width: 820px;
            color: #475569 !important;
            margin: 0.95rem 0 0 0;
            font-size: 1.05rem;
            line-height: 1.75;
        }

        .rg-section {
            margin-top: 2.35rem;
            margin-bottom: 0.75rem;
        }

        .rg-section-label {
            color: #6366f1 !important;
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 0.25rem;
        }

        .rg-section-title {
            color: inherit !important;
            font-size: 1.55rem;
            line-height: 1.25;
            font-weight: 800;
            letter-spacing: -0.025em;
        }

        .rg-section-description {
            color: #64748b !important;
            margin-top: 0.35rem;
            margin-bottom: 1rem;
            max-width: 880px;
            line-height: 1.6;
        }

        .rg-status {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.75rem 0.8rem;
            border: 1px solid rgba(255,255,255,0.1);
            background: rgba(255,255,255,0.045);
            border-radius: 12px;
            margin-bottom: 0.55rem;
        }

        .rg-dot-ready,
        .rg-dot-waiting {
            width: 8px;
            height: 8px;
            border-radius: 999px;
            flex: 0 0 auto;
        }

        .rg-dot-ready { background: #22c55e; }
        .rg-dot-waiting { background: #64748b; }

        .rg-status-text {
            font-size: 0.84rem;
            color: #e2e8f0 !important;
        }

        /* Native widgets: only shape/spacing, not text/background theme */
        div[data-testid="stTextArea"] textarea,
        div[data-baseweb="select"] > div {
            border-radius: 12px !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 16px;
        }

        div[data-testid="stAlert"] {
            border-radius: 12px;
        }

        div[data-testid="stMetric"] {
            border-radius: 16px;
            padding: 1rem 1.05rem;
        }

        [data-testid="stChatMessage"] {
            border-radius: 16px;
            padding: 0.55rem 0.75rem;
            margin-bottom: 0.75rem;
        }

        /* Buttons: explicit contrast in normal + hover states */
        .stButton > button,
        .stDownloadButton > button {
            border-radius: 11px;
            font-weight: 700;
            min-height: 2.75rem;
            transition: all 0.18s ease;
        }

        button[kind="primary"] {
            background: linear-gradient(135deg, #4f46e5, #6366f1) !important;
            border: 1px solid #4f46e5 !important;
            color: #ffffff !important;
        }

        button[kind="primary"] *,
        button[kind="primary"]:hover *,
        button[kind="primary"]:focus *,
        button[kind="primary"]:active * {
            color: #ffffff !important;
        }

        button[kind="primary"]:hover,
        button[kind="primary"]:focus,
        button[kind="primary"]:active {
            background: #4338ca !important;
            border-color: #4338ca !important;
            color: #ffffff !important;
            transform: translateY(-1px);
            box-shadow: 0 8px 18px rgba(67, 56, 202, 0.22);
        }

        .stButton > button:not([kind="primary"]),
        .stDownloadButton > button {
            background: #ffffff !important;
            color: #0f172a !important;
            border: 1px solid #cbd5e1 !important;
        }

        .stButton > button:not([kind="primary"]) *,
        .stDownloadButton > button *,
        .stButton > button:not([kind="primary"]):hover *,
        .stDownloadButton > button:hover * {
            color: #0f172a !important;
        }

        .stButton > button:not([kind="primary"]):hover,
        .stDownloadButton > button:hover {
            background: #f8fafc !important;
            color: #0f172a !important;
            border-color: #94a3b8 !important;
            transform: translateY(-1px);
            box-shadow: 0 8px 18px rgba(15, 23, 42, 0.08);
        }

        /* File uploader: ONLY resume/JD upload widgets */
        [data-testid="stFileUploader"] > label,
        [data-testid="stFileUploader"] > label *,
        [data-testid="stFileUploader"] [data-testid="stWidgetLabel"],
        [data-testid="stFileUploader"] [data-testid="stWidgetLabel"] * {
            color: #f8fafc !important;
        }

        [data-testid="stFileUploader"] section {
            background: #ffffff !important;
            border: 1px dashed #cbd5e1 !important;
            border-radius: 16px !important;
        }

        [data-testid="stFileUploader"] section p,
        [data-testid="stFileUploader"] section span,
        [data-testid="stFileUploader"] section small {
            color: #0f172a !important;
        }

        /* Uploaded file chip: dark surface must use light filename/size text */
        [data-testid="stFileUploaderFile"] {
            background: #111827 !important;
            border: 1px solid #334155 !important;
            border-radius: 10px !important;
        }

        [data-testid="stFileUploaderFile"],
        [data-testid="stFileUploaderFile"] *,
        [data-testid="stFileUploaderFileName"],
        [data-testid="stFileUploaderFileName"] * {
            color: #f8fafc !important;
        }

        [data-testid="stFileUploaderFile"] small {
            color: #cbd5e1 !important;
        }

        [data-testid="stFileUploader"] button {
            background: #eef2ff !important;
            color: #312e81 !important;
            border: 1px solid #c7d2fe !important;
        }

        [data-testid="stFileUploader"] button *,
        [data-testid="stFileUploader"] button:hover * {
            color: #312e81 !important;
        }

        [data-testid="stFileUploader"] button:hover {
            background: #e0e7ff !important;
            color: #312e81 !important;
            border-color: #a5b4fc !important;
        }

        /* Inputs/selects: explicit readable foreground/background */
        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea,
        [data-testid="stChatInput"] textarea,
        [data-testid="stChatInput"] input,
        div[data-baseweb="select"] > div {
            background: #ffffff !important;
            color: #0f172a !important;
        }

        [data-testid="stTextInput"] input::placeholder,
        [data-testid="stTextArea"] textarea::placeholder,
        [data-testid="stChatInput"] textarea::placeholder,
        [data-testid="stChatInput"] input::placeholder {
            color: #64748b !important;
            opacity: 1 !important;
        }

        /* Expanders/tabs outside sidebar */
        [data-testid="stMain"] [data-testid="stExpander"] {
            border-radius: 14px;
        }

        [data-testid="stMain"] [data-testid="stExpander"] summary,
        [data-testid="stMain"] [data-testid="stExpander"] summary * {
            color: inherit !important;
        }

        button[data-baseweb="tab"],
        button[data-baseweb="tab"] * {
            color: inherit !important;
        }

        /* JSON / code blocks:
           never override the internal syntax colours. Only shape the panel. */
        [data-testid="stJson"],
        [data-testid="stCodeBlock"],
        pre {
            border-radius: 12px !important;
        }

        hr {
            margin: 2rem 0 !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def section_header(label: str, title: str, description: str = ""):
    description_html = (
        f'<div class="rg-section-description">{description}</div>'
        if description
        else ""
    )
    st.markdown(
        f"""
        <div class="rg-section">
            <div class="rg-section-label">{label}</div>
            <div class="rg-section-title">{title}</div>
            {description_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# SESSION
# =========================================================

session_id = get_session_id()


# =========================================================
# STREAMLIT SESSION STATE
# =========================================================

if "resume_result" not in st.session_state:
    st.session_state["resume_result"] = None

if "job_result" not in st.session_state:
    st.session_state["job_result"] = None

if "resume_genie_result" not in st.session_state:
    st.session_state["resume_genie_result"] = None

if "resume_history" not in st.session_state:
    st.session_state["resume_history"] = []

if "job_history" not in st.session_state:
    st.session_state["job_history"] = []

if "history_loaded" not in st.session_state:
    st.session_state["history_loaded"] = False

if "career_coach_messages" not in st.session_state:
    st.session_state["career_coach_messages"] = []

if "cover_letter_result" not in st.session_state:
    st.session_state["cover_letter_result"] = None


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown(
        """
        <div class="rg-brand">
            <div class="rg-brand-title">✨ Resume Genie</div>
            <div class="rg-brand-subtitle">AI-Powered Career Suite</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption("WORKFLOW")
    st.markdown("**1.** Upload resume")
    st.markdown("**2.** Add job description")
    st.markdown("**3.** Select saved application")
    st.markdown("**4.** Run analysis")
    st.markdown("**5.** Use Coach & Cover Letter")

    st.divider()
    st.caption("CURRENT STATUS")

    resume_ready = st.session_state.get("resume_result") is not None
    job_ready = st.session_state.get("job_result") is not None
    analysis_ready = st.session_state.get("resume_genie_result") is not None

    st.markdown(
        f"""
        <div class="rg-status">
            <span class="{'rg-dot-ready' if resume_ready else 'rg-dot-waiting'}"></span>
            <span class="rg-status-text">Resume {'ready' if resume_ready else 'not processed'}</span>
        </div>
        <div class="rg-status">
            <span class="{'rg-dot-ready' if job_ready else 'rg-dot-waiting'}"></span>
            <span class="rg-status-text">Job description {'ready' if job_ready else 'not processed'}</span>
        </div>
        <div class="rg-status">
            <span class="{'rg-dot-ready' if analysis_ready else 'rg-dot-waiting'}"></span>
            <span class="rg-status-text">Analysis {'ready' if analysis_ready else 'not generated'}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()
    with st.expander("Session details"):
        st.caption("Session ID")
        st.code(session_id, language=None)


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
    <div class="rg-hero">
        <div class="rg-kicker">AI Career Intelligence</div>
        <h1>Build a stronger job application.</h1>
        <p>
            Analyze your resume against real job descriptions, understand ATS alignment,
            generate a grounded tailored resume, ask a RAG-powered Career Coach, and create
            an evidence-based cover letter — all in one workflow.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# RESUME
# =========================================================

section_header(
    "Step 1",
    "📄 Resume",
    "Upload a PDF resume and convert it into structured, searchable candidate data.",
)

uploaded_resume = st.file_uploader(
    "Upload your resume in PDF format",
    type=["pdf"],
    key="resume_upload",
)


if uploaded_resume is not None:

    st.write(
        f"**Selected file:** {uploaded_resume.name}"
    )

    if st.button(
        "Process Resume",
        key="process_resume",
    ):

        with st.spinner(
            "Processing your resume..."
        ):

            try:

                result = upload_resume(
                    file_bytes=uploaded_resume.getvalue(),
                    filename=uploaded_resume.name,
                    session_id=session_id,
                )

                # Store the API response
                # in Streamlit session state.
                st.session_state["resume_result"] = result

                # Refresh saved history because a new resume was created.
                st.session_state["history_loaded"] = False

                st.success(
                    "Resume processed successfully."
                )

            except requests.exceptions.RequestException as e:

                st.error(
                    f"Backend request failed: {e}"
                )

            except Exception as e:

                st.error(
                    f"Something went wrong: {e}"
                )


# =========================================================
# DISPLAY RESUME RESULT
# =========================================================

resume_result = st.session_state["resume_result"]


if resume_result is not None:

    resume_meta_col1, resume_meta_col2 = st.columns(2)

    with resume_meta_col1:
        st.metric(
            "Resume ID",
            resume_result.get("resume_id", "N/A"),
        )

    with resume_meta_col2:
        st.metric(
            "Stored Chunks",
            resume_result.get("chunk_count", "N/A"),
        )

    with st.expander(
        "View Structured Resume"
    ):

        st.json(
            resume_result.get("resume")
        )


st.divider()


# =========================================================
# JOB DESCRIPTION
# =========================================================

section_header(
    "Step 2",
    "💼 Job Description",
    "Paste a job description or upload a PDF so Resume Genie can extract the target role requirements.",
)

job_input_method = st.radio(
    "How would you like to provide the job description?",
    options=[
        "Paste Text",
        "Upload PDF",
    ],
    horizontal=True,
)


# =========================================================
# JD TEXT
# =========================================================

if job_input_method == "Paste Text":

    job_text = st.text_area(
        "Paste the Job Description here",
        height=300,
        placeholder=(
            "Paste the complete job description here..."
        ),
        key="job_text",
    )

    if st.button(
        "Process Job Description",
        key="process_job_text",
    ):

        if not job_text.strip():

            st.warning(
                "Please paste a job description first."
            )

        else:

            with st.spinner(
                "Processing job description..."
            ):

                try:

                    result = process_job_text(
                        job_text=job_text,
                        session_id=session_id,
                    )

                    # Store the API response
                    # in Streamlit session state.
                    st.session_state["job_result"] = result

                    # Refresh saved history because a new job was created.
                    st.session_state["history_loaded"] = False

                    st.success(
                        "Job description processed successfully."
                    )

                except requests.exceptions.RequestException as e:

                    st.error(
                        f"Backend request failed: {e}"
                    )

                except Exception as e:

                    st.error(
                        f"Something went wrong: {e}"
                    )


# =========================================================
# JD PDF
# =========================================================

else:

    uploaded_job = st.file_uploader(
        "Upload the Job Description PDF",
        type=["pdf"],
        key="job_upload",
    )

    if uploaded_job is not None:

        st.write(
            f"**Selected file:** {uploaded_job.name}"
        )

        if st.button(
            "Process Job Description PDF",
            key="process_job_pdf",
        ):

            with st.spinner(
                "Processing job description..."
            ):

                try:

                    result = upload_job_pdf(
                        file_bytes=uploaded_job.getvalue(),
                        filename=uploaded_job.name,
                        session_id=session_id,
                    )

                    # Store the API response
                    # in Streamlit session state.
                    st.session_state["job_result"] = result

                    # Refresh saved history because a new job was created.
                    st.session_state["history_loaded"] = False

                    st.success(
                        "Job description processed successfully."
                    )
                except requests.exceptions.RequestException as e:

                    st.error(
                        f"Backend request failed: {e}"
                    )

                except Exception as e:

                    st.error(
                        f"Something went wrong: {e}"
                    )


# =========================================================
# DISPLAY JOB RESULT
# =========================================================

job_result = st.session_state["job_result"]


if job_result is not None:

    st.metric(
        "Job ID",
        job_result.get("job_id", "N/A"),
    )

    with st.expander(
        "View Structured Job Description"
    ):

        st.json(
            job_result.get(
                "job_description"
            )
        )


st.divider()


# =========================================================
# ANALYSIS PREPARATION
# =========================================================

section_header(
    "Step 3",
    "🎯 Resume–Job Analysis",
    "Choose the resume and job you want to compare, then run the complete matching, ATS, tailoring, and validation pipeline.",
)


# =========================================================
# RESUME & JOB HISTORY
# =========================================================

st.subheader("📚 Your Saved Work")


# =========================================================
# LOAD SAVED HISTORY
# =========================================================

if not st.session_state["history_loaded"]:

    try:

        resume_history_result = get_resumes(
            session_id=session_id,
        )

        job_history_result = get_jobs(
            session_id=session_id,
        )

        st.session_state["resume_history"] = (
            resume_history_result.get(
                "resumes",
                [],
            )
        )

        st.session_state["job_history"] = (
            job_history_result.get(
                "jobs",
                [],
            )
        )

        st.session_state["history_loaded"] = True

    except requests.exceptions.RequestException:

        st.session_state["resume_history"] = []
        st.session_state["job_history"] = []
        st.session_state["history_loaded"] = True

    except Exception:

        st.session_state["resume_history"] = []
        st.session_state["job_history"] = []
        st.session_state["history_loaded"] = True


# =========================================================
# GET HISTORY FROM SESSION STATE
# =========================================================

resume_history = st.session_state.get(
    "resume_history",
    [],
)

job_history = st.session_state.get(
    "job_history",
    [],
)


# =========================================================
# DISPLAY SAVED WORK
# =========================================================

history_col1, history_col2 = st.columns(2)

with history_col1:
    with st.container(border=True):
        st.markdown("#### 📄 Saved Resumes")

        if resume_history:
            for resume in resume_history:
                st.write(
                    f"**{resume.get('filename', 'Unknown Resume')}**  "
                    f"\nResume ID: `{resume.get('resume_id')}`"
                )
        else:
            st.info("No saved resumes yet.")

with history_col2:
    with st.container(border=True):
        st.markdown("#### 💼 Saved Job Descriptions")

        if job_history:
            for job in job_history:
                st.write(
                    f"**{job.get('job_title') or 'Unknown Job'}**  "
                    f"\n{job.get('company') or 'Unknown Company'}  "
                    f"\nJob ID: `{job.get('job_id')}`"
                )
        else:
            st.info("No saved job descriptions yet.")


st.divider()


# =========================================================
# DETERMINE RESUME AND JOB IDs
# =========================================================

resume_id = None
job_id = None
selected_resume_id = None
selected_job_id = None

# ---------------------------------------------------------
# SAVED HISTORY AVAILABLE
# ---------------------------------------------------------

if len(resume_history) > 0 and len(job_history) > 0:

    st.subheader("📚 Select Resume & Job")

    resume_options = {
        (
            f"{resume.get('filename', 'Unknown Resume')} "
            f"(ID: {resume.get('resume_id')})"
        ): resume.get("resume_id")
        for resume in resume_history
    }

    job_options = {
        (
            f"{job.get('job_title') or 'Unknown Job'} "
            f"- {job.get('company') or 'Unknown Company'} "
            f"(ID: {job.get('job_id')})"
        ): job.get("job_id")
        for job in job_history
    }

    selection_col1, selection_col2 = st.columns(2)

    with selection_col1:
        selected_resume_label = st.selectbox(
            "Select Resume",
            options=list(resume_options.keys()),
            key="selected_resume",
        )

    with selection_col2:
        selected_job_label = st.selectbox(
            "Select Job Description",
            options=list(job_options.keys()),
            key="selected_job",
        )

    resume_id = resume_options[
        selected_resume_label
    ]

    job_id = job_options[
        selected_job_label
    ]

    selection_key = f"{resume_id}:{job_id}"

    if st.session_state.get(
        "career_coach_selection"
    ) != selection_key:

        st.session_state["career_coach_messages"] = []

        st.session_state[
            "cover_letter_result"
        ] = None

        st.session_state[
            "career_coach_selection"
        ] = selection_key

    st.success(
        f"Selected Resume ID: {resume_id} | "
        f"Selected Job ID: {job_id}"
    )


# ---------------------------------------------------------
# CURRENTLY PROCESSED RESUME + JOB
# ---------------------------------------------------------

elif resume_result is not None and job_result is not None:

    resume_id = resume_result.get(
        "resume_id"
    )

    job_id = job_result.get(
        "job_id"
    )

    st.subheader("✅ Current Resume & Job")

    st.info(
        "Using the Resume and Job Description you just processed."
    )

    current_col1, current_col2 = st.columns(2)

    with current_col1:
        st.metric("Resume ID", resume_id)

    with current_col2:
        st.metric("Job ID", job_id)


# ---------------------------------------------------------
# WAITING FOR RESUME / JOB
# ---------------------------------------------------------

else:

    if resume_result is None and job_result is None:

        st.info(
            "Process a resume and a job description to continue."
        )

    elif resume_result is None:

        st.info(
            "Resume is missing. Process your resume first."
        )

    else:

        st.info(
            "Job description is missing. Process a JD first."
        )


# =========================================================
# ANALYZE RESUME AGAINST JOB
# =========================================================

if resume_id is not None and job_id is not None:

    st.divider()

    with st.container(border=True):
        st.markdown("#### 🚀 Ready to analyze")

        st.caption(
            "Run the matching, ATS, tailoring, and validation pipeline for the selected resume and job."
        )

        analysis_button_label = (
            "🔄 Run Analysis Again"
            if st.session_state.get("resume_genie_result") is not None
            else "🔍 Analyze Resume Against Job"
        )

        if st.button(
            analysis_button_label,
            key="analyze_resume",
            type="primary",
        ):

            with st.spinner(
                "Running Resume Genie analysis..."
            ):

                try:

                    result = run_resume_genie(
                        resume_id=resume_id,
                        job_id=job_id,
                        session_id=session_id,
                    )

                    st.session_state[
                        "resume_genie_result"
                    ] = result

                    st.success(
                        "Resume Genie analysis completed successfully."
                    )

                except requests.exceptions.RequestException as e:

                    st.error(
                        f"Backend request failed: {e}"
                    )

                except Exception as e:

                    st.error(
                        f"Something went wrong: {e}"
                    )

# =========================================================
# DISPLAY RESUME GENIE RESULT
# =========================================================

resume_genie_result = st.session_state[
    "resume_genie_result"
]


if resume_genie_result is not None:

    st.divider()

    section_header(
        "Results",
        "📊 Resume Genie Analysis",
        "A structured view of your match quality, ATS compatibility, evidence, recommendations, and tailored resume.",
    )

    # -----------------------------------------------------
    # EXTRACT RESULTS
    # -----------------------------------------------------

    analysis = resume_genie_result.get(
        "analysis"
    )

    tailored_resume = resume_genie_result.get(
        "tailored_resume"
    )

    validation = resume_genie_result.get(
        "validation"
    )

    ats = resume_genie_result.get(
        "ats"
    )

    # -----------------------------------------------------
    # KEY SCORES
    # -----------------------------------------------------

    overall_score = None
    ats_score = None

    if isinstance(analysis, dict):

        overall_score = analysis.get(
            "overall_score"
        )

    if isinstance(ats, dict):

        ats_score = ats.get(
            "ats_score"
        )

    # -----------------------------------------------------
    # KEY SCORE DISPLAY
    # -----------------------------------------------------

    validation_status = validation.get("valid") if isinstance(validation, dict) else None

    score_col1, score_col2, score_col3 = st.columns(3)

    with score_col1:

        if overall_score is not None:

            st.metric(
                "🎯 Overall Match Score",
                f"{overall_score:.2f}",
            )

        else:

            st.metric(
                "🎯 Overall Match Score",
                "N/A",
            )

    with score_col2:

        if ats_score is not None:

            st.metric(
                "📋 ATS Score",
                f"{ats_score:.2f}",
            )

        else:

            st.metric(
                "📋 ATS Score",
                "N/A",
            )

    with score_col3:
        validation_label = (
            "Passed" if validation_status is True
            else "Needs Review" if validation_status is False
            else "N/A"
        )
        st.metric("✅ Validation", validation_label)

    # -----------------------------------------------------
    # APPLICATION INFORMATION
    # -----------------------------------------------------

    with st.expander("📌 Application Information"):
        info_col1, info_col2, info_col3 = st.columns(3)

        with info_col1:
            st.metric(
                "Application ID",
                resume_genie_result.get(
                    "application_id",
                    "N/A",
                ),
            )

        with info_col2:
            st.metric(
                "Resume ID",
                resume_genie_result.get(
                    "resume_id",
                    "N/A",
                ),
            )

        with info_col3:
            st.metric(
                "Job ID",
                resume_genie_result.get(
                    "job_id",
                    "N/A",
                ),
            )

    # -----------------------------------------------------
    # ANALYSIS TABS
    # -----------------------------------------------------

    overview_tab, skills_tab, projects_tab, evidence_tab, resume_tab = st.tabs(
        [
            "📈 Overview",
            "🧩 Skills",
            "🛠 Projects",
            "🔎 Evidence",
            "📝 Tailored Resume",
        ]
    )

    with overview_tab:
        if isinstance(analysis, dict):

            score_components = analysis.get(
                "score_components"
            )

            if isinstance(score_components, dict) and score_components:

                st.markdown("### Score Breakdown")

                component_columns = st.columns(
                    min(len(score_components), 4)
                )

                for column, (
                    component_name,
                    component_value,
                ) in zip(
                    component_columns,
                    score_components.items(),
                ):

                    with column:

                        display_name = (
                            component_name
                            .replace("_", " ")
                            .title()
                        )

                        if isinstance(
                            component_value,
                            (int, float),
                        ):

                            st.metric(
                                display_name,
                                f"{component_value:.2f}",
                            )

                        else:

                            st.write(
                                f"**{display_name}**"
                            )

                            st.write(
                                component_value
                            )

            recommendations = analysis.get(
                "improvement_recommendations",
                [],
            )

            st.markdown("### 💡 Improvement Recommendations")

            if recommendations:

                for recommendation in recommendations:

                    skill = recommendation.get(
                        "skill",
                        "N/A",
                    )

                    category = recommendation.get(
                        "category",
                        "N/A",
                    )

                    reason = recommendation.get(
                        "reason",
                        "",
                    )

                    suggestion = recommendation.get(
                        "recommendation",
                        "",
                    )

                    with st.container(border=True):

                        st.markdown(
                            f"#### 🎯 {skill.title()}"
                        )

                        st.caption(
                            f"Category: {category.replace('_', ' ').title()}"
                        )

                        if reason:

                            st.markdown(
                                f"**Why it matters:** {reason}"
                            )

                        if suggestion:

                            st.markdown(
                                f"**What to improve:** {suggestion}"
                            )

            else:

                st.info(
                    "No improvement recommendations were generated."
                )

            st.markdown("### 👔 Experience Insights")

            experience_improvements = analysis.get(
                "experience_improvements",
                []
            )

            experience_note = analysis.get(
                "experience_note",
                ""
            )

            if experience_improvements:

                for experience in experience_improvements:

                    with st.container(border=True):

                        st.markdown(
                            f"• {experience}"
                        )

            elif experience_note:

                st.info(
                    experience_note
                )

            else:

                st.info(
                    "No experience-specific insights were generated."
                )

        st.markdown("### 📋 ATS Compatibility")

        if isinstance(ats, dict):

            ats_score = ats.get(
                "ats_score"
            )

            if ats_score is not None:

                st.metric(
                    "ATS Score",
                    f"{ats_score:.2f}",
                )

            else:

                st.info(
                    "ATS score is not available."
                )

        else:

            st.info(
                "ATS result is not available."
            )

        st.markdown("### ✅ Tailored Resume Validation")

        if isinstance(validation, dict):

            validation_status = validation.get(
                "valid"
            )

            if validation_status is True:

                st.success(
                    "Tailored resume passed validation."
                )

            elif validation_status is False:

                st.error(
                    "Tailored resume did not pass validation."
                )

            else:

                st.info(
                    "Validation status is not available."
                )

        else:

            st.info(
                "Validation result is not available."
            )

    with skills_tab:
        if isinstance(analysis, dict):

            matched_required_skills = analysis.get(
                "matched_required_skills",
                [],
            )

            missing_required_skills = analysis.get(
                "missing_required_skills",
                [],
            )

            matched_preferred_skills = analysis.get(
                "matched_preferred_skills",
                [],
            )

            missing_preferred_skills = analysis.get(
                "missing_preferred_skills",
                [],
            )

            st.markdown("### 🔴 Required Skills")
            required_col1, required_col2 = st.columns(2)

            with required_col1:
                with st.container(border=True):
                    st.markdown("#### ✅ Matched")

                    if matched_required_skills:
                        for skill in matched_required_skills:
                            st.success(skill)
                    else:
                        st.info("No required skills matched.")

            with required_col2:
                with st.container(border=True):
                    st.markdown("#### ⚠️ Missing")

                    if missing_required_skills:
                        for skill in missing_required_skills:
                            st.warning(skill)
                    else:
                        st.success("No required skills are missing.")

            st.markdown("### 🟡 Preferred Skills")
            preferred_col1, preferred_col2 = st.columns(2)

            with preferred_col1:
                with st.container(border=True):
                    st.markdown("#### ✅ Matched")

                    if matched_preferred_skills:
                        for skill in matched_preferred_skills:
                            st.success(skill)
                    else:
                        st.info("No preferred skills matched.")

            with preferred_col2:
                with st.container(border=True):
                    st.markdown("#### ⚠️ Missing")

                    if missing_preferred_skills:
                        for skill in missing_preferred_skills:
                            st.warning(skill)
                    else:
                        st.success("No preferred skills are missing.")

    with projects_tab:
        if isinstance(analysis, dict):

            project_improvements = analysis.get(
                "project_improvements",
                []
            )

            if project_improvements:

                for project in project_improvements:

                    project_name = project.get(
                        "project_name",
                        "Unknown Project",
                    )

                    strength = project.get(
                        "strength",
                        "",
                    )

                    weakness = project.get(
                        "weakness",
                        "",
                    )

                    recommendation = project.get(
                        "recommendation",
                        "",
                    )

                    with st.container(border=True):

                        st.markdown(
                            f"#### 📌 {project_name}"
                        )

                        if strength:

                            st.markdown(
                                f"**Strength:** {strength}"
                            )

                        if weakness:

                            st.markdown(
                                f"**Weakness:** {weakness}"
                            )

                        if recommendation:

                            st.markdown(
                                f"**Recommendation:** {recommendation}"
                            )

            else:

                st.info(
                    "No project-specific improvements were generated."
                )

    with evidence_tab:
        if isinstance(analysis, dict):

            semantic_evidence = analysis.get(
                "semantic_evidence",
                []
            )

            if semantic_evidence:

                for evidence in semantic_evidence:

                    job_requirement = evidence.get(
                        "job_requirement",
                        "N/A",
                    )

                    category = evidence.get(
                        "category",
                        "N/A",
                    )

                    resume_skill = evidence.get(
                        "resume_skill",
                        "N/A",
                    )

                    similarity = evidence.get(
                        "similarity"
                    )

                    with st.container(border=True):

                        st.markdown(
                            f"**Job Requirement:** {job_requirement}"
                        )

                        st.markdown(
                            f"**Resume Evidence:** {resume_skill}"
                        )

                        st.caption(
                            f"Category: "
                            f"{category.replace('_', ' ').title()}"
                        )

                        if similarity is not None:

                            st.metric(
                                "Semantic Similarity",
                                f"{similarity:.4f}",
                            )

            else:

                st.info(
                    "No semantic evidence was generated."
                )

    with resume_tab:
        if tailored_resume is not None:

            with st.expander(
                "View Tailored Resume Data"
            ):

                st.json(
                    tailored_resume
                )

        else:

            st.info(
                "Tailored resume is not available."
            )

        st.markdown("### 📄 Download Tailored Resume")

        pdf_path = resume_genie_result.get(
            "pdf"
        )

        if pdf_path:

            pdf_file = Path(
                pdf_path
            )

            if pdf_file.exists():

                st.success(
                    "Tailored resume PDF is ready."
                )

                with open(
                    pdf_file,
                    "rb",
                ) as file:

                    st.download_button(
                        label="⬇️ Download Tailored Resume",
                        data=file,
                        file_name=pdf_file.name,
                        mime="application/pdf",
                        key="download_tailored_resume",
                    )

            else:

                st.error(
                    "The tailored resume PDF could not be found."
                )

        else:

            st.info(
                "No tailored PDF was generated."
            )

    with st.expander("Developer / Raw Results"):
        raw_tab1, raw_tab2, raw_tab3 = st.tabs(
            ["Analysis JSON", "ATS JSON", "Validation JSON"]
        )

        with raw_tab1:
            st.json(analysis)

        with raw_tab2:
            st.json(ats)

        with raw_tab3:
            st.json(validation)


st.divider()

section_header(
    "Step 4",
    "🤖 AI Career Coach",
    "Ask grounded questions about your selected resume, target job, match quality, missing skills, projects, or career fit.",
)

if resume_id is None or job_id is None:

    st.info(
        "Select a saved resume and job description above "
        "to use the AI Career Coach."
    )

else:

    with st.container(border=True):
        st.caption(
            f"Active context · Resume ID {resume_id} · Job ID {job_id}"
        )

        # Display previous Career Coach messages
        for message in st.session_state["career_coach_messages"]:

            with st.chat_message(
                message["role"]
            ):
                st.markdown(
                    message["content"]
                )

        question = st.chat_input(
            "Ask your Career Coach a question..."
        )

        if question:

            # Display user message immediately
            st.session_state["career_coach_messages"].append(
                {
                    "role": "user",
                    "content": question,
                }
            )

            with st.chat_message("user"):
                st.markdown(question)

            try:

                with st.chat_message("assistant"):

                    with st.spinner(
                        "Career Coach is thinking..."
                    ):

                        response = ask_career_coach(
                            question=question,
                            resume_id=resume_id,
                            job_id=job_id,
                            session_id=session_id,
                        )

                    answer = response.get(
                        "answer",
                        "No answer was returned.",
                    )

                    st.markdown(answer)

                # Store assistant response
                st.session_state["career_coach_messages"].append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )

            except Exception as exc:

                st.error(
                    f"Career Coach request failed: {exc}"
                )

# =========================================================
# COVER LETTER GENERATOR
# =========================================================

st.divider()

section_header(
    "Step 5",
    "✉️ Cover Letter Generator",
    "Generate a concise, job-specific cover letter grounded only in evidence from the selected resume and job description.",
)

if resume_id is None or job_id is None:

    st.info(
        "Select a resume and job description above "
        "to generate a cover letter."
    )

else:

    with st.container(border=True):
        action_col1, action_col2 = st.columns([2, 1])

        with action_col1:
            st.markdown("#### Generate for the active application")
            st.caption(
                f"Resume ID {resume_id} · Job ID {job_id}"
            )

        with action_col2:
            if st.button(
                "✉️ Generate Cover Letter",
                key="generate_cover_letter",
                type="primary",
                use_container_width=True,
            ):

                with st.spinner(
                    "Generating your cover letter..."
                ):

                    try:

                        response = generate_cover_letter(
                            resume_id=resume_id,
                            job_id=job_id,
                            session_id=session_id,
                        )

                        st.session_state[
                            "cover_letter_result"
                        ] = response

                        st.success(
                            "Cover letter generated successfully."
                        )

                    except requests.exceptions.RequestException as e:

                        st.error(
                            f"Backend request failed: {e}"
                        )

                    except Exception as e:

                        st.error(
                            f"Something went wrong: {e}"
                        )


# =========================================================
# DISPLAY COVER LETTER
# =========================================================

cover_letter_result = st.session_state[
    "cover_letter_result"
]

if cover_letter_result is not None:

    cover_letter = cover_letter_result.get(
        "cover_letter"
    )

    if isinstance(cover_letter, dict):

        st.markdown("### 📄 Generated Cover Letter")

        with st.container(border=True):
            st.markdown(
                cover_letter.get(
                    "opening",
                    ""
                )
            )

            st.markdown(
                cover_letter.get(
                    "relevant_experience",
                    ""
                )
            )

            st.markdown(
                cover_letter.get(
                    "relevant_projects",
                    ""
                )
            )

            st.markdown(
                cover_letter.get(
                    "motivation",
                    ""
                )
            )

            st.markdown(
                cover_letter.get(
                    "closing",
                    ""
                )
            )

    else:

        st.warning(
            "Cover letter content was not returned "
            "in the expected format."
        )
