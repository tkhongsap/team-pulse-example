# LLM Knowledge Bases for Internal Data — Claude Code Memory System

> Source: Video transcript (YouTube)
> Topic: Adapting Karpathy's LLM Knowledge Base pattern from external data to
> internal codebase knowledge using Claude Code hooks and the Agent SDK.
> Original transcript preserved in: ideas/transcript.txt

---

## Summary

Karpathy's LLM Knowledge Base pattern works with **external** data (articles, papers,
web content). This video presents an adaptation for **internal** data — giving Claude
Code a persistent memory that evolves with your codebase by automatically capturing
session logs, extracting knowledge, and building a searchable wiki.

The system is built entirely on **Claude Code hooks** (no external integrations needed)
and uses the **Claude Agent SDK** for background processing.

---

## 1. Karpathy's Architecture (Recap)

The compiler analogy — knowledge flows like code compilation:

```
Source Code     →  Compiler    →  Executable   →  Test Suite  →  Runtime
(raw articles)    (LLM)          (wiki)           (linting)      (Q&A queries)
```

| Stage | Code Analogy | Knowledge Base |
|-------|-------------|----------------|
| Source | Source code files | Articles, papers, web clips in `raw/` |
| Compiler | Build system | LLM processes raw → structured wiki |
| Executable | Running application | The wiki: concepts, connections, index |
| Test suite | Unit tests, linting | Health checks: gaps, stale data, broken links |
| Runtime | User runs the app | Q&A: agent searches wiki to answer questions |

Key insight from Karpathy:
> "I thought I had to reach for fancy RAG, but the LLM has been pretty good about
> auto-maintaining index files."

No vector database. No semantic search. Just an index file that tells the agent where
to look, and it navigates the markdown files directly.

---

## 2. The Adaptation: External → Internal Data

| Karpathy (External) | This System (Internal) |
|---------------------|----------------------|
| Web articles, papers, repos | Claude Code session conversations |
| Manual web clipping (Obsidian Web Clipper) | Automatic capture via hooks |
| User decides what to ingest | Every session is captured |
| Compiles into topic wiki | Compiles into codebase knowledge wiki |
| Q&A about research topics | Q&A about your project's history, decisions, patterns |

The core difference: **you don't have to manually collect anything.** The hooks
automatically capture every Claude Code session and extract knowledge from it.

---

## 3. System Architecture

### Directory Structure

```
project/
├── agents.md              # System description (like CLAUDE.md)
│                           # Tells the agent how the knowledge system works
├── daily-logs/            # Raw equivalent — session summaries
│   ├── 2026-04-11.md      # Each day's conversations, auto-generated
│   └── ...
├── knowledge/             # Wiki equivalent — compiled knowledge
│   ├── index.md           # Master index of all knowledge articles
│   ├── concepts/          # Extracted concepts from conversations
│   └── connections/       # How concepts relate to each other
└── scripts/
    ├── compile.py         # LLM processes logs → knowledge articles
    └── flush.py           # Daily extraction from logs to wiki
```

### Three Claude Code Hooks

**1. Session Start Hook**
- Loads `agents.md` (system description) into context
- Loads `knowledge/index.md` so the agent knows what's in the wiki
- Result: every new session starts with full awareness of the knowledge base

**2. Pre-Compact Hook** (before memory compaction)
- Sends latest messages to Claude Agent SDK (background process)
- Agent SDK extracts: decisions made, lessons learned, action items
- Saves structured summary to `daily-logs/YYYY-MM-DD.md`
- Prevents knowledge loss when context window compacts

**3. Session End Hook**
- Same as pre-compact but triggers on session close
- Ensures nothing is lost even if the session ends naturally

### The Flush Process (Daily)

Once per day, a background process:
1. Reads all new entries from `daily-logs/`
2. Extracts concepts and connections
3. Updates `knowledge/` wiki articles
4. Updates `knowledge/index.md`

This is the "compiler" step — raw session logs become structured, searchable knowledge.

---

## 4. The Compounding Knowledge Loop

```
Ask question → Agent searches wiki → Synthesizes answer
                                           |
                                     Answer filed back
                                     into knowledge base
                                           |
                              Wiki grows → Next query is better
```

Every conversation makes the system smarter:
- New sessions automatically captured
- Logs automatically processed into knowledge articles
- Knowledge articles cross-referenced and linked
- Agent searches get more comprehensive over time
- **No manual maintenance required**

---

## 5. Key Advantages Over Other Approaches

1. **No fancy RAG needed** — Index file + markdown navigation is sufficient at
   small-to-medium scale (hundreds of articles, ~400K words)
2. **No external services** — Runs entirely on Claude Code hooks + Agent SDK
3. **Self-contained** — The system can explain itself to Claude Code because
   `agents.md` describes the entire architecture
4. **Self-improving** — Claude Code can modify the prompts in `scripts/` to
   customize how knowledge is extracted
5. **Viewable in Obsidian** — Graph view shows connections between concepts,
   making the knowledge base visually navigable
6. **Customizable extraction** — You can modify the compile/flush prompts to
   extract different types of knowledge (decisions, patterns, gotchas, etc.)

---

## 6. Relevance to Team Pulse

This is essentially what we're building, but for **team-level operations data**
instead of individual codebase knowledge:

| This System | Team Pulse |
|-------------|-----------|
| Claude Code session logs | GitHub activity snapshots (AM/PM) |
| Automatic hook capture | `team_pulse.py` scheduled extraction |
| `agents.md` schema | `.claude/commands/` insight prompts |
| `knowledge/` wiki | `docs/insights/` analysis reports |
| Daily flush/compile | `/morning-briefing`, `/eod-summary` |
| Index file for search | Summary tables in each daily note |
| Compounding loop | Each insight informs the next query |
| Obsidian as viewer | GitHub markdown rendering |

**What we could adopt from this system:**
- Automatic index maintenance (currently manual)
- Hook-based capture instead of manual script runs
- Background Agent SDK processing for insights (our Option B)
- Concept/connection extraction from daily patterns over time

---

## 7. References

- Karpathy's original tweet (April 3, 2026)
- Claude Code hooks: settings.json hook configuration
- Claude Agent SDK: background LLM processing
- Obsidian: markdown viewer with graph visualization
- Related file: ideas/llm-knowledge-base.md (Karpathy's original, organized)
- Related file: ideas/second-brain.md (implementation guide for Team Pulse)
