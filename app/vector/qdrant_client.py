from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

from app.core.config import settings

client = QdrantClient(url=settings.QDRANT_URL)


def ensure_collection() -> None:
    collections = client.get_collections().collections
    exists = any(collection.name == settings.COLLECTION for collection in collections)

    if exists:
        try:
            info = client.get_collection(collection_name=settings.COLLECTION)
            current_dim = info.config.params.vectors.size
            if current_dim != settings.EMBED_DIM:
                client.delete_collection(collection_name=settings.COLLECTION)
                exists = False
        except Exception:
            pass

    if not exists:
        client.create_collection(
            collection_name=settings.COLLECTION,
            vectors_config=VectorParams(size=settings.EMBED_DIM, distance=Distance.COSINE),
        )
