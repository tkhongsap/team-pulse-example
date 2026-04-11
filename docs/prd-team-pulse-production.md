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
- Reports: Auto-generated and pushed to Slack
- Q&A: Web chat interface (like claude.ai)
- Output: Web dashboard + Slack notifications
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

**Goal:** Reports generate automatically. Team leads get morning briefings in Slack without touching any tool.

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
│    4. notify.py                    → Slack webhook       │
│                                                         │
│  18:00 Bangkok:                                         │
│    1. team_pulse.py --period pm    → raw/github-daily/  │
│    2. compile.py                   → wiki/ updated      │
│    3. generate_eod.py              → wiki/reports/      │
│    4. notify.py                    → Slack webhook       │
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

**`scripts/notify.py`** — Slack/email notification
- Reads the generated report markdown
- Converts to Slack blocks or email HTML
- Sends via Slack webhook or SMTP
- Cost: free

**`scripts/run_pipeline.py`** — Orchestrator
- Single entry point: `python scripts/run_pipeline.py --period am`
- Runs: extract → compile → generate report → notify → git commit + push
- Handles errors, logs, retries

### Infrastructure

- **Cron:** Linux crontab, GitHub Actions scheduled workflow, or cloud function (AWS Lambda / GCP Cloud Run)
- **API key:** Anthropic API key stored in `.env`
- **Slack webhook:** Configured in `.env`
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
- [ ] `scripts/notify.py` — Slack/email delivery
- [ ] `scripts/run_pipeline.py` — orchestrator
- [ ] Cron configuration (crontab or GitHub Actions)
- [ ] `.env` template with API key + Slack webhook
- [ ] Test: run full pipeline end-to-end, verify Slack delivery

### wt-project.md Coverage

| Mechanism | How Phase 1 delivers it |
|---|---|
| 4.1 Morning check-in | Auto morning briefing in Slack at 7 AM |
| 4.1 Evening check-out | Auto EOD summary in Slack at 6 PM |
| 4.2 Status categorization | Workload table with Backlog/InProgress/Stuck/Idle |
| 4.3 Burnout detection | Late-night/overload flags in reports |
| 4.4 Management dashboard | Morning briefing replaces stand-up status checks |

---

## 4. Phase 2: Web Dashboard (Read-Only)

**Goal:** Management can browse reports, contributor profiles, and patterns in a web browser. No terminal needed.

**Timeline:** 2-3 weeks after Phase 1

### What Gets Built

```
┌──────────────────────────────────────────────────────┐
│  Web App (Next.js)                                    │
│                                                       │
│  Routes:                                              │
│    /                  → Today's morning briefing       │
│    /reports           → Browse all reports by date     │
│    /reports/2026-04-11-eod-summary                     │
│    /contributors      → List all contributor profiles  │
│    /contributors/garrytan                              │
│    /projects          → Project health pages           │
│    /patterns          → Detected patterns              │
│    /dashboard         → Team health score + metrics    │
│                                                       │
│  Data source: reads wiki/ and raw/ from git repo      │
│  (or a deployed copy synced on each pipeline run)     │
└──────────────────────────────────────────────────────┘
```

### Key Design Decisions

**Data source:** The web app reads markdown files from the git repo. Two options:
1. **Git pull on each request** — always fresh, simple, but slow
2. **Build step** — pipeline pushes to git, CI rebuilds the site, deploys static HTML

Option 2 is better — the site rebuilds after each pipeline run (2x/day). Between rebuilds, it's fast static HTML.

**Markdown rendering:** Use a library like `next-mdx-remote` or `unified/remark` to render wiki markdown with wikilink support.

**Authentication:** Required — this is internal team data. Use existing SSO (Google Workspace, GitHub OAuth, or company SAML).

### Deliverables

- [ ] Next.js app with routes for reports, contributors, projects, patterns
- [ ] Markdown renderer with wikilink support
- [ ] Dashboard page with team health score
- [ ] Authentication (GitHub OAuth or company SSO)
- [ ] CI/CD: auto-deploy on git push (Vercel, Netlify, or internal)
- [ ] Mobile-responsive (team leads check on phone)

### Cost Estimate (Phase 2)

| Item | Cost |
|---|---|
| Vercel/Netlify hosting (free tier) | $0 |
| Domain (optional) | $12/year |
| Development time | 2-3 weeks |

---

## 5. Phase 3: Chat Interface (Full Q&A)

**Goal:** Anyone on the team can ask questions about team activity in a chat interface, like claude.ai. Answers are backed by the wiki.

**Timeline:** 2-3 weeks after Phase 2

### What Gets Built

```
┌──────────────────────────────────────────────────────┐
│  Chat Interface (added to Phase 2 web app)            │
│                                                       │
│  ┌────────────────────────────────────────────────┐   │
│  │  Team Pulse Assistant                          │   │
│  │                                                │   │
│  │  User: "Who was busiest last week?"            │   │
│  │                                                │   │
│  │  Assistant: Based on wiki data, garrytan was   │   │
│  │  the busiest with 25 commits across 7 days...  │   │
│  │  [View sources: garrytan.md, gstack.md]        │   │
│  │                                                │   │
│  │  User: "What should we address in tomorrow's   │   │
│  │  stand-up?"                                    │   │
│  │                                                │   │
│  │  [input box]                          [Send]   │   │
│  └────────────────────────────────────────────────┘   │
│                                                       │
│  Backend: Claude Agent SDK with wiki/ file access     │
└──────────────────────────────────────────────────────┘
```

