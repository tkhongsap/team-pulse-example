#!/usr/bin/env python3
"""
Team Pulse — Wiki Compilation via Agent SDK

Reads wiki/log.md to find uncompiled raw sources in raw/github-daily/,
then uses the Claude Agent SDK to compile new knowledge into wiki articles.

Usage:
    python scripts/compile.py              # compile all unprocessed files
    python scripts/compile.py 2026-04-11   # compile specific date only
"""

import argparse
import asyncio
import os
import re
import sys
import time
from datetime import datetime, timedelta

from dotenv import load_dotenv

from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, query

from config import PROJECT_ROOT, RAW_DIR, WIKI_LOG, COMPILE_LOCK


def load_env() -> None:
    """Load .env file and verify ANTHROPIC_API_KEY is set."""
    load_dotenv(PROJECT_ROOT / ".env")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print(
            "Error: ANTHROPIC_API_KEY environment variable is required.",
            file=sys.stderr,
        )
        print("Set it in .env or export it directly.", file=sys.stderr)
        sys.exit(1)


def get_raw_files() -> list[str]:
    """List all raw source files in raw/github-daily/."""
    if not RAW_DIR.exists():
        return []
    return sorted(f.name for f in RAW_DIR.iterdir() if f.suffix == ".md")


def get_compiled_files() -> set[str]:
    """Parse wiki/log.md to find already-compiled raw file names.

    Handles both explicit file references (raw/github-daily/YYYY-MM-DD-am.md)
    and range expressions (... through ...) found in the bootstrap log entry.
    """
    if not WIKI_LOG.exists():
        return set()

    log_content = WIKI_LOG.read_text()
    compiled: set[str] = set()

    # Find explicit file references
    for match in re.finditer(
        r"raw/github-daily/(\d{4}-\d{2}-\d{2}-(am|pm)\.md)", log_content
    ):
        compiled.add(match.group(1))

    # Expand "through" ranges (e.g., bootstrap log entry)
    range_pattern = (
        r"raw/github-daily/(\d{4}-\d{2}-\d{2})-(am|pm)\.md"
        r"\s+through\s+"
        r"raw/github-daily/(\d{4}-\d{2}-\d{2})-(am|pm)\.md"
    )
    for match in re.finditer(range_pattern, log_content):
        start_date = datetime.strptime(match.group(1), "%Y-%m-%d").date()
        end_date = datetime.strptime(match.group(3), "%Y-%m-%d").date()
        current = start_date
        while current <= end_date:
            date_str = current.strftime("%Y-%m-%d")
            compiled.add(f"{date_str}-am.md")
            compiled.add(f"{date_str}-pm.md")
            current += timedelta(days=1)

    return compiled


def find_uncompiled(date_filter: str | None = None) -> list[str]:
    """Find raw files that haven't been compiled yet."""
    all_files = get_raw_files()
    compiled = get_compiled_files()

    uncompiled = [f for f in all_files if f not in compiled]

    if date_filter:
        uncompiled = [f for f in uncompiled if f.startswith(date_filter)]

    return uncompiled


def build_prompt(uncompiled_files: list[str]) -> str:
    """Build the compilation prompt for the Agent SDK."""
    file_list = "\n".join(f"- raw/github-daily/{f}" for f in uncompiled_files)

    return f"""You are the Team Pulse wiki compiler. Compile the following new raw source files into the wiki.

## Files to Compile

{file_list}

## Instructions

1. Read `wiki/log.md` to understand what has already been compiled.
2. Read `wiki/index.md` to understand what articles already exist.
3. For each new raw source file listed above:
   a. Read the file fully from `raw/github-daily/`.
   b. Extract knowledge into wiki articles:
      - **Contributors**: Create or update `wiki/contributors/{{name}}.md` for each active contributor. Accumulate their activity, patterns, and roles across days.
      - **Projects**: Create or update `wiki/projects/{{repo}}.md` for each tracked repo. Track health trajectory, PR patterns, issue trends.
      - **Patterns**: Create or update `wiki/patterns/{{pattern}}.md` when you detect recurring signals (stuck items, burnout, review bottlenecks, velocity changes).
      - **Connections**: Create `wiki/connections/{{slug}}.md` when you discover non-obvious relationships between two or more concepts.
   c. Each article must follow the format in CLAUDE.md (YAML frontmatter + structured markdown).
   d. Use `[[wikilinks]]` to connect related articles.
4. Update `wiki/index.md` — add new rows, update summaries and dates for modified articles.
5. Append to `wiki/log.md` with timestamp and summary:
   ```
   ## [YYYY-MM-DD] ingest | compiled {{N}} files
   - Articles created: [[contributors/name]], [[patterns/name]]
   - Articles updated: [[projects/gstack]], [[contributors/garrytan]]
   - Sources: {', '.join(f'raw/github-daily/{f}' for f in uncompiled_files)}
   ```

## Guidelines

- **Accumulate, don't replace.** When updating an existing article, ADD new information from the latest source. Don't overwrite what was already there.
- **Be specific.** Use PR numbers, commit counts, dates, and names. Not "someone was busy" but "garrytan merged 3 PRs and committed at 03:13 UTC."
- **Detect patterns across days.** If you see recurring signals across multiple snapshots, create or update pattern articles.
- **Keep articles 200-500 words.** Dense and scannable, not verbose.
- **Track resolutions.** Compare today's stuck items against previous days. Items that were stuck but are now merged/closed = RESOLVED.
"""


