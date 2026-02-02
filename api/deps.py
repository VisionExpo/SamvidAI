"""
Shared FastAPI dependencies for SamvidAI.
Centralized here to avoid circular imports and duplication.
"""

from samvidai.llm.agents import LegalAgent
from samvidai.retrieval import Retriever


def get_legal_agent() -> LegalAgent:
    """
    Dependency provider for LegalAgent.
    Stateless, safe to reuse.
    """
    return LegalAgent()


def get_retriever() -> Retriever:
    """
    Dependency provider for Retriever.
    IMPORTANT: returns a fresh instance per request
    to avoid cross-request vector pollution.
    """
    return Retriever()
