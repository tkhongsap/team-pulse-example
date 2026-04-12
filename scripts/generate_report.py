#!/usr/bin/env python3
"""
Team Pulse — Report Generation via Agent SDK

Generates morning briefings, EOD summaries, or management dashboards
by sending the appropriate prompt to the Claude Agent SDK.

Usage:
    python scripts/generate_report.py --type morning
    python scripts/generate_report.py --type eod --date 2026-04-11
    python scripts/generate_report.py --type dashboard
"""

import argparse
import asyncio
import os
import sys
import time
from datetime import datetime, timedelta

from dotenv import load_dotenv

from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, query

from config import PROJECT_ROOT, today_local


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




def build_morning_prompt(date: str) -> str:
    """Build the morning briefing prompt."""
    return f"""You are the Team Pulse morning briefing analyst. Produce an actionable morning briefing for {date}.

## Instructions

1. Read the AM snapshot at `raw/github-daily/{date}-am.md`.
2. Read `wiki/index.md` to find relevant wiki articles (contributor profiles, patterns, project history). Read the most relevant articles for context.
3. Read the organizational context at `docs/wt-project.md` (sections 4.1 and 4.2).
4. Generate the morning briefing report with these sections:
   - **Top Priorities Today** (3-5 items ranked by urgency with owners and actions)
   - **Status Board** (each contributor categorized: Backlog / In Progress / Stuck / Ready to Hand Off)
   - **Review Queue** (PRs needing review, sorted by age)
   - **Stuck Items Triage** (what's stuck, why, and how to unblock)
   - **Overnight Activity** (new issues/PRs/comments since last check)
5. Save the report to `wiki/reports/{date}-morning-briefing.md`.

## Report Header
```
# Morning Briefing — {date}
> Generated from: raw/github-daily/{date}-am.md
> Purpose: What needs attention today (wt-project 4.1 + 4.2)
```

## Tone
Direct and actionable. Use names, PR numbers, and specific recommendations. No fluff.

If the AM snapshot doesn't exist for {date}, report that the file is missing and suggest running:
`python scripts/team_pulse.py --period am --date {date}`
"""


def build_eod_prompt(date: str) -> str:
    """Build the EOD summary prompt."""
    return f"""You are the Team Pulse end-of-day analyst. Compare the day's AM and PM snapshots to produce an EOD summary for {date}.

## Instructions

1. Read BOTH snapshot files:
   - `raw/github-daily/{date}-am.md` (morning state)
   - `raw/github-daily/{date}-pm.md` (evening state)
2. Read `wiki/reports/{date}-morning-briefing.md` if it exists (for cross-referencing morning priorities vs evening outcomes).
3. Read `wiki/index.md` and relevant wiki articles for context.
4. Read the organizational context at `docs/wt-project.md` (sections 4.1 and 4.3).
5. Compare the two snapshots and generate the EOD summary with these sections:
   - **Day at a Glance** (AM vs PM comparison table with deltas)
   - **Proof of Progress** (verifiable output per contributor per wt-project 4.1)
   - **What Got Done** (narrative of accomplishments)
   - **Morning vs Evening Cross-Reference** (if morning briefing exists: priority outcomes table)
   - **What Didn't Get Done** (items still stuck, PRs that aged)
   - **Burnout & Workload Signals** (late-night commits, weekend work, overload — per wt-project 4.3)
   - **Tomorrow's Carry-Over** (items for first thing tomorrow)
6. Save the report to `wiki/reports/{date}-eod-summary.md`.

## Report Header
```
# End-of-Day Summary — {date}
> Generated from: AM + PM snapshots
> Purpose: What got done today, proof of progress, and concerns (wt-project 4.1 + 4.3)
```

## Tone
Factual and evidence-based. Highlight wins but don't hide concerns. Use names, PR numbers, commit counts.

If either snapshot is missing, report which file is needed and suggest:
`python scripts/team_pulse.py --period am|pm --date {date}`
"""


