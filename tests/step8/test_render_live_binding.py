from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_render_live_binding_uses_william_imported_state(repo_root: Path = Path(__file__).resolve().parents[2]) -> None:
    imported = repo_root / "artifacts" / "imported_state" / "william"
    imported.mkdir(parents=True, exist_ok=True)
    (imported / "memory_bundle.json").write_text(
        json.dumps(
            {
                "agent_key": "william",
                "critical": [
                    {
                        "memory_id": "crit-1",
                        "text": "William is a conservative, evidence-first security specialist.",
                        "tags": ["security", "evidence"],
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
        "agent_key": "william",
        "session_id": "sess-1",
        "channel_type": "discord",
        "channel_id": "chan-1",
        "user_id": "user-1",
        "task_text": "Review this confidential host issue.",
        "session_messages": ["Need a careful security answer."],
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
    assert "Ganglion William Pilot Context" in out["rewrite"]
    assert "evidence-first security specialist" in out["rewrite"]
    assert "confidential host issue" in out["rewrite"]
