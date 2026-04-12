#!/usr/bin/env python3
"""
Team Pulse — Shared Configuration

Central location for paths, timezone, and environment-derived constants.
Import from here instead of re-defining these in each script.
"""

import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent

SCRIPTS_DIR  = PROJECT_ROOT / "scripts"
RAW_DIR      = PROJECT_ROOT / "raw" / "github-daily"
WIKI_DIR     = PROJECT_ROOT / "wiki"
WIKI_LOG     = WIKI_DIR / "log.md"
OUTPUTS_DIR  = PROJECT_ROOT / "outputs"
SESSIONS_DIR = OUTPUTS_DIR / ".sessions"
COMPILE_LOCK = PROJECT_ROOT / ".compile-lock"

# ── Timezone ───────────────────────────────────────────────────────────
# Override by setting TZ_OFFSET_HOURS in .env (integer UTC offset).
# Default: 7 (UTC+7, Asia/Bangkok / ICT).
_offset = int(os.environ.get("TZ_OFFSET_HOURS", "7"))
TZ = timezone(timedelta(hours=_offset))

# ── Model ──────────────────────────────────────────────────────────────
# Override by setting ANTHROPIC_MODEL in .env. Default: latest Sonnet.
# All Agent SDK call sites (ask_server, compile, generate_report) read
# from here so the project is reproducible across machines regardless of
# whatever the operator's local claude CLI defaults to.
MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6")


def now_local() -> datetime:
    """Current datetime in the configured local timezone."""
    return datetime.now(TZ)


def today_local() -> str:
    """Today's date string (YYYY-MM-DD) in the configured local timezone."""
    return now_local().strftime("%Y-%m-%d")
