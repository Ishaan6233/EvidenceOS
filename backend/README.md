# EvidenceOS backend

Initial modular FastAPI scaffold. This provides configuration, health routes, and architectural contracts only; it does not implement database access, ingestion, retrieval, or AI providers.

## Requirements

Python 3.11 or newer.

## Local setup (PowerShell, from this directory)

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Health: <http://127.0.0.1:8000/health> and <http://127.0.0.1:8000/api/v1/health>. OpenAPI UI: <http://127.0.0.1:8000/docs>.
