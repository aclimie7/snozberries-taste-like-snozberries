import httpx

WALMART_API_BASE = "https://developer.walmart.com/api/detail"
WALMART_SEARCH_URL = "https://api.walmart.com/v1/search"


class WalmartClient:
    def __init__(self, api_key: str):
        self._api_key = api_key

    async def search_products(self, query: str, zip_code: str, limit: int = 10) -> list[dict]:
        async with httpx.AsyncClient() as http:
            resp = await http.get(
                WALMART_SEARCH_URL,
                headers={
                    "WM_SEC.KEY_VERSION": "1",
                    "WM_CONSUMER.ID": self._api_key,
                    "Accept": "application/json",
                },
                params={
                    "query": query,
                    "numItems": min(limit, 25),
                    "responseGroup": "full",
                    "storeId": zip_code,
                },
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()
        return data.get("items", [])
