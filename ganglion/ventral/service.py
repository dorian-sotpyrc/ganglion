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
    def __init__(self) -> None:
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

    def get_critical_memory(self, agent_key: str) -> list[MemoryItem]:
        return list(self._critical.get(agent_key, []))

    def get_relevant_episodic_memory(self, agent_key: str, task_text: str, limit: int = 3) -> list[MemoryItem]:
        words = {w.strip(".,:;!?()[]{}").lower() for w in task_text.split() if w.strip()}
        candidates = []
        for item in self._episodic.get(agent_key, []):
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
