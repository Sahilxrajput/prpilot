from dotenv import load_dotenv

load_dotenv()

from app.services.embedding.huggingface import HuggingFaceEmbedding


embedding_service = HuggingFaceEmbedding()

vector = embedding_service.embed(
    """
    Function: verify_token

    This function verifies a JWT token
    and returns the authenticated user.
    """
)

print("Dimension:", len(vector))
print("First 5 values:", vector[:5])