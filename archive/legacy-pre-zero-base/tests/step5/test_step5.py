from __future__ import annotations

from pathlib import Path
import json

from ganglion.antennule.openclaw_adapter import handle_openclaw_request
from ganglion.forager.search import ArchiveSearch
from ganglion.ventral.service import MemoryService


def test_critical_memory_loads() -> None:
    svc = MemoryService()
    items = svc.get_critical_memory("surgeon")
    assert len(items) >= 1
    assert items[0].memory_type == "critical"


def test_relevant_episodic_memory_is_selected() -> None:
    svc = MemoryService()
    items = svc.get_relevant_episodic_memory("surgeon", "Check service logs and diagnosis flow")
    assert len(items) >= 1


def test_session_summary_compacts() -> None:
    svc = MemoryService()
    summary = svc.build_session_summary(["a" * 300, "b" * 300], max_chars=120)
    assert len(summary) <= 120
    assert summary.endswith("...")


def test_archive_search_returns_results() -> None:
    search = ArchiveSearch(Path.cwd() / "artifacts" / "archive_docs")
    results = search.search("service logs")
    assert len(results) >= 1


def test_run_artifact_is_written() -> None:
    payload = {
        "agent_key": "surgeon",
        "session_id": "sess-step5-artifact",
        "channel_type": "discord",
        "channel_id": "chan-step5-artifact",
        "user_id": "user-step5-artifact",
        "task_text": "Diagnose service logs for this confidential task.",
        "session_messages": [
            "Service failed after restart.",
            "Need to check logs and dependencies.",
        ],
    }
    response = handle_openclaw_request(Path.cwd(), payload)
    artifact_path = Path(response["metadata"]["artifact_path"])
    assert artifact_path.exists()
    body = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert body["payload"]["agent_key"] == "surgeon"
    assert body["payload"]["memory"]["critical_count"] >= 1
