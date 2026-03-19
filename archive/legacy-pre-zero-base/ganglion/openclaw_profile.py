from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

INTEGRATION_PROFILE_OPENCLAW_STRICT = "openclaw_strict"
SESSION_COMPACTIONS_DIRNAME = "session_compactions"
IMPORTED_STATE_DIRNAME = "imported_state"
RUNS_DIRNAME = "runs"
TRACES_DIRNAME = "traces"
BRAIN_METRICS_DIRNAME = "brain_metrics"


@dataclass(frozen=True)
class OpenClawStrictPolicy:
    integration_profile: str = INTEGRATION_PROFILE_OPENCLAW_STRICT
    require_request_id: bool = True
    require_agent_key: bool = True
    require_session_id: bool = True
    require_channel_type: bool = True
    require_channel_id: bool = True
    require_user_id: bool = True
    require_task_text: bool = True
    require_metadata_dict: bool = True
    require_naming_conventions: bool = True


def canonical_trace_path(root: str | Path, request_id: str) -> Path:
    return Path(root) / TRACES_DIRNAME / f"{request_id}.json"


def canonical_run_path(root: str | Path, session_id: str) -> Path:
    return Path(root) / RUNS_DIRNAME / f"{session_id}.json"


def canonical_imported_state_path(root: str | Path, agent_key: str) -> Path:
    return Path(root) / IMPORTED_STATE_DIRNAME / agent_key / "memory_bundle.json"


def canonical_session_compaction_path(root: str | Path, agent_key: str, session_id: str) -> Path:
    return Path(root) / SESSION_COMPACTIONS_DIRNAME / agent_key / f"{session_id}.json"
