from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ganglion.antennule.openclaw_adapter import handle_openclaw_request


MAX_MEMORY_ITEMS = 4
MAX_ITEM_CHARS = 280


def shorten(text: str, limit: int) -> str:
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: render_live_binding.py <payload-json-file>")

    payload_path = Path(sys.argv[1]).resolve()
    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    repo_root = REPO_ROOT
    agent_key = str(payload.get("agent_key") or "agent").strip() or "agent"

    result = handle_openclaw_request(repo_root, payload)
    metadata = result.get("metadata", {})
    memory = metadata.get("memory", {})
    routing = metadata.get("routing", {})

    critical = [shorten(str(x), MAX_ITEM_CHARS) for x in memory.get("critical", [])[:MAX_MEMORY_ITEMS]]
    episodic = [shorten(str(x), MAX_ITEM_CHARS) for x in memory.get("episodic", [])[:MAX_MEMORY_ITEMS]]
    session_summary = shorten(str(memory.get("session_summary", "")), 600)
    execution_note = shorten(str(result.get("message", "")), 500)
    runtime_checksum = str(result.get("compiled_checksum", ""))

    lines = [
        "[Ganglion Pilot Context]",
        f"Use the following as {agent_key}'s active brain/memory/routing context for this turn.",
        "Do not mention Ganglion unless the user explicitly asks.",
        f"Brain checksum: {runtime_checksum}",
        f"Routing lane: {routing.get('lane', 'unknown')}",
        f"Provider/model intent: {routing.get('provider', 'unknown')}/{routing.get('model', 'unknown')}",
    ]

    if critical:
        lines.append("Critical memory:")
        lines.extend(f"- {item}" for item in critical)
    if episodic:
        lines.append("Relevant episodic memory:")
        lines.extend(f"- {item}" for item in episodic)
    if session_summary:
        lines.append(f"Session summary: {session_summary}")
    if execution_note:
        lines.append(f"Execution note: {execution_note}")

    lines.extend(
        [
            f"Answer as {agent_key} in the agent's normal voice, using the Ganglion context above to guide memory and judgment.",
            "--- END GANGLION PILOT CONTEXT ---",
            payload.get("task_text", ""),
        ]
    )

    sys.stdout.write(
        json.dumps(
            {
                "ok": True,
                "rewrite": "\n\n".join(lines).strip(),
                "artifact_path": metadata.get("artifact_path"),
                "trace_path": metadata.get("trace_path"),
                "compiled_checksum": runtime_checksum,
            }
        )
    )


if __name__ == "__main__":
    main()
