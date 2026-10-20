"""FastAPI application entry point."""

from fastapi import FastAPI

from app.api.router import router
from app.core.config import settings

app = FastAPI(title=settings.app_name)
app.include_router(router)
app.include_router(router, prefix=settings.api_v1_prefix)