### Architecture

**Backend API route:** `/api/ask`
1. Receives user question
2. Reads `wiki/index.md` + selects relevant articles (Agent SDK navigates)
3. Calls Claude Agent SDK with file tools (read wiki articles, raw data)
4. Streams response back to frontend
5. Saves answer to `outputs/` (optional, configurable)

**Why Agent SDK (not simple API):**
Free-form Q&A is unpredictable — the model needs to decide which articles to read based on the question. The Agent SDK gives Claude tool access to:
- Read specific wiki articles
- Grep across the wiki for keywords
- Read raw daily snapshots for specific dates
- Navigate the index to find relevant content

This is closest to how `/ask` works in Claude Code today.

**Conversation memory:** Each chat session maintains context. Follow-up questions work:
- "Who was busiest last week?" → answer
- "What about the week before?" → uses conversation context

### Deliverables

- [ ] `/api/ask` backend route using Claude Agent SDK
- [ ] Chat UI component (streaming responses)
- [ ] Source citation display (clickable links to wiki articles)
- [ ] Conversation history within session
- [ ] Save answer to `outputs/` toggle
- [ ] Rate limiting (prevent API cost overruns)
- [ ] Usage dashboard (track queries, costs)

### Cost Estimate (Phase 3)

| Operation | Cost per query | Monthly (50 queries/day) |
|---|---|---|
| Agent SDK Q&A | $0.25-0.50 | $375-750 |
| With caching (repeated questions) | $0.10-0.25 | $150-375 |

**Cost control:** Cache common questions, set daily query limits per user, use simple API for questions that match known report types.

---

## 6. Tech Stack Summary

| Component | Phase 1 | Phase 2 | Phase 3 |
|---|---|---|---|
| **Extraction** | `team_pulse.py` (Python, gh CLI) | Same | Same |
| **Compilation** | Anthropic SDK (Python) | Same | Same |
| **Reports** | Anthropic SDK (Python) | Same | Same |
| **Notifications** | Slack webhook, email | Same | Same |
| **Web frontend** | — | Next.js + Tailwind | Same + chat component |
| **Chat backend** | — | — | Claude Agent SDK (Python) |
| **Auth** | — | GitHub OAuth / SSO | Same |
| **Hosting** | Cron on server | Vercel/Netlify | Same |
| **Data store** | Git repo (markdown) | Same | Same |
| **Scheduling** | Crontab / GitHub Actions | Same | Same |

---

## 7. Migration Path from PoC

| PoC (now) | Phase 1 | Phase 2 | Phase 3 |
|---|---|---|---|
| `team_pulse.py` (manual) | Cron-automated | Same | Same |
| `/compile-wiki` (Claude Code) | `scripts/compile.py` (API) | Same | Same |
| `/morning-briefing` (Claude Code) | `scripts/generate_report.py` (API) | Web page | Same |
| `/eod-summary` (Claude Code) | `scripts/generate_report.py` (API) | Web page | Same |
| `/ask` (Claude Code) | Not available | Not available | Chat UI + Agent SDK |
| Terminal output | Slack messages | Web dashboard | Web + chat |
| 1 user | 1 user + Slack readers | All users (read) | All users (read + ask) |

---

## 8. Success Metrics (from wt-project.md section 6)

| Metric | Target | Phase 1 | Phase 2 | Phase 3 |
|---|---|---|---|---|
| Stand-up meeting time | 50% reduction | Morning briefing in Slack replaces status rounds | Dashboard accessible to all leads | Leads ask follow-ups in chat |
| Stuck task resolution | <24h from alert | Auto-flagged in reports | Visible on dashboard | Queryable ("what's still stuck?") |
| Stuck detection speed | Flagged at 3+ days | Automated daily | Same | Same |
| Employee wellbeing | Reduced burnout | Burnout signals in reports | Burnout dashboard page | "Who needs help?" queries |
| Team migration | 100% on GitHub by M6 | GitHub is the data source | GitHub data visible to all | All roles can query |

---

## 9. Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| API cost overrun (Phase 3) | $750+/month if uncapped | Daily query limits, caching, usage dashboard |
| "AI surveillance" perception | Team resistance | Frame as protective (wt-project section 7). Show burnout alerts protect, not punish. |
| Stale wiki data | Wrong answers | Pipeline runs 2x/day + lint checks flag stale articles |
| Single point of failure (one repo) | System down if repo unavailable | Git is distributed. Add monitoring for pipeline failures. |
| Agent SDK hallucination | Incorrect Q&A answers | Always show source citations. Require wiki-backed answers only. |

---

## 10. Open Questions

1. **Hosting:** Internal server (on-prem) vs cloud (Vercel + API)? Depends on data sensitivity.
2. **Auth:** GitHub OAuth sufficient, or need company SSO (SAML)?
3. **Slack vs Teams:** Which messaging platform does the team use?
4. **Budget approval:** Phase 3 API costs (~$300-750/month) need sign-off.
5. **Data retention:** How long to keep daily snapshots? Archive after 90 days?
