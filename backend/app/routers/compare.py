from fastapi import APIRouter
from ..models.shopping import ComparisonRequest
from ..models.product import ComparisonResult
from ..services.comparison import run_comparison

router = APIRouter()


@router.post("/compare", response_model=ComparisonResult)
async def compare(request: ComparisonRequest) -> ComparisonResult:
    return await run_comparison(request)
