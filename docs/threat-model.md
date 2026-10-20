# EvidenceOS threat model

**Status:** Design baseline; mitigations marked planned are not yet implemented.
**Related issue:** [#6 — DOC-02](https://github.com/Ishaan6233/EvidenceOS/issues/6)

## Scope and security goals

This model covers the MVP document ingestion, retrieval, answer, citation, and claim-verification workflow. It assumes a multi-tenant service even though authentication and persistence are not implemented in the current scaffold.

Security goals:

- A tenant can access only its own documents, chunks, jobs, answers, evidence, and object bytes.
- Citations resolve to immutable document versions and source spans; stale or deleted evidence is not served.
- Untrusted document text cannot change system policy, authorization, or provider-egress configuration.
- Local-only mode makes no external model request and has no external fallback.
- Sensitive source text, credentials, and prompts are excluded from routine logs.
- Security-relevant actions can be audited without copying unnecessary document contents.

## Assets

| Asset | Confidentiality / integrity concern |
|---|---|
| Original document bytes and extracted text | Confidentiality; integrity and version consistency |
| Tenant, collection, document, and job metadata | Cross-tenant confidentiality; lifecycle correctness |
| Embeddings, lexical indexes, caches | Tenant isolation; stale or deleted content |
| Questions, answers, citations, claims, evidence links | Confidentiality; source attribution integrity |
| Provider credentials and egress policy | Secret confidentiality; policy integrity |
| Audit events and operational logs | Sensitive metadata disclosure; tampering |
| Evaluation corpora and relevance labels | Access control and result integrity |

## Trust boundaries

1. **User/client to API:** requests, uploaded files, IDs, and questions are untrusted. Authentication and server-side authorization must be applied before resource access.
2. **API/worker to PostgreSQL:** database access must use tenant-scoped repository methods and transactional lifecycle changes. Derived search data must retain tenant and version identity.
3. **Application to object storage:** object keys are opaque references, not authorization. Access is mediated by the application/storage adapter, with tenant scoping and deletion reconciliation.
4. **Worker/parser to extracted text:** document contents can be malformed, oversized, exploit parser bugs, or contain adversarial instructions. Parsing must have limits and treat text as data.
5. **Application to model providers:** an external provider is a separate trust domain. Only configured and policy-permitted context may cross this boundary.
6. **Application to logs/telemetry:** logs and traces are separately accessible systems. They must not capture bodies, prompts, secrets, or evidence text by default.

## Threat actors

- An unauthenticated or low-privilege user attempting to access another tenant's data.
- A malicious tenant submitting crafted documents or prompt-injection instructions.
- A compromised or misconfigured worker, provider credential, or storage identity.
- An external model provider receiving explicitly shared context under the configured service terms.
- An operator or attacker with access to logs, backups, indexes, or deployment configuration.

## Threats and controls

| Threat | Required mitigation | Current status / residual risk |
|---|---|---|
| Cross-tenant IDOR through document, job, answer, or citation IDs | Derive tenant identity from authenticated context; scope every repository, object, search, cache, and verification operation; test cross-tenant denial | Planned; authentication and data paths are not implemented |
| Tenant filter applied after global retrieval | Apply tenant/permission predicates inside every retrieval backend before candidates reach reranking or model context | Planned; retrieval is not implemented |
| Prompt injection in uploaded or retrieved text | Treat all document text as quoted/untrusted evidence; keep system policy outside retrieved content; never let content alter tools, authorization, or egress policy | Planned; prompt handling is not implemented |
| External disclosure under local-only configuration | Enforce egress policy at provider gateway and transport boundary; fail closed; test with outbound-request interception | Policy decided; gateway/tests not implemented |
| Unintended disclosure when external generation is enabled | Require explicit provider/model and permitted context class; disclose provider boundary; minimize context; audit policy decision | Planned. External generation necessarily sends permitted context to that provider; zero third-party disclosure is not claimed |
| Forged citations or unsupported claims | Resolve citations to stored chunk/version/span; independently verify claim evidence; permit insufficient-evidence and review-required outcomes | Planned; citation and verification logic not implemented |
| Stale evidence after deletion or re-ingestion | Version immutable source records; invalidate jobs/caches; remove lexical/vector records; reconcile partial failures; test deleted content cannot be retrieved | Planned; persistence/index lifecycle not implemented |
| Malformed or hostile document parser input | Validate type/size, sandbox or isolate parsing where practical, impose resource/time limits, handle parser failure without marking ready | Planned; parser not implemented |
| Secrets or evidence in logs | Structured allowlisted fields only; sanitize error codes; exclude bodies, credentials, prompt/context text, and query strings | Basic scaffold convention documented; production telemetry not implemented |
| Job replay or partial indexing | Atomic job leases, bounded retries, idempotent stage keys, state transitions, recovery tests | Planned; job system not implemented |
| Object-key disclosure or direct object bypass | Keep object keys opaque, mediate reads through authorization, scope service credentials, reconcile deletes | Planned; storage adapter not implemented |
| Resource exhaustion via uploads/queries | Bound file size, parser work, query sizes, concurrent jobs, provider timeouts, and retry rate | Planned; limits not yet implemented |

## MVP security validation

Before release, automate tests for cross-tenant document/job/search/answer access; malicious prompt-injection fixtures; forbidden egress in local-only mode; secrets and document text absent from captured logs; citation resolution to correct source versions; and deletion/re-ingestion removing stale search results. Failure cases must fail closed and must not expose protected content.

## Residual risks and assumptions

- The current backend is a small unauthenticated health/API scaffold. It is not suitable for sensitive or multi-tenant production data.
- Managed PostgreSQL and object storage introduce operator, identity, backup, residency, and retention risks that depend on deployment configuration.
- If external generation is enabled, provider terms and processing controls apply to the context sent. Application-side minimization does not make that disclosure zero.
- Prompt-injection mitigations reduce risk but cannot guarantee that model behavior is fully reliable. High-impact decisions need human review.
- This threat model must be updated when authentication, providers, deployment, or data flows change.
