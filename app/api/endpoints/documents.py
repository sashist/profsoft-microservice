from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.database_models import Document
from app.models.schemas import DocumentCreate, DocumentOut
from app.services.index_service import create_document

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/", response_model=DocumentOut, summary="Поставить документ в очередь индексации")
async def enqueue_document(payload: DocumentCreate, db: Session = Depends(get_db)):
    return create_document(db, source=payload.source, text=payload.text)


@router.get("/", response_model=list[DocumentOut], summary="Получить список всех документов")
async def list_documents(db: Session = Depends(get_db)):
    return db.query(Document).all()


@router.get("/{document_id}", response_model=DocumentOut, summary="Получить документ по ID")
async def get_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

