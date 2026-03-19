from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ganglion.carapace.manifests import BrainManifest, load_manifest


@dataclass(frozen=True)
class BrainRecord:
    manifest_path: Path
    manifest: BrainManifest
    root_dir: Path


class BrainRegistry:
    def __init__(self, repo_root: str | Path) -> None:
        self.repo_root = Path(repo_root)
        self.brains_root = self.repo_root / "brains"

    def shared_root(self) -> Path:
        return self.brains_root / "shared"

    def agent_root(self, agent_key: str) -> Path:
        return self.brains_root / "agents" / agent_key

    def get_agent_brain(self, agent_key: str) -> BrainRecord:
        manifest_path = self.agent_root(agent_key) / "manifest.json"
        manifest = load_manifest(manifest_path)
        return BrainRecord(
            manifest_path=manifest_path,
            manifest=manifest,
            root_dir=manifest_path.parent,
        )

    def get_active_brain(self, agent_key: str) -> BrainRecord:
        record = self.get_agent_brain(agent_key)
        if record.manifest.status != "active":
            raise ValueError(f"No active brain for agent {agent_key}")
        return record
