# from app.services.embedding.huggingface import HuggingFaceEmbedding
# from app.services.vector.pinecone import PineconeService


# class RepositoryIndexer:

#     def __init__(self):
#         self.embedding_service = HuggingFaceEmbedding()
#         self.pinecone_service = PineconeService()

#     def index_chunks(self, chunks: list[dict], repo_name: str):
#         vectors = []

#         for chunk in chunks:

#             text = self._build_embedding_text(chunk=chunk, repo_name=repo_name)

#             embedding = self.embedding_service.embed(text)

#             vector_id = self._create_vector_id(repo_name, chunk)

#             vectors.append(
#                 {
#                     "id": vector_id,
#                     "values": embedding,
#                     "metadata": {
#                         "repo": repo_name,
#                         "file_path": chunk["file_path"],
#                         "language": chunk["language"],
#                         "symbol": chunk.get("symbol", ""),
#                         "start_line": chunk.get("start_line", 0),
#                         "end_line": chunk.get("end_line", 0),
#                         "code": chunk["code"],
#                     },
#                 }
#             )

#         if vectors:
#             self.pinecone_service.upsert_batch(vectors)

#         return len(vectors)

#     def _build_embedding_text(self, chunk: dict, repo_name: str) -> str:

#         return f"""
# Repository: {repo_name}

# File: {chunk["file_path"]}

# Language: {chunk["language"]}

# Symbol: {chunk.get("symbol", "")}

# Lines: {chunk.get("start_line", "")}-{chunk.get("end_line", "")}

# Code:
# {chunk["code"]}
# """.strip()

#     def _create_vector_id(self, repo_name: str, chunk: dict) -> str:

#         return (
#             f"{repo_name}:"
#             f"{chunk['file_path']}:"
#             f"{chunk.get('start_line', 0)}:"
#             f"{chunk.get('end_line', 0)}"
#         )


from pathlib import Path

from app.services.embedding.huggingface import HuggingFaceEmbedding
from app.services.vector.pinecone import PineconeService
from app.services.rag.chunker import chunk_repository


class RepositoryIndexer:

    def __init__(self):
        self.embedding_service = HuggingFaceEmbedding()
        self.pinecone_service = PineconeService()

    def index_repository(self, repo_path: str, repo_name: str) -> int:

        chunks = chunk_repository(Path(repo_path))

        print(f"Found {len(chunks)} chunks")

        return self.index_chunks(chunks=chunks, repo_name=repo_name)

    def index_chunks(self, chunks: list[dict], repo_name: str) -> int:

        vectors = []

        for chunk in chunks:

            content = chunk["content"]

            embedding_text = self._build_embedding_text(
                chunk=chunk, repo_name=repo_name
            )

            embedding = self.embedding_service.embed(embedding_text)

            vector_id = self._create_vector_id(repo_name=repo_name, chunk=chunk)

            vectors.append(
                {
                    "id": vector_id,
                    "values": embedding,
                    "metadata": {
                        "repo": repo_name,
                        "file": chunk["file"],
                        "name": chunk["name"],
                        "content": content,
                    },
                }
            )

        if vectors:
            self.pinecone_service.upsert_batch(vectors)

        print(f"Indexed {len(vectors)} chunks")

        return len(vectors)

    def _build_embedding_text(self, chunk: dict, repo_name: str) -> str:

        return f"""
Repository: {repo_name}

File: {chunk["file"]}

Symbol: {chunk["name"]}

Code:
{chunk["content"]}
""".strip()

    def _create_vector_id(self, repo_name: str, chunk: dict) -> str:

        return f"{repo_name}:{chunk['id']}"
