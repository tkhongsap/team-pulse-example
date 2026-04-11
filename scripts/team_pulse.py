#!/usr/bin/env python3
"""
Team Pulse — Daily GitHub Activity Snapshot (AM/PM)

Extracts daily activity from configured GitHub repos and writes a
structured markdown report to docs/daily/YYYY-MM-DD-am.md or -pm.md.

Designed to run twice daily (Bangkok time, UTC+7):
  - 07:00  →  Morning snapshot (what needs attention today)
  - 18:00  →  Evening snapshot (what got done today)

Prerequisites: gh CLI installed and authenticated.

Usage:
    python scripts/team_pulse.py                          # auto-detect AM/PM
    python scripts/team_pulse.py --period am              # force morning
    python scripts/team_pulse.py --period pm              # force evening
    python scripts/team_pulse.py --date 2026-04-11 --period am
    python scripts/team_pulse.py --date 2026-04-11 --period pm
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# ── Config ───────────────────────────────────────────────────���────────
DEFAULT_REPOS = [
    "karpathy/autoresearch",
    "garrytan/gstack",
]

def _get_repos_from_env() -> list[str] | None:
    """Read TEAM_PULSE_REPOS from environment if set."""
    env_repos = os.environ.get("TEAM_PULSE_REPOS")
    if env_repos:
        return [r.strip() for r in env_repos.split(",") if r.strip()]
    return None
STUCK_THRESHOLD_DAYS = 3
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "raw" / "github-daily"
PER_PAGE = 100  # max items per API page

# Bangkok timezone (ICT = UTC+7)
TZ_BANGKOK = timezone(timedelta(hours=7))

PERIOD_CONFIG = {
    "am": {
        "label": "Morning Snapshot",
        "time": "07:00",
        "icon": "sunrise",
        "focus": "What needs attention today",
        "prompts": [
            "Morning to-do list — prioritize what needs action today",
            "Stuck items triage — what's been blocked and who should unblock it",
            "Review queue — which PRs need review before they go stale",
            "Workload check — is anyone overloaded or idle heading into today",
        ],
    },
    "pm": {
        "label": "Evening Snapshot",
        "time": "18:00",
        "icon": "city_sunset",
        "focus": "What got done today",
        "prompts": [
            "End-of-day summary — what the team accomplished today",
            "Compare with this morning's snapshot — what changed during the day",
            "Unfinished items — what carried over and needs attention tomorrow",
            "Burnout signals — who worked late, who had an unusually heavy day",
        ],
    },
}


# ── GitHub API helpers ────────────────────────────────────────────────

def gh_api(endpoint, paginate=False):
    """Call `gh api` and return parsed JSON. Returns [] on failure."""
    cmd = ["gh", "api", endpoint]
    if paginate:
        cmd.append("--paginate")

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        print(f"  Warning: gh api {endpoint}: {result.stderr.strip()}", file=sys.stderr)
        return []

    text = result.stdout.strip()
    if not text:
        return []

    # --paginate can concatenate multiple JSON arrays: ][
    text = text.replace("]\n[", ",").replace("][", ",")
    try:
        data = json.loads(text)
        return data if isinstance(data, list) else [data]
    except json.JSONDecodeError:
        return []


# ── Data collection ───────────────────────────────────────────────────

def fetch_commits(repo, date_str):
    """Commits pushed to default branch on `date_str`."""
    since = f"{date_str}T00:00:00Z"
    next_day = (datetime.strptime(date_str, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
    until = f"{next_day}T00:00:00Z"

    raw = gh_api(
        f"repos/{repo}/commits?since={since}&until={until}&per_page={PER_PAGE}",
        paginate=True,
    )

    commits = []
    for c in raw:
        commit_obj = c.get("commit", {})
        author_info = commit_obj.get("author", {})
        ts = author_info.get("date", "")
        commits.append({
            "sha": c.get("sha", "")[:7],
            "author": (c.get("author") or {}).get("login") or author_info.get("name", "unknown"),
            "message": commit_obj.get("message", "").split("\n")[0][:80],
            "time": ts[11:16] if len(ts) > 16 else "",
            "hour": int(ts[11:13]) if len(ts) > 13 else -1,
            "url": c.get("html_url", ""),
        })
    return commits


def fetch_pulls(repo):
    """All recently-updated PRs (state=all, sorted by updated desc)."""
    return gh_api(
        f"repos/{repo}/pulls?state=all&sort=updated&direction=desc&per_page={PER_PAGE}",
    )


def fetch_issues(repo):
    """All recently-updated issues, excluding PRs."""
    raw = gh_api(
        f"repos/{repo}/issues?state=all&sort=updated&direction=desc&per_page={PER_PAGE}",
    )
    return [i for i in raw if "pull_request" not in i]


# ── Analysis / filtering ─────────────────────────────────────────────

def filter_prs_by_date(pulls, date_str):
    """Split pulls into: opened_today, merged_today, open_needing_attention."""
    opened_today = []
    merged_today = []
    open_prs = []

    ref_date = datetime.strptime(date_str, "%Y-%m-%d")

    for pr in pulls:
        created = pr.get("created_at", "")[:10]
        merged_at = pr.get("merged_at")
        state = pr.get("state", "")
        author = pr.get("user", {}).get("login", "unknown")
        title = pr.get("title", "")[:80]
        number = pr.get("number", 0)
        url = pr.get("html_url", "")
        labels = [l["name"] for l in pr.get("labels", [])]
        requested_reviewers = [r.get("login", "") for r in pr.get("requested_reviewers", [])]

        if created == date_str:
            opened_today.append({
                "number": number,
                "title": title,
                "author": author,
                "url": url,
                "labels": labels,
                "requested_reviewers": requested_reviewers,
            })

        if merged_at and merged_at[:10] == date_str:
            created_dt = _parse_ts(pr["created_at"])
            merged_dt = _parse_ts(merged_at)
            ttm_hours = (merged_dt - created_dt).total_seconds() / 3600 if created_dt and merged_dt else 0

            merged_today.append({
                "number": number,
                "title": title,
                "author": author,
                "merged_by": (pr.get("merged_by") or {}).get("login", "—"),
                "time_to_merge": _format_duration(ttm_hours),
                "url": url,
            })

        if state == "open":
            created_dt = _parse_ts(pr["created_at"])
            days_open = max(0, (ref_date - created_dt.replace(tzinfo=None)).days) if created_dt else 0

            open_prs.append({
                "number": number,
                "title": title,
                "author": author,
                "days_open": days_open,
                "requested_reviewers": requested_reviewers,
                "labels": labels,
                "url": url,
                "stuck": days_open >= STUCK_THRESHOLD_DAYS and len(requested_reviewers) == 0,
            })

    return opened_today, merged_today, open_prs


def filter_issues_by_date(issues, date_str):
    """Split issues into: opened_today, closed_today, open_issues."""
    opened_today = []
    closed_today = []
    open_issues = []

    ref_date = datetime.strptime(date_str, "%Y-%m-%d")

    for issue in issues:
        created = issue.get("created_at", "")[:10]
        closed_at = issue.get("closed_at")
        state = issue.get("state", "")
        author = issue.get("user", {}).get("login", "unknown")
        title = issue.get("title", "")[:80]
        number = issue.get("number", 0)
        url = issue.get("html_url", "")
        labels = [l["name"] for l in issue.get("labels", [])]
        assignees = [a.get("login", "") for a in issue.get("assignees", [])]
        comments = issue.get("comments", 0)

        if created == date_str:
            opened_today.append({
                "number": number,
                "title": title,
                "author": author,
                "labels": labels,
                "assignees": assignees,
                "url": url,
            })

        if closed_at and closed_at[:10] == date_str:
            closed_today.append({
                "number": number,
                "title": title,
                "author": author,
                "closed_by": author,
                "url": url,
            })

        if state == "open":
            last_update_dt = _parse_ts(issue.get("updated_at", ""))
            days_stale = max(0, (ref_date - last_update_dt.replace(tzinfo=None)).days) if last_update_dt else 0

            open_issues.append({
                "number": number,
                "title": title,
                "author": author,
                "assignees": assignees,
                "labels": labels,
                "comments": comments,
                "days_since_update": days_stale,
                "url": url,
                "stuck": days_stale >= STUCK_THRESHOLD_DAYS and comments == 0,
            })

    return opened_today, closed_today, open_issues


def aggregate_workload_by_assignee(repo_data):
    """Aggregate per-assignee workload from existing repo_data. No extra API calls."""
    people = {}

    for r in repo_data:
        # Count assigned open issues per person
        for issue in r["open_issues"]:
            for assignee in issue["assignees"]:
                people.setdefault(assignee, {
                    "assigned_issues": 0, "open_prs_authored": 0,
                    "review_requests": 0, "active_today": False,
                    "max_days_stale": 0,
                })
                people[assignee]["assigned_issues"] += 1
                people[assignee]["max_days_stale"] = max(
                    people[assignee]["max_days_stale"], issue["days_since_update"]
                )

        # Count open PRs authored per person
        for pr in r["open_prs"]:
            name = pr["author"]
            people.setdefault(name, {
                "assigned_issues": 0, "open_prs_authored": 0,
                "review_requests": 0, "active_today": False,
                "max_days_stale": 0,
            })
            people[name]["open_prs_authored"] += 1

        # Count review requests per person
        for pr in r["open_prs"]:
            for reviewer in pr.get("requested_reviewers", []):
                people.setdefault(reviewer, {
                    "assigned_issues": 0, "open_prs_authored": 0,
                    "review_requests": 0, "active_today": False,
                    "max_days_stale": 0,
                })
                people[reviewer]["review_requests"] += 1

        # Detect today's activity from commits, prs_opened, prs_merged
        for c in r["commits"]:
            if c["author"] in people:
                people[c["author"]]["active_today"] = True
        for p in r["prs_opened"]:
            if p["author"] in people:
                people[p["author"]]["active_today"] = True
        for p in r["prs_merged"]:
            if p["author"] in people:
                people[p["author"]]["active_today"] = True

    # Assign status
    result = []
    for name, stats in sorted(people.items()):
        total_load = stats["assigned_issues"] + stats["open_prs_authored"] + stats["review_requests"]
        if total_load == 0:
            status = "Idle"
        elif stats["active_today"]:
            status = "In Progress"
        elif stats["assigned_issues"] > 0 and stats["max_days_stale"] >= STUCK_THRESHOLD_DAYS:
            status = "Stuck"
        else:
            status = "Backlog"

        result.append({
            "assignee": name,
            "assigned_issues": stats["assigned_issues"],
            "open_prs_authored": stats["open_prs_authored"],
            "review_requests": stats["review_requests"],
            "status": status,
        })

    return result


# ── Helpers ───────────────────────────────────────────────────────────

def _parse_ts(ts_str):
    """Parse ISO timestamp string to datetime."""
    if not ts_str:
        return None
    try:
        return datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
    except ValueError:
        return None


def _format_duration(hours):
    """Human-readable duration from hours."""
    if hours < 1:
        return f"{int(hours * 60)}m"
    if hours < 24:
        return f"{hours:.1f}h"
    days = hours / 24
    return f"{days:.1f}d"


def _label_str(labels):
    if not labels:
        return ""
    return " ".join(f"`{l}`" for l in labels)


def _now_bangkok():
    """Current datetime in Bangkok timezone."""
    return datetime.now(TZ_BANGKOK)


def _detect_period():
    """Auto-detect AM or PM based on Bangkok time. Before 12:00 = am."""
    now = _now_bangkok()
    return "am" if now.hour < 12 else "pm"


# ── Markdown report generation ────────────────────────────────────────

def generate_report(date_str, period, repo_data, output_dir):
    """Build the full daily pulse markdown from collected repo data."""
    conf = PERIOD_CONFIG[period]
    now_bkk = _now_bangkok()
    lines = []
    w = lines.append

    # ── Header ──
    w(f"# Daily Pulse — {date_str} ({conf['label']})")
    w("")
    w(f"> Period: **{period.upper()}** ({conf['focus']})")
    w(f"> Snapshot taken: {now_bkk.strftime('%Y-%m-%d %H:%M')} (Bangkok, UTC+7)")
    w(f"> Repos: {', '.join(r['repo'] for r in repo_data)}")

    # Reference the other snapshot if it exists
    other_period = "pm" if period == "am" else "am"
    other_file = output_dir / f"{date_str}-{other_period}.md"
    if other_file.exists():
        w(f"> Companion: [{date_str}-{other_period}.md]({date_str}-{other_period}.md)")
    w("")

    # ── Totals bar ──
    total_commits = sum(len(r["commits"]) for r in repo_data)
    total_prs_opened = sum(len(r["prs_opened"]) for r in repo_data)
    total_prs_merged = sum(len(r["prs_merged"]) for r in repo_data)
    total_issues_opened = sum(len(r["issues_opened"]) for r in repo_data)
    total_issues_closed = sum(len(r["issues_closed"]) for r in repo_data)
    total_open_prs = sum(len(r["open_prs"]) for r in repo_data)
    total_open_issues = sum(len(r["open_issues"]) for r in repo_data)
    stuck_prs = sum(1 for r in repo_data for p in r["open_prs"] if p["stuck"])
    stuck_issues = sum(1 for r in repo_data for i in r["open_issues"] if i["stuck"])

    w("## Summary")
    w("")
    w("| Metric | Count |")
    w("|--------|-------|")
    w(f"| Commits | {total_commits} |")
    w(f"| PRs opened | {total_prs_opened} |")
    w(f"| PRs merged | {total_prs_merged} |")
    w(f"| Issues opened | {total_issues_opened} |")
    w(f"| Issues closed | {total_issues_closed} |")
    w(f"| Open PRs | {total_open_prs} |")
    w(f"| Open issues | {total_open_issues} |")
    w(f"| Stuck PRs (>{STUCK_THRESHOLD_DAYS}d, no reviewer) | {stuck_prs} |")
    w(f"| Stuck issues (>{STUCK_THRESHOLD_DAYS}d, no comments) | {stuck_issues} |")
    w("")

    # ── Commits ──
    w("---")
    w("")
    w(f"## Commits ({total_commits})")
    w("")
    if total_commits == 0:
        w("_No commits on this date._")
    else:
        w("| Repo | Author | Message | Time (UTC) |")
        w("|------|--------|---------|------------|")
        for r in repo_data:
            repo_short = r["repo"].split("/")[1]
            for c in r["commits"]:
                w(f"| {repo_short} | {c['author']} | {c['message']} | {c['time']} |")
    w("")

    # ── PRs Opened ──
    w("---")
    w("")
    w(f"## PRs Opened ({total_prs_opened})")
    w("")
    if total_prs_opened == 0:
        w("_No PRs opened on this date._")
    else:
        w("| Repo | # | Author | Title | Reviewers | Labels |")
        w("|------|---|--------|-------|-----------|--------|")
        for r in repo_data:
            repo_short = r["repo"].split("/")[1]
            for p in r["prs_opened"]:
                reviewers = ", ".join(p["requested_reviewers"]) or "—"
                labels = _label_str(p["labels"]) or "—"
                w(f"| {repo_short} | [#{p['number']}]({p['url']}) | {p['author']} | {p['title']} | {reviewers} | {labels} |")
    w("")

    # ── PRs Merged ──
    w("---")
    w("")
    w(f"## PRs Merged ({total_prs_merged})")
    w("")
    if total_prs_merged == 0:
        w("_No PRs merged on this date._")
    else:
        w("| Repo | # | Author | Merged by | Title | Time to Merge |")
        w("|------|---|--------|-----------|-------|---------------|")
        for r in repo_data:
            repo_short = r["repo"].split("/")[1]
            for p in r["prs_merged"]:
                w(f"| {repo_short} | [#{p['number']}]({p['url']}) | {p['author']} | {p['merged_by']} | {p['title']} | {p['time_to_merge']} |")
    w("")

    # ── Open PRs ──
    w("---")
    w("")
    w(f"## Open PRs ({total_open_prs})")
    w("")
    if total_open_prs == 0:
        w("_No open PRs._")
    else:
        w("| Repo | # | Author | Title | Days Open | Reviewers | Stuck? |")
        w("|------|---|--------|-------|-----------|-----------|--------|")
        for r in repo_data:
            repo_short = r["repo"].split("/")[1]
            for p in sorted(r["open_prs"], key=lambda x: -x["days_open"]):
                reviewers = ", ".join(p["requested_reviewers"]) or "—"
                stuck_flag = "**YES**" if p["stuck"] else ""
                w(f"| {repo_short} | [#{p['number']}]({p['url']}) | {p['author']} | {p['title']} | {p['days_open']} | {reviewers} | {stuck_flag} |")
    w("")

    # ── Issues Opened ──
    w("---")
    w("")
    w(f"## Issues Opened ({total_issues_opened})")
    w("")
    if total_issues_opened == 0:
        w("_No issues opened on this date._")
    else:
        w("| Repo | # | Author | Title | Assignees | Labels |")
        w("|------|---|--------|-------|-----------|--------|")
        for r in repo_data:
            repo_short = r["repo"].split("/")[1]
            for i in r["issues_opened"]:
                assignees = ", ".join(i["assignees"]) or "—"
                labels = _label_str(i["labels"]) or "—"
                w(f"| {repo_short} | [#{i['number']}]({i['url']}) | {i['author']} | {i['title']} | {assignees} | {labels} |")
    w("")

    # ── Issues Closed ──
    w("---")
    w("")
    w(f"## Issues Closed ({total_issues_closed})")
    w("")
    if total_issues_closed == 0:
        w("_No issues closed on this date._")
    else:
        w("| Repo | # | Author | Title |")
        w("|------|---|--------|-------|")
        for r in repo_data:
            repo_short = r["repo"].split("/")[1]
            for i in r["issues_closed"]:
                w(f"| {repo_short} | [#{i['number']}]({i['url']}) | {i['author']} | {i['title']} |")
    w("")

    # ── Open Issues ──
    w("---")
    w("")
    w(f"## Open Issues ({total_open_issues})")
    w("")
    if total_open_issues == 0:
        w("_No open issues._")
    else:
        w("| Repo | # | Author | Title | Assignees | Comments | Days Stale | Stuck? |")
        w("|------|---|--------|-------|-----------|----------|------------|--------|")
        for r in repo_data:
            repo_short = r["repo"].split("/")[1]
            for i in sorted(r["open_issues"], key=lambda x: -x["days_since_update"]):
                assignees = ", ".join(i["assignees"]) or "—"
                stuck_flag = "**YES**" if i["stuck"] else ""
                w(f"| {repo_short} | [#{i['number']}]({i['url']}) | {i['author']} | {i['title']} | {assignees} | {i['comments']} | {i['days_since_update']} | {stuck_flag} |")
    w("")

    # ── Workload by Assignee ──
    workload = aggregate_workload_by_assignee(repo_data)
    w("---")
    w("")
    w(f"## Workload by Assignee ({len(workload)})")
    w("")
    if not workload:
        w("_No assignee workload data._")
    else:
        w("| Assignee | Assigned Issues | Open PRs Authored | Review Requests | Status |")
        w("|----------|----------------|-------------------|-----------------|--------|")
        for person in workload:
            status = f"**{person['status']}**" if person["status"] in ("Stuck", "Idle") else person["status"]
            w(f"| {person['assignee']} | {person['assigned_issues']} | {person['open_prs_authored']} | {person['review_requests']} | {status} |")
    w("")

    # ── Contributor Activity ──
    w("---")
    w("")
    w("## Contributor Activity")
    w("")

    people = {}
    for r in repo_data:
        for c in r["commits"]:
            name = c["author"]
            people.setdefault(name, {"commits": 0, "prs_opened": 0, "prs_merged": 0, "late_night": 0})
            people[name]["commits"] += 1
            if c["hour"] >= 22 or (0 <= c["hour"] < 6):
                people[name]["late_night"] += 1

        for p in r["prs_opened"]:
            name = p["author"]
            people.setdefault(name, {"commits": 0, "prs_opened": 0, "prs_merged": 0, "late_night": 0})
            people[name]["prs_opened"] += 1

        for p in r["prs_merged"]:
            name = p["author"]
            people.setdefault(name, {"commits": 0, "prs_opened": 0, "prs_merged": 0, "late_night": 0})
            people[name]["prs_merged"] += 1

    if not people:
        w("_No contributor activity on this date._")
    else:
        w("| Contributor | Commits | PRs Opened | PRs Merged | Late-Night Commits |")
        w("|-------------|---------|------------|------------|--------------------|")
        for name, stats in sorted(people.items(), key=lambda x: -x[1]["commits"]):
            late = f"**{stats['late_night']}**" if stats["late_night"] > 0 else "0"
            w(f"| {name} | {stats['commits']} | {stats['prs_opened']} | {stats['prs_merged']} | {late} |")
    w("")

    # ── Stuck Items Alert ──
    all_stuck_prs = [(r["repo"], p) for r in repo_data for p in r["open_prs"] if p["stuck"]]
    all_stuck_issues = [(r["repo"], i) for r in repo_data for i in r["open_issues"] if i["stuck"]]

    if all_stuck_prs or all_stuck_issues:
        w("---")
        w("")
        w("## Stuck Items Alert")
        w("")
        if all_stuck_prs:
            w(f"### Stuck PRs ({len(all_stuck_prs)})")
            w("")
            for repo_name, p in all_stuck_prs:
                w(f"- [{repo_name.split('/')[1]}#{p['number']}]({p['url']}) — **{p['title']}** by {p['author']} ({p['days_open']}d open, no reviewer assigned)")
            w("")
        if all_stuck_issues:
            w(f"### Stuck Issues ({len(all_stuck_issues)})")
            w("")
            for repo_name, i in all_stuck_issues:
                w(f"- [{repo_name.split('/')[1]}#{i['number']}]({i['url']}) — **{i['title']}** by {i['author']} ({i['days_since_update']}d since last update, 0 comments)")
            w("")

    # ── Footer with period-specific prompts ──
    w("---")
    w("")
    w(f"*{conf['label']} — {conf['focus']}. Ask Claude to analyze this snapshot for:*")
    for prompt in conf["prompts"]:
        w(f"- *{prompt}*")
    w("")

    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Team Pulse — Daily GitHub Snapshot (AM/PM)",
        epilog="Schedule: 07:00 Bangkok (AM) and 18:00 Bangkok (PM)",
    )
    parser.add_argument(
        "--date",
        default=_now_bangkok().strftime("%Y-%m-%d"),
        help="Date to extract (YYYY-MM-DD, default: today in Bangkok time)",
    )
    parser.add_argument(
        "--period",
        choices=["am", "pm"],
        default=None,
        help="Snapshot period (default: auto-detect from Bangkok time)",
    )
    parser.add_argument(
        "--repos", nargs="+", default=_get_repos_from_env() or DEFAULT_REPOS,
        help="GitHub repos to track (owner/name). Reads TEAM_PULSE_REPOS env var if set.",
    )
    parser.add_argument(
        "--output-dir", type=Path, default=OUTPUT_DIR,
        help="Output directory for daily notes",
    )
    args = parser.parse_args()

    date_str = args.date
    period = args.period or _detect_period()
    repos = args.repos
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    conf = PERIOD_CONFIG[period]
    now_bkk = _now_bangkok()

    print(f"Team Pulse — {conf['label']}")
    print(f"Date: {date_str}  |  Period: {period.upper()}  |  Bangkok time: {now_bkk.strftime('%H:%M')}")
    print(f"Repos: {', '.join(repos)}")
    print()

    repo_data = []

    for repo in repos:
        print(f"  [{repo}] Fetching commits...")
        commits = fetch_commits(repo, date_str)
        print(f"    > {len(commits)} commits")

        print(f"  [{repo}] Fetching pull requests...")
        pulls = fetch_pulls(repo)
        prs_opened, prs_merged, open_prs = filter_prs_by_date(pulls, date_str)
        print(f"    > {len(prs_opened)} opened, {len(prs_merged)} merged, {len(open_prs)} open")

        print(f"  [{repo}] Fetching issues...")
        issues = fetch_issues(repo)
        issues_opened, issues_closed, open_issues = filter_issues_by_date(issues, date_str)
        print(f"    > {len(issues_opened)} opened, {len(issues_closed)} closed, {len(open_issues)} open")

        repo_data.append({
            "repo": repo,
            "commits": commits,
            "prs_opened": prs_opened,
            "prs_merged": prs_merged,
            "open_prs": open_prs,
            "issues_opened": issues_opened,
            "issues_closed": issues_closed,
            "open_issues": open_issues,
        })

    print()
    print("Generating report...")
    report = generate_report(date_str, period, repo_data, output_dir)

    output_file = output_dir / f"{date_str}-{period}.md"
    output_file.write_text(report)
    print(f"Written to: {output_file}")
    print("Done.")


if __name__ == "__main__":
    main()
