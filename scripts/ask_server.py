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
import time
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

from dotenv import load_dotenv

from config import PROJECT_ROOT, SESSIONS_DIR, MODEL

load_dotenv(PROJECT_ROOT / ".env")

# Session storage — persisted to outputs/.sessions/{sessionId}.json
SESSIONS_DIR.mkdir(parents=True, exist_ok=True)


def _load_session(session_id: str) -> str | None:
    """Load a session resume token from disk, or None if not found."""
    path = SESSIONS_DIR / f"{session_id}.json"
    if path.exists():
        try:
            return json.loads(path.read_text()).get("resume")
        except (json.JSONDecodeError, OSError):
            return None
    return None


def _save_session(session_id: str, resume_token: str) -> None:
    """Persist a session resume token to disk."""
    path = SESSIONS_DIR / f"{session_id}.json"
    try:
        path.write_text(json.dumps({"session_id": session_id, "resume": resume_token}))
    except OSError:
        pass


def _normalize_question(question: str) -> str:
    return " ".join(
        question.lower()
        .replace("—", "-")
        .replace("–", "-")
        .replace("’", "'")
        .split()
    )


def _strip_frontmatter(text: str) -> str:
    if text.startswith("---\n"):
        parts = text.split("\n---\n", 1)
        if len(parts) == 2:
            return parts[1]
    return text


def _read_relative_markdown(relative_path: str) -> str | None:
    path = PROJECT_ROOT / relative_path
    if not path.exists():
        return None

    try:
        return _strip_frontmatter(path.read_text()).strip()
    except OSError:
        return None


def _latest_report_path(suffix: str) -> str | None:
    reports_dir = PROJECT_ROOT / "wiki" / "reports"
    matches = sorted(reports_dir.glob(f"*{suffix}"))
    if not matches:
        return None

    latest = matches[-1]
    return latest.relative_to(PROJECT_ROOT).as_posix()


def _build_structured_prompt(question: str) -> tuple[str, list[str], str] | None:
    normalized = _normalize_question(question)
    relative_paths: list[str] = []
    instruction = ""
    progress_status = "Loading selected Team Pulse sources..."

    if "morning briefing" in normalized or "top priorities" in normalized:
        latest_briefing = _latest_report_path("-morning-briefing.md")
        if not latest_briefing:
            return None
        relative_paths = [latest_briefing]
        instruction = (
            "Answer using only the provided morning briefing. "
            "Return a concise markdown briefing with top priorities and action items."
        )
        progress_status = "Loading the latest morning briefing..."
    elif "weekly team health summary" in normalized or (
        "weekly" in normalized and "management" in normalized and "team" in normalized
    ):
        latest_eod = _latest_report_path("-eod-summary.md")
        relative_paths = [
            "wiki/patterns/review-bottleneck.md",
            "wiki/patterns/stuck-items-growth.md",
            "wiki/patterns/burnout-signals.md",
            "wiki/connections/sole-maintainer-and-stuck-growth.md",
            "wiki/projects/gstack.md",
            "wiki/projects/autoresearch.md",
        ]
        if latest_eod:
            relative_paths.insert(0, latest_eod)
        instruction = (
            "Write a weekly team health summary for management. "
            "Highlight overall status, major risks, and concrete actions."
        )
        progress_status = "Loading weekly health sources..."
    elif "compare" in normalized and "gstack" in normalized and "autoresearch" in normalized:
        relative_paths = [
            "wiki/projects/gstack.md",
            "wiki/projects/autoresearch.md",
            "wiki/patterns/review-bottleneck.md",
            "wiki/patterns/stuck-items-growth.md",
        ]
        instruction = (
            "Compare the health of gstack and autoresearch. "
            "Explain which repo needs more attention and why."
        )
        progress_status = "Loading repo health sources..."
    elif "burnout risk" in normalized or (
        "highest burnout risk" in normalized and "stuck" in normalized
    ):
        latest_eod = _latest_report_path("-eod-summary.md")
        relative_paths = [
            "wiki/patterns/burnout-signals.md",
            "wiki/patterns/review-bottleneck.md",
            "wiki/patterns/stuck-items-growth.md",
            "wiki/connections/sole-maintainer-and-stuck-growth.md",
            "wiki/projects/gstack.md",
            "wiki/projects/autoresearch.md",
        ]
        if latest_eod:
            relative_paths.insert(0, latest_eod)
        instruction = (
            "Identify who needs help most urgently. "
            "Call out burnout risks, blocked contributors, and the clearest manager actions."
        )
        progress_status = "Loading burnout and bottleneck sources..."
    else:
        return None

    selected_docs: list[tuple[str, str]] = []
    for relative_path in relative_paths:
        content = _read_relative_markdown(relative_path)
        if content:
            selected_docs.append((relative_path, content))

    if not selected_docs:
        return None

    context = "\n\n".join(
        f"## Source: {relative_path}\n{content}"
        for relative_path, content in selected_docs
    )

    prompt = f"""Answer the following Team Pulse question using only the preselected source documents below.
Do not use tools. Do not rely on unstated assumptions.
Keep the answer concise, factual, and management-friendly.
{instruction}

Question: {question}

Source documents:
{context}"""

    return prompt, [relative_path for relative_path, _ in selected_docs], progress_status

