# tests/test_email_extractor.py
# SCRUM-50: Unit tests for EmailExtractor service

import pytest
from src.services.email_extractor import EmailExtractor, review_queue


@pytest.fixture(autouse=True)
def clear_review_queue():
    """Clear the review queue before each test."""
    review_queue.clear()
    yield


@pytest.fixture
def extractor():
    return EmailExtractor()


def test_extract_fields_success(extractor):
    """AC1: All key fields extracted from a valid email."""
    raw = {
        "from":    "sender@example.com",
        "subject": "Test Subject",
        "date":    "2026-09-25",
        "body":    "Hello, this is a test email."
    }
    parsed = extractor.parse_email(raw)
    fields = extractor.extract_fields(parsed)

    assert fields["sender"]  == "sender@example.com"
    assert fields["subject"] == "Test Subject"
    assert fields["date"]    == "2026-09-25"
    assert fields["body"]    == "Hello, this is a test email."


def test_validate_fields_invalid_schema(extractor):
    """AC2: Validation fails and flags item when fields are missing."""
    incomplete_fields = {"sender": "test@example.com", "subject": "Hi"}

    result = extractor.validate_fields(incomplete_fields)

    assert result is False
    assert len(review_queue) == 1
    assert "Missing fields" in review_queue[0]["error"]


def test_flag_failure_on_extraction_error(extractor):
    """AC3: Extraction error results in item flagged to review queue."""
    # Pass None to force an extraction failure
    fields = extractor.extract_fields(None)

    assert fields == {}
    assert len(review_queue) == 1
    assert review_queue[0]["error"] is not None