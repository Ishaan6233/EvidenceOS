"""Collect route modules for the unversioned and `/api/v1` API paths.

`main.py` mounts this router. As document, search, answer, and verification
routes are added, register them here so the HTTP boundary stays in one place.
"""

from fastapi import APIRouter

from app.api.routes.health import router as health_router

router = APIRouter()
router.include_router(health_router)