SERVER_START = time.time()


def _build_status_html(project_root: str, uptime: str, has_key: bool) -> str:
    key_dot = "#22c55e" if has_key else "#ef4444"
    key_label = "Configured" if has_key else "Missing"
    return f"""\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Team Pulse &mdash; Ask Server</title>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
                 Helvetica, Arial, sans-serif;
    background: #f8fafc; color: #1e293b; padding: 2rem 1rem;
    display: flex; flex-direction: column; align-items: center;
    min-height: 100vh;
  }}
  .container {{ max-width: 560px; width: 100%; }}
  header {{
    display: flex; align-items: center; gap: .75rem;
    margin-bottom: 1.5rem;
  }}
  header .dot {{
    width: 12px; height: 12px; border-radius: 50%;
    background: #22c55e; flex-shrink: 0;
    box-shadow: 0 0 6px rgba(34,197,94,.5);
  }}
  header h1 {{ font-size: 1.25rem; font-weight: 600; }}
  .card {{
    background: #fff; border: 1px solid #e2e8f0; border-radius: .75rem;
    padding: 1.25rem 1.5rem; margin-bottom: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,.04);
  }}
  .card h2 {{
    font-size: .75rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: .05em; color: #94a3b8; margin-bottom: .75rem;
  }}
  .row {{
    display: flex; justify-content: space-between; align-items: center;
    padding: .4rem 0; border-bottom: 1px solid #f1f5f9;
  }}
  .row:last-child {{ border-bottom: none; }}
  .label {{ color: #64748b; font-size: .875rem; }}
  .value {{ font-size: .875rem; font-weight: 500; font-family: "SF Mono",
            "Cascadia Code", "Fira Code", Menlo, monospace; }}
  .badge {{
    display: inline-flex; align-items: center; gap: .35rem;
    font-size: .8rem; font-weight: 500; padding: .15rem .55rem;
    border-radius: 9999px;
  }}
  .badge .dot {{ width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }}
  .endpoint {{
    display: flex; align-items: baseline; gap: .5rem;
    padding: .5rem 0; border-bottom: 1px solid #f1f5f9;
  }}
  .endpoint:last-child {{ border-bottom: none; }}
  .method {{
    font-size: .7rem; font-weight: 700; padding: .15rem .4rem;
    border-radius: .25rem; font-family: monospace;
  }}
  .method-get {{ background: #dbeafe; color: #1d4ed8; }}
  .method-post {{ background: #dcfce7; color: #15803d; }}
  .path {{ font-family: monospace; font-size: .875rem; font-weight: 500; }}
  .desc {{ color: #64748b; font-size: .8rem; margin-left: auto; }}
  footer {{
    margin-top: 1.5rem; text-align: center;
    font-size: .75rem; color: #94a3b8;
  }}
</style>
</head>
<body>
  <div class="container">
    <header>
      <div class="dot"></div>
      <h1>Team Pulse &mdash; Ask Server</h1>
    </header>

    <div class="card">
      <h2>Status</h2>
      <div class="row">
        <span class="label">Service</span>
        <span class="value">team-pulse-ask-server</span>
      </div>
      <div class="row">
        <span class="label">Status</span>
        <span class="badge">
          <span class="dot" style="background:#22c55e"></span> Healthy
        </span>
      </div>
      <div class="row">
        <span class="label">Uptime</span>
        <span class="value">{uptime}</span>
      </div>
      <div class="row">
        <span class="label">Anthropic API Key</span>
        <span class="badge">
          <span class="dot" style="background:{key_dot}"></span> {key_label}
        </span>
      </div>
      <div class="row">
        <span class="label">Project Root</span>
        <span class="value" style="font-size:.75rem">{project_root}</span>
      </div>
    </div>

    <div class="card">
      <h2>Endpoints</h2>
      <div class="endpoint">
        <span class="method method-get">GET</span>
        <span class="path">/</span>
        <span class="desc">This status page</span>
      </div>
      <div class="endpoint">
        <span class="method method-get">GET</span>
        <span class="path">/health</span>
        <span class="desc">JSON health check</span>
      </div>
      <div class="endpoint">
        <span class="method method-post">POST</span>
        <span class="path">/ask</span>
        <span class="desc">SSE streaming query</span>
      </div>
    </div>

    <footer>Team Pulse Ask Server &middot; Agent SDK Streaming API</footer>
  </div>
</body>
</html>"""


