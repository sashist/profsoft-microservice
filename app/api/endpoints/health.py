from fastapi import APIRouter

router = APIRouter()


@router.get("/health", summary="Health check")
async def health_check() -> dict:
    """Returns service liveness status."""
    return {"status": "ok"}
