import pytest

from app.domain.entities import DocumentStatus, SourceSpan


def test_source_span_accepts_valid_offsets_and_page() -> None:
    span = SourceSpan(document_version_id="version-1", start_offset=4, end_offset=12, page_number=2)

    assert span.start_offset == 4
    assert span.end_offset == 12
    assert span.page_number == 2


@pytest.mark.parametrize(
    ("start_offset", "end_offset"),
    [(-1, 2), (3, 2)],
)
def test_source_span_rejects_negative_or_reversed_offsets(
    start_offset: int, end_offset: int
) -> None:
    with pytest.raises(ValueError, match="non-negative and ordered"):
        SourceSpan("version-1", start_offset, end_offset)


def test_document_status_has_expected_lifecycle_values() -> None:
    assert {status.value for status in DocumentStatus} == {
        "queued",
        "processing",
        "ready",
        "failed",
    }
