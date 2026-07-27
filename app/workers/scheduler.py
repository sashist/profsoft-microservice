import logging

from apscheduler.schedulers.background import BackgroundScheduler

from app.core.config import settings
from app.db.database import SessionLocal
from app.services.ai_service import classify
from app.services.export_service import send_result
from app.services.task_service import (
    claim_one_pending,
    list_done_for_export,
    mark_done,
    mark_failed_or_retry,
    mark_sent,
    reset_stuck,
)

logger = logging.getLogger(__name__)


def process_pending() -> None:
    db = SessionLocal()
    try:
        task = claim_one_pending(db)
        if task is None:
            return

        logger.info("Task claimed for processing: external_id=%s, status=processing", task.external_id)

        try:
            result = classify(task.input_text or "")
            mark_done(db, task, result)
            logger.info(
                "Task processed successfully: external_id=%s, status=done, result=%s",
                task.external_id,
                result,
            )
        except Exception as exc:
            mark_failed_or_retry(db, task, str(exc))
            logger.exception(
                "Task processing failed: external_id=%s, attempts=%s, new_status=%s",
                task.external_id,
                task.attempts,
                task.status,
            )
    finally:
        db.close()


def export_done() -> None:
    db = SessionLocal()
    try:
        tasks = list_done_for_export(db)
        for task in tasks:
            try:
                ok = send_result(task)
                if ok:
                    mark_sent(db, task)
                    logger.info("Task exported: external_id=%s, status=sent", task.external_id)
                else:
                    logger.warning("Task export failed (will retry): external_id=%s", task.external_id)
            except Exception:
                logger.exception("Unexpected export error for external_id=%s", task.external_id)
    finally:
        db.close()


def reset_stuck_job() -> None:
    db = SessionLocal()
    try:
        n = reset_stuck(db)
        if n > 0:
            logger.warning("Reset stuck tasks: count=%s", n)
    finally:
        db.close()


def start_scheduler() -> BackgroundScheduler:
    scheduler = BackgroundScheduler()

    scheduler.add_job(process_pending, "interval", seconds=settings.POLL_INTERVAL, id="process_pending")
    scheduler.add_job(export_done, "interval", seconds=settings.POLL_INTERVAL, id="export_done")
    scheduler.add_job(reset_stuck_job, "interval", seconds=60, id="reset_stuck_job")

    scheduler.start()
    logger.info(
        "Scheduler started: process_pending=%ss, export_done=%ss, reset_stuck_job=60s",
        settings.POLL_INTERVAL,
        settings.POLL_INTERVAL,
    )
    return scheduler
