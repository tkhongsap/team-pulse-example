# PRD: Team Pulse Production System

## Introduction

Team Pulse is an LLM-maintained knowledge base for team operations intelligence.
It extracts daily GitHub activity, compiles it into a persistent wiki, and provides
AI-powered reports and Q&A — following Karpathy's LLM Wiki pattern.

The PoC runs manually in the terminal via Claude Code. This PRD covers the production
system: an automated backend (Phase 1) and a claude.ai-style web app (Phase 2+3) that
share the same backend — CLAUDE.md, .claude/commands/, wiki/, raw/.

**Ref:** `docs/prd-team-pulse-production.md` (detailed PRD), `docs/wt-project.md`
(organizational goals), `docs/frontend-design.md` (UI spec), `CLAUDE.md` (system schema).

## Goals

- Automate daily extraction + wiki compilation + report generation (zero manual steps)
- Provide a claude.ai-style web interface for the 150+ person team to browse reports and ask questions
- Maintain one backend shared by terminal (Claude Code) and web (Agent SDK)
- Track GitHub activity for `karpathy/autoresearch` and `garrytan/gstack`
- Deliver wt-project.md mechanisms: morning briefing, EOD summary, status categorization, burnout detection

## User Stories

### Phase 1: Automated Backend

---

### US-001: Create Agent SDK compile script
**Description:** As a system operator, I want wiki compilation to run via the Agent SDK so that it can be triggered by cron without Claude Code.

**Acceptance Criteria:**
- [ ] `scripts/compile.py` exists and is executable with `python scripts/compile.py`
- [ ] Uses `claude_agent_sdk.query()` with `allowed_tools=["Read", "Write", "Edit", "Glob", "Grep"]`
- [ ] Sets `setting_sources=["project"]` so CLAUDE.md is loaded automatically
- [ ] Reads `wiki/log.md` to identify uncompiled raw files
- [ ] Creates/updates wiki articles in `wiki/contributors/`, `wiki/projects/`, `wiki/patterns/`, `wiki/connections/`
- [ ] Updates `wiki/index.md` with new/modified entries
- [ ] Appends to `wiki/log.md` with timestamp and summary
- [ ] Requires `ANTHROPIC_API_KEY` environment variable
- [ ] Prints cost estimate after completion
- [ ] Typecheck/lint passes

---

### US-002: Create Agent SDK report generation script
**Description:** As a system operator, I want report generation to run via the Agent SDK so that morning briefings and EOD summaries are generated automatically.

**Acceptance Criteria:**
- [ ] `scripts/generate_report.py` exists with `--type morning|eod|dashboard` and `--date YYYY-MM-DD` flags
- [ ] Uses `claude_agent_sdk.query()` with `allowed_tools=["Read", "Glob", "Grep", "Write"]`
- [ ] Sets `setting_sources=["project"]` so CLAUDE.md and .claude/commands/ are loaded
- [ ] For `--type morning`: reads `raw/github-daily/YYYY-MM-DD-am.md` + wiki articles, writes to `wiki/reports/YYYY-MM-DD-morning-briefing.md`
- [ ] For `--type eod`: reads both AM + PM snapshots + morning briefing + wiki, writes to `wiki/reports/YYYY-MM-DD-eod-summary.md`
- [ ] For `--type dashboard`: reads 7 days of data + wiki, writes to `wiki/reports/YYYY-MM-DD-team-dashboard.md`
- [ ] Output matches the format produced by the corresponding `.claude/commands/` file
- [ ] Requires `ANTHROPIC_API_KEY` environment variable
- [ ] Typecheck/lint passes

---

### US-003: Create pipeline orchestrator
**Description:** As a system operator, I want a single command that runs the full pipeline (extract → compile → report → git commit) so that cron only needs one entry.

**Acceptance Criteria:**
- [ ] `scripts/run_pipeline.py` exists with `--period am|pm` flag
- [ ] Runs `team_pulse.py --period {am|pm}` and verifies output file was created
- [ ] Runs `compile.py` and verifies wiki was updated
- [ ] Runs `generate_report.py --type morning` (for AM) or `--type eod` (for PM)
- [ ] Runs `git add . && git commit && git push` after all steps complete
- [ ] Logs each step's status and timing to `scripts/pipeline.log`
- [ ] Exits with non-zero code if any step fails (does NOT commit partial state)
- [ ] Prints summary: files created, articles updated, cost
- [ ] Typecheck/lint passes

---

### US-004: Create crontab configuration
**Description:** As a system operator, I want cron entries so the pipeline runs automatically at 7AM and 6PM Bangkok time.

