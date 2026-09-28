from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    app_name: str = "VietTree Education API"
    api_v1_prefix: str = "/api/v1"
    database_url: str = "postgresql+psycopg://postgres:123456@localhost:5432/viettree"
    jwt_secret_key: str = "development-only-change-me"
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 15
    refresh_token_days: int = 30
    refresh_cookie_secure: bool = False
    cors_origins: str = "http://localhost:3000,http://localhost:8080,http://localhost:8000"


@lru_cache
def get_settings() -> Settings:
    return Settings()
