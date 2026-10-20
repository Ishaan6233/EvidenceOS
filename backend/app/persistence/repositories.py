"""Describe how domain/application services will request persisted data.

Services call these repository contracts after API authorization; concrete
PostgreSQL implementations are future work and must scope every lookup by tenant.
"""

from typing import Protocol


class DocumentRepository(Protocol):
    def get_status(self, tenant_id: str, document_id: str) -> str | None:
        """Return a tenant-scoped lifecycle status, or None when absent."""
        ...
