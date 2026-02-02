import faiss
import numpy as np
from typing import List, Dict


class VectorStore:
    """
    FAISS vector store with clause metadata
    """

    def __init__(self, dim: int):
        self.index = faiss.IndexFlatL2(dim)
        self.records: List[Dict] = []

    def add(self, vectors, records: List[Dict]):
        if len(vectors) != len(records):
            raise ValueError("Vectors and records length mismatch")

        self.index.add(np.array(vectors))
        self.records.extend(records)

    def search(self, query_vector, top_k: int = 5) -> List[Dict]:
        _, indices = self.index.search(query_vector, top_k)
        return [self.records[i] for i in indices[0]]
