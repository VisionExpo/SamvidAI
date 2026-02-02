from typing import List
from samvidai.retrieval.embeddings import EmbeddingModel
from samvidai.retrieval.vector_store import VectorStore


class Retriever:
    """
    Semantic retriever for OpticalRAG
    """

    def __init__(self):
        self.embedder = EmbeddingModel()
        self.store = VectorStore(dim=self.embedder.dim)

    def index(self, texts: List[str]):
        vectors = self.embedder.encode(texts)
        self.store.add(vectors, texts)

    def retrieve(self, query: str, top_k: int = 5) -> List[str]:
        query_vec = self.embedder.encode([query])
        return self.store.search(query_vec, top_k=top_k)
