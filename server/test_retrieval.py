from dotenv import load_dotenv

load_dotenv()

from app.services.rag.retriever import CodeRetriever

retriever = CodeRetriever()

query = "Where is the GitHub webhook signature verified?"

results = retriever.retrieve(query=query, top_k=5)

print("\nSearch results:\n")

for result in results:
    print("Score:", result["score"])
    print("File:", result["file"])
    print("Symbol:", result["name"])
    print("Code:")
    print(result["content"])
    print("-" * 60)
