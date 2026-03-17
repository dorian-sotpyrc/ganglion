from __future__ import annotations

from pathlib import Path
import json
from datetime import datetime, timezone


class ArtifactWriter:
    def __init__(self, root: str | Path = "artifacts") -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def write_run_artifact(self, run_id: str, payload: dict) -> Path:
        run_dir = self.root / "runs"
        run_dir.mkdir(parents=True, exist_ok=True)
        path = run_dir / f"{run_id}.json"
        body = {
            "written_at": datetime.now(timezone.utc).isoformat(),
            "payload": payload,
        }
        path.write_text(json.dumps(body, indent=2), encoding="utf-8")
        return path