async def run_compile(date_filter: str | None = None, force: bool = False) -> None:
    """Main compilation workflow."""
    load_env()

    print("Team Pulse — Wiki Compilation")
    print(f"Project root: {PROJECT_ROOT}")
    print()

    # Lock file guard — prevents partial wiki state from a crashed prior run
    if COMPILE_LOCK.exists():
        if force:
            print(f"Warning: Stale lock file found at {COMPILE_LOCK}. Proceeding (--force).")
            COMPILE_LOCK.unlink()
        else:
            print(
                f"Error: Lock file exists at {COMPILE_LOCK}",
                file=sys.stderr,
            )
            print(
                "A previous compile may have been interrupted. Inspect wiki/ for partial state,",
                file=sys.stderr,
            )
            print("then remove the lock file or re-run with --force.", file=sys.stderr)
            sys.exit(1)

    # Find uncompiled files
    uncompiled = find_uncompiled(date_filter)

    if not uncompiled:
        if date_filter:
            print(f"No uncompiled files found for date: {date_filter}")
        else:
            print("All raw files have already been compiled. Nothing to do.")
        return

    print(f"Found {len(uncompiled)} uncompiled file(s):")
    for f in uncompiled:
        print(f"  - raw/github-daily/{f}")
    print()

    # Build prompt and run Agent SDK
    prompt = build_prompt(uncompiled)

    print("Starting Agent SDK compilation...")
    start_time = time.time()

    result_text = ""
    total_cost = 0.0

    COMPILE_LOCK.write_text(f"locked at {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}\n")
    try:
        async for message in query(
            prompt=prompt,
            options=ClaudeAgentOptions(
                allowed_tools=["Read", "Write", "Edit", "Glob", "Grep"],
                setting_sources=["project"],
                permission_mode="acceptEdits",
                cwd=str(PROJECT_ROOT),
                max_turns=50,
            ),
        ):
            if isinstance(message, ResultMessage):
                result_text = message.result or ""
                total_cost = message.total_cost_usd or 0.0
    finally:
        if COMPILE_LOCK.exists():
            COMPILE_LOCK.unlink()

    elapsed = time.time() - start_time

    # Print summary
    print()
    print("=" * 60)
    print("Compilation Complete")
    print("=" * 60)
    print(f"Files compiled: {len(uncompiled)}")
    print(f"Time elapsed:   {elapsed:.1f}s")
    print(f"Estimated cost: ${total_cost:.4f}")
    print()
    if result_text:
        # Truncate long results for console output
        preview = result_text[:1000]
        if len(result_text) > 1000:
            preview += "\n... (truncated)"
        print("Agent summary:")
        print(preview)


def main() -> None:
    """Entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description="Team Pulse — Compile raw sources into wiki articles via Agent SDK",
    )
    parser.add_argument(
        "date",
        nargs="?",
        default=None,
        help="Optional date filter (YYYY-MM-DD). Compiles only that date's files.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Ignore a stale lock file and proceed anyway.",
    )
    args = parser.parse_args()

    asyncio.run(run_compile(args.date, force=args.force))


if __name__ == "__main__":
    main()
