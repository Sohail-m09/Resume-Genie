from fastapi import FastAPI

from backend.routes.health import (
    router as health_router,
)
from backend.routes.resume import (
    router as resume_router,
)
from backend.routes.job_api import (
    router as job_router,
)
from backend.routes.analysis import (
    router as analysis_router,
)
from backend.routes.career_coach import (
    router as career_coach_router,
)
from backend.routes.tailored_resume import (
    router as tailored_resume_router,
)
from backend.routes.ats import (
    router as ats_router,
)
from backend.routes.pdf import (
    router as pdf_router,
)
from backend.routes.resume_genie import (
    router as resume_genie_router,
)
from backend.routes.history import (
    router as history_router,
)

app = FastAPI(
    title="Resume Genie API",
    description="Backend API for the Resume Genie application.",
    version="1.0.0",
)


app.include_router(
    health_router,
)

app.include_router(
    resume_router,
)

app.include_router(
    job_router,
)
app.include_router(
    analysis_router,
)
app.include_router(
    career_coach_router,
)
app.include_router(
    tailored_resume_router,
)
app.include_router(
    ats_router,
)
app.include_router(
    pdf_router,
)
app.include_router(
    resume_genie_router,
)
app.include_router(
    history_router,
)