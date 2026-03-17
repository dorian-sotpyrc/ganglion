from __future__ import annotations

from pathlib import Path
import json
from datetime import datetime, timezone


class DeploymentManager:
    def __init__(self, root: str | Path = "artifacts/deployments") -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def record_deployment(self, agent_key: str, version: str, checksum: str) -> Path:
        path = self.root / f"{agent_key}_active.json"
        body = {
            "agent_key": agent_key,
            "version": version,
            "checksum": checksum,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
        }
        path.write_text(json.dumps(body, indent=2), encoding="utf-8")
        return path

    def read_active(self, agent_key: str) -> dict:
        path = self.root / f"{agent_key}_active.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def rollback(self, agent_key: str, previous_version: str, previous_checksum: str) -> Path:
        path = self.root / f"{agent_key}_rollback.json"
        body = {
            "agent_key": agent_key,
            "rollback_to_version": previous_version,
            "rollback_to_checksum": previous_checksum,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
        }
        path.write_text(json.dumps(body, indent=2), encoding="utf-8")
        return path
