from functools import lru_cache
from pathlib import Path

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT / ".env", extra="ignore")
    app_env: str = "development"
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "viettree-education"
    db_user: str = "postgres"
    db_password: str = ""
    allowed_origins: str = "http://localhost:3000"
    cookie_secure: bool = False
    session_hours: int = 8
    seed_admin_password: str = ""
    seed_student_password: str = ""

    @model_validator(mode="after")
    def production_safety(self):
        if self.app_env == "production":
            if not self.cookie_secure or self.db_user == "postgres" or len(self.db_password) < 16:
                raise ValueError(
                    "Production cần cookie secure và tài khoản DB riêng, mật khẩu mạnh"
                )
            if any(not origin.startswith("https://") for origin in self.origins):
                raise ValueError("Production cần HTTPS origins")
        return self

    @property
    def origins(self) -> list[str]:
        return [value.strip().rstrip("/") for value in self.allowed_origins.split(",")]

    @property
    def database_url(self) -> URL:
        return URL.create(
            "postgresql+psycopg",
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
        )


@lru_cache
def settings() -> Settings:
    return Settings()
