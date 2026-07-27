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
