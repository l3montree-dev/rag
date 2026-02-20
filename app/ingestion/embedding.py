from collections.abc import Sequence
from typing import cast
from app.clients import get_mistral_client
from app.config import BATCH_SIZE, MODEL_EMBEDDING

# get the embeddings for a list of chunks, return a list of embeddings
def get_embeddings(chunks: list[str]) -> list[list[float]]:
    client = get_mistral_client()
    embeddings: list[list[float]] = []
    # call the api with batches to avoid hitting the rate limit
    for i in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[i:i + BATCH_SIZE]
        response = client.embeddings.create(
            model=MODEL_EMBEDDING,
            inputs=batch
        )
        for data_item in response.data:
            embedding: Sequence[float] = cast(Sequence[float], data_item.embedding)
            embeddings.append(list(embedding))
    return embeddings

# get embedding for a single chunk of text
def text_embedding(chunk: str) -> list[float]:
    client = get_mistral_client()
    # call the mistral api to get the embedding for the given text
    response = client.embeddings.create(
        model=MODEL_EMBEDDING,
        inputs=[chunk]
    )
    embedding = cast(Sequence[float], response.data[0].embedding)
    return list(embedding)