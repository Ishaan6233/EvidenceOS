"""Persistence contracts. Concrete PostgreSQL adapters are future work."""

from typing import Protocol


class DocumentRepository(Protocol):
    def get_status(self, tenant_id: str, document_id: str) -> str | None:
        """Return a tenant-scoped lifecycle status, or None when absent."""
        ...
