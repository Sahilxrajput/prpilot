from app.services.embedding.huggingface import HuggingFaceEmbedding
from app.services.vector.pinecone import PineconeService


class CodeRetriever:

    def __init__(self):
        self.embedding_service = HuggingFaceEmbedding()
        self.vector_store = PineconeService()

    def retrieve(self, query: str, top_k: int = 5) -> list[dict]:

        query_vector = self.embedding_service.embed(query)

        results = self.vector_store.search(vector=query_vector, top_k=top_k)

        chunks = []

        for match in results["matches"]:

            metadata = match.get("metadata", {})

            chunks.append(
                {
                    "id": match["id"],
                    "score": match["score"],
                    "file": metadata.get("file", metadata.get("file_path")),
                    "name": metadata.get("name", metadata.get("symbol")),
                    "content": metadata.get("content", metadata.get("code")),
                }
            )

        return chunks
