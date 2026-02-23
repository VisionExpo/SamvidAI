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
    provider_name = os.getenv("LLM_PROVIDER", "gemini").lower()

    if provider_name == "mock":
        provider = MockProvider()
    else:
        # Use mock if no API key is set
        if not os.getenv("GEMINI_API_KEY"):
            provider = MockProvider()
        else:
            provider = GeminiProvider()

    return LegalAgent(provider)


def get_risk_engine():
    return RiskClassifier(), RiskScorer()
