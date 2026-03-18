from __future__ import annotations

from pathlib import Path
from typing import Any

from ganglion.antennule.integration_contract import normalise_envelope
from ganglion.openclaw_profile import OpenClawStrictPolicy
from ganglion.antennule.request_adapter import adapt_openclaw_request
from ganglion.pleon.orchestrator import Orchestrator


def handle_openclaw_request(repo_root: str | Path, payload: dict[str, Any]) -> dict[str, Any]:
    envelope = normalise_envelope(payload, OpenClawStrictPolicy())

    request_payload = {
        "agent_key": envelope.agent_key,
        "session_id": envelope.session_id,
        "channel_type": envelope.channel_type,
        "channel_id": envelope.channel_id,
        "user_id": envelope.user_id,
        "task_text": envelope.task_text,
        "session_messages": envelope.session_messages,
        "requested_model": envelope.requested_model,
        "requested_provider": envelope.requested_provider,
        "requested_mode": envelope.requested_lane,
        "risk_hint": envelope.risk_hint,
        "request_id": envelope.request_id,
        "metadata": envelope.metadata,
    }

    request = adapt_openclaw_request(request_payload)
    orchestrator = Orchestrator(repo_root)
    response = orchestrator.run(request)

    return {
        "status": response.status,
        "request_id": envelope.request_id,
        "agent_key": response.agent_key,
        "session_id": response.session_id,
        "compiled_checksum": response.compiled_checksum,
        "message": response.message,
        "metadata": response.metadata,
    }
