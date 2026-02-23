from samvidai.utils.guardrails import has_sufficient_context

def test_guard_blocks_empty_context():
    assert not has_sufficient_context([])

def test_guard_allows_valid_context():
    # Must be at least 50 chars (MIN_CONTEXT_CHARS)
    context = ["This agreement may be terminated with notice after a 30-day period."]
    assert has_sufficient_context(context)
