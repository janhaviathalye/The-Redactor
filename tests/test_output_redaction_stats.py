import pytest
import sys
import os
from io import StringIO
from redactor import output_redaction_stats  # Replace with the actual module name

def test_output_redaction_stats_stdout(monkeypatch):
    stats = {
        "names": 2,
        "dates": 1,
        "phones": 0,
        "addresses": 1,
        "concepts": 3
    }

    # Capture stdout
    captured_output = StringIO()
    monkeypatch.setattr(sys, 'stdout', captured_output)

    output_redaction_stats(stats, 'stdout')

    # Check if the captured output matches expected output
    expected_output = (
        "Names redacted: 2\n"
        "Dates redacted: 1\n"
        "Phone numbers redacted: 0\n"
        "Addresses redacted: 1\n"
        "Concepts redacted: 3\n"
    )
    
    assert captured_output.getvalue() == expected_output

def test_output_redaction_stats_stderr(monkeypatch):
    stats = {
        "names": 2,
        "dates": 1,
        "phones": 0,
        "addresses": 1,
        "concepts": 3
    }

    # Capture stderr
    captured_output = StringIO()
    monkeypatch.setattr(sys, 'stderr', captured_output)

    output_redaction_stats(stats, 'stderr')

    # Check if the captured output matches expected output
    expected_output = (
        "Names redacted: 2\n"
        "Dates redacted: 1\n"
        "Phone numbers redacted: 0\n"
        "Addresses redacted: 1\n"
        "Concepts redacted: 3\n"
    )

    assert captured_output.getvalue() == expected_output

def test_output_redaction_stats_file(monkeypatch, tmp_path):
    stats = {
        "names": 2,
        "dates": 1,
        "phones": 0,
        "addresses": 1,
        "concepts": 3
    }

    # Create a temporary file
    temp_file = tmp_path / "stats_report.txt"

    output_redaction_stats(stats, str(temp_file))

    # Check if the file contains the correct output
    expected_output = (
        "Names redacted: 2\n"
        "Dates redacted: 1\n"
        "Phone numbers redacted: 0\n"
        "Addresses redacted: 1\n"
        "Concepts redacted: 3\n"
    )

    with open(temp_file, 'r', encoding='utf-8') as f:
        file_content = f.read()
    
    assert file_content == expected_output
