"""Small initial domain types; persistence schemas belong in adapters."""

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
