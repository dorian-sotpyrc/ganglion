from __future__ import annotations

from pathlib import Path
from typing import Any

from ganglion.antennule.request_adapter import adapt_openclaw_request
from ganglion.pleon.orchestrator import Orchestrator


def handle_openclaw_request(repo_root: str | Path, payload: dict[str, Any]) -> dict[str, Any]:
    request = adapt_openclaw_request(payload)
    orchestrator = Orchestrator(repo_root)
    response = orchestrator.run(request)

    return {
        "status": response.status,
        "agent_key": response.agent_key,
        "session_id": response.session_id,
        "compiled_checksum": response.compiled_checksum,
        "message": response.message,
        "metadata": response.metadata,
    }
