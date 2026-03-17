from __future__ import annotations

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from ganglion.config.settings import get_settings


def get_engine(database_url: str | None = None) -> Engine:
    settings = get_settings()
    return create_engine(database_url or settings.database_url, future=True)


def ping_database(database_url: str | None = None) -> bool:
    engine = get_engine(database_url)
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return True
