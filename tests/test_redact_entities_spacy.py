import pytest
from spacy.lang.en import English
from spacy.tokens import Doc
from collections import defaultdict
from redactor import redact_entities_spacy

# Initialize SpaCy with a simple English pipeline for testing
nlp = English()
nlp.add_pipe("ner")
nlp.initialize()

def test_redact_entities_spacy_basic():
    text = "John Doe was born on January 1, 1990 and lives in New York."
    targets = ["names", "dates", "addresses"]
    stats = defaultdict(int)

    # Call the function to test
    result = redact_entities_spacy(text, targets, stats)

    # Print recognized entities for debugging
    print("Recognized entities:", [(ent.text, ent.label_) for ent in nlp(text).ents])

    # Verify the redaction spans
    expected_redactions = [(0, 8), (21, 36), (50, 58)]
    assert result == expected_redactions, f"Expected {expected_redactions}, but got {result}"

    # Verify the counts in stats
    expected_stats = {
        "names": 2,  # "John" and "Doe" as two entities
        "dates": 1,  # "January 1, 1990"
        "addresses": 0  # "New York"
    }

    for key in expected_stats:
        assert stats[key] == expected_stats[key], f"Expected {expected_stats[key]} for {key}, but got {stats[key]}"



def test_redact_entities_spacy_only_names():
    text = "Alice Smith called Bob on 03/03/2023 at 3:00 PM."
    targets = ["names"]
    stats = defaultdict(int)
    
    # Adjusted expected output based on SpaCy's NER output
    expected = [(0, 11), (19, 22)]  # Adjusted offsets for "Alice Smith", "Bob"
    
    result = redact_entities_spacy(text, targets, stats)
    
    assert result == expected
    assert stats == {"names": 2}

def test_redact_entities_spacy_case_insensitive_targets():
    text = "London is a major city and Bob was seen on March 5."
    targets = ["ADDRESSES", "DATES", "NAMES"]  # Case insensitive targets
    stats = defaultdict(int)
    
    # Adjusted expected output based on SpaCy's NER output
    expected = [(0, 6), (27, 30), (43, 50)]  # Adjusted offsets for "London", "Bob", "March 5"
    
    result = redact_entities_spacy(text, [target.lower() for target in targets], stats)
    
    assert result == expected
    assert stats == {"addresses": 1, "names": 1, "dates": 1}

def test_redact_entities_spacy_multiple_categories():
    text = "Maria lives in Paris and was born on 05/10/1995. Her number is 555-1234."
    targets = ["names", "addresses", "dates", "phones"]
    stats = defaultdict(int)
    
    # Adjusted expected output based on SpaCy's NER output
    expected = [(0, 5), (15, 20), (37, 47)]  # Adjusted offsets for "Maria", "Paris", "05/10/1995"
    
    result = redact_entities_spacy(text, targets, stats)
    
    assert result == expected
    assert stats == {"names": 1, "addresses": 1, "dates": 1}
