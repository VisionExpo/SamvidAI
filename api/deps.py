from dotenv import load_dotenv

load_dotenv()


from samvidai.retrieval.embedding import EmbeddingModel
from samvidai.llm.providers.gemini_provider import GeminiProvider
from samvidai.llm.agents.legal_agent import LegalAgent
from samvidai.risk_engine.classifier import RiskClassifier
from samvidai.risk_engine.scorer import RiskScorer


def get_embedder():
    return EmbeddingModel()


def get_legal_agent():
    provider = GeminiProvider()
    return LegalAgent(provider)


def get_risk_engine():
    return RiskClassifier(), RiskScorer()
