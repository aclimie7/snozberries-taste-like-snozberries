from fastapi import APIRouter, Query
from ..models.shopping import LocationResult
from ..models.product import Store
from ..config import settings

router = APIRouter()

_MOCK_LOCATIONS: list[LocationResult] = [
    LocationResult(
        store=Store.kroger,
        store_id="70300168",
        name="Kroger",
        address="123 Main St (demo)",
        distance_miles=1.2,
    ),
    LocationResult(
        store=Store.walmart,
        store_id="2648",
        name="Walmart Supercenter (demo)",
        address="456 Commerce Blvd (demo)",
        distance_miles=2.1,
    ),
]


@router.get("/locations", response_model=list[LocationResult])
async def locations(
    zip_code: str = Query(pattern=r"^\d{5}$"),
) -> list[LocationResult]:
    if not settings.use_kroger_mock:
        from ..services.kroger.client import KrogerClient
        client = KrogerClient(settings.kroger_client_id, settings.kroger_client_secret)
        location_id = await client.find_location(zip_code)
        if location_id:
            return [
                LocationResult(
                    store=Store.kroger,
                    store_id=location_id,
                    name="Kroger",
                    address=f"Near {zip_code}",
                    distance_miles=None,
                ),
                *([loc for loc in _MOCK_LOCATIONS if loc.store == Store.walmart]),
            ]
    return _MOCK_LOCATIONS
