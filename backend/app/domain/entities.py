"""Define starter product types used throughout ingestion and evidence flow.

`DocumentStatus` describes ingestion lifecycle. `SourceSpan` identifies where
text came from, so future chunks and citations can resolve to exact versions
and offsets. These are domain values, not database or HTTP schemas.
"""

from dataclasses import dataclass
from enum import StrEnum


class DocumentStatus(StrEnum):
    QUEUED = "queued"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"


@dataclass(frozen=True)
class SourceSpan:
    document_version_id: str
    start_offset: int
    end_offset: int
    page_number: int | None = None

    def __post_init__(self) -> None:
        if self.start_offset < 0 or self.end_offset < self.start_offset:
            raise ValueError("Source span offsets must be non-negative and ordered")
