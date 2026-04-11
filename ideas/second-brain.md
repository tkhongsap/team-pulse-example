# Second Brain for Team Pulse
## Applying Karpathy's LLM Knowledge Base Pattern to Team Intelligence

> Origin: Andrej Karpathy (@karpathy), April 3 2026
> Extended by: Corey Ganim (@coreyganim), community discussion
> Adapted for: Team Pulse — AI-Driven Workspace Transformation (wt-project.md)

---

## 1. The Core Idea

Use LLMs not just to write code, but to **compile, maintain, and query a knowledge base**
that gets smarter over time. Raw data goes in, structured knowledge comes out, and every
query enhances the system for the next one.

Karpathy's architecture:
```
raw/        →  LLM compiles  →  wiki/        →  LLM queries  →  outputs/
(source data)                   (structured      (answers,
                                 .md wiki)        reports,
                                                  slides)
                    ↑                                   |
                    └───────── filed back ──────────────┘
```

The critical insight: **You rarely edit the wiki manually. The LLM maintains it.**
A schema file (CLAUDE.md) tells the LLM what the knowledge base is about and how to
organize it. The human curates sources and asks questions. The LLM does everything else.

---

## 2. How This Maps to Team Pulse

We are already building this pattern. Here's the mapping:

| Karpathy's Pattern       | Team Pulse Implementation                  | Status     |
|--------------------------|---------------------------------------------|------------|
| `raw/` — source data     | `docs/daily/` — AM/PM GitHub snapshots      | Done       |
| Schema file (CLAUDE.md)  | `.claude/commands/` — insight commands       | Done       |
| `wiki/` — compiled wiki  | `docs/insights/` — LLM-generated analysis   | Done       |
| `outputs/` — reports     | Morning briefings, EOD summaries, dashboards | Done       |
| Data ingest pipeline     | `scripts/team_pulse.py` (7AM + 6PM Bangkok) | Done       |
| Q&A against wiki         | `/morning-briefing`, `/eod-summary`, etc.    | Done       |
| Compounding loop         | Insights filed back, inform next queries     | Partial    |
| Monthly health check     | Weekly linting / consistency review          | Not yet    |
| Search tool over wiki    | CLI or web UI to search daily notes          | Not yet    |
| Synthetic data / finetune| Train model on team patterns                 | Future     |

**What we have is already a "Second Brain" for team operations.**
The daily snapshots are the raw data. The insight commands compile it into structured
analysis. Each morning briefing builds on the previous day's context.

---

## 3. What We Should Build Next (Implementation Roadmap)

### Phase 1: The Compounding Loop (high priority)
Right now insights are generated but not fed back. We need:

- [ ] **Index file**: Auto-maintain `docs/insights/INDEX.md` listing all generated
      reports with one-line summaries. This lets the LLM quickly scan what analysis
      already exists before generating new reports.
- [ ] **Cross-referencing**: EOD summaries should reference the morning briefing.
      Team dashboards should reference the full week's insights.
- [ ] **Trend accumulation**: A `docs/insights/weekly-trends.md` that accumulates
      week-over-week metrics so each new dashboard builds on historical context.

### Phase 2: Health Check / Linting (medium priority)
Per Karpathy: "small mistakes compound into garbage answers six months later."

- [ ] **Weekly consistency review command** (`/weekly-review`):
      - Cross-check daily notes for data gaps (missing AM or PM snapshots)
      - Flag contradictions between days (e.g., stuck item count went down but
        no merges recorded)
      - Identify recurring stuck items that never get resolved
      - Suggest process improvements based on patterns
- [ ] **Data quality checks**: Verify that the extraction script captured all
      expected data points. Flag empty sections.

### Phase 3: Search and Retrieval (medium priority)
When the knowledge base grows large enough, scanning all files becomes expensive.

- [ ] **Simple search CLI**: Python script to search across all daily notes and
      insights by keyword, date range, contributor, or PR number.
- [ ] **Summary index**: Each daily note already has a summary table. Compile these
      into a single `docs/daily/INDEX.md` for quick lookup.
- [ ] **Tool for LLM**: Expose search as a CLI tool that Claude can call during
      analysis (e.g., "find all days where garrytan had late-night commits").

### Phase 4: Passive Updates (future)
Community insight from @danserikson: "The only version that works long-term is one
that updates itself passively — from your conversations, not from drag-and-drop."

- [ ] **Automated extraction**: Cron job or scheduled task runs `team_pulse.py`
      at 7AM and 6PM Bangkok time automatically.
- [ ] **Auto-generate insights**: After extraction, automatically run the insight
      commands via Claude API (Option B from our earlier discussion).
- [ ] **Notification**: Push the morning briefing to Slack or email so team leads
      don't need to open Claude Code.

### Phase 5: Beyond Markdown (future)
- [ ] **Visualization**: Generate charts (matplotlib/plotly) for trends, embed in
      weekly reports. Viewable in Obsidian or a simple web dashboard.
- [ ] **Slides**: Generate Marp-format slide decks for management presentations.
- [ ] **Fine-tuning**: Once we have 3-6 months of daily data + insights, explore
      fine-tuning a model on our team's patterns for faster, cheaper analysis.

---

## 4. Architecture Principles (from Karpathy + Community)

### Do
- **Let the LLM own the wiki.** You curate sources and ask questions. The LLM
  organizes, summarizes, links, and maintains everything in `docs/insights/`.
- **Use a schema file.** Our `.claude/commands/` serve this purpose — they tell
  the LLM exactly what structure to produce and what context to reference.
- **File outputs back into the system.** Every morning briefing, EOD summary, and
  dashboard should be saved as markdown. Future queries benefit from past analysis.
- **Run health checks.** At least monthly, validate the knowledge base for
  consistency, gaps, and compounding errors.
- **Keep it simple.** Three folders and text files outperform a fancy tool stack.
  Our structure (`docs/daily/`, `docs/insights/`, `scripts/`) follows this.

### Don't
- **Don't over-engineer the tooling.** (Tom Callahan: "The tool has never mattered.
  You can have WAY less token usage using files and a proper index.")
- **Don't skip the health check.** (Tom Solid: "The monthly health check is the
  part that actually keeps the system alive.")
- **Don't require manual maintenance.** (Dan Serikson: "The manual knowledge base
  dies within a month. The only version that works is one that updates passively.")
- **Don't duplicate raw data unnecessarily.** Keep extractions lean. Our daily
  snapshots are ~30KB each — manageable for years.

---

## 5. Key Metrics for Our Second Brain

Track these to know if the system is working:

| Metric                          | Target                    | How to Measure              |
|---------------------------------|---------------------------|-----------------------------|
| Daily snapshot coverage         | 100% (AM + PM every day)  | Count files in docs/daily/  |
| Insight generation frequency    | At least 1/day            | Count files in docs/insights|
| Time to morning briefing        | < 5 min after extraction   | Manual timing               |
| Stuck item detection accuracy   | Matches reality            | Spot-check against GitHub   |
| Knowledge base size (6 months)  | ~500 daily notes, ~200 insights | File count            |
| Management adoption             | Leads use dashboards daily | Usage tracking              |

---

## 6. References

- Andrej Karpathy original post: https://x.com/karpathy/status/... (Apr 3, 2026)
- Corey Ganim explainer: https://x.com/coreyganim/status/2041144598446092411
- Obsidian Second Brain template: https://github.com/eugeniughelbur/obsidian-second-brain
- Team Pulse wt-project: docs/wt-project.md
- Team Pulse extraction script: scripts/team_pulse.py
- Team Pulse insight commands: .claude/commands/morning-briefing.md, eod-summary.md, team-dashboard.md
