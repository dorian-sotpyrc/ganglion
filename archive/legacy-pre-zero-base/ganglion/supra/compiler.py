from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

from ganglion.carapace.registry import BrainRegistry
from ganglion.supra.selectors import CORE_SECTION_ORDER, select_core_sections


@dataclass(frozen=True)
class CompiledBrain:
    agent_key: str
    version: str
    sections: dict[str, str]
    section_sources: dict[str, str]
    compiled_text: str
    checksum: str


def compile_brain(repo_root: str | Path, agent_key: str) -> CompiledBrain:
    repo_root = Path(repo_root)
    registry = BrainRegistry(repo_root)
    record = registry.get_active_brain(agent_key)

    shared_core = registry.shared_root() / "core"
    agent_core = record.root_dir / "core"

    selected = select_core_sections(shared_core, agent_core)

    sections: dict[str, str] = {}
    section_sources: dict[str, str] = {}

    ordered_chunks: list[str] = []
    for name, path in selected:
        content = path.read_text(encoding="utf-8").strip()
        key = name.replace(".md", "")
        sections[key] = content
        section_sources[key] = str(path.relative_to(repo_root))
        ordered_chunks.append(f"## {key}\n{content}")

    compiled_text = "\n\n".join(ordered_chunks).strip()
    checksum = hashlib.sha256(compiled_text.encode("utf-8")).hexdigest()

    return CompiledBrain(
        agent_key=agent_key,
        version=record.manifest.version,
        sections=sections,
        section_sources=section_sources,
        compiled_text=compiled_text,
        checksum=checksum,
    )
