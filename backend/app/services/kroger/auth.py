import base64
from datetime import datetime, timedelta
import httpx


KROGER_TOKEN_URL = "https://api.kroger.com/v1/connect/oauth2/token"


class KrogerAuthClient:
    def __init__(self, client_id: str, client_secret: str):
        self._client_id = client_id
        self._client_secret = client_secret
        self._token: str | None = None
        self._expires_at: datetime | None = None

    def _credentials_b64(self) -> str:
        raw = f"{self._client_id}:{self._client_secret}"
        return base64.b64encode(raw.encode()).decode()

    def _is_valid(self) -> bool:
        return (
            self._token is not None
            and self._expires_at is not None
            and datetime.utcnow() < self._expires_at - timedelta(seconds=30)
        )

    async def get_token(self) -> str:
        if self._is_valid():
            return self._token  # type: ignore[return-value]

        async with httpx.AsyncClient() as http:
            resp = await http.post(
                KROGER_TOKEN_URL,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": f"Basic {self._credentials_b64()}",
                },
                data={"grant_type": "client_credentials", "scope": "product.compact"},
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()

        self._token = data["access_token"]
        self._expires_at = datetime.utcnow() + timedelta(seconds=data.get("expires_in", 1800))
        return self._token