def create_handler(project_root: str):
    """Create a request handler class with the project root bound."""

    class AskHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            """Health check: HTML status page at /, JSON at /health."""
            has_key = bool(os.environ.get("ANTHROPIC_API_KEY"))
            uptime_s = int(time.time() - SERVER_START)
            days, rem = divmod(uptime_s, 86400)
            hours, rem = divmod(rem, 3600)
            minutes, secs = divmod(rem, 60)
            parts = []
            if days:
                parts.append(f"{days}d")
            if hours:
                parts.append(f"{hours}h")
            if minutes:
                parts.append(f"{minutes}m")
            parts.append(f"{secs}s")
            uptime = " ".join(parts)

            if self.path == "/health":
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "ok",
                    "service": "team-pulse-ask-server",
                    "uptime": uptime,
                    "anthropic_key_set": has_key,
                }).encode())
                return

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(_build_status_html(
                project_root, uptime, has_key,
            ).encode())

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
                self.close_connection = True

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
                TextBlock,
                query,
            )

            resume_token = _load_session(session_id) if session_id else None
            result_text = ""
            new_session_id = session_id
            sources_read: list[str] = []
            last_progress = ""

            def send_progress(status: str) -> None:
                nonlocal last_progress
                if status and status != last_progress:
                    last_progress = status
                    self._send_sse("progress", json.dumps({"status": status}))

            structured_query = _build_structured_prompt(question)
            if structured_query:
                prompt, structured_sources, initial_status = structured_query
                sources_read.extend(structured_sources)
                send_progress(initial_status)
                send_progress("Drafting the summary...")

                structured_options = ClaudeAgentOptions(
                    model=MODEL,
                    allowed_tools=[],
                    setting_sources=["project"],
                    permission_mode="default",
                    cwd=cwd,
                    max_turns=2,
                )
                if resume_token:
                    structured_options.resume = resume_token

                cost = 0.0
                async for message in query(prompt=prompt, options=structured_options):
                    if isinstance(message, SystemMessage):
                        if hasattr(message, "data") and isinstance(message.data, dict):
                            sid = message.data.get("session_id")
                            if sid:
                                new_session_id = sid

                    if isinstance(message, AssistantMessage):
                        if hasattr(message, "content"):
                            for block in getattr(message, "content", []):
                                if isinstance(block, TextBlock):
                                    result_text += block.text

                    if isinstance(message, ResultMessage):
                        if not result_text:
                            result_text = message.result or ""
                        cost = message.total_cost_usd or 0.0
                        if new_session_id and hasattr(message, "session_id"):
                            _save_session(new_session_id, message.session_id)

                self._send_sse(
                    "result",
                    json.dumps({
                        "text": result_text or "No response generated.",
                        "cost": cost,
                        "sessionId": new_session_id,
                        "sources": sources_read,
                    }),
                )
                self._send_sse("done", "{}")
                return

            options = ClaudeAgentOptions(
                model=MODEL,
                allowed_tools=["Read"],
                setting_sources=["project"],
                permission_mode="default",
                cwd=cwd,
                max_turns=8,
            )
            if resume_token:
                options.resume = resume_token

            wiki_index = ""
            index_path = PROJECT_ROOT / "wiki" / "index.md"
            try:
                wiki_index = index_path.read_text()
            except OSError:
                pass

            if wiki_index:
                prompt = f"""Answer the following question using the Team Pulse wiki.
The wiki index is included below, so do not read wiki/index.md again.
Use the index to identify the 2-4 most relevant articles.
Read only those articles unless you need one extra source to resolve ambiguity.
Keep the answer concise, factual, and management-friendly.
Stop reading once you have enough evidence and produce the final answer within this request.

Wiki index:
{wiki_index}

Question: {question}"""
            else:
                prompt = f"""Answer the following question using the Team Pulse wiki.
Read wiki/index.md first to identify the 2-4 most relevant articles.
Read only those articles unless you need one extra source to resolve ambiguity.
Keep the answer concise, factual, and management-friendly.
Stop reading once you have enough evidence and produce the final answer within this request.

Question: {question}"""

            send_progress(
                "Loaded wiki index..." if wiki_index else "Starting Team Pulse research..."
            )

            async for message in query(prompt=prompt, options=options):
                if isinstance(message, SystemMessage):
                    # Capture session ID from init
                    if hasattr(message, "data") and isinstance(message.data, dict):
                        sid = message.data.get("session_id")
                        if sid:
                            new_session_id = sid
                            send_progress("Reading the team wiki...")

                if isinstance(message, AssistantMessage):
                    # Track Read tool calls for source citations
                    if hasattr(message, "content"):
                        for block in getattr(message, "content", []):
                            block_name = getattr(block, "name", "")
                            if block_name == "Read":
                                block_input = getattr(block, "input", {})
                                file_path = ""
                                if isinstance(block_input, dict):
                                    file_path = block_input.get("file_path", "")
                                if "wiki/" in file_path and file_path not in sources_read:
                                    # Extract relative path from wiki/
                                    wiki_idx = file_path.find("wiki/")
                                    if wiki_idx >= 0:
                                        rel = file_path[wiki_idx:]
                                        if rel not in sources_read:
                                            sources_read.append(rel)
                                        if rel == "wiki/index.md":
                                            send_progress("Scanning wiki index...")
                                        else:
                                            send_progress(f"Reading {rel}...")
                            elif block_name in {"Glob", "Grep"}:
                                send_progress("Finding the most relevant wiki articles...")

                if isinstance(message, ResultMessage):
                    result_text = message.result or ""
                    cost = message.total_cost_usd or 0.0
                    send_progress("Drafting the summary...")
                    if new_session_id and hasattr(message, "session_id"):
                        _save_session(new_session_id, message.session_id)
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
    server = ThreadingHTTPServer(("0.0.0.0", args.port), handler)
    print(f"Ask server running on http://localhost:{args.port}")
    print(f"Project root: {PROJECT_ROOT}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.server_close()


if __name__ == "__main__":
    main()
