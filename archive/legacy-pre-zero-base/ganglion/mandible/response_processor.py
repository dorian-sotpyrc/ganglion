from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class RunResponse:
    status: str
    agent_key: str
    session_id: str
    compiled_checksum: str
    compiled_text: str
    message: str
    metadata: dict[str, Any] = field(default_factory=dict)


def process_response(
    *,
    agent_key: str,
    session_id: str,
    compiled_checksum: str,
    compiled_text: str,
    message: str,
    metadata: dict[str, Any] | None = None,
) -> RunResponse:
    return RunResponse(
        status="ok",
        agent_key=agent_key,
        session_id=session_id,
        compiled_checksum=compiled_checksum,
        compiled_text=compiled_text,
        message=message.strip(),
        metadata=metadata or {},
    )
