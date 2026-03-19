from pathlib import Path
import json

from ganglion.antennule.openclaw_adapter import handle_openclaw_request
from ganglion.ventral.service import MemoryService


def test_imported_memory_bundle_is_loaded(tmp_path: Path) -> None:
    imported = tmp_path / "artifacts" / "imported_state" / "surgeon"
    imported.mkdir(parents=True)
    payload = {
        "agent_key": "surgeon",
        "critical": [
            {
                "memory_id": "s-crit-001",
                "text": "Surgeon handles conservative environment review.",
                "tags": ["safety", "surgeon"],
                "source": "test",
            }
        ],
        "episodic": [
            {
                "memory_id": "s-epi-001",
                "text": "Previous host check reviewed firewall and SSH posture.",
                "tags": ["host", "firewall", "ssh"],
                "source": "test",
            }
        ],
    }
    (imported / "memory_bundle.json").write_text(json.dumps(payload), encoding="utf-8")

    svc = MemoryService(tmp_path)
    critical = svc.get_critical_memory("surgeon")
    episodic = svc.get_relevant_episodic_memory("surgeon", "Review host firewall and ssh posture")

    assert critical
    assert critical[0].text == "Surgeon handles conservative environment review."
    assert episodic
    assert "firewall" in episodic[0].text.lower()


def test_handle_request_uses_imported_agent_state(repo_root: Path = Path(__file__).resolve().parents[2]) -> None:
    imported = repo_root / "artifacts" / "imported_state" / "surgeon"
    imported.mkdir(parents=True, exist_ok=True)
    bundle = {
        "agent_key": "surgeon",
        "critical": [
            {
                "memory_id": "s-crit-002",
                "text": "Surgeon is an evidence-first environment specialist.",
                "tags": ["safety", "evidence"],
                "source": "test",
            }
        ],
        "episodic": [
            {
                "memory_id": "s-epi-002",
                "text": "A prior confidential host review required stronger routing.",
                "tags": ["confidential", "host", "routing"],
                "source": "test",
            }
        ],
    }
    (imported / "memory_bundle.json").write_text(json.dumps(bundle, indent=2), encoding="utf-8")

    result = handle_openclaw_request(
        repo_root,
        {
            "request_id": "req-surgeon-test-001",
            "agent_key": "surgeon",
            "session_id": "sess-surgeon-test-001",
            "channel_type": "discord",
            "channel_id": "chan-surgeon-test-001",
            "user_id": "user-test-001",
            "task_text": "Review this confidential host issue and outline risks.",
            "session_messages": ["Earlier host concern", "Need evidence-first review"],
            "requested_model": "gpt-5.4",
            "metadata": {"source": "test"},
        },
    )

    assert result["status"] == "ok"
    assert result["agent_key"] == "surgeon"
    assert result["metadata"]["memory"]["critical"]
    assert "evidence-first environment specialist" in " ".join(result["metadata"]["memory"]["critical"])
