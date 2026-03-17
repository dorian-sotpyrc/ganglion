from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RunMetric:
    run_id: str
    success: bool
    latency_ms: int
    used_fallback: bool
    confidentiality: str
    lane: str
    provider: str
    model: str
    task_text: str
