"""Expose a liveness check so operators can confirm the API process responds.

This route does not read documents or prove that database, storage, or model
dependencies are ready; readiness checks can be added when those exist.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["health"])
def health() -> dict[str, str]:
    """Report that the API process is responding."""
    return {"status": "ok"}
