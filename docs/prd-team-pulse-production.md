# PRD: Team Pulse Production System

**Product: AI-Driven Workspace Transformation — Production Deployment**
**Status: Draft**
**Date: 2026-04-11**
**Ref: docs/wt-project.md (project charter), CLAUDE.md (system schema)**

---

## 0. Core Design Principle: One Backend, Two Interfaces

```
┌──────────────────────────────────────────────────────────────────┐
│                     SHARED BACKEND                                │
│                                                                   │
│  raw/github-daily/  →  wiki/  →  wiki/reports/  →  outputs/      │
│  CLAUDE.md (schema)    index.md    .claude/commands/              │
│  scripts/              Agent SDK                                  │
│                                                                   │
│  Same data. Same wiki. Same prompts. Same behavior.              │
└────────────────┬──────────────────────────┬──────────────────────┘
                 │                          │
    ┌────────────▼────────────┐  ┌─────────▼──────────────────┐
    │  Terminal (Claude Code)  │  │  Frontend (Web UI)          │
    │                          │  │                              │
    │  /morning-briefing       │  │  Dashboard → same report     │
    │  /eod-summary            │  │  Chat → same /ask logic      │
    │  /compile-wiki           │  │  Reports → same wiki/reports │
    │  /ask "question"         │  │                              │
    │                          │  │  Uses Agent SDK to call      │
    │  You (developer)         │  │  the same prompts            │
    └──────────────────────────┘  └──────────────────────────────┘
```

**The rule:** Every operation that works in the terminal must produce the
same output when triggered from the web UI. This is enforced by:

1. **Single source of truth:** `CLAUDE.md` defines the schema. Both interfaces read it.
2. **Same prompts:** `.claude/commands/*.md` define the prompts. The Agent SDK loads
   them via `setting_sources=["project"]`. The web backend uses the same prompt files.
3. **Same data layer:** Both read from `raw/` and `wiki/`. Both write to `wiki/` and `outputs/`.
4. **Same tools:** Claude Code uses Read/Write/Edit/Glob/Grep. Agent SDK uses the same tools.

If you change a command in `.claude/commands/morning-briefing.md`, it takes effect
in both the terminal AND the web UI — no duplication, no drift.

---

## 1. Background

We have a working PoC that extracts daily GitHub activity, compiles it into an LLM-maintained wiki, and generates morning briefings, EOD summaries, and ad-hoc Q&A — all running locally via Claude Code in the terminal.

This PRD describes how to make it production-ready for the 150+ person dev organization described in wt-project.md.

### Current State (PoC)

```
Manual terminal commands → local markdown files → one person can use it
```

- Extraction: `python scripts/team_pulse.py` (manual, CLI)
- Compilation: `/compile-wiki` (manual, Claude Code)
- Reports: `/morning-briefing`, `/eod-summary` (manual, Claude Code)
- Q&A: `/ask` (manual, Claude Code)
- Output: Markdown files in git repo
- Users: 1 (the person running Claude Code)

### Target State (Production)

```
Automated pipeline → web dashboard + chat → entire team can use it
```

- Extraction: Automated (cron)
- Compilation: Automated (API)
- Reports: Auto-generated, available on web app
- Q&A: Web chat interface (like claude.ai)
- Output: Web dashboard + chat interface
- Users: 150+ (team leads, managers, contributors)

---

## 2. Architecture Decision: Claude Agent SDK

### The Problem

Claude Code (terminal) has full agent capabilities — it reads files, browses the wiki,
reasons about which articles to consult. Moving to production requires the same
capabilities without a human in the terminal.

### The Solution: Claude Agent SDK

The [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview) provides
the **same built-in tools as Claude Code** — Read, Write, Edit, Bash, Glob, Grep —
programmable in Python. Claude navigates files autonomously, no manual file reading needed.

Critical feature: `setting_sources=["project"]` makes the agent read `CLAUDE.md`
automatically — it knows our wiki schema, article format, and operations without
repeating them in the prompt.

```python
from claude_agent_sdk import query, ClaudeAgentOptions

async for message in query(
    prompt="Compile new raw sources into wiki following CLAUDE.md schema",
    options=ClaudeAgentOptions(
        allowed_tools=["Read", "Write", "Edit", "Glob", "Grep"],
        setting_sources=["project"],  # reads CLAUDE.md automatically
    ),
):
    if hasattr(message, "result"):
        print(message.result)
```

### Why Agent SDK (not simple Anthropic API)

