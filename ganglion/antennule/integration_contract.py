from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class OpenClawEnvelope:
    request_id: str
    agent_key: str
    session_id: str
    channel_type: str
    channel_id: str
    user_id: str
    task_text: str
    session_messages: list[str] = field(default_factory=list)
    requested_model: str | None = None
    requested_provider: str | None = None
    requested_lane: str | None = None
    risk_hint: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class EnvelopeValidationError(ValueError):
    pass


def normalise_envelope(payload: dict[str, Any]) -> OpenClawEnvelope:
    required = [
        "request_id",
        "agent_key",
        "session_id",
        "channel_type",
        "channel_id",
        "user_id",
        "task_text",
    ]
    missing = [k for k in required if not payload.get(k)]
    if missing:
        raise EnvelopeValidationError(f"Missing envelope fields: {', '.join(missing)}")

    return OpenClawEnvelope(
        request_id=str(payload["request_id"]),
        agent_key=str(payload["agent_key"]),
        session_id=str(payload["session_id"]),
        channel_type=str(payload["channel_type"]),
        channel_id=str(payload["channel_id"]),
        user_id=str(payload["user_id"]),
        task_text=str(payload["task_text"]),
        session_messages=list(payload.get("session_messages", [])),
        requested_model=payload.get("requested_model"),
        requested_provider=payload.get("requested_provider"),
        requested_lane=payload.get("requested_lane"),
        risk_hint=payload.get("risk_hint"),
        metadata=dict(payload.get("metadata", {})),
    )
