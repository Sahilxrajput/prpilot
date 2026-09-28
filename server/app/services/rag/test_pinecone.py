from app.services.rag.vectorstore import index

stats = index.describe_index_stats()

print(stats)
