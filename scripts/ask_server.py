#!/usr/bin/env python3
"""
Team Pulse — Ask Server (Agent SDK Streaming API)

Lightweight HTTP server that accepts questions and streams Agent SDK
responses via Server-Sent Events. Used by the Next.js web app.

Usage:
    python scripts/ask_server.py              # starts on port 3001
    python scripts/ask_server.py --port 3002  # custom port
"""

import argparse
import asyncio
import json
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from threading import Thread

from dotenv import load_dotenv

# Project root (parent of scripts/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

# Session storage (in-memory for v1)
sessions: dict[str, str] = {}


def create_handler(project_root: str):
    """Create a request handler class with the project root bound."""

    class AskHandler(BaseHTTPRequestHandler):
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
            session_id = data.get("sessionId")

            if not question:
                self.send_error(400, "Missing question")
                return

            if not os.environ.get("ANTHROPIC_API_KEY"):
                self.send_error(500, "ANTHROPIC_API_KEY not configured")
                return

            # Set SSE headers
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            # Run the async Agent SDK query in a thread
            loop = asyncio.new_event_loop()
            try:
                loop.run_until_complete(
                    self._stream_response(question, session_id, project_root)
                )
            except Exception as e:
                self._send_sse("error", json.dumps({"error": str(e)}))
            finally:
                loop.close()

        def do_OPTIONS(self) -> None:
            """Handle CORS preflight."""
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()

        async def _stream_response(
            self, question: str, session_id: str | None, cwd: str
        ) -> None:
            from claude_agent_sdk import (
                ClaudeAgentOptions,
                ResultMessage,
                AssistantMessage,
                SystemMessage,
                query,
                ContentBlock,
                ToolUseBlock,
                ToolResultBlock,
            )

            options = ClaudeAgentOptions(
                allowed_tools=["Read", "Glob", "Grep"],
                setting_sources=["project"],
                permission_mode="bypassPermissions",
                cwd=cwd,
                max_turns=20,
            )

            if session_id and session_id in sessions:
                options.resume = sessions[session_id]

            prompt = f"""Answer the following question using the Team Pulse wiki.
Read wiki/index.md first to find relevant articles, then read those articles to answer.

Question: {question}"""

            result_text = ""
            new_session_id = None
            sources_read: list[str] = []

            async for message in query(prompt=prompt, options=options):
                if isinstance(message, SystemMessage):
                    # Capture session ID from init
                    if hasattr(message, "data") and isinstance(message.data, dict):
                        sid = message.data.get("session_id")
                        if sid:
                            new_session_id = sid

                if isinstance(message, AssistantMessage):
                    # Track Read tool calls for source citations
                    if hasattr(message, "content"):
                        for block in getattr(message, "content", []):
                            if hasattr(block, "name") and block.name == "Read":
                                file_path = getattr(block, "input", {}).get("file_path", "")
                                if "wiki/" in file_path and file_path not in sources_read:
                                    # Extract relative path from wiki/
                                    wiki_idx = file_path.find("wiki/")
                                    if wiki_idx >= 0:
                                        rel = file_path[wiki_idx:]
                                        if rel not in sources_read:
                                            sources_read.append(rel)

                if isinstance(message, ResultMessage):
                    result_text = message.result or ""
                    cost = message.total_cost_usd or 0.0
                    self._send_sse(
                        "result",
                        json.dumps({
                            "text": result_text,
                            "cost": cost,
                            "sessionId": new_session_id,
                            "sources": sources_read,
                        }),
                    )

            if not result_text:
                self._send_sse(
                    "result",
                    json.dumps({"text": "No response generated.", "cost": 0}),
                )

            self._send_sse("done", "{}")

        def _send_sse(self, event: str, data: str) -> None:
            try:
                self.wfile.write(f"event: {event}\ndata: {data}\n\n".encode())
                self.wfile.flush()
            except BrokenPipeError:
                pass

        def log_message(self, format: str, *args: object) -> None:
            # Quieter logging
            print(f"[ask-server] {args[0] if args else ''}")

    return AskHandler


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Team Pulse — Ask Server (Agent SDK Streaming API)",
    )
    parser.add_argument("--port", type=int, default=3001, help="Server port")
    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Warning: ANTHROPIC_API_KEY not set. Requests will fail.", file=sys.stderr)

    handler = create_handler(str(PROJECT_ROOT))
    server = HTTPServer(("0.0.0.0", args.port), handler)
    print(f"Ask server running on http://localhost:{args.port}")
    print(f"Project root: {PROJECT_ROOT}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.server_close()


if __name__ == "__main__":
    main()
