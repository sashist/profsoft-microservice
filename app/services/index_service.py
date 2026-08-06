import logging
from uuid import uuid4

from qdrant_client.http.models import PointStruct
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.database_models import Document
from app.services.chunking import split_text
from app.services.embeddings import embed_texts
from app.vector.qdrant_client import ensure_collection
from app.vector.qdrant_client import client as qdrant_client

logger = logging.getLogger(__name__)


def create_document(db: Session, source: str, text: str) -> Document:
    existing = db.query(Document).filter(Document.source == source).first()
    if existing:
        existing.text = text
        existing.status = "idle"
        db.commit()
        db.refresh(existing)
        return existing

    document = Document(source=source, text=text, status="idle")
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


def claim_one_idle_document(db: Session) -> Document | None:
    stmt = (
        select(Document)
        .where(Document.status == "idle")
        .order_by(Document.created_at.asc())
        .limit(1)
        .with_for_update(skip_locked=True)
    )
    document = db.execute(stmt).scalar_one_or_none()
    if document is None:
        return None

    document.status = "syncing"
    db.commit()
    db.refresh(document)
    return document


def index_document(db: Session, document: Document) -> None:
    try:
        chunks = split_text(
            text=document.text or "",
            size=settings.CHUNK_SIZE,
            overlap=settings.CHUNK_OVERLAP,
        )
        if not chunks:
            raise ValueError("Document text is empty after chunking")

        vectors = embed_texts(chunks)
        if len(vectors) != len(chunks):
            raise RuntimeError("Embeddings count mismatch")

        ensure_collection()

        points = [
            PointStruct(
                id=str(uuid4()),
                vector=vector,
                payload={
                    "text": chunk,
                    "source": document.source,
                    "doc_id": document.id,
                    "section": idx + 1,
                },
            )
            for idx, (chunk, vector) in enumerate(zip(chunks, vectors, strict=False))
        ]

        qdrant_client.upsert(
            collection_name=settings.COLLECTION,
            points=points,
        )

        document.status = "indexed"
        db.commit()
        db.refresh(document)
        logger.info("Document indexed: doc_id=%s, source=%s, chunks=%s", document.id, document.source, len(points))
    except Exception:
        document.status = "failed"
        db.commit()
        db.refresh(document)
        logger.exception("Document indexing failed: doc_id=%s, source=%s", document.id, document.source)
