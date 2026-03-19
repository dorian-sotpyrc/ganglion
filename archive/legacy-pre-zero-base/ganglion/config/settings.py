from __future__ import annotations

from pathlib import Path
import structlog
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="GANGLION_",
        extra="ignore",
    )

    env: str = Field(default="development")
    log_level: str = Field(default="INFO")
    artifact_root: Path = Field(default=Path("./artifacts"))
    database_url: str = Field(
        default="postgresql+psycopg://postgres:postgres@localhost:5432/ganglion"
    )


def configure_logging(level: str = "INFO") -> None:
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(level.upper()),
        logger_factory=structlog.PrintLoggerFactory(),
    )


def get_settings() -> Settings:
    settings = Settings()
    settings.artifact_root.mkdir(parents=True, exist_ok=True)
    return settings
