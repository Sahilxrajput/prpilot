from dotenv import load_dotenv

load_dotenv()

from app.services.indexing.repository_indexer import RepositoryIndexer

indexer = RepositoryIndexer()

count = indexer.index_repository(repo_path=".", repo_name="PrPilot")

print(f"\nSuccessfully indexed {count} chunks.")
