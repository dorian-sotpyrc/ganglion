from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class TraceStep:
    step_key: str
    status: str
    summary: str
    data: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TraceBundle:
    request_id: str
    agent_key: str
    session_id: str
    input_summary: dict[str, Any]
    steps: list[TraceStep]
    output_summary: dict[str, Any]
