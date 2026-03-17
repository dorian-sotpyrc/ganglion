from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class RunRequest:
    agent_key: str
    session_id: str
    channel_type: str
    channel_id: str
    user_id: str
    task_text: str
    tool_permissions: list[str] = field(default_factory=list)
    priority_hint: str | None = None
    risk_hint: str | None = None
    requested_mode: str | None = None
    raw_payload: dict[str, Any] = field(default_factory=dict)


class RequestAdapterError(ValueError):
    pass


def adapt_openclaw_request(payload: dict[str, Any]) -> RunRequest:
    required = ["agent_key", "session_id", "channel_type", "channel_id", "user_id", "task_text"]
    missing = [k for k in required if not payload.get(k)]
    if missing:
        raise RequestAdapterError(f"Missing required request fields: {', '.join(missing)}")

    return RunRequest(
        agent_key=str(payload["agent_key"]),
        session_id=str(payload["session_id"]),
        channel_type=str(payload["channel_type"]),
        channel_id=str(payload["channel_id"]),
        user_id=str(payload["user_id"]),
        task_text=str(payload["task_text"]),
        tool_permissions=list(payload.get("tool_permissions", [])),
        priority_hint=payload.get("priority_hint"),
        risk_hint=payload.get("risk_hint"),
        requested_mode=payload.get("requested_mode"),
        raw_payload=payload,
    )
