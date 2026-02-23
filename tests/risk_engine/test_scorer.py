from samvidai.risk_engine.scorer import RiskScorer


def test_high_risk_scoring():
    """Test scoring with HIGH risk clauses."""
    scorer = RiskScorer()
    clause_levels = ["HIGH", "HIGH", "MEDIUM"]
    result = scorer.score(clause_levels)
    
    assert result["risk_score"] >= 70
    assert result["risk_level"] == "HIGH"
    assert result["clauses_analyzed"] == 3


def test_medium_risk_scoring():
    """Test scoring with MEDIUM risk clauses."""
    scorer = RiskScorer()
    clause_levels = ["MEDIUM", "MEDIUM", "LOW"]
    result = scorer.score(clause_levels)
    
    assert 40 <= result["risk_score"] < 70
    assert result["risk_level"] == "MEDIUM"
    assert result["clauses_analyzed"] == 3


def test_low_risk_scoring():
    """Test scoring with LOW risk clauses."""
    scorer = RiskScorer()
    clause_levels = ["LOW", "LOW", "LOW"]
    result = scorer.score(clause_levels)
    
    assert result["risk_score"] < 40
    assert result["risk_level"] == "LOW"
    assert result["clauses_analyzed"] == 3


def test_empty_clause_levels():
    """Test scoring with no clauses."""
    scorer = RiskScorer()
    result = scorer.score([])
    
    assert result["risk_score"] == 0
    assert result["risk_level"] == "LOW"
