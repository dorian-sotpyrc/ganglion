from __future__ import annotations

from pathlib import Path
import json

from ganglion.antennule.openclaw_adapter import handle_openclaw_request


def main() -> None:
    payload = {
        "request_id": "req-harness-001",
        "agent_key": "surgeon",
        "session_id": "sess-harness-001",
        "channel_type": "discord",
        "channel_id": "chan-harness-001",
        "user_id": "user-harness-001",
        "task_text": "Review this confidential service failure and prepare rollback guidance.",
        "session_messages": [
            "Service failed after restart.",
            "Need logs and rollback plan.",
        ],
        "requested_model": "gpt-5.4",
        "metadata": {"source": "step7a_harness"},
    }
    result = handle_openclaw_request(Path.cwd(), payload)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
