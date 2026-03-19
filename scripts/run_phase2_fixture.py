#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

from ganglion.pipeline import MockProviderAdapter, run_pipeline


def main() -> int:
    if len(sys.argv) != 4:
        print("usage: run_phase2_fixture.py <ingress-json> <runtime-root> <success|error>", file=sys.stderr)
        return 2
    ingress_path = Path(sys.argv[1])
    runtime_root = Path(sys.argv[2])
    mode = sys.argv[3]
    ingress = json.loads(ingress_path.read_text(encoding="utf-8"))
    adapter = MockProviderAdapter(mode=mode, response_text="__ECHO__")
    result = run_pipeline(ingress, runtime_root=runtime_root, adapter=adapter)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
