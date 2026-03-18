from __future__ import annotations

import argparse
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from ganglion.cortex_api import CortexMetricsService


def make_handler(service: CortexMetricsService):
    class Handler(BaseHTTPRequestHandler):
        def _send(self, body: dict, status: int = 200) -> None:
            payload = json.dumps(body, indent=2).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def do_GET(self) -> None:  # noqa: N802
            parsed = urlparse(self.path)
            parts = [p for p in parsed.path.split("/") if p]
            if parsed.path == "/cortex/health":
                return self._send({"ok": True, "service": "ganglion-cortex-api"})
            if parsed.path == "/cortex/brains":
                return self._send(service.brains_index())
            if len(parts) == 3 and parts[0] == "cortex" and parts[1] == "brains":
                agent_key = parts[2]
                return self._send({"brain": service.brain_overview(agent_key).__dict__})
            return self._send({"error": "Not found"}, status=HTTPStatus.NOT_FOUND)

        def log_message(self, format: str, *args) -> None:  # noqa: A003
            return

    return Handler


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Ganglion Cortex API")
    parser.add_argument("--repo-root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()

    service = CortexMetricsService(args.repo_root)
    server = ThreadingHTTPServer((args.host, args.port), make_handler(service))
    print(json.dumps({"ok": True, "service": "ganglion-cortex-api", "host": args.host, "port": args.port}))
    server.serve_forever()


if __name__ == "__main__":
    main()