| | Simple API | Agent SDK |
|---|---|---|
| File access | You read files, stuff into prompt | Claude reads files itself |
| Multi-step reasoning | Single request/response | Agent loop with tool calls |
| Wiki navigation | Must pre-select files | Claude browses index → selects articles |
| CLAUDE.md support | Must include manually | Auto-loaded via setting_sources |
| Sessions | Stateless | Resumable conversations |
| Hooks | None | PreToolUse, PostToolUse, audit logging |

The Agent SDK is the right choice for ALL operations — compile, reports, and Q&A.
No need for a hybrid approach. One SDK, one code path.

### Cost (per Anthropic API billing)

| Operation | Estimated cost |
|---|---|
| Compile wiki | ~$0.30-0.50/run |
| Generate report | ~$0.10-0.20/report |
| Q&A query | ~$0.25-0.50/query |
| Monthly total (2 runs/day + Q&A) | ~$30-50 + Q&A usage |

See `ideas/agent-sdk-reference.md` for full SDK documentation and code examples.

---

## 3. Phase 1: Automated Backend (No Frontend)

**Goal:** Reports generate automatically. Team leads access them on the web app.

**Timeline:** 1-2 weeks

### What Gets Built

```
┌────────────────────────────────────────────────────────┐
│  Cron Job (runs on server or local machine)             │
│                                                         │
│  07:00 Bangkok:                                         │
│    1. team_pulse.py --period am    → raw/github-daily/  │
│    2. compile.py                   → wiki/ updated      │
│    3. generate_briefing.py         → wiki/reports/      │
│    4. git commit + push            → web app refreshes   │
│                                                         │
│  18:00 Bangkok:                                         │
│    1. team_pulse.py --period pm    → raw/github-daily/  │
│    2. compile.py                   → wiki/ updated      │
│    3. generate_eod.py              → wiki/reports/      │
│    4. git commit + push            → web app refreshes   │
│                                                         │
│  git auto-commit + push after each run                  │
└────────────────────────────────────────────────────────┘
```

### New Scripts to Build

**`scripts/compile.py`** — Wiki compilation via Anthropic SDK
- Reads new raw files since last `wiki/log.md` entry
- Reads existing wiki articles
- Calls Claude API with structured prompt (same logic as `/compile-wiki` command)
- Writes updated wiki articles, index.md, log.md
- Cost: ~$0.30-0.50 per run

**`scripts/generate_report.py`** — Report generation via Anthropic SDK
- Mode: `--type morning|eod|dashboard`
- Reads raw snapshot + wiki articles
- Calls Claude API with structured prompt (same logic as `/morning-briefing` etc.)
- Writes to `wiki/reports/`
- Cost: ~$0.10-0.20 per report

**`scripts/run_pipeline.py`** — Orchestrator
- Single entry point: `python scripts/run_pipeline.py --period am`
- Runs: extract → compile → generate report → git commit + push
- Handles errors, logs, retries
- Web app reads from git — auto-refreshes when new data is pushed

### Infrastructure

- **Cron:** Linux crontab, GitHub Actions scheduled workflow, or cloud function (AWS Lambda / GCP Cloud Run)
- **API key:** Anthropic API key stored in `.env`
- **Git:** Auto-commit and push after each pipeline run

### Cost Estimate (Phase 1)

| Operation | Frequency | Cost per run | Monthly |
|---|---|---|---|
| Morning extraction + compile + briefing | 1x/day | ~$0.50 | ~$15 |
| Evening extraction + compile + EOD | 1x/day | ~$0.50 | ~$15 |
| Total | | | **~$30/month** |

### Deliverables

- [ ] `scripts/compile.py` — wiki compilation via API
- [ ] `scripts/generate_report.py` — report generation via API
- [ ] `scripts/run_pipeline.py` — orchestrator
- [ ] Cron configuration (crontab or GitHub Actions)
- [ ] `.env` template with API key
- [ ] Test: run full pipeline end-to-end, verify reports generated

### wt-project.md Coverage

| Mechanism | How Phase 1 delivers it |
|---|---|
| 4.1 Morning check-in | Auto morning briefing at 7 AM, available on web app |
| 4.1 Evening check-out | Auto EOD summary at 6 PM, available on web app |
| 4.2 Status categorization | Workload table with Backlog/InProgress/Stuck/Idle |
| 4.3 Burnout detection | Late-night/overload flags in reports |
| 4.4 Management dashboard | Morning briefing replaces stand-up status checks |

---

## 4. Phase 2+3: Web App — Dashboard + Chat (claude.ai-style)

