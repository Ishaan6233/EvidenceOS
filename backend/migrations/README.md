# PostgreSQL migrations

`0001_initial_schema.sql` defines the first tenant-scoped metadata schema. It is additive and starts a transaction. Apply it to a **disposable, empty PostgreSQL database** with `psql`:

```powershell
psql "$env:EVIDENCEOS_DATABASE_URL" -v ON_ERROR_STOP=1 -f .\migrations\0001_initial_schema.sql
```

The connection string must point to the intended scratch database. This migration does not install PostgreSQL, provision a database, configure production credentials, or connect the FastAPI scaffold to PostgreSQL. Do not apply it to a database containing valuable data without a reviewed backup and migration plan.

The application must set `evidenceos.tenant_id` transaction-locally after authenticating the caller. Tenant predicates and row-level security are defense in depth; RLS does not authenticate a caller, and an application database role able to choose arbitrary tenant settings can still impersonate a tenant. The runtime DB role must not be a superuser or have `BYPASSRLS`.

The schema stores vectors outside this initial metadata migration. Embedding dimensions and retrieval index design remain dependent on the embedding contract and retrieval evaluation; add those in a later versioned migration. PostgreSQL full-text and vector indexes should be introduced with the retrieval implementation.

## Validation still required

Before treating DATA-01 as complete, run the migration against a fresh PostgreSQL instance and verify rollback/failure behavior, constraints, RLS with two tenants, cross-tenant foreign-key rejection, and repeatability through the selected migration runner. The repository does not yet include an automated PostgreSQL migration test or DB repository implementation.
