import hashlib
import math
import re

from app.ai.client import embedding_client
from app.core.config import settings


def _test_embedding(text: str) -> list[float]:
    vector = [0.0] * settings.EMBED_DIM
    tokens = re.findall(r"\w+", text.lower(), flags=re.UNICODE)

    for token in tokens:
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        index = int.from_bytes(digest[:4], "big") % settings.EMBED_DIM
        vector[index] += 1.0 if digest[4] % 2 else -1.0

    norm = math.sqrt(sum(value * value for value in vector))
    if norm:
        return [value / norm for value in vector]
    return vector


def embed_texts(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []

    if settings.TEST_MODE:
        return [_test_embedding(text) for text in texts]

    response = embedding_client.embeddings.create(model=settings.EMBED_MODEL, input=texts)
    return [item.embedding for item in response.data]