**Goal:** Team-wide access to reports, wiki, and Q&A in a single web app styled after
claude.ai's chat interface. Dashboard and chat are unified — not separate phases.

**Timeline:** 3-4 weeks after Phase 1

**Full design spec:** See `docs/frontend-design.md`

### Why Combine Phase 2 and 3

The claude.ai layout naturally combines dashboard browsing and chat in one interface:
- Sidebar has reports + wiki articles (dashboard browsing)
- Main area has chat with streaming responses (Q&A)
- Input bar is always visible, even when viewing a report (ask follow-ups)

Building them separately would mean two deployments and a jarring transition when chat
is added later. Better to ship one unified app.

### Layout (claude.ai-style)

```
┌──────────────┬────────────────────────────────────────────┐
│   Sidebar    │  Header: Team Pulse | Apr 11 | User | ⚙    │
│   (280px)    ├────────────────────────────────────────────┤
│              │                                            │
│  [+ New Chat]│  Chat messages OR wiki/report view         │
│              │                                            │
│  Chat History│  AI responses with:                        │
│  ── Today    │  - Markdown rendering (tables, code)       │
│  ── Reports  │  - [[wikilink]] clickable chips            │
│    Morning   │  - Source citation blocks                  │
│    EOD       │  - Status badges (Stuck, In Progress...)   │
│    Dashboard │                                            │
│  ── Wiki     │                                            │
│    Contrib.  ├────────────────────────────────────────────┤
│    Projects  │                                            │
│    Patterns  │  [Ask anything about your team...]  [Send] │
│              │                                            │
└──────────────┴────────────────────────────────────────────┘
```

### Backend Architecture

**Two API routes powered by Claude Agent SDK:**

**`/api/ask`** — Chat Q&A (streaming)
```python
async for message in query(
    prompt=user_question,
    options=ClaudeAgentOptions(
        allowed_tools=["Read", "Glob", "Grep"],
        setting_sources=["project"],   # reads CLAUDE.md
        resume=session_id,             # conversation memory
    ),
):
    yield message  # stream to frontend
```
- Agent SDK navigates wiki/ to answer free-form questions
- Sessions enable follow-up questions ("what about last week?")
- Saves answers to `outputs/` (configurable)

**`/api/reports/:date/:type`** — Report viewer
- Reads pre-generated `wiki/reports/YYYY-MM-DD-{type}.md`
- Returns rendered markdown (no API call, just file read)
- Fast and free — reports were already generated by Phase 1 pipeline

**`/api/wiki/:category/:slug`** — Wiki article viewer
- Reads `wiki/contributors/garrytan.md` etc.
- Returns rendered markdown
- Wikilinks resolved to internal app routes

### Key Design Decisions

**Design reference:** claude.ai chat interface (see `docs/frontend-design.md`)
- Clean, minimal — content-first
- Dark/light mode
- Mobile responsive (sidebar collapses)

**Data source:** Git repo synced on each pipeline run (2x/day). Between syncs,
cached markdown served as static content. Chat queries hit Agent SDK in real-time.

**Auth:** GitHub OAuth (team already uses GitHub). SSO upgrade path for enterprise.

**Conversation memory:** Agent SDK sessions. Each chat conversation persists —
follow-up questions use full context. Session ID stored in browser.

### Deliverables

- [ ] Next.js app with claude.ai-style three-panel layout
- [ ] Sidebar: chat history, quick actions, reports archive, wiki browser
- [ ] Chat interface with streaming Agent SDK responses
- [ ] Markdown renderer with wikilink support + status badges
- [ ] Source citation display (clickable links to wiki articles)
- [ ] Report/wiki article viewer (click from sidebar or from citation)
- [ ] Suggested questions on empty chat state
- [ ] Dark/light mode toggle
- [ ] Authentication (GitHub OAuth)
- [ ] Session persistence (conversation memory via Agent SDK)
- [ ] Rate limiting + usage tracking
- [ ] Mobile responsive (sidebar collapse, full-width chat)
- [ ] CI/CD: auto-deploy on git push (Vercel)

### Tech Stack

| Component | Library |
|-----------|---------|
| Framework | Next.js 14+ (App Router) |
| Styling | Tailwind CSS |
| Components | shadcn/ui |
| Markdown | react-markdown + remark-gfm |
| Chat streaming | Agent SDK streaming via API route |
| Auth | NextAuth.js (GitHub OAuth) |
| State | React context or Zustand |
| Deployment | Vercel |

### Cost Estimate

