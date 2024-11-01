import pytest
from unittest.mock import patch

# Assuming redact_entities_hf is defined in redactor.py
from redactor import redact_entities_hf

# Sample text and mock response from hf_ner_pipeline
sample_text = "John lives in New York."
mock_ner_results = [
    {'entity_group': 'PER', 'start': 0, 'end': 4},  # "John" - Person entity
    {'entity_group': 'LOC', 'start': 14, 'end': 22} # "New York" - Location entity
]

def test_redact_entities_hf():
    # Define targets and initialize stats
    targets = ['names', 'addresses']
    stats = {'names': 0, 'addresses': 0}

    # Patch hf_ner_pipeline to return mock_ner_results
    with patch('redactor.hf_ner_pipeline', return_value=mock_ner_results):
        # Call the function
        redaction_spans = redact_entities_hf(sample_text, targets, stats)
        
        # Assertions for redaction spans
        assert redaction_spans == [(0, 4), (14, 22)], "Redaction spans do not match expected output."

        # Assertions for stats dictionary
        assert stats['names'] == 1, "Names redaction count incorrect in stats."
        assert stats['addresses'] == 1, "Addresses redaction count incorrect in stats."
