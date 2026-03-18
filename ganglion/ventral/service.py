from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import json
from typing import Any


@dataclass(frozen=True)
class MemoryItem:
    memory_id: str
    memory_type: str
    text: str
    confidence: float = 1.0
    tags: list[str] = field(default_factory=list)
    source: str = "seed"


class MemoryService:
    def __init__(self, repo_root: str | Path | None = None) -> None:
        self.repo_root = Path(repo_root) if repo_root else None
        self._critical: dict[str, list[MemoryItem]] = {
            "surgeon": [
                MemoryItem(
                    memory_id="crit-001",
                    memory_type="critical",
                    text="Surgeon brain prioritises safe changes, verification, and rollback planning.",
                    confidence=1.0,
                    tags=["safety", "rollback", "verification"],
                    source="seed",
                )
            ]
        }
        self._episodic: dict[str, list[MemoryItem]] = {
            "surgeon": [
                MemoryItem(
                    memory_id="epi-001",
                    memory_type="episodic",
                    text="Previous service failures were best diagnosed by checking service state, logs, and dependencies first.",
                    confidence=0.9,
                    tags=["service", "logs", "diagnosis"],
                    source="seed",
                ),
                MemoryItem(
                    memory_id="epi-002",
                    memory_type="episodic",
                    text="When working with confidential infrastructure tasks, prefer stronger models and minimal disclosure.",
                    confidence=0.95,
                    tags=["confidential", "routing", "policy"],
                    source="seed",
                ),
            ]
        }
        self._imported_cache: dict[str, dict[str, list[MemoryItem]]] = {}

    def _imported_memory_path(self, agent_key: str) -> Path | None:
        if not self.repo_root:
            return None
        return self.repo_root / "artifacts" / "imported_state" / agent_key / "memory_bundle.json"

    def _load_imported_memory(self, agent_key: str) -> dict[str, list[MemoryItem]]:
        if agent_key in self._imported_cache:
            return self._imported_cache[agent_key]

        empty = {"critical": [], "episodic": []}
        path = self._imported_memory_path(agent_key)
        if not path or not path.exists():
            self._imported_cache[agent_key] = empty
            return empty

        payload = json.loads(path.read_text(encoding="utf-8"))

        def parse_items(kind: str) -> list[MemoryItem]:
            items = []
            for idx, raw in enumerate(payload.get(kind, []), start=1):
                text = str(raw.get("text", "")).strip()
                if not text:
                    continue
                items.append(
                    MemoryItem(
                        memory_id=str(raw.get("memory_id") or f"imported-{kind}-{idx:03d}"),
                        memory_type=kind[:-1] if kind.endswith("s") else kind,
                        text=text,
                        confidence=float(raw.get("confidence", 0.9)),
                        tags=[str(t) for t in raw.get("tags", [])],
                        source=str(raw.get("source", "imported")),
                    )
                )
            return items

        loaded = {
            "critical": parse_items("critical"),
            "episodic": parse_items("episodic"),
        }
        self._imported_cache[agent_key] = loaded
        return loaded

    def get_critical_memory(self, agent_key: str) -> list[MemoryItem]:
        imported = self._load_imported_memory(agent_key)
        return list(imported["critical"] or self._critical.get(agent_key, []))

    def get_relevant_episodic_memory(self, agent_key: str, task_text: str, limit: int = 3) -> list[MemoryItem]:
        words = {w.strip(".,:;!?()[]{}").lower() for w in task_text.split() if w.strip()}
        imported = self._load_imported_memory(agent_key)
        source_items = imported["episodic"] or self._episodic.get(agent_key, [])
        candidates = []
        for item in source_items:
            score = 0
            for tag in item.tags:
                if tag.lower() in words:
                    score += 2
            item_words = {w.strip(".,:;!?()[]{}").lower() for w in item.text.split()}
            score += len(words & item_words)
            if score > 0:
                candidates.append((score, item))
        candidates.sort(key=lambda x: (-x[0], -x[1].confidence, x[1].memory_id))
        return [item for _, item in candidates[:limit]]

    def build_session_summary(self, session_messages: list[str], max_chars: int = 400) -> str:
        joined = " | ".join(m.strip() for m in session_messages if m.strip())
        if len(joined) <= max_chars:
            return joined
        return joined[: max_chars - 3].rstrip() + "..."

    def memory_bundle(self, agent_key: str, task_text: str, session_messages: list[str] | None = None) -> dict[str, Any]:
        session_messages = session_messages or []
        critical = self.get_critical_memory(agent_key)
        episodic = self.get_relevant_episodic_memory(agent_key, task_text)
        summary = self.build_session_summary(session_messages)
        return {
            "critical": critical,
            "episodic": episodic,
            "session_summary": summary,
        }
