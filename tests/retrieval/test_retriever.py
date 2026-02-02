from samvidai.retrieval import Retriever

def test_retriever_index_and_search():
    retriever = Retriever()
    clauses = [
        {"clause_id": "C1", "text": "Termination with notice"},
        {"clause_id": "C2", "text": "Payment terms"},
    ]

    retriever.index(clauses)
    results = retriever.retrieve("termination")

    assert len(results) > 0
    assert "termination" in results[0]["text"].lower()
