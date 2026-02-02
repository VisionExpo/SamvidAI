from samvidai.risk_engine.classifier import classify_clause

def test_detects_termination_risk():
    text = "The contract may be terminated without notice."
    risks = classify_clause(text)
    assert "termination" in risks
