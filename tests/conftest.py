import socket
import subprocess
import sys
import time
from pathlib import Path
from unittest.mock import MagicMock

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ── Import path setup ────────────────────────────────────────────────
# Add scripts/ so tests can `import team_pulse`, `import config`, etc.
_scripts_dir = str(PROJECT_ROOT / "scripts")
if _scripts_dir not in sys.path:
    sys.path.insert(0, _scripts_dir)

# Mock claude_agent_sdk before compile.py is imported (it imports at module level)
if "claude_agent_sdk" not in sys.modules:
    sys.modules["claude_agent_sdk"] = MagicMock()


# ── Factory helpers ──────────────────────────────────────────────────

def make_pr(**overrides):
    """Return a dict resembling a GitHub API PR response."""
    pr = {
        "number": 1,
        "title": "Add feature X",
        "state": "open",
        "created_at": "2026-04-10T10:00:00Z",
        "merged_at": None,
        "html_url": "https://github.com/owner/repo/pull/1",
        "user": {"login": "alice"},
        "labels": [],
        "requested_reviewers": [],
        "merged_by": None,
    }
    pr.update(overrides)
    return pr


def make_issue(**overrides):
    """Return a dict resembling a GitHub API issue response."""
    issue = {
        "number": 10,
        "title": "Bug in widget",
        "state": "open",
        "created_at": "2026-04-10T10:00:00Z",
        "closed_at": None,
        "updated_at": "2026-04-10T10:00:00Z",
        "html_url": "https://github.com/owner/repo/issues/10",
        "user": {"login": "bob"},
        "labels": [],
        "assignees": [],
        "comments": 0,
    }
    issue.update(overrides)
    return issue


def make_repo_data(**overrides):
    """Return a single repo_data entry for aggregate/report functions."""
    data = {
        "repo": "owner/repo",
        "commits": [],
        "prs_opened": [],
        "prs_merged": [],
        "open_prs": [],
        "issues_opened": [],
        "issues_closed": [],
        "open_issues": [],
    }
    data.update(overrides)
    return data


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _wait_for_port(port: int, timeout: float = 10.0) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.5):
                return
        except OSError:
            time.sleep(0.2)
    raise TimeoutError(f"Server on port {port} did not start within {timeout}s")


@pytest.fixture(scope="session")
def ask_server():
    """Start the real ask_server.py on an ephemeral port."""
    port = _free_port()
    proc = subprocess.Popen(
        [sys.executable, str(PROJECT_ROOT / "scripts" / "ask_server.py"), "--port", str(port)],
        cwd=str(PROJECT_ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        _wait_for_port(port)
        yield f"http://127.0.0.1:{port}"
    finally:
        proc.terminate()
        proc.wait(timeout=5)
