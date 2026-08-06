from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.endpoints import documents, health, rag, tasks
from app.core.config import settings
from app.vector.qdrant_client import ensure_collection
from app.workers.scheduler import start_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = None
    ensure_collection()

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
app.include_router(documents.router)
app.include_router(rag.router)

