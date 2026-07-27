import logging

import httpx

from app.core.config import settings
from app.models.database_models import Task

logger = logging.getLogger(__name__)


def send_result(task: Task) -> bool:
    payload = {"external_id": task.external_id, "result": task.result}

    if settings.TEST_MODE or not settings.RESULT_URL:
        logger.info("Skip export (TEST_MODE or empty RESULT_URL): %s", payload)
        return True

    try:
        response = httpx.post(settings.RESULT_URL, json=payload, timeout=10)
        return 200 <= response.status_code < 300
    except httpx.HTTPError:
        logger.exception("Failed to export task result for external_id=%s", task.external_id)
        return False