| Item | Cost |
|---|---|
| Vercel hosting (free tier or Pro $20/mo) | $0-20/month |
| Agent SDK Q&A queries (50/day avg) | $150-375/month |
| Domain | $12/year |
| **Total** | **~$170-400/month** |

**Cost control:** Cache common questions, daily query limits per user, rate limiting.

---

## 5. Tech Stack Summary

| Component | Phase 1 (Backend) | Phase 2+3 (Web App) |
|---|---|---|
| **Extraction** | `team_pulse.py` (Python, gh CLI) | Same |
| **Compilation** | Agent SDK (Python) | Same |
| **Reports** | Agent SDK (Python) | Same + web viewer |
| **Notifications** | — (web app is the delivery channel) | Same |
| **Web frontend** | — | Next.js + Tailwind + shadcn/ui |
| **Chat backend** | — | Agent SDK streaming via API route |
| **Auth** | — | NextAuth.js (GitHub OAuth) |
| **Hosting** | Cron on server | Vercel |
| **Data store** | Git repo (markdown) | Same |
| **Scheduling** | Crontab / GitHub Actions | Same |

---

## 6. Migration Path from PoC

| PoC (now) | Phase 1 | Phase 2+3 |
|---|---|---|
| `team_pulse.py` (manual) | Cron-automated | Same |
| `/compile-wiki` (Claude Code) | `scripts/compile.py` (Agent SDK) | Same |
| `/morning-briefing` (Claude Code) | `scripts/generate_report.py` (Agent SDK) | Web page |
| `/eod-summary` (Claude Code) | `scripts/generate_report.py` (Agent SDK) | Web page |
| `/ask` (Claude Code) | Not available via web | Chat UI + Agent SDK |
| Terminal only | Terminal + web app | Terminal + web app |
| 1 user | 1 user + web readers | All users (read + ask) |

**Key principle:** Terminal commands (Claude Code) and web app (Agent SDK) share the
same backend — CLAUDE.md, .claude/commands/, wiki/, raw/. See Section 0.

---

## 7. Success Metrics (from wt-project.md section 6)

| Metric | Target | Phase 1 | Phase 2+3 |
|---|---|---|---|
| Stand-up meeting time | 50% reduction | Morning briefing on web app replaces status rounds | Dashboard + chat replaces stand-ups entirely |
| Stuck task resolution | <24h from alert | Auto-flagged in reports | Visible on dashboard + queryable |
| Stuck detection speed | Flagged at 3+ days | Automated daily | Same |
| Employee wellbeing | Reduced burnout | Burnout signals in reports | Burnout dashboard + "who needs help?" queries |
| Team migration | 100% on GitHub by M6 | GitHub is the data source | GitHub data visible to all, all roles can query |

---

## 8. Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| API cost overrun (Phase 3) | $750+/month if uncapped | Daily query limits, caching, usage dashboard |
| "AI surveillance" perception | Team resistance | Frame as protective (wt-project section 7). Show burnout alerts protect, not punish. |
| Stale wiki data | Wrong answers | Pipeline runs 2x/day + lint checks flag stale articles |
| Single point of failure (one repo) | System down if repo unavailable | Git is distributed. Add monitoring for pipeline failures. |
| Agent SDK hallucination | Incorrect Q&A answers | Always show source citations. Require wiki-backed answers only. |

---

## 9. Open Questions

1. **Hosting:** Internal server (on-prem) vs cloud (Vercel + API)? Depends on data sensitivity.
2. **Auth:** GitHub OAuth sufficient, or need company SSO (SAML)?
3. **Notifications:** Add email/Slack push later if web-only access is insufficient?
4. **Budget approval:** API costs (~$200-400/month) need sign-off.
5. **Data retention:** How long to keep daily snapshots? Archive after 90 days?

---

## 10. Reference Documents

| Document | Location | Description |
|---|---|---|
| Project charter | `docs/wt-project.md` | Organizational goals, 4 mechanisms, success metrics |
| System schema | `CLAUDE.md` | Three layers, operations, article format |
| Frontend design | `docs/frontend-design.md` | claude.ai-style layout, colors, typography, components |
| Current process | `docs/process.md` | What's manual vs automated today |
| Agent SDK reference | `ideas/agent-sdk-reference.md` | SDK tools, code examples, cost estimates |
| LLM Wiki pattern | `ideas/llm-wiki.md` | Karpathy's canonical architecture |
| Second Brain mapping | `ideas/second-brain.md` | How the pattern maps to Team Pulse |
