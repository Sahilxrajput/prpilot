# from openai import OpenAI

# from app.config import OPENAI_API_KEY

# client = OpenAI(api_key=OPENAI_API_KEY)


# def embed_text(text):

#     response = client.embeddings.create(model="text-embedding-3-small", input=text)

#     return response.data[0].embedding


# def embed_chunks(chunks):

#     vectors = []

#     for chunk in chunks:

#         embedding = embed_text(chunk["content"])

#         vectors.append(
#             {
#                 "id": chunk["id"],
#                 "values": embedding,
#                 "metadata": {"file": chunk["file"], "name": chunk["name"]},
#             }
#         )

#     return vectors


from app.services.embedding.huggingface import HuggingFaceEmbedding

_embedding_service = HuggingFaceEmbedding()


def embed_text(text: str) -> list[float]:
    return _embedding_service.embed(text)


def embed_chunks(chunks: list[dict]) -> list[dict]:

    vectors = []

    for chunk in chunks:

        embedding = embed_text(chunk["content"])

        vectors.append(
            {
                "id": chunk["id"],
                "values": embedding,
                "metadata": {
                    "file": chunk["file"],
                    "name": chunk["name"],
                    "content": chunk["content"],
                },
            }
        )

    return vectors
