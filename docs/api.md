# EvidenceOS API conventions

**Status:** Contract baseline; product endpoints below are planned unless marked implemented.
**Related issue:** [#7 — DOC-03](https://github.com/Ishaan6233/EvidenceOS/issues/7)

## Conventions

- Product endpoints are versioned under `/api/v1`.
- JSON request and response bodies use `snake_case` field names.
- IDs are opaque identifiers. Tenant identity comes from authenticated server context, never from a client-supplied tenant ID alone.
- Timestamps use ISO 8601 UTC. Document references include immutable document version IDs.
- Collection/document filtering must be authorized server-side before retrieval or source text is returned.
- FastAPI publishes the generated OpenAPI document at `/openapi.json` and interactive docs at `/docs` while the application is running.
- Pagination, idempotency, and upload limits must be defined by each endpoint before implementation; this scaffold does not yet expose product APIs.

## Current endpoint inventory

| Method | Path | Status | Contract |
|---|---|---|---|
| GET | `/health` | Implemented | Liveness only; returns `{"status":"ok"}` |
| GET | `/api/v1/health` | Implemented | Versioned liveness only; same response |
| GET | `/openapi.json` | Implemented by FastAPI | OpenAPI document for currently registered routes |
| GET | `/docs` | Implemented by FastAPI | Interactive API docs for currently registered routes |

Liveness does not prove PostgreSQL, object storage, worker, or model readiness. Readiness is not implemented.

## Planned MVP endpoint inventory

These are design targets and are **not implemented** in the current scaffold.

| Method | Path | Purpose | Success response (planned) |
|---|---|---|---|
| POST | `/api/v1/documents` | Stream and register a document upload | `202` with `document_id`, `version_id`, `job_id`, and `status` |
| GET | `/api/v1/documents` | List authorized documents, optionally filtered by collection/status | `200` with paginated document summaries |
| GET | `/api/v1/documents/{document_id}` | Read document metadata and current processing state | `200` with document/version metadata |
| DELETE | `/api/v1/documents/{document_id}` | Request deletion and derived-index cleanup | `202` with deletion job/status |
| GET | `/api/v1/jobs/{job_id}` | Read authorized ingestion job status | `200` with state, attempts, timestamps, and safe error code |
| POST | `/api/v1/search` | Retrieve evidence within an authorized collection scope | `200` with ranked chunk references and source locations |
| POST | `/api/v1/answers` | Create an answer from retrieved evidence | `202` or `200` per chosen sync/async execution contract; response includes answer ID and state |
| GET | `/api/v1/answers/{answer_id}` | Read answer, validated citations, claims, and verification | `200` with persisted result and provenance |
| POST | `/api/v1/answers/{answer_id}/verification` | Request independent claim verification when deferred/retryable | `202` with verification job/state |
| GET | `/health` | Liveness | `200` when the API process responds |
| GET | `/ready` | Dependency readiness | Not yet designed as a contract; implement only once dependencies exist |

The answer endpoint's synchronous/asynchronous behavior is an unresolved contract decision. Choose one before implementing `POST /answers`; do not return different semantics implicitly based on provider latency.

## Evidence and provenance shapes (planned)

A search result, a citation, and an evidence link have different meanings and should not be represented by one generic “source” object.

- **Search result:** `chunk_id`, `document_id`, `document_version_id`, rank/score, excerpt, and source location. It indicates relevance only.
- **Citation:** `document_id`, `document_version_id`, `chunk_id`, and validated span/page reference used by the answer. Client-provided or model-generated IDs must be resolved against stored authorized records.
- **Claim:** stable claim ID, exact claim text, answer span offsets, and verification state.
- **Verification:** verdict (`supported`, `contradicted`, `insufficient_evidence`, or `review_required`), evidence-link IDs, verifier/configuration identifier, and optional operational execution state.
- **Evidence link:** claim ID, source chunk/version, source span, and relation to the claim. It must be tenant-scoped and resolvable after the response is stored.

Exact persisted entity schemas remain subject to the metadata schema issue (#4); request/response schemas should be finalized alongside API implementation in issue #18.

## Error model

The target error contract uses the envelope below. It is not yet wired into the current FastAPI scaffold. Clients should branch on `error.code`; messages are safe for display but are not stable identifiers.

```json
{
  "error": {
    "code": "not_found",
    "message": "The requested resource was not found."
  },
  "request_id": "correlation-id"
}
```

Validation failures use HTTP 422 and may include a `fields` array of field locations and validator types. Values, document contents, credentials, prompts, and internal exception details are not echoed. Unexpected failures return a generic `internal_error` with HTTP 500. Authorization failures must not reveal whether another tenant's resource exists.

Initial stable error codes: `bad_request`, `unauthorized`, `forbidden`, `not_found`, `conflict`, `payload_too_large`, `unsupported_media_type`, `validation_error`, `rate_limited`, `request_failed`, and `internal_error`.

## Links

- [Live OpenAPI JSON](http://127.0.0.1:8000/openapi.json) (available only when the local API is running)
- [Interactive API docs](http://127.0.0.1:8000/docs) (available only when the local API is running)
- [Error and observability conventions](observability.md)
- [MVP architecture](architecture/mvp-architecture.md)
