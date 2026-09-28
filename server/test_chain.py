from dotenv import load_dotenv

load_dotenv()

from app.services.rag.chain import RAGChain

chain = RAGChain()

query = """
Review the GitHub webhook authentication and signature verification.
Look for security or correctness issues.
"""

result = chain.review(query=query, top_k=5)

print("\n")
print("=" * 80)
print("AI CODE REVIEW")
print("=" * 80)
print()
print(result)
from dotenv import load_dotenv

load_dotenv()

from app.services.rag.chain import RAGChain

chain = RAGChain()

query = """
Review the GitHub webhook signature verification for
actual security or correctness vulnerabilities.

Only report genuine issues supported by the code.
Do not report missing features or style improvements.
"""

result = chain.review(query=query, top_k=5)

print("\n")
print("=" * 80)
print("AI CODE REVIEW")
print("=" * 80)
print()
print(result)
