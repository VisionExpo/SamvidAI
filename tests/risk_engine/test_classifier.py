from samvidai.risk_engine.classifier import RiskClassifier


def test_detects_high_risk_unlimited_liability():
    """Test that unlimited liability clause is classified as HIGH risk."""
    classifier = RiskClassifier()
    text = "Unlimited liability applies to all parties."
    level = classifier.classify_clause(text, "This is HIGH risk.")
    assert level == "HIGH"


def test_detects_high_risk_termination():
    """Test that unilateral termination without cause is HIGH risk."""
    classifier = RiskClassifier()
    text = "Party may terminate at any time without cause."
    level = classifier.classify_clause(text, "This is MEDIUM risk.")
    assert level == "HIGH"


def test_mutual_termination_low_risk():
    """Test that mutual termination is classified as LOW risk."""
    classifier = RiskClassifier()
    text = "Mutual termination by both parties."
    level = classifier.classify_clause(text, "This is HIGH risk.")
    assert level == "LOW"


def test_classify_from_llm_output():
    """Test classification falls back to LLM output when no rule matches."""
    classifier = RiskClassifier()
    text = "Some standard clause text."
    level = classifier.classify_clause(text, "This clause is MEDIUM risk.")
    assert level == "MEDIUM"


def test_default_low_risk():
    """Test default LOW risk when no keywords found."""
    classifier = RiskClassifier()
    text = "Standard payment terms apply."
    level = classifier.classify_clause(text, "Normal clause.")
    assert level == "LOW"
