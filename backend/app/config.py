from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    kroger_client_id: str = ""
    kroger_client_secret: str = ""
    walmart_api_key: str = ""
    demo_mode: bool = False
    backend_port: int = 8000
    split_savings_threshold: float = 2.00

    @property
    def use_kroger_mock(self) -> bool:
        return self.demo_mode or not (self.kroger_client_id and self.kroger_client_secret)

    @property
    def use_walmart_mock(self) -> bool:
        return self.demo_mode or not self.walmart_api_key


settings = Settings()
