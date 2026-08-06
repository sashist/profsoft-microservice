from app.core.config import settings
from app.services.embeddings import embed_texts
from app.vector.qdrant_client import client as qdrant_client


def search(question: str, k: int | None = None) -> list:
    vectors = embed_texts([question])
    if not vectors:
        return []

    response = qdrant_client.query_points(
        collection_name=settings.COLLECTION,
        query=vectors[0],
        limit=k or settings.TOP_K,
        with_payload=True,
    )
    return list(response.points)