**Acceptance Criteria:**
- [ ] `scripts/crontab.txt` contains two cron entries for 7AM and 6PM Bangkok (UTC+7 = 0:00 and 11:00 UTC)
- [ ] Each entry runs `run_pipeline.py --period am` or `--period pm`
- [ ] Entries include `cd /path/to/team-pulse-example &&` to set working directory
- [ ] Entries redirect stdout/stderr to `scripts/pipeline.log`
- [ ] `scripts/setup-cron.sh` installs the crontab entries
- [ ] README or comment explains how to install: `crontab scripts/crontab.txt`

---

### US-005: Create .env template and configuration
**Description:** As a system operator, I want a documented .env template so I can configure the system.

**Acceptance Criteria:**
- [ ] `.env.example` exists with all required variables documented
- [ ] Contains: `ANTHROPIC_API_KEY=your-key-here`
- [ ] Contains: `GITHUB_TOKEN=` (optional, for private repos)
- [ ] Contains: `TEAM_PULSE_REPOS=karpathy/autoresearch,garrytan/gstack`
- [ ] Contains: `TEAM_PULSE_TIMEZONE=Asia/Bangkok`
- [ ] `scripts/team_pulse.py` reads `TEAM_PULSE_REPOS` from env if set (falls back to DEFAULT_REPOS)
- [ ] All Agent SDK scripts load `.env` via `python-dotenv`
- [ ] `.env` is in `.gitignore` (already is)
- [ ] Typecheck/lint passes

---

### Phase 2+3: Web App (claude.ai-style)

---

### US-006: Initialize Next.js project with Tailwind and shadcn/ui
**Description:** As a developer, I need the web app project scaffolded so I can build components.

**Acceptance Criteria:**
- [ ] `web/` directory created with Next.js 14+ (App Router)
- [ ] Tailwind CSS configured
- [ ] shadcn/ui initialized with default theme
- [ ] Inter font loaded (body text)
- [ ] JetBrains Mono loaded (code blocks)
- [ ] `web/package.json` has all dependencies
- [ ] `npm run dev` starts dev server on port 3000
- [ ] Root page renders "Team Pulse" placeholder text
- [ ] Typecheck passes

---

### US-007: Build sidebar layout with navigation
**Description:** As a team lead, I want a left sidebar to browse chat history, reports, and wiki articles so I can navigate the system.

**Acceptance Criteria:**
- [ ] Sidebar is 280px wide on desktop, collapsible on mobile (<768px)
- [ ] Sidebar has three sections: Quick Actions, Reports Archive, Wiki Browser
- [ ] Quick Actions: "New Chat", "Morning Briefing", "EOD Summary", "Team Dashboard" buttons
- [ ] Reports Archive: lists dates, expandable to show morning-briefing and eod-summary for each
- [ ] Wiki Browser: collapsible sections for Contributors, Projects, Patterns, Connections
- [ ] Wiki Browser reads file list from `wiki/` directory (or API route that returns it)
- [ ] Clicking a sidebar item loads content in the main area
- [ ] Active item is highlighted in sidebar
- [ ] Sidebar background: `#f9fafb` light / `#1e293b` dark
- [ ] Typecheck passes
- [ ] Verify in browser on localhost:3000

---

### US-008: Build markdown report viewer
**Description:** As a team lead, I want to view morning briefings, EOD summaries, and dashboards as rendered markdown so I can read them in the browser.

**Acceptance Criteria:**
- [ ] API route `GET /api/reports/[date]/[type]` returns markdown content from `wiki/reports/`
- [ ] Main area renders markdown with: headers, tables, bold, code blocks, lists
- [ ] `[[wikilinks]]` render as clickable chips that navigate to the wiki article
- [ ] Status badges render with colors: Stuck=red, In Progress=green, Backlog=yellow, Idle=gray
- [ ] "Back to Chat" button returns to chat mode
- [ ] Route: `/reports/[date]/[type]` (e.g., `/reports/2026-04-11/morning-briefing`)
- [ ] Typecheck passes
- [ ] Verify in browser: load `/reports/2026-04-11/morning-briefing`, confirm tables render

---

### US-009: Build wiki article viewer
**Description:** As a team lead, I want to browse contributor profiles, project pages, and pattern articles in the browser.

**Acceptance Criteria:**
- [ ] API route `GET /api/wiki/[...slug]` returns markdown from `wiki/` directory
- [ ] Route: `/wiki/contributors/garrytan`, `/wiki/projects/gstack`, etc.
- [ ] YAML frontmatter parsed and displayed as metadata header (title, updated date, sources)
- [ ] `[[wikilinks]]` render as clickable links navigating within the app
- [ ] Related section links are clickable
- [ ] Typecheck passes
- [ ] Verify in browser: load `/wiki/contributors/garrytan`, confirm content renders

