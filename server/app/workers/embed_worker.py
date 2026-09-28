from pathlib import Path

from app.services.rag.chunker import chunk_repository
from app.services.indexing.repository_indexer import RepositoryIndexer


def index_repository(repo_path: str, repo_name: str):

    chunks = chunk_repository(Path(repo_path))

    indexer = RepositoryIndexer()

    count = indexer.index_chunks(chunks=chunks, repo_name=repo_name)

    return {"repo": repo_name, "chunks_indexed": count}
