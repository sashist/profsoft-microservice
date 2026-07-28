from typing import Annotated

import httpx
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.database import get_db
from app.models.schemas import TaskCreate, TaskOut
from app.services.task_service import create_task, list_tasks

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskOut, summary="Импортировать задачу")
async def import_task(
    payload: Annotated[
        TaskCreate,
        Body(
            examples=[
                {
                    "external_id": "external123",
                    "input_text": "Товар пришел в стандартной упаковке, характеристики соответствуют описанию.",
                }
            ]
        ),
    ],
    db: Session = Depends(get_db),
):
    """Импортирует задачу (с дедупликацией по external_id)."""
    return create_task(
        db, external_id=payload.external_id, input_text=payload.input_text
    )


@router.post(
    "/mock", response_model=TaskOut, summary="Импортировать задачу из внешнего API"
)
async def import_task_from_source(db: Session = Depends(get_db)):
    """Забирает одну задачу из API_URL и сохраняет её через create_task (с дедупликацией)."""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(settings.API_URL)
            response.raise_for_status()
            payload = response.json()
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502, detail=f"Failed to fetch task from API_URL: {exc}"
        ) from exc

    if isinstance(payload, list):
        if not payload:
            raise HTTPException(
                status_code=404, detail="Source API returned empty list"
            )
        payload = payload[0]

    if not isinstance(payload, dict):
        raise HTTPException(
            status_code=502, detail="Source API returned invalid payload format"
        )

    external_id = payload.get("external_id")
    input_text = payload.get("input_text")

    if not external_id or not isinstance(external_id, str):
        raise HTTPException(
            status_code=502, detail="Source payload missing valid 'external_id'"
        )
    if not input_text or not isinstance(input_text, str):
        raise HTTPException(
            status_code=502, detail="Source payload missing valid 'input_text'"
        )

    return create_task(db, external_id=external_id, input_text=input_text)


@router.get("/", response_model=list[TaskOut], summary="Список всех задач")
async def get_all_tasks(db: Session = Depends(get_db)):
    """Возвращает все задачи."""
    return list_tasks(db)
