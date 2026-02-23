import torch
from sentence_transformers import SentenceTransformer
from typing import List

class EmbeddingModel:
    """
    Wrapper around sentence-transformers for consistent embeddings
    Uses GPU if available for faster encoding
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        
        # Use GPU if available
        if torch.cuda.is_available():
            self.device = torch.device("cuda")
            self.model = self.model.to(self.device)
            print(f"Using GPU: {torch.cuda.get_device_name(0)}")
        else:
            self.device = torch.device("cpu")
            print("Using CPU")
        
        self.dim = self.model.get_sentence_embedding_dimension()

    def encode(self, texts: List[str]):
        return self.model.encode(texts, show_progress_bar=False, device=self.device)
