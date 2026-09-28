# from pinecone import Pinecone

# from app.config import PINECONE_API_KEY, PINECONE_INDEX

# pc = Pinecone(api_key=PINECONE_API_KEY)

# if PINECONE_INDEX is None:
# 	raise ValueError("PINECONE_INDEX must be set")

# index = pc.Index(PINECONE_INDEX)


# def upsert_vectors(vectors):
#     index.upsert(vectors=vectors)


from app.services.vector.pinecone import PineconeService

_vector_store = PineconeService()


def upsert_vectors(vectors: list[dict]):
    return _vector_store.upsert_batch(vectors)


def search_vectors(vector: list[float], top_k: int = 5):
    return _vector_store.search(vector=vector, top_k=top_k)
