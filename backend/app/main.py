"""Assemble the FastAPI application and connect its HTTP routes.

Incoming requests enter here, then pass to the API router. Routes should hand
product work to domain/application services rather than implement it themselves.
"""

from fastapi import FastAPI

from app.api.router import router
from app.core.config import settings

app = FastAPI(title=settings.app_name)
app.include_router(router)
app.include_router(router, prefix=settings.api_v1_prefix)
