from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone


class RetentionPolicy:
    def __init__(self, root: str | Path = "artifacts/runs") -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def list_artifacts(self) -> list[Path]:
        return sorted([p for p in self.root.glob("*.json") if p.is_file()])

    def prune_to_latest(self, keep_latest: int = 10) -> list[str]:
        files = self.list_artifacts()
        if len(files) <= keep_latest:
            return []

        to_remove = files[:-keep_latest]
        removed = []
        for path in to_remove:
            removed.append(str(path))
            path.unlink(missing_ok=True)
        return removed
