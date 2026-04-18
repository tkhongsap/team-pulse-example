# Team Pulse — LLM Wiki Schema

This file describes the Team Pulse knowledge base system. Read this first in every session.

## What This Is

An LLM-maintained knowledge base for team operations intelligence, following Karpathy's
LLM Wiki pattern. Raw data from GitHub (and future sources) is compiled by an LLM into
a persistent wiki that compounds over time. The wiki powers daily briefings, EOD summaries,
and management dashboards for a 150+ person dev organization.

See `docs/wt-project.md` for the organizational goals this system serves.

## Three Layers

### 1. Raw Sources (`raw/`)
Immutable source data. The LLM reads from here but never modifies these files.

- `raw/github-daily/` — AM/PM GitHub activity snapshots (commits, PRs, issues)
- `raw/sources.md` — registry of all data sources and how to add new ones

Future sources: `raw/google-docs/`, `raw/slack/`, `raw/clickup/`

### 2. The Wiki (`wiki/`)
LLM-owned markdown files. The LLM writes and maintains all of this. Humans read it
but rarely edit directly.

- `wiki/index.md` — master catalog of all articles. **Read this first** when answering
  questions or generating reports. Organized by category with one-line summaries.
- `wiki/log.md` — append-only chronological record of all operations (ingest, query, lint).
  Each entry: `## [YYYY-MM-DD] operation | description`
- `wiki/contributors/` — per-person knowledge articles (accumulated over time)
- `wiki/projects/` — per-repo/project status and history articles
- `wiki/patterns/` — recurring signals detected across multiple days
- `wiki/connections/` — cross-cutting insights linking two or more concepts
- `wiki/reports/` — morning briefings, EOD summaries, dashboards (daily reports live here)

### 4. Outputs (`outputs/`)
Saved Q&A answers from `/ask` queries. These accumulate over time — every question
you ask against the wiki gets its answer saved here. Notable answers can be filed
back into `wiki/` to enhance the knowledge base. This is the compounding loop.

## Four Operations

### Ingest (`/compile-wiki`)
Process new raw sources into the wiki. The LLM reads new files, extracts knowledge,
creates or updates wiki articles, updates `wiki/index.md`, and appends to `wiki/log.md`.
A single source may touch 10-15 wiki pages.

### Query (`/morning-briefing`, `/eod-summary`, `/team-dashboard`)
Ask questions against the wiki. The LLM reads `wiki/index.md` first to find relevant
articles, then reads those articles, then synthesizes an answer. Notable findings
should be filed back into the wiki to compound knowledge.

### Ask (`/ask`)
Ask any question against the wiki. The LLM reads `wiki/index.md`, selects relevant
articles, synthesizes an answer, and saves it to `outputs/YYYY-MM-DD-{slug}.md`.
Notable answers can be filed back into `wiki/` to compound knowledge.

### Lint (`/lint-wiki`)
Health-check the wiki. Find broken links, orphan pages, uncompiled sources, stale
articles, sparse articles, and contradictions.

## Wiki Article Format

Every wiki article uses this structure:

```markdown
---
title: "Article Title"
tags: [contributor, project, pattern, connection, report]
sources:
  - "raw/github-daily/2026-04-11-am.md"
created: 2026-04-11
updated: 2026-04-11
---

# Article Title

[2-4 sentence summary]

## Key Points
- [3-5 self-contained bullets]

## Details
[Deeper explanation, encyclopedia-style]

## Related
- [[contributors/garrytan]] — connection explanation
- [[patterns/stuck-items]] — how this relates
```

## Data Flow

```
raw/github-daily/  →  /compile-wiki  →  wiki/              →  /morning-briefing   →  wiki/reports/
(immutable)           (LLM ingest)      (index.md,             /eod-summary           (briefings,
                                         contributors/,        /team-dashboard          summaries,
                                         projects/,                 |                    dashboards)
                                         patterns/)                 |
                          ↑                                         |
                          └──── findings feed next compile ─────────┘
```

## Status Categories (from wt-project.md 4.2)

| Status | Definition |
|---|---|
| **Backlog** | Assigned but untouched tasks |
| **In Progress** | Consistent commits or steady progress |
| **Stuck** | No movement for 3+ days, or repetitive churn |
| **Ready to Hand Off** | Completed tasks ready for next phase |

## Stuck Thresholds

- PRs: open 3+ days with no reviewer assigned
- Issues: no update for 3+ days with 0 comments

## Burnout Signals

- Commits between 22:00-06:00 UTC
- Weekend work
- Disproportionately high activity vs peers
- Sole maintainer of high-volume repo
