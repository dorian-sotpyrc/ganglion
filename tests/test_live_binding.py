from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from ganglion.live_binding import handle_live_binding


def test_handle_live_binding_uses_imported_state(tmp_path: Path, repo_root: Path = Path(__file__).resolve().parents[1]) -> None:
    imported = tmp_path / "artifacts" / "imported_state" / "william"
    imported.mkdir(parents=True, exist_ok=True)
    (imported / "memory_bundle.json").write_text(
        json.dumps(
            {
                "agent_key": "william",
                "critical": [
                    {"memory_id": "crit-1", "text": "William is a conservative cybersecurity specialist.", "source": "test"}
                ],
                "episodic": [
                    {"memory_id": "epi-1", "text": "He previously reviewed a confidential edge host issue.", "source": "test"}
                ],
                "session_summary_seed": "Prior issue involved confidential edge host checks.",
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    payload = {
        "request_id": "req-1",
        "agent_key": "william",
        "session_id": "agent:william:discord:channel:1234567890",
        "channel_type": "discord",
        "task_text": "Review this confidential host issue.",
        "session_messages": ["Need a careful answer."],
        "requested_model": "gpt-5.4",
        "requested_provider": "openai",
        "metadata": {"source": "test"},
        "timestamp": "2026-03-19T02:30:00Z",
    }
    result = handle_live_binding(tmp_path, payload)
    assert result["status"] == "success"
    assert "Ganglion Pilot Context" in result["rewrite"]
    assert "conservative cybersecurity specialist" in result["rewrite"]
    assert "confidential host issue" in result["rewrite"]
    assert Path(result["ganglion_metadata"]["artifact_path"]).exists()


def test_render_live_binding_script_derives_missing_channel_id(tmp_path: Path) -> None:
    imported = tmp_path / "artifacts" / "imported_state" / "william"
    imported.mkdir(parents=True, exist_ok=True)
    (imported / "memory_bundle.json").write_text(json.dumps({"agent_key": "william", "critical": [], "episodic": []}), encoding="utf-8")
    payload = {
        "request_id": "req-2",
        "agent_key": "william",
        "session_id": "agent:william:discord:channel:1234567890",
        "channel_type": "discord",
        "task_text": "Check host posture.",
        "session_messages": ["Check host posture."],
        "requested_model": "gpt-5.4",
        "requested_provider": "openai",
        "metadata": {"source": "test"},
        "timestamp": "2026-03-19T02:30:00Z",
    }
    payload_path = tmp_path / "payload.json"
    payload_path.write_text(json.dumps(payload), encoding="utf-8")

    # run via a temp repo copy layout
    (tmp_path / "scripts").mkdir(exist_ok=True)
    (tmp_path / "src").mkdir(exist_ok=True)
    subprocess.run(["cp", str(Path(__file__).resolve().parents[1] / "scripts" / "render_live_binding.py"), str(tmp_path / "scripts" / "render_live_binding.py")], check=True)
    subprocess.run(["cp", "-R", str(Path(__file__).resolve().parents[1] / "src" / "ganglion"), str(tmp_path / "src" / "ganglion")], check=True)

    proc = subprocess.run(
        [sys.executable, str(tmp_path / "scripts" / "render_live_binding.py"), str(payload_path)],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
    )
    out = json.loads(proc.stdout)
    assert out["ok"] is True
    assert "Ganglion Pilot Context" in out["rewrite"]
