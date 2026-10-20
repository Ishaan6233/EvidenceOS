# API errors and observability conventions

**Status:** Proposed conventions; only the health routes are currently implemented.
**Related issue:** [#3 — ENG-02](https://github.com/Ishaan6233/EvidenceOS/issues/3)

## Error responses

API errors use a stable JSON envelope:

```json
{
  "error": {
    "code": "not_found",
    "message": "The requested resource was not found."
  },
  "request_id": "a-correlation-id"
}
```

Clients should branch on the stable `error.code`, not parse human-readable messages. Validation errors return a `fields` array containing field locations and validator types. Submitted field values, document contents, credentials, internal exception text, and stack traces are not returned to clients. Unexpected server failures use HTTP 500 and the generic `internal_error` code.

Expected application failures should be raised as `APIError(status_code, code, message)` with a deliberately safe public message. Framework HTTP errors are mapped to stable codes and messages. New public error codes should be added to the API documentation and contract tests.

## Request correlation and logs

- Every request receives an `X-Request-ID` response header. A client-supplied ID is accepted only when it is 1–64 characters from `[A-Za-z0-9._-]`; otherwise the server generates a UUID.
- EvidenceOS access logs are JSON lines with timestamp, level, event, request ID, method, path, status, and elapsed milliseconds.
- Logs must not include request or response bodies, authorization headers, query strings, document text, prompts, retrieved evidence, or secrets by default.
- Error logs use stable error codes. Unhandled exceptions log the exception class, not exception text or traceback, to avoid accidentally copying sensitive values into logs. Operational diagnostics may be expanded only with explicit sanitization.
- Audit events are a separate domain record for security-relevant actions; they are not a substitute for application logs and should store only the minimum necessary metadata.

## Health and readiness

- `GET /health` and `GET /api/v1/health` are implemented liveness endpoints. HTTP 200 with `{"status":"ok"}` means only that the API process is responding.
- Readiness is **not implemented**. Do not report database, object storage, worker, or model readiness until the corresponding dependency is integrated and checked.
- Once stateful dependencies exist, readiness should check only required dependencies with bounded timeouts and should return a non-200 status while the instance cannot safely serve its advertised operations.

## Implementation scope

The current scaffold does not yet add request IDs, structured access/error logs, or a shared error response handler. Metrics, distributed tracing, persistent audit events, alerting, and dependency readiness checks also remain future work. No telemetry backend is selected yet.
