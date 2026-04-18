import httpx
from .auth import KrogerAuthClient

KROGER_API_BASE = "https://api.kroger.com/v1"


class KrogerClient:
    def __init__(self, client_id: str, client_secret: str):
        self._auth = KrogerAuthClient(client_id, client_secret)

    async def search_products(self, query: str, location_id: str, limit: int = 10) -> list[dict]:
        token = await self._auth.get_token()
        async with httpx.AsyncClient() as http:
            resp = await http.get(
                f"{KROGER_API_BASE}/products",
                headers={"Authorization": f"Bearer {token}"},
                params={
                    "filter.term": query,
                    "filter.locationId": location_id,
                    "filter.limit": min(limit, 50),
                },
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()
        return data.get("data", [])

    async def find_location(self, zip_code: str) -> str | None:
        token = await self._auth.get_token()
        async with httpx.AsyncClient() as http:
            resp = await http.get(
                f"{KROGER_API_BASE}/locations",
                headers={"Authorization": f"Bearer {token}"},
                params={"filter.zipCode.near": zip_code, "filter.limit": 1},
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()
        locations = data.get("data", [])
        if locations:
            return locations[0].get("locationId")
        return None
