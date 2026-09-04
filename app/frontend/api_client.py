import requests


BACKEND_URL = "http://127.0.0.1:8000"


def upload_resume(
    file_bytes: bytes,
    filename: str,
    session_id: str,
) -> dict:

    url = f"{BACKEND_URL}/api/resume/upload"

    files = {
        "file": (
            filename,
            file_bytes,
            "application/pdf",
        )
    }

    headers = {
        "X-Session-ID": session_id,
    }

    response = requests.post(
        url,
        files=files,
        headers=headers,
        timeout=120,
    )

    response.raise_for_status()

    return response.json()


def process_job_text(
    job_text: str,
    session_id: str,
) -> dict:

    url = f"{BACKEND_URL}/api/job/text"

    headers = {
        "X-Session-ID": session_id,
    }

    payload = {
        "job_text": job_text,
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers,
        timeout=120,
    )

    response.raise_for_status()

    return response.json()


def upload_job_pdf(
    file_bytes: bytes,
    filename: str,
    session_id: str,
) -> dict:

    url = f"{BACKEND_URL}/api/job/pdf"

    files = {
        "file": (
            filename,
            file_bytes,
            "application/pdf",
        )
    }

    headers = {
        "X-Session-ID": session_id,
    }

    response = requests.post(
        url,
        files=files,
        headers=headers,
        timeout=120,
    )

    response.raise_for_status()

    return response.json()

def get_resumes(
    session_id: str,
) -> dict:

    url = f"{BACKEND_URL}/api/resume/list"

    headers = {
        "X-Session-ID": session_id,
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def get_jobs(
    session_id: str,
) -> dict:

    url = f"{BACKEND_URL}/api/job/list"

    headers = {
        "X-Session-ID": session_id,
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()

def run_resume_genie(
    resume_id: int,
    job_id: int,
    session_id: str,
) -> dict:
    url = f"{BACKEND_URL}/api/resume-genie/run"

    headers = {
        "X-Session-ID": session_id,
    }

    payload = {
        "resume_id": resume_id,
        "job_id": job_id,
        "section_order": None,
        "removed_sections": None,
        "removed_projects": None,
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers,
        timeout=300,
    )

    response.raise_for_status()

    return response.json()

def ask_career_coach(
    question: str,
    resume_id: int,
    job_id: int,
    session_id: str,
) -> dict:
    """
    Send a Career Coach question for a selected
    saved resume and job.
    """

    url = f"{BACKEND_URL}/api/career-coach/ask"

    headers = {
        "X-Session-ID": session_id
    }

    payload = {
        "question": question,
        "resume_id": resume_id,
        "job_id": job_id,
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers,
        timeout=180,
    )

    response.raise_for_status()

    return response.json()

def generate_cover_letter(
    resume_id: int,
    job_id: int,
    session_id: str,
) -> dict:
    """
    Generate a Cover Letter for a selected
    saved resume and job description.
    """

    url = f"{BACKEND_URL}/api/cover-letter/generate"

    headers = {
        "X-Session-ID": session_id,
    }

    payload = {
        "resume_id": resume_id,
        "job_id": job_id,
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers,
        timeout=180,
    )

    response.raise_for_status()

    return response.json()