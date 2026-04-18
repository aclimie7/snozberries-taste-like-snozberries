from fastapi import APIRouter
from ..config import settings

router = APIRouter()


@router.get("/health")
async def health():
    return {
        "status": "ok",
        "demo_mode": settings.use_kroger_mock or settings.use_walmart_mock,
        "kroger_mock": settings.use_kroger_mock,
        "walmart_mock": settings.use_walmart_mock,
    }
