import pytest
from redactor import redact_email_text

def test_redact_email_text():
    # Sample email text with headers to redact
    sample_text = (
        "From: John Doe <john.doe@example.com>\n"
        "To: Jane Smith <jane.smith@example.com>\n"
        "Cc: admin@example.com\n"
        "Subject: Meeting\n"
        "\n"
        "Hello, this is a message."
    )

    # Target categories and initial stats
    targets = ['names']
    stats = {'names': 0}

    # Updated expected redaction spans based on character positions in sample_text
    expected_spans = [
        (6, 14),  # "John Doe" in From header
        (16, 20),  # "john" in email address local part
        (21, 24),  # "doe" in email address local part
        (42, 52),  # "Jane Smith" in To header
        (54, 58),  # "jane" in email address local part
        (59, 64),  # "smith" in email address local part
        (82, 87)   # "admin" in Cc email address local part
    ]

    # Call the function
    redaction_spans = redact_email_text(sample_text, targets, stats)

    # Assertions for redaction spans
    assert redaction_spans == expected_spans, f"Expected {expected_spans} but got {redaction_spans}"

    # Assertions for stats
    assert stats['names'] == 7, f"Expected 7 names redacted, but got {stats['names']}"
