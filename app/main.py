from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.endpoints import health, tasks
from app.core.config import settings
from app.workers.scheduler import start_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = None
    if settings.RUN_WORKER:
        scheduler = start_scheduler()
        app.state.scheduler = scheduler

    try:
        yield
    finally:
        if scheduler is not None:
            scheduler.shutdown()


app = FastAPI(title="AI microservice skeleton", lifespan=lifespan)

# Подключение роутеров
app.include_router(health.router)
app.include_router(tasks.router)

