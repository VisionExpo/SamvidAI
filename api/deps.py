import os

from samvidai.llm.providers.gemini_provider import GeminiProvider
from samvidai.llm.providers.mock_provider import MockProvider
from samvidai.llm.agents.legal_agent import LegalAgent
from samvidai.retrieval.embedding import EmbeddingModel
from samvidai.risk_engine.classifier import RiskClassifier
from samvidai.risk_engine.scorer import RiskScorer


def get_embedder():
    return EmbeddingModel()


def get_legal_agent():
    # Always use Gemini provider if API key is available
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set in environment")
    
    provider = GeminiProvider()
    return LegalAgent(provider)


def get_risk_engine():
    return RiskClassifier(), RiskScorer()
