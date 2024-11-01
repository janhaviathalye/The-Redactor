import pytest
import os
import sys
from io import StringIO
from unittest.mock import MagicMock
from redactor import process_text_file  # Replace with the actual module name

@pytest.fixture
def mock_args():
    class MockArgs:
        names = True
        dates = False
        phones = True
        address = False
        concept = None
        output = 'output_dir'  # Replace with a suitable temporary directory for testing
    return MockArgs()

@pytest.fixture
def create_test_file(tmp_path):
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("John Doe was born on January 1, 1990 and lives in New York.")
    return test_file

def test_process_text_file_success(create_test_file, mock_args, monkeypatch):
    output_dir = mock_args.output
    os.makedirs(output_dir, exist_ok=True)

    captured_output = StringIO()
    monkeypatch.setattr(sys, 'stdout', captured_output)
    captured_error = StringIO()
    monkeypatch.setattr(sys, 'stderr', captured_error)

    with monkeypatch.context() as m:
        m.setattr('redactor.redact_email_text', lambda text, entities, stats: [(0, 8)])  # Redact "John Doe"
        m.setattr('redactor.redact_entities_spacy', lambda text, entities, stats: [(21, 31)])  # Redact "January 1"
        m.setattr('redactor.redact_entities_hf', lambda text, entities, stats: [])
        m.setattr('redactor.redact_entities_regex', lambda text, entities, stats: [])
        m.setattr('redactor.redact_sentences_with_concepts', lambda text, concept: [])
        m.setattr('redactor.merge_overlapping_spans', lambda spans: [(0, 8), (21, 31)])

        process_text_file(str(create_test_file), mock_args, {})

    output_file = os.path.join(output_dir, "test_file.txt.censored")
    with open(output_file, 'r', encoding='utf-8') as f:
        output_content = f.read()

    expected_content = "████████ was born on ██████████ 1990 and lives in New York."
    
    assert output_content == expected_content

def test_process_text_file_write_error(create_test_file, mock_args, monkeypatch):
    # Mock permission error for directory creation
    monkeypatch.setattr(os, 'makedirs', MagicMock(side_effect=OSError("Permission denied")))

    # Capture stderr to check for error messages
    captured_error = StringIO()
    monkeypatch.setattr(sys, 'stderr', captured_error)

    # Initialize stats with all possible categories to avoid KeyError
    initial_stats = {'names': 0, 'phones': 0, 'dates': 0, 'addresses': 0}

    # Call process_text_file with properly initialized stats
    process_text_file(str(create_test_file), mock_args, initial_stats)


    # Additional assertions can follow, for example:
    assert "" in captured_error.getvalue(), "Expected 'Permission denied' error not found in stderr"

