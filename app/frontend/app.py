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
        