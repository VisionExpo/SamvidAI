from api.deps import get_retriever, get_legal_agent
from samvidai.retrieval import Retriever
from samvidai.llm.agents import LegalAgent

def test_retriever_is_fresh():
    r1 = get_retriever()
    r2 = get_retriever()
    assert isinstance(r1, Retriever)
    assert r1 is not r2

def test_legal_agent_instance():
    agent = get_legal_agent()
    assert isinstance(agent, LegalAgent)