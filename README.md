# EvidenceOS

EvidenceOS is being developed as a local-first platform for document ingestion, evidence retrieval, cited answers, and claim verification. The repository currently contains an initial FastAPI backend scaffold; the product workflows are not implemented yet.

Architecture and current implementation status: [MVP architecture](docs/architecture/mvp-architecture.md).

## Prerequisites

- Windows PowerShell
- Python 3.11 or newer
- [uv](https://docs.astral.sh/uv/) for Python environment and dependency management

## Set up the backend from a clean checkout

From the repository root, enter the backend directory and install the project and development dependencies:

```
cd .\backend
uv sync
```

uv creates and uses the project's `.venv` automatically. You do not need to activate it.
Create a local environment file from the safe template.

## Run tests

From `backend\`:

```
uv run pytest
```

## Start the API locally

From `backend\`, start the development server:

```
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

## Configuration and current limits

The backend reads application settings from environment variables with the `EVIDENCEOS_` prefix. See [`backend/.env.example`](backend/.env.example) for the settings currently supported.
