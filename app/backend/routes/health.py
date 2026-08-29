from fastapi import APIRouter

from backend.services.health_service import (
    get_health_status,
)


router = APIRouter(
    prefix="/api",
    tags=["Health"],
)


@router.get("/health")
def health_check():
    """
    Check whether the Resume Genie API is running.
    """

    return get_health_status()

