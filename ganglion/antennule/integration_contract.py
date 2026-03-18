from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ganglion.openclaw_profile import INTEGRATION_PROFILE_OPENCLAW_STRICT, OpenClawStrictPolicy


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


def normalise_envelope(payload: dict[str, Any], policy: OpenClawStrictPolicy | None = None) -> OpenClawEnvelope:
    policy = policy or OpenClawStrictPolicy()
    required = [
        "request_id",
        "agent_key",
        "session_id",
        "channel_type",
        "channel_id",
        "user_id",
        "task_text",
    ]
    missing = [k for k in required if getattr(policy, f"require_{k}", False) and not payload.get(k)]
    if missing:
        raise EnvelopeValidationError(f"Missing envelope fields: {', '.join(missing)}")
    metadata = payload.get("metadata", {})
    if policy.require_metadata_dict and metadata is not None and not isinstance(metadata, dict):
        raise EnvelopeValidationError("metadata must be a dict under openclaw_strict")
    if policy.require_naming_conventions:
        if any(ch.isspace() for ch in str(payload.get("agent_key", ""))):
            raise EnvelopeValidationError("agent_key must not contain whitespace under openclaw_strict")
        if "/" in str(payload.get("agent_key", "")):
            raise EnvelopeValidationError("agent_key must not contain path separators under openclaw_strict")
    payload = dict(payload)
    payload["metadata"] = dict(metadata or {})
    payload["metadata"].setdefault("integration_profile", INTEGRATION_PROFILE_OPENCLAW_STRICT)

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
