from __future__ import annotations

from pathlib import Path

CORE_SECTION_ORDER = [
    "identity.md",
    "constraints.md",
    "style.md",
    "tool_contract.md",
    "memory_policy.md",
]


def existing_sections(root: Path) -> list[Path]:
    return [root / name for name in CORE_SECTION_ORDER if (root / name).exists()]


def select_core_sections(shared_core_root: Path, agent_core_root: Path) -> list[tuple[str, Path]]:
    selected: list[tuple[str, Path]] = []
    for name in CORE_SECTION_ORDER:
        agent_path = agent_core_root / name
        shared_path = shared_core_root / name
        if agent_path.exists():
            selected.append((name, agent_path))
        elif shared_path.exists():
            selected.append((name, shared_path))
    return selected
