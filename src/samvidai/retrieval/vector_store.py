import faiss
import numpy as np
from typing import List


class VectorStore:
    """
    In-memory FAISS vector store for contract clauses
    """

    def __init__(self, dim: int):
        self.index = faiss.IndexFlatL2(dim)
        self.texts: List[str] = []

    def add(self, vectors, texts: List[str]):
        if len(vectors) != len(texts):
            raise ValueError("Vectors and texts length mismatch")

        self.index.add(np.array(vectors))
        self.texts.extend(texts)

    def search(self, query_vector, top_k: int = 5) -> List[str]:
        _, indices = self.index.search(query_vector, top_k)
        return [self.texts[i] for i in indices[0]]