---

### US-010: Build chat interface with Agent SDK streaming
**Description:** As a team member, I want to ask free-form questions and get streaming AI answers backed by the wiki, like claude.ai.

**Acceptance Criteria:**
- [ ] Chat is the default view at `/`
- [ ] Input bar at bottom: auto-expanding text area + Send button
- [ ] POST `/api/ask` accepts `{ question, sessionId? }` and streams response
- [ ] Backend uses `claude_agent_sdk.query()` with `allowed_tools=["Read", "Glob", "Grep"]` and `setting_sources=["project"]`
- [ ] Responses stream word-by-word to the frontend (Server-Sent Events or WebSocket)
- [ ] User messages styled with light gray background, left-aligned with "You" label
- [ ] AI messages styled white background, left-aligned with "Team Pulse" label
- [ ] Markdown rendered in AI responses (tables, headers, bold, code)
- [ ] Conversation history maintained within session (Agent SDK `resume=session_id`)
- [ ] Typecheck passes
- [ ] Verify in browser: type "Who is busiest today?", confirm streaming response

---

### US-011: Display source citations in chat responses
**Description:** As a team lead, I want to see which wiki articles were consulted so I can verify the answer's basis.

**Acceptance Criteria:**
- [ ] Source citations block displayed at bottom of each AI response
- [ ] Each source is a clickable chip: `[garrytan.md]` `[burnout-signals.md]`
- [ ] Clicking a source navigates to the wiki article viewer
- [ ] `[[wikilinks]]` within response text also render as clickable chips
- [ ] Typecheck passes
- [ ] Verify in browser: ask a question, confirm source chips appear and are clickable

---

### US-012: Add dark/light mode toggle
**Description:** As a user, I want to switch between dark and light themes.

**Acceptance Criteria:**
- [ ] Toggle button in header bar (sun/moon icon)
- [ ] Light mode: white bg, `#111827` text, `#4f46e5` accent (per frontend-design.md)
- [ ] Dark mode: `#0f172a` bg, `#f1f5f9` text, `#818cf8` accent (per frontend-design.md)
- [ ] Preference persisted in localStorage
- [ ] All components (sidebar, chat, report viewer) respect the theme
- [ ] Typecheck passes
- [ ] Verify in browser: toggle dark mode, confirm all areas switch

---

### US-013: Add GitHub OAuth authentication
**Description:** As an admin, I want only authenticated team members to access the app.

**Acceptance Criteria:**
- [ ] NextAuth.js configured with GitHub OAuth provider
- [ ] Login page shown for unauthenticated users
- [ ] User avatar and name displayed in header bar
- [ ] Logout option in user dropdown
- [ ] `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` in `.env.example`
- [ ] Unauthorized API requests return 401
- [ ] Typecheck passes
- [ ] Verify in browser: access `/` while logged out, confirm redirect to login

---

### US-014: Add suggested questions on empty chat state
**Description:** As a new user, I want to see suggested questions when the chat is empty so I know what to ask.

**Acceptance Criteria:**
- [ ] Empty chat shows 4 suggestion cards in a 2x2 grid
- [ ] Cards: "Who needs help?" (burnout), "Today's briefing" (morning report), "Weekly summary" (management), "Compare repos" (gstack vs autoresearch)
- [ ] Clicking a card sends that question to the chat
- [ ] Cards disappear once the first message is sent
- [ ] Typecheck passes
- [ ] Verify in browser: load `/`, confirm 4 cards visible, click one, confirm chat starts

---

### US-015: Make layout mobile responsive
**Description:** As a team lead, I want to use the app on my phone.

**Acceptance Criteria:**
- [ ] At <768px: sidebar hidden, hamburger menu icon in header to toggle sidebar as overlay
- [ ] At 768-1024px: sidebar collapsed to 60px icon-only mode
- [ ] At >1024px: full sidebar (280px)
- [ ] Chat input bar always visible at bottom on all screen sizes
- [ ] Tables in reports scroll horizontally on small screens
- [ ] Typecheck passes
- [ ] Verify in browser: resize to 375px width, confirm sidebar hidden, chat usable

---

### US-016: Add rate limiting and usage tracking
**Description:** As an admin, I want to limit API costs and track usage.

**Acceptance Criteria:**
- [ ] Rate limit: max 100 `/api/ask` requests per user per day
- [ ] Rate limit response: 429 with message "Daily query limit reached. Resets at midnight Bangkok time."
- [ ] Usage counter displayed in settings page: "X/100 queries used today"
- [ ] Admin can see aggregate usage (total queries, estimated cost) at `/settings/usage`
- [ ] Cost estimated at $0.35/query displayed alongside usage
- [ ] Typecheck passes

