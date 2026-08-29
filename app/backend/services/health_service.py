def get_health_status() -> dict:
    """
    Return the current API health status.
    """

    return {
        "status": "healthy",
        "service": "Resume Genie API",
    }
