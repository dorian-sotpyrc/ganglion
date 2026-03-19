from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "src"))

from ganglion.live_binding import derive_channel_id, handle_live_binding


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: render_live_binding.py <payload-json-file>")

    payload_path = Path(sys.argv[1]).resolve()
    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    if not payload.get("channel_id"):
        channel_id = derive_channel_id(payload)
        if channel_id:
            payload["channel_id"] = channel_id

    result = handle_live_binding(REPO_ROOT, payload)
    sys.stdout.write(
        json.dumps(
            {
                "ok": True,
                "rewrite": result["rewrite"],
                "artifact_path": result["ganglion_metadata"]["artifact_path"],
                "compiled_checksum": result["ganglion_metadata"]["compiled_checksum"],
                "trace_id": result["trace_id"],
                "run_id": result["run_id"],
            }
        )
    )


if __name__ == "__main__":
    main()
