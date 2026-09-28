import os
import numpy as np
from huggingface_hub import InferenceClient


class HuggingFaceEmbedding:

    def __init__(self):
        self.client = InferenceClient(
            provider="hf-inference", api_key=os.getenv("HF_TOKEN")
        )

        self.model = os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3")

    def embed(self, text: str) -> list[float]:

        result = self.client.feature_extraction(text, model=self.model)

        # Convert numpy array → Python list
        embedding = np.asarray(result).flatten()

        return embedding.tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:

        embeddings = []

        for text in texts:
            embedding = self.embed(text)
            embeddings.append(embedding)

        return embeddings
