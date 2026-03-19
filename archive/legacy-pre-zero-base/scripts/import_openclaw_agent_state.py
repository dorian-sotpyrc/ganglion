from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_text_if_exists(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace").strip()


def extract_session_messages(session_jsonl: Path, limit: int = 12) -> list[str]:
    messages: list[str] = []
    if not session_jsonl.exists():
        return messages
    for line in session_jsonl.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("type") != "message":
            continue
        message = obj.get("message", {})
        if message.get("role") != "user":
            continue
        chunks = message.get("content", [])
        texts = [str(chunk.get("text", "")).strip() for chunk in chunks if chunk.get("type") == "text"]
        text = "\n".join(t for t in texts if t).strip()
        if text:
            messages.append(text)
    return messages[-limit:]


def main() -> None:
    parser = argparse.ArgumentParser(description="Import legacy OpenClaw agent state into Ganglion imported_state bundle")
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--agent-key", required=True)
    parser.add_argument("--workspace-dir", required=True)
    parser.add_argument("--agent-root", required=True, help="OpenClaw agent root (contains memory.json, sessions/, etc)")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    agent_key = args.agent_key.strip().lower()
    workspace_dir = Path(args.workspace_dir).resolve()
    agent_root = Path(args.agent_root).resolve()

    out_dir = repo_root / "artifacts" / "imported_state" / agent_key
    out_dir.mkdir(parents=True, exist_ok=True)

    workspace_memory = read_text_if_exists(workspace_dir / "MEMORY.md")
    legacy_memory_payload: dict[str, Any] = {}
    memory_json = agent_root / "memory.json"
    if memory_json.exists():
        legacy_memory_payload = json.loads(memory_json.read_text(encoding="utf-8"))

    sessions_index_path = agent_root / "sessions" / "sessions.json"
    sessions_index: dict[str, Any] = {}
    if sessions_index_path.exists():
        sessions_index = json.loads(sessions_index_path.read_text(encoding="utf-8"))

    transcript_path = None
    if sessions_index:
        newest = max(
            sessions_index.values(),
            key=lambda item: item.get("updatedAt", 0),
        )
        if newest.get("sessionFile"):
            candidate = Path(newest["sessionFile"])
            if candidate.exists():
                transcript_path = candidate
            else:
                local_candidate = agent_root / "sessions" / candidate.name
                if local_candidate.exists():
                    transcript_path = local_candidate

    if transcript_path is None:
        session_dir = agent_root / "sessions"
        jsonl_files = sorted(session_dir.glob("*.jsonl")) if session_dir.exists() else []
        if jsonl_files:
            transcript_path = jsonl_files[-1]

    session_messages = extract_session_messages(transcript_path) if transcript_path else []

    critical: list[dict[str, Any]] = []
    if workspace_memory:
        critical.append(
            {
                "memory_id": f"{agent_key}-workspace-memory",
                "text": workspace_memory,
                "confidence": 0.95,
                "tags": ["workspace", "memory", agent_key],
                "source": str(workspace_dir / "MEMORY.md"),
            }
        )

    for idx, entry in enumerate(legacy_memory_payload.get("entries", []), start=1):
        summary = str(entry.get("summary", "")).strip()
        if not summary:
            continue
        critical.append(
            {
                "memory_id": str(entry.get("memory_id") or f"{agent_key}-legacy-critical-{idx:03d}"),
                "text": summary,
                "confidence": 0.9,
                "tags": [str(tag) for tag in entry.get("tags", [])],
                "source": str(memory_json),
            }
        )

    episodic: list[dict[str, Any]] = []
    for idx, msg in enumerate(session_messages, start=1):
        episodic.append(
            {
                "memory_id": f"{agent_key}-session-{idx:03d}",
                "text": msg,
                "confidence": 0.75,
                "tags": ["session", "imported", agent_key],
                "source": str(transcript_path) if transcript_path else "unknown",
            }
        )

    bundle = {
        "agent_key": agent_key,
        "critical": critical,
        "episodic": episodic,
        "session_summary_seed": " | ".join(m.replace("\n", " ") for m in session_messages[-4:]),
        "sources": {
            "workspace_memory": str(workspace_dir / "MEMORY.md"),
            "legacy_memory_json": str(memory_json),
            "sessions_index": str(sessions_index_path),
            "transcript": str(transcript_path) if transcript_path else None,
        },
    }

    (out_dir / "memory_bundle.json").write_text(json.dumps(bundle, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "output": str(out_dir / 'memory_bundle.json'), "critical": len(critical), "episodic": len(episodic)}, indent=2))


if __name__ == "__main__":
    main()
