from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_render_live_binding_uses_imported_agent_state(repo_root: Path = Path(__file__).resolve().parents[2]) -> None:
    imported = repo_root / "artifacts" / "imported_state" / "surgeon"
    imported.mkdir(parents=True, exist_ok=True)
    (imported / "memory_bundle.json").write_text(
        json.dumps(
            {
                "agent_key": "surgeon",
                "critical": [
                    {
                        "memory_id": "crit-1",
                        "text": "Surgeon is a conservative, evidence-first environment specialist.",
                        "tags": ["safety", "evidence"],
                        "source": "test",
                    }
                ],
                "episodic": [
                    {
                        "memory_id": "epi-1",
                        "text": "A prior host review checked SSH posture and firewall exposure first.",
                        "tags": ["ssh", "firewall", "host"],
                        "source": "test",
                    }
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    payload = {
        "request_id": "req-1",
        "agent_key": "surgeon",
        "session_id": "sess-1",
        "channel_type": "discord",
        "channel_id": "chan-1",
        "user_id": "user-1",
        "task_text": "Review this confidential host issue.",
        "session_messages": ["Need a careful answer."],
        "requested_model": "gpt-5.4",
        "requested_provider": "openai-codex",
        "metadata": {"source": "test"},
    }
    payload_path = repo_root / "artifacts" / "test_render_live_binding_payload.json"
    payload_path.write_text(json.dumps(payload), encoding="utf-8")

    proc = subprocess.run(
        [sys.executable, str(repo_root / "scripts" / "render_live_binding.py"), str(payload_path)],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )
    out = json.loads(proc.stdout)
    assert out["ok"] is True
    assert "Ganglion Pilot Context" in out["rewrite"]
    assert "evidence-first environment specialist" in out["rewrite"]
    assert "confidential host issue" in out["rewrite"]


def test_render_live_binding_derives_missing_channel_id(repo_root: Path = Path(__file__).resolve().parents[2]) -> None:
    payload = {
        "request_id": "req-2",
        "agent_key": "surgeon",
        "session_id": "agent:surgeon:discord:channel:1234567890",
        "channel_type": "discord",
        "user_id": "user-1",
        "task_text": "Check host posture.",
        "session_messages": ["Check host posture."],
        "requested_model": "gpt-5.4",
        "requested_provider": "openai-codex",
        "metadata": {"source": "test"},
    }
    payload_path = repo_root / "artifacts" / "test_render_live_binding_missing_channel.json"
    payload_path.write_text(json.dumps(payload), encoding="utf-8")

    proc = subprocess.run(
        [sys.executable, str(repo_root / "scripts" / "render_live_binding.py"), str(payload_path)],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )
    out = json.loads(proc.stdout)
    assert out["ok"] is True
    assert "Ganglion Pilot Context" in out["rewrite"]
