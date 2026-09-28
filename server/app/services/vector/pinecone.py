import os
from pinecone import Pinecone


class PineconeService:

    def __init__(self):
        api_key = os.getenv("PINECONE_API_KEY")
        index_name = os.getenv("PINECONE_INDEX")

        if not api_key:
            raise RuntimeError("PINECONE_API_KEY is missing")

        if not index_name:
            raise RuntimeError("PINECONE_INDEX is missing")

        self.client = Pinecone(api_key=api_key)
        self.index = self.client.Index(index_name)

    def upsert(self, vector_id: str, vector: list[float], metadata: dict):
        self.index.upsert(
            vectors=[{"id": vector_id, "values": vector, "metadata": metadata}]
        )

    def upsert_batch(self, vectors: list[dict]):
        self.index.upsert(vectors=vectors)

    def search(self, vector: list[float], top_k: int = 5):
        return self.index.query(vector=vector, top_k=top_k, include_metadata=True)

    def delete(self, vector_id: str):
        self.index.delete(ids=[vector_id])

    def delete_all(self):
        self.index.delete(delete_all=True)