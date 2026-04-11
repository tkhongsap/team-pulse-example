# Team Pulse — Current Process (PoC)

## Daily Workflow

```
07:00 Bangkok    python scripts/team_pulse.py --period am     MANUAL
                 /compile-wiki                                 MANUAL
                 /morning-briefing                             MANUAL

During the day    /ask "any question"                          MANUAL (on demand)

18:00 Bangkok    python scripts/team_pulse.py --period pm     MANUAL
                 /compile-wiki                                 MANUAL
                 /eod-summary                                  MANUAL

Weekly           /team-dashboard                               MANUAL (on demand)
                 /lint-wiki                                     MANUAL (on demand)
```

## What Each Step Does

| Step | Input | Output | Auto/Manual |
|------|-------|--------|-------------|
| `team_pulse.py --period am` | GitHub API (commits, PRs, issues) | `raw/github-daily/YYYY-MM-DD-am.md` | **Manual** (run CLI) |
| `team_pulse.py --period pm` | GitHub API | `raw/github-daily/YYYY-MM-DD-pm.md` | **Manual** (run CLI) |
| `/compile-wiki` | `raw/github-daily/` new files | `wiki/` articles + `index.md` + `log.md` | **Manual** (run command) |
| `/morning-briefing` | `raw/` + `wiki/` + `docs/wt-project.md` | `wiki/reports/YYYY-MM-DD-morning-briefing.md` | **Manual** (run command) |
| `/eod-summary` | AM + PM snapshots + morning briefing + `wiki/` | `wiki/reports/YYYY-MM-DD-eod-summary.md` | **Manual** (run command) |
| `/team-dashboard` | `wiki/` + 7 days of snapshots | `wiki/reports/YYYY-MM-DD-team-dashboard.md` | **Manual** (run command) |
| `/ask "question"` | `wiki/index.md` + relevant articles | Terminal answer + `outputs/YYYY-MM-DD-{slug}.md` | **Manual** (on demand) |
| `/lint-wiki` | `wiki/` + `raw/` | `wiki/reports/YYYY-MM-DD-lint-report.md` | **Manual** (on demand) |

## What's Automated vs Manual

**Automated (zero human effort):**
- Nothing yet. All steps require manual trigger.

**Semi-automated (one command, LLM does the work):**
- Extraction: `python scripts/team_pulse.py` — one command, script handles all API calls
- All `/commands` — one trigger, LLM reads files, generates output, saves to disk

**Fully manual:**
- Remembering to run extraction at 7 AM and 6 PM
- Running `/compile-wiki` after each extraction
- Running briefing/summary commands

## Data Flow

```
GitHub API → team_pulse.py → raw/github-daily/ → /compile-wiki → wiki/
                                                                    ↓
                                            /morning-briefing ← wiki/index.md
                                            /eod-summary      ← wiki/ articles
                                            /team-dashboard    ← wiki/ patterns
                                            /ask               ← wiki/ (any question)
                                                    ↓
                                              wiki/reports/     (briefings, summaries)
                                              outputs/          (ad-hoc Q&A answers)
```

## Repo Structure

```
team-pulse-example/
├── CLAUDE.md                    # Schema (describes entire system)
├── raw/github-daily/            # 16 AM/PM snapshots (Apr 4-11)
├── wiki/                        # 11 articles + 9 reports
│   ├── index.md                 # Master catalog
│   ├── log.md                   # Build history
│   ├── contributors/            # 6 people
│   ├── projects/                # 2 repos
│   ├── patterns/                # 3 patterns
│   ├── connections/             # 1 insight
│   └── reports/                 # 1 morning briefing + 8 EOD summaries
├── outputs/                     # 1 Q&A answer
├── scripts/team_pulse.py        # Extraction script
├── .claude/commands/            # 7 commands
│   ├── morning-briefing.md
│   ├── eod-summary.md
│   ├── team-dashboard.md
│   ├── compile-wiki.md
│   ├── lint-wiki.md
│   └── ask.md
├── docs/                        # Project docs
└── ideas/                       # Reference materials
```

## Next: What to Automate

1. **Cron extraction** — schedule `team_pulse.py` at 7AM/6PM Bangkok
2. **Auto-compile** — run `/compile-wiki` inside briefing commands
3. **Claude API calls** — replace manual `/commands` with Python script using Anthropic SDK
4. **Notifications** — push morning briefing to Slack/email