def build_dashboard_prompt(date: str) -> str:
    """Build the management dashboard prompt."""
    # Calculate 7-day range for trend analysis
    end_date = datetime.strptime(date, "%Y-%m-%d")
    start_date = end_date - timedelta(days=6)
    start_str = start_date.strftime("%Y-%m-%d")

    return f"""You are the Team Pulse management dashboard analyst. Produce a team health report for {date}.

## Instructions

1. Read the latest snapshots for {date}:
   - `raw/github-daily/{date}-am.md`
   - `raw/github-daily/{date}-pm.md` (if available)
2. For trend analysis, read snapshots from {start_str} to {date} (7 days) in `raw/github-daily/`.
3. Read the organizational context at `docs/wt-project.md` (sections 4.2, 4.3, 4.4, and 6).
4. Check `wiki/reports/` for prior briefings and summaries for context.
5. Read relevant wiki articles from `wiki/index.md`.
6. Generate the dashboard with these sections:
   - **Team Health Score** (1-10 scale with factor breakdown: velocity, stuck ratio, workload balance, review responsiveness, burnout risk)
   - **Status Distribution** (each contributor categorized per wt-project 4.2)
   - **Who Needs Help** (stuck contributors, burnout risk, idle, blocked PRs — with actions)
   - **Key Metrics** (today vs 7-day avg with trends)
   - **Week-over-Week Trends** (velocity, stuck items, balance)
   - **Recommendations** (3-5 specific actions for the team lead)
   - **Success Metrics Tracker** (per wt-project section 6)
7. Save the report to `wiki/reports/{date}-team-dashboard.md`.

## Report Header
```
# Team Dashboard — {date}
> Purpose: Management overview for team leads (wt-project 4.4)
> Data: Daily snapshots from raw/github-daily/
```

## Tone
Executive-level: concise, scannable, decision-oriented. Lead with what needs attention.
"""


PROMPT_BUILDERS = {
    "morning": build_morning_prompt,
    "eod": build_eod_prompt,
    "dashboard": build_dashboard_prompt,
}

OUTPUT_FILES = {
    "morning": "morning-briefing",
    "eod": "eod-summary",
    "dashboard": "team-dashboard",
}

REPORT_LABELS = {
    "morning": "Morning Briefing",
    "eod": "End-of-Day Summary",
    "dashboard": "Team Dashboard",
}


async def run_report(report_type: str, date: str) -> None:
    """Generate a report using the Agent SDK."""
    load_env()

    label = REPORT_LABELS[report_type]
    output_name = OUTPUT_FILES[report_type]
    output_path = f"wiki/reports/{date}-{output_name}.md"

    print(f"Team Pulse — {label}")
    print(f"Date: {date}")
    print(f"Output: {output_path}")
    print()

    # Build the prompt
    prompt = PROMPT_BUILDERS[report_type](date)

    print("Starting Agent SDK report generation...")
    start_time = time.time()

    result_text = ""
    total_cost = 0.0

    async for message in query(
        prompt=prompt,
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Glob", "Grep", "Write"],
            setting_sources=["project"],
            permission_mode="acceptEdits",
            cwd=str(PROJECT_ROOT),
            max_turns=30,
        ),
    ):
        if isinstance(message, ResultMessage):
            result_text = message.result or ""
            total_cost = message.total_cost_usd or 0.0

    elapsed = time.time() - start_time

    # Print summary
    print()
    print("=" * 60)
    print(f"{label} Complete")
    print("=" * 60)
    print(f"Output: {output_path}")
    print(f"Time elapsed: {elapsed:.1f}s")
    print(f"Estimated cost: ${total_cost:.4f}")
    print()
    if result_text:
        preview = result_text[:500]
        if len(result_text) > 500:
            preview += "\n... (truncated)"
        print("Agent summary:")
        print(preview)


def main() -> None:
    """Entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description="Team Pulse — Generate reports via Agent SDK",
    )
    parser.add_argument(
        "--type",
        choices=["morning", "eod", "dashboard"],
        required=True,
        help="Report type: morning (briefing), eod (end-of-day summary), or dashboard",
    )
    parser.add_argument(
        "--date",
        default=None,
        help="Target date (YYYY-MM-DD). Defaults to today in Bangkok time.",
    )
    args = parser.parse_args()

    date = args.date or today_local()

    asyncio.run(run_report(args.type, date))


if __name__ == "__main__":
    main()
