#!/bin/bash
# Team Pulse — Cron Setup Script
#
# Installs the Team Pulse crontab entries for automated AM/PM pipelines.
#
# Usage:
#   bash scripts/setup-cron.sh          # install cron jobs
#   bash scripts/setup-cron.sh --remove # remove cron jobs
#
# What it does:
#   - 00:00 UTC (7AM Bangkok): run_pipeline.py --period am
#   - 11:00 UTC (6PM Bangkok): run_pipeline.py --period pm

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

if [ "$1" = "--remove" ]; then
    echo "Removing Team Pulse cron entries..."
    crontab -l 2>/dev/null | grep -v "run_pipeline.py" | crontab -
    echo "Done. Cron entries removed."
    exit 0
fi

# Check prerequisites
echo "Checking prerequisites..."

if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 not found. Install Python 3.10+."
    exit 1
fi

if ! command -v gh &>/dev/null; then
    echo "ERROR: gh CLI not found. Install: https://cli.github.com/"
    exit 1
fi

if [ ! -f "$PROJECT_DIR/.env" ]; then
    echo "WARNING: .env file not found at $PROJECT_DIR/.env"
    echo "  Copy .env.example and configure: cp .env.example .env"
fi

# Build cron entries with resolved paths
AM_ENTRY="0 0 * * * cd $PROJECT_DIR && python3 scripts/run_pipeline.py --period am >> scripts/pipeline.log 2>&1"
PM_ENTRY="0 11 * * * cd $PROJECT_DIR && python3 scripts/run_pipeline.py --period pm >> scripts/pipeline.log 2>&1"

echo "Installing Team Pulse cron entries..."
echo "  AM (7:00 Bangkok / 00:00 UTC): run_pipeline.py --period am"
echo "  PM (6:00 Bangkok / 11:00 UTC): run_pipeline.py --period pm"
echo "  Project dir: $PROJECT_DIR"
echo ""

# Add entries (preserving existing crontab, removing old Team Pulse entries)
(crontab -l 2>/dev/null | grep -v "run_pipeline.py"; echo "$AM_ENTRY"; echo "$PM_ENTRY") | crontab -

echo "Done. Verify with: crontab -l"
