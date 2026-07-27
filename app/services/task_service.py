from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.database_models import Task


def create_task(db: Session, external_id: str, input_text: str | None = None) -> Task:
    """Создаёт задачу, если её нет. Если есть — возвращает существующую."""
    existing_task = db.query(Task).filter(Task.external_id == external_id).first()
    if existing_task:
        return existing_task

    new_task = Task(external_id=external_id, input_text=input_text, status="pending")
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def claim_one_pending(db: Session) -> Task | None:
    stmt = (
        select(Task)
        .where(Task.status == "pending")
        .order_by(Task.created_at.asc())
        .limit(1)
        .with_for_update(skip_locked=True)
    )
    task = db.execute(stmt).scalar_one_or_none()
    if task is None:
        return None

    task.status = "processing"
    task.error = None
    db.commit()
    db.refresh(task)
    return task


def mark_done(db: Session, task: Task, result: str) -> None:
    task.status = "done"
    task.result = result
    task.error = None
    db.commit()
    db.refresh(task)


def mark_failed_or_retry(db: Session, task: Task, error_msg: str) -> None:
    task.attempts = (task.attempts or 0) + 1
    task.error = error_msg

    if task.attempts >= settings.MAX_ATTEMPTS:
        task.status = "failed"
    else:
        task.status = "pending"

    db.commit()
    db.refresh(task)


def list_done_for_export(db: Session) -> list[Task]:
    return db.query(Task).filter(Task.status == "done").all()


def mark_sent(db: Session, task: Task) -> None:
    task.status = "sent"
    db.commit()
    db.refresh(task)


def reset_stuck(db: Session) -> int:
    cutoff = datetime.utcnow() - timedelta(minutes=settings.STUCK_MINUTES)
    stuck_tasks = (
        db.query(Task)
        .filter(
            Task.status == "processing",
            Task.updated_at.is_not(None),
            Task.updated_at < cutoff,
        )
        .all()
    )

    for task in stuck_tasks:
        task.status = "pending"

    if stuck_tasks:
        db.commit()

    return len(stuck_tasks)


def list_tasks(db: Session) -> list[Task]:
    """Возвращает все задачи, отсортированные от новых к старым."""
    return db.query(Task).order_by(Task.created_at.desc()).all()
