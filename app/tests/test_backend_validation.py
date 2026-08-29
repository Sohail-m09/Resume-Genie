import pytest
from fastapi import HTTPException

from backend.services.request_validation import (
    validate_job_input,
)


def test_job_text_only():
    validate_job_input(
        job_text="Junior Data Scientist with Python and SQL.",
        job_pdf_path=None,
    )


def test_job_pdf_only():
    validate_job_input(
        job_text=None,
        job_pdf_path="data/Data_Scientist_JD.pdf",
    )


def test_both_job_inputs_rejected():
    with pytest.raises(HTTPException) as exc:

        validate_job_input(
            job_text="Junior Data Scientist with Python and SQL.",
            job_pdf_path="data/Data_Scientist_JD.pdf",
        )

    assert exc.value.status_code == 400


def test_missing_job_input_rejected():
    with pytest.raises(HTTPException) as exc:

        validate_job_input(
            job_text=None,
            job_pdf_path=None,
        )

    assert exc.value.status_code == 400
