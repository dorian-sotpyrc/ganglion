from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Augment a Ganglion run artifact with actual metrics")
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--input-tokens", type=float)
    parser.add_argument("--output-tokens", type=float)
    parser.add_argument("--total-tokens", type=float)
    parser.add_argument("--latency-ms", type=float)
    parser.add_argument("--cost-usd", type=float)
    args = parser.parse_args()

    run_path = Path(args.repo_root) / "artifacts" / "runs" / f"{args.session_id}.json"
    if not run_path.exists():
        raise SystemExit(f"run artifact not found: {run_path}")
    doc = json.loads(run_path.read_text(encoding="utf-8"))
    payload = doc.setdefault("payload", {})
    actual = payload.setdefault("actual_metrics", {})
    if args.input_tokens is not None:
        actual["input_tokens"] = args.input_tokens
    if args.output_tokens is not None:
        actual["output_tokens"] = args.output_tokens
    if args.total_tokens is not None:
        actual["total_tokens"] = args.total_tokens
    if args.latency_ms is not None:
        actual["latency_ms"] = args.latency_ms
    if args.cost_usd is not None:
        actual["cost_usd"] = args.cost_usd
    run_path.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "run_path": str(run_path), "actual_metrics": actual}, indent=2))


if __name__ == "__main__":
    main()
