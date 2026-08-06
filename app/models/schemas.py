from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TaskOut(BaseModel):
    """Response schema for a task."""

    id: int
    external_id: str
    input_text: Optional[str] = None
    status: str
    result: Optional[str] = None
    attempts: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TaskCreate(BaseModel):
    """Request schema for creating a task."""

    external_id: str
    input_text: str


class DocumentCreate(BaseModel):
    """Request schema for adding a document to indexing queue."""

    source: str
    text: str


class DocumentOut(BaseModel):
    """Response schema for a document in indexing queue."""

    id: int
    source: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AskRequest(BaseModel):
    question: str


class SourceOut(BaseModel):
    source: str
    doc_id: int | None = None
    section: int | None = None
    text: str
    score: float


class AskResponse(BaseModel):
    answer: str
    sources: list[SourceOut]
