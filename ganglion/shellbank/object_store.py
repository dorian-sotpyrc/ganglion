from __future__ import annotations

from pathlib import Path

from ganglion.config.settings import get_settings


class ObjectStore:
    def __init__(self, root: Path | None = None) -> None:
        settings = get_settings()
        self.root = Path(root or settings.artifact_root)
        self.root.mkdir(parents=True, exist_ok=True)

    def write_text(self, relative_path: str, content: str) -> Path:
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def read_text(self, relative_path: str) -> str:
        path = self.root / relative_path
        return path.read_text(encoding="utf-8")
