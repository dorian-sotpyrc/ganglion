from __future__ import annotations

from pathlib import Path
import json
import shutil


class BrainExportService:
    def __init__(self, root: str | Path = "artifacts/exports") -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def export_brain(self, agent_key: str, source_dir: str | Path) -> Path:
        source_dir = Path(source_dir)
        export_dir = self.root / agent_key
        if export_dir.exists():
            shutil.rmtree(export_dir)
        shutil.copytree(source_dir, export_dir)

        manifest = {
            "agent_key": agent_key,
            "source_dir": str(source_dir),
            "export_dir": str(export_dir),
        }
        (export_dir / "_export_manifest.json").write_text(
            json.dumps(manifest, indent=2),
            encoding="utf-8",
        )
        return export_dir

    def import_brain(self, export_dir: str | Path, destination_dir: str | Path) -> Path:
        export_dir = Path(export_dir)
        destination_dir = Path(destination_dir)
        if destination_dir.exists():
            shutil.rmtree(destination_dir)
        shutil.copytree(export_dir, destination_dir)
        return destination_dir
