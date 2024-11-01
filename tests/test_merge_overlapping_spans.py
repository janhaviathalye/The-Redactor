import pytest
from redactor import merge_overlapping_spans  # replace 'your_module' with the actual module name

def test_merge_overlapping_spans_non_overlapping():
    spans = [(0, 5), (10, 15), (20, 25)]
    result = merge_overlapping_spans(spans)
    expected = [(0, 5), (10, 15), (20, 25)]
    assert result == expected

def test_merge_overlapping_spans_overlapping():
    spans = [(0, 5), (3, 10), (9, 15)]
    result = merge_overlapping_spans(spans)
    expected = [(0, 15)]
    assert result == expected

def test_merge_overlapping_spans_adjacent():
    spans = [(0, 5), (5, 10), (10, 15)]
    result = merge_overlapping_spans(spans)
    expected = [(0, 15)]
    assert result == expected

def test_merge_overlapping_spans_mixed():
    spans = [(0, 5), (4, 10), (15, 20), (18, 25)]
    result = merge_overlapping_spans(spans)
    expected = [(0, 10), (15, 25)]
    assert result == expected

def test_merge_overlapping_spans_single_span():
    spans = [(0, 5)]
    result = merge_overlapping_spans(spans)
    expected = [(0, 5)]
    assert result == expected

def test_merge_overlapping_spans_empty():
    spans = []
    result = merge_overlapping_spans(spans)
    expected = []
    assert result == expected

def test_merge_overlapping_spans_identical_spans():
    spans = [(0, 5), (0, 5), (0, 5)]
    result = merge_overlapping_spans(spans)
    expected = [(0, 5)]
    assert result == expected


