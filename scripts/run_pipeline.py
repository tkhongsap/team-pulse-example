#!/usr/bin/env python3
"""
Team Pulse — Pipeline Orchestrator

Runs the full data pipeline: extract -> compile -> report -> git push.
Designed as the single entry point for cron jobs.

Usage:
    python scripts/run_pipeline.py --period am    # morning pipeline
    python scripts/run_pipeline.py --period pm    # evening pipeline
"""

import argparse
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Project root (parent of scripts/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
PIPELINE_LOG = SCRIPTS_DIR / "pipeline.log"
RAW_DIR = PROJECT_ROOT / "raw" / "github-daily"
WIKI_LOG = PROJECT_ROOT / "wiki" / "log.md"

# Bangkok timezone (ICT = UTC+7)
TZ_BANGKOK = timezone(timedelta(hours=7))

# Report type mapping
REPORT_TYPE = {"am": "morning", "pm": "eod"}


def now_bangkok() -> datetime:
    """Current datetime in Bangkok timezone."""
    return datetime.now(TZ_BANGKOK)


def log(msg: str) -> None:
    """Print and append to pipeline log."""
    timestamp = now_bangkok().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(PIPELINE_LOG, "a") as f:
        f.write(line + "\n")


def run_step(name: str, cmd: list[str]) -> float:
    """Run a pipeline step, return elapsed seconds. Raises on failure."""
    log(f"START: {name}")
    start = time.time()

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(PROJECT_ROOT),
        timeout=600,
    )

    elapsed = time.time() - start

    if result.stdout.strip():
        for line in result.stdout.strip().split("\n"):
            log(f"  {line}")

    if result.returncode != 0:
        log(f"FAILED: {name} (exit code {result.returncode}, {elapsed:.1f}s)")
        if result.stderr.strip():
            for line in result.stderr.strip().split("\n"):
                log(f"  ERROR: {line}")
        raise RuntimeError(f"Step '{name}' failed with exit code {result.returncode}")

    log(f"DONE: {name} ({elapsed:.1f}s)")
    return elapsed


def run_pipeline(period: str, date: str) -> None:
    """Execute the full pipeline."""
    report_type = REPORT_TYPE[period]
    raw_file = RAW_DIR / f"{date}-{period}.md"

    log("=" * 60)
    log(f"Pipeline started: period={period}, date={date}")
    log("=" * 60)

    total_start = time.time()
    files_created: list[str] = []
    steps_timing: list[tuple[str, float]] = []

    # Step 1: Extract — run team_pulse.py
    elapsed = run_step(
        "Extract GitHub data",
        [sys.executable, str(SCRIPTS_DIR / "team_pulse.py"), "--period", period, "--date", date],
    )
    steps_timing.append(("Extract", elapsed))

    if not raw_file.exists():
        log(f"FAILED: Expected output file not found: {raw_file}")
        raise RuntimeError(f"Extract step did not create {raw_file}")
    files_created.append(str(raw_file.relative_to(PROJECT_ROOT)))
    log(f"  Created: {raw_file.relative_to(PROJECT_ROOT)}")

    # Step 2: Compile — run compile.py
    wiki_log_before = WIKI_LOG.read_text() if WIKI_LOG.exists() else ""

    elapsed = run_step(
        "Compile wiki",
        [sys.executable, str(SCRIPTS_DIR / "compile.py"), date],
    )
    steps_timing.append(("Compile", elapsed))

    wiki_log_after = WIKI_LOG.read_text() if WIKI_LOG.exists() else ""
    if wiki_log_after != wiki_log_before:
        log("  wiki/log.md was updated")
    else:
        log("  wiki/log.md unchanged (may already be compiled)")

    # Step 3: Generate report
    elapsed = run_step(
        f"Generate {report_type} report",
        [sys.executable, str(SCRIPTS_DIR / "generate_report.py"), "--type", report_type, "--date", date],
    )
    steps_timing.append(("Report", elapsed))

    report_patterns = {
        "morning": f"{date}-morning-briefing.md",
        "eod": f"{date}-eod-summary.md",
        "dashboard": f"{date}-team-dashboard.md",
    }
    report_filename = report_patterns[report_type]
    report_path = PROJECT_ROOT / "wiki" / "reports" / report_filename
    if report_path.exists():
        files_created.append(f"wiki/reports/{report_filename}")
        log(f"  Created: wiki/reports/{report_filename}")

    # Step 4: Git commit and push
    elapsed = run_step(
        "Git add",
        ["git", "add", "-A"],
    )

    # Check if there are changes to commit
    status_result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
        cwd=str(PROJECT_ROOT),
    )

    if status_result.stdout.strip():
        commit_msg = f"data: {date} {period.upper()} pipeline — extract, compile, {report_type} report"
        elapsed = run_step(
            "Git commit",
            ["git", "commit", "-m", commit_msg],
        )
        steps_timing.append(("Git commit", elapsed))

        elapsed = run_step(
            "Git push",
            ["git", "push"],
        )
        steps_timing.append(("Git push", elapsed))
    else:
        log("  No changes to commit")
        steps_timing.append(("Git", 0.0))

    # Print summary
    total_elapsed = time.time() - total_start
    log("")
    log("=" * 60)
    log("Pipeline Complete")
    log("=" * 60)
    log(f"Files created: {', '.join(files_created) if files_created else 'none'}")
    log(f"Step timings:")
    for step_name, step_time in steps_timing:
        log(f"  {step_name}: {step_time:.1f}s")
    log(f"Total time: {total_elapsed:.1f}s")


def main() -> None:
    """Entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description="Team Pulse — Pipeline Orchestrator (extract, compile, report, push)",
    )
    parser.add_argument(
        "--period",
        choices=["am", "pm"],
        required=True,
        help="Pipeline period: am (morning) or pm (evening)",
    )
    parser.add_argument(
        "--date",
        default=None,
        help="Target date (YYYY-MM-DD). Defaults to today in Bangkok time.",
    )
    args = parser.parse_args()

    date = args.date or now_bangkok().strftime("%Y-%m-%d")

    try:
        run_pipeline(args.period, date)
    except RuntimeError as e:
        log(f"PIPELINE FAILED: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
