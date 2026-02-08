import json
from pathlib import Path
import faiss
import numpy as np


class VectorIndex:
    def __init__(self, dim: int):
        # Inner Product similarity
        self.index = faiss.IndexFlatIP(dim)
        self.metadata = []

    def add(self, embeddings: np.ndarray, metadatas: list[dict]):
        if embeddings.ndim != 2:
            raise ValueError("Embeddings must be 2D array")
        self.index.add(embeddings)
        self.metadata.extend(metadatas)

    def search(self, query_embedding: np.ndarray, top_k: int = 5):
        scores, indices = self.index.search(query_embedding, top_k)
        results = []

        for idx, score in zip(indices[0], scores[0]):
            if idx == -1:
                continue
            results.append(
                {
                    "score": float(score),
                    **self.metadata[idx],
                }
            )
        return results

    def save(self, index_path: Path, meta_path: Path):
        faiss.write_index(self.index, str(index_path))
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)

    @classmethod
    def load(cls, index_path: Path, meta_path: Path):
        index = faiss.read_index(str(index_path))
        with open(meta_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)

        obj = cls(index.d)
        obj.index = index
        obj.metadata = metadata
        return obj

    @classmethod
    def build(cls, chunks: list[dict], embedder, output_dir: Path):
        if not chunks:
            raise ValueError("No chunks provided for indexing")

        texts = [c["text"] for c in chunks]
        embeddings = embedder.encode(texts)
        embeddings = np.asarray(embeddings, dtype="float32")

        # Normalize for cosine similarity via inner product
        faiss.normalize_L2(embeddings)

        dim = embeddings.shape[1]
        index = cls(dim)
        index.add(embeddings, chunks)

        output_dir.mkdir(parents=True, exist_ok=True)
        index.save(
            index_path=output_dir / "vectors.index",
            meta_path=output_dir / "metadata.json",
        )

        return index