---

## Functional Requirements

### Backend (Phase 1)
- FR-1: `scripts/compile.py` compiles raw sources into wiki using Agent SDK with `setting_sources=["project"]`
- FR-2: `scripts/generate_report.py` generates morning/eod/dashboard reports using Agent SDK
- FR-3: `scripts/run_pipeline.py` orchestrates extract → compile → report → git push
- FR-4: Cron runs pipeline at 07:00 and 18:00 Bangkok time (00:00 and 11:00 UTC)
- FR-5: All scripts load config from `.env` via python-dotenv
- FR-6: `team_pulse.py` reads `TEAM_PULSE_REPOS` from environment if set
- FR-7: Pipeline does NOT commit if any step fails

### Web App (Phase 2+3)
- FR-8: Web app reads wiki/ and raw/ from the git repo (synced on each pipeline push)
- FR-9: Chat uses Agent SDK streaming for real-time responses
- FR-10: Agent SDK sessions enable follow-up questions within a conversation
- FR-11: All markdown rendered with table, header, bold, code block, and list support
- FR-12: `[[wikilinks]]` render as clickable navigation chips throughout the app
- FR-13: Status badges (Stuck, In Progress, Backlog, Idle) render with distinct colors
- FR-14: Authentication required for all routes
- FR-15: Dark/light mode persisted per user in localStorage
- FR-16: Rate limiting at 100 queries/user/day on `/api/ask`

### Shared
- FR-17: Terminal commands (Claude Code) and web app (Agent SDK) produce identical output for the same operation
- FR-18: Both read the same CLAUDE.md, .claude/commands/, wiki/, raw/
- FR-19: Changes to `.claude/commands/morning-briefing.md` affect both terminal and web

## Non-Goals

- No Slack or email integration (web app is the delivery channel)
- No real-time GitHub webhooks (cron-based extraction only, 2x/day)
- No user-level permissions (all authenticated users see all data)
- No custom repo configuration per user (all users see same repos)
- No mobile native app (responsive web only)
- No data export (CSV, PDF) in v1
- No multi-tenant support (single team, single wiki)
- No Obsidian integration (web app replaces Obsidian as the viewer)

## Design Considerations

- **UI Reference:** claude.ai chat interface — see `docs/frontend-design.md` for full spec
- **Layout:** Three-panel: sidebar (280px) + header (56px) + main area (chat or report viewer)
- **Color palette:** Indigo accent (`#4f46e5`), status colors (red/green/yellow/gray)
- **Typography:** Inter (body), JetBrains Mono (code)
- **Components:** Reuse shadcn/ui Button, Card, Input, Badge, Sheet (sidebar), Dialog
- **Empty state:** 4 suggested question cards in 2x2 grid

## Technical Considerations

- **Agent SDK version:** `claude-agent-sdk>=0.1.29` (Python)
- **Next.js version:** 14+ with App Router
- **API key:** `ANTHROPIC_API_KEY` required for all Agent SDK calls
- **Data sync:** Web app reads from the same git repo. Pipeline pushes to git, web refreshes on next request or rebuild.
- **Streaming:** Server-Sent Events from `/api/ask` route. Agent SDK `query()` yields messages that are forwarded to the client.
- **Sessions:** Agent SDK `resume=session_id` for conversation memory. Session ID stored in browser sessionStorage.
- **Working directory:** Agent SDK must run in the repo root so `setting_sources=["project"]` finds CLAUDE.md.
- **Existing code to reuse:** `scripts/team_pulse.py` (extraction), `.claude/commands/*.md` (prompts), `CLAUDE.md` (schema).

## Success Metrics

- Pipeline runs 2x/day without failure for 7 consecutive days
- Morning briefing available on web app by 7:15 AM Bangkok time
- EOD summary available on web app by 6:15 PM Bangkok time
- Chat answers reference wiki articles with source citations >90% of the time
- Page load time <2 seconds for report viewer
- Chat response streaming starts within 3 seconds of sending question
- Zero manual intervention required for daily report generation
- Web app accessible on mobile (375px width) without horizontal scroll

## Open Questions

1. Should the web app deploy on Vercel (easy) or internal server (data privacy)?
2. Should we add GitHub org restriction to OAuth (only team members can log in)?
3. How to handle Agent SDK failures gracefully in the web UI (retry? fallback message?)?
4. Should chat conversations be persisted in a database or just browser sessionStorage?
5. At what wiki size (~articles) should we add search beyond index.md scanning?
