from api.deps import get_embedder, get_legal_agent, get_risk_engine
from samvidai.retrieval.embedding import EmbeddingModel
from samvidai.llm.agents.legal_agent import LegalAgent
from samvidai.risk_engine.classifier import RiskClassifier
from samvidai.risk_engine.scorer import RiskScorer


def test_embedder_is_fresh():
    e1 = get_embedder()
    e2 = get_embedder()
    assert isinstance(e1, EmbeddingModel)
    assert e1 is not e2


def test_legal_agent_instance():
    agent = get_legal_agent()
    assert isinstance(agent, LegalAgent)


def test_risk_engine_components():
    classifier, scorer = get_risk_engine()
    assert isinstance(classifier, RiskClassifier)
    assert isinstance(scorer, RiskScorer)
