from __future__ import annotations

from pathlib import Path
import os

from ganglion.config.settings import get_settings
from ganglion.storage.db import get_engine
from ganglion.shellbank.object_store import ObjectStore


def test_imports_and_settings_load(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("GANGLION_ARTIFACT_ROOT", str(tmp_path / "artifacts"))
    settings = get_settings()
    assert settings.env
    assert settings.artifact_root.exists()


def test_db_module_builds_engine(monkeypatch) -> None:
    monkeypatch.setenv("GANGLION_DATABASE_URL", "sqlite+pysqlite:///:memory:")
    engine = get_engine()
    assert str(engine.url).startswith("sqlite")


def test_object_store_write_read(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("GANGLION_ARTIFACT_ROOT", str(tmp_path / "artifacts"))
    store = ObjectStore()
    store.write_text("smoke/hello.txt", "ganglion-step1")
    assert store.read_text("smoke/hello.txt") == "ganglion-step1"


def test_alembic_files_exist() -> None:
    assert Path("alembic.ini").exists()
    assert Path("migrations/env.py").exists()
    assert Path("migrations/versions/0001_step1_init.py").exists()
