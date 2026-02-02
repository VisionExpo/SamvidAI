from samvidai.risk_engine.scorer import score_risks, risk_level
from domain.enums import RiskLevel

def test_risk_scoring():
    risks = ["termination", "liability"]
    score = score_risks(risks)
    level = risk_level(score)

    assert score == 2
    assert level == RiskLevel.HIGH