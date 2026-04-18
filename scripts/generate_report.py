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

from config import PROJECT_ROOT, today_local, MODEL


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
4. Generate the morning briefing report in this EXACT section order:
   - **Top-Line Summary** (3-5 bullets max)
   - **What Changed Since Yesterday**
   - **Top 3 Unblockers**
   - **Review Queue** with these subsections: **Urgent Today**, **Review Soon**, **Watchlist**
   - **Status Board**
   - **New Overnight Signals**
   - **Recommended Actions Today**
5. Save the report to `wiki/reports/{date}-morning-briefing.md`.

## Formatting Requirements

- Optimize for **team leads** and immediate operational action.
- Keep section order stable and deterministic.
- Use only these severity labels when you need a priority marker: **critical**, **high**, **medium**, **watch**.
- Use only these contributor status labels: **Backlog**, **In Progress**, **Stuck**, **Ready to Hand Off**.
- Every item in **Top 3 Unblockers** must include:
  - **Owner**
  - **Next step**
  - **Due window**
  - **Why now**
- Keep prose tight. Prefer tables and short bullets over long narrative paragraphs.
- Clearly separate **new information from the last 24 hours** from older backlog context.

## Report Header
```
# Morning Briefing — {date}
> Generated from: raw/github-daily/{date}-am.md
> Purpose: What needs attention today (wt-project 4.1 + 4.2)
```

## Tone
Direct, specific, and action-first. Use names, PR numbers, and concrete owner/action language. No fluff.

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
5. Compare the two snapshots and generate the EOD summary in this EXACT section order:
   - **Top-Line Summary** (3-5 bullets max)
   - **Morning Commitments vs Actual Outcomes**
   - **Day at a Glance**
   - **Resolved Today**
   - **Newly Stuck Today**
   - **Proof of Progress**
   - **Risks & Burnout Signals**
   - **Carry-Over to Tomorrow**
   - **Tomorrow's First Moves**
6. Save the report to `wiki/reports/{date}-eod-summary.md`.

## Formatting Requirements

- Optimize for **team leads** who need a scoreboard and handoff, not a retrospective essay.
- Keep section order stable and deterministic.
- Use only these severity labels when needed: **critical**, **high**, **medium**, **watch**.
- Use only these status labels: **Backlog**, **In Progress**, **Stuck**, **Ready to Hand Off**.
- Put the comparison of the morning plan vs actual outcomes near the top.
- Keep **Proof of Progress** concise and evidence-based, ideally as a table or short bullets with links.
- End with a short, concrete next-step handoff for the next morning briefing.

## Report Header
```
# End-of-Day Summary — {date}
> Generated from: AM + PM snapshots
> Purpose: What got done today, proof of progress, and concerns (wt-project 4.1 + 4.3)
```

## Tone
Factual, concise, and operational. Highlight wins, blockers, and what needs to happen first tomorrow.

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
6. Generate the dashboard in this EXACT section order:
   - **Top-Line Summary** (3-5 bullets max)
   - **Team Health Score**
   - **Repo Health Split**
   - **Top Risks**
   - **Top Manager Actions**
   - **Key Metrics vs Targets**
   - **Needs Help Now**
   - **Monitor This Week**
   - **Confidence / Freshness**
   - **Success Metrics Tracker**
7. Save the report to `wiki/reports/{date}-team-dashboard.md`.

## Formatting Requirements

- Optimize for **team leads** who need to decide what to do next.
- Lead with the most actionable information above the fold.
- Keep section order stable and deterministic.
- Use only these severity labels when needed: **critical**, **high**, **medium**, **watch**.
- Use only these status labels: **Backlog**, **In Progress**, **Stuck**, **Ready to Hand Off**.
- Make the dashboard scan-friendly: prefer concise bullets and tables over long prose.
- In **Key Metrics vs Targets**, show current value, target, and trend direction where possible.
- In **Needs Help Now**, include named owners and concrete actions.
- In **Monitor This Week**, separate watch items from immediate interventions.
- In **Confidence / Freshness**, explicitly say whether the dashboard is complete, partial, or using fallback/limited data.

## Report Header
```
# Team Dashboard — {date}
> Purpose: Management overview for team leads (wt-project 4.4)
> Data: Daily snapshots from raw/github-daily/
```

## Tone
Decision-oriented, crisp, and operational. Lead with what needs intervention now.
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
            model=MODEL,
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
