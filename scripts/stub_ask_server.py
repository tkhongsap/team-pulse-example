#!/usr/bin/env python3
"""
Stub Ask Server for E2E testing.

Returns deterministic SSE responses in the same format as the real ask_server.py,
so Playwright can exercise the full UI -> Next API -> SSE flow without Anthropic.
"""

import argparse
import json
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler


STUB_ANSWER = "This is an E2E stub response. The real server uses Claude Agent SDK."


class StubHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok", "stub": True}).encode())

    def do_POST(self) -> None:
        if self.path != "/ask":
            self.send_error(404)
            return

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
            return

        question = data.get("question", "").strip()
        if not question:
            self.send_error(400, "Missing question")
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "close")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        result = json.dumps({
            "text": STUB_ANSWER,
            "cost": 0.0,
            "sessionId": None,
            "sources": ["wiki/index.md"],
        })
        self.wfile.write(f"event: result\ndata: {result}\n\n".encode())
        self.wfile.write(b"event: done\ndata: {}\n\n")
        self.wfile.flush()

    def do_OPTIONS(self) -> None:
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, format: str, *args: object) -> None:
        print(f"[stub-ask] {args[0] if args else ''}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Stub Ask Server for E2E tests")
    parser.add_argument("--port", type=int, default=3999, help="Server port")
    args = parser.parse_args()

    server = ThreadingHTTPServer(("0.0.0.0", args.port), StubHandler)
    print(f"Stub ask server running on http://localhost:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down stub...")
        server.server_close()


if __name__ == "__main__":
    main()
