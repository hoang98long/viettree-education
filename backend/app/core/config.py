from functools import lru_cache
from pathlib import Path
from typing import Literal
from urllib.parse import urlsplit

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT / ".env", extra="ignore", hide_input_in_errors=True
    )
    app_env: Literal["development", "test", "production"] = "development"
    db_host: str = "localhost"
    db_port: int = Field(default=5432, ge=1, le=65535)
    db_name: str = "viettree-education"
    db_user: str = "postgres"
    db_password: str = ""
    db_connect_timeout: int = Field(default=5, ge=1, le=30)
    db_statement_timeout_ms: int = Field(default=30000, ge=1000, le=300000)
    db_lock_timeout_ms: int = Field(default=5000, ge=1000, le=30000)
    db_pool_size: int = Field(default=5, ge=1, le=50)
    db_pool_max_overflow: int = Field(default=5, ge=0, le=50)
    db_pool_timeout: int = Field(default=5, ge=1, le=30)
    server_workers: int = Field(default=2, ge=1, le=8)
    server_limit_concurrency: int = Field(default=128, ge=16, le=2000)
    server_graceful_timeout: int = Field(default=30, ge=5, le=120)
    password_verify_concurrency: int = Field(default=2, ge=1, le=8)
    allowed_origins: str = "http://localhost:3000"
    cookie_secure: bool = False
    session_hours: int = Field(default=8, ge=1, le=24)
    remember_session_days: int = Field(default=7, ge=1, le=30)
    login_ip_limit: int = Field(default=120, ge=10, le=1000)
    login_account_limit: int = Field(default=10, ge=3, le=30)
    seed_admin_password: str = ""
    seed_student_password: str = ""
    ai_provider: Literal["simulation", "ollama"] = "simulation"
    ai_training_only: bool = True
    ai_ollama_url: str = "http://127.0.0.1:11434"
    ai_ollama_model: str = Field(default="", max_length=100)
    ai_media_root: Path = ROOT / "var/ai-media"

    @model_validator(mode="after")
    def production_safety(self):
        provider_url = urlsplit(self.ai_ollama_url)
        if (
            provider_url.scheme not in {"http", "https"}
            or provider_url.hostname
            not in {"localhost", "127.0.0.1", "ollama", "host.docker.internal"}
            or provider_url.username
            or provider_url.password
            or provider_url.query
            or provider_url.fragment
            or provider_url.path.rstrip("/")
        ):
            raise ValueError(
                "AI_OLLAMA_URL phải trỏ tới dịch vụ local được cho phép, không chứa secret hoặc đường dẫn"
            )
        for origin in self.origins:
            try:
                parsed = urlsplit(origin)
                valid_port = parsed.port
            except ValueError:
                raise ValueError("ALLOWED_ORIGINS phải chứa các origin hợp lệ") from None
            if (
                parsed.scheme not in {"http", "https"}
                or not parsed.hostname
                or "*" in origin
                or "\\" in origin
                or any(char.isspace() for char in origin)
                or parsed.username is not None
                or parsed.password is not None
                or parsed.path
                or parsed.query
                or parsed.fragment
                or valid_port == 0
            ):
                raise ValueError(
                    "ALLOWED_ORIGINS chỉ nhận scheme://host[:port], không có đường dẫn"
                )
        if not self.origins:
            raise ValueError("ALLOWED_ORIGINS không được để trống")
        if self.app_env == "production":
            if (
                not self.cookie_secure
                or self.db_user.strip().casefold() == "postgres"
                or len(self.db_password) < 16
                or self.db_password.startswith("CHANGE_ME")
            ):
                raise ValueError(
                    "Production cần cookie secure và tài khoản DB riêng, mật khẩu mạnh"
                )
            if any(not origin.startswith("https://") for origin in self.origins):
                raise ValueError("Production cần HTTPS origins")
        return self

    @property
    def origins(self) -> list[str]:
        return list(
            dict.fromkeys(
                value.strip().rstrip("/")
                for value in self.allowed_origins.split(",")
                if value.strip()
            )
        )

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
