from samvidai.utils.guardrails import has_sufficient_context

def test_guard_blocks_empty_context():
    assert not has_sufficient_context([])

def test_guard_allows_valid_context():
    context = ["This agreement may be terminated with notice."]
    assert has_sufficient_context(context)
