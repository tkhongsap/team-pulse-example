# LLM Knowledge Bases

> Source: Andrej Karpathy (@karpathy) — April 3, 2026
> Context: A pattern for using LLMs to build and maintain personal knowledge bases,
> shifting token usage from code manipulation to **knowledge manipulation**.

---

## Overview

Use LLMs to build personal knowledge bases for research topics. Source documents are
indexed into a `raw/` directory, then an LLM incrementally "compiles" them into a wiki
of structured `.md` files. The wiki is the LLM's domain — you rarely edit it directly.

```
raw/                    wiki/                   outputs/
(articles, papers,  →   (.md files,         →   (answers, reports,
 repos, datasets,       summaries,               slides, charts)
 images)                backlinks,                    |
                        concept articles,             |
                        index)                        |
      ↑                                               |
      └──────────── filed back to enhance ────────────┘
```

---

## The Six Components

### 1. Data Ingest

Index source documents (articles, papers, repos, datasets, images) into `raw/`.
The LLM incrementally compiles a wiki from these sources:
- Summaries of all data in `raw/`
- Backlinks between related concepts
- Categorized topic articles with cross-links
- Auto-maintained index files

**Tools:** Obsidian Web Clipper to convert web articles to `.md`, hotkey to download
related images locally so the LLM can reference them.

### 2. IDE / Frontend

Obsidian serves as the "IDE" to view:
- Raw source data
- The compiled wiki
- Derived visualizations (charts, slides)

Key principle: **The LLM writes and maintains all wiki data. You rarely touch it directly.**

Plugins: Marp (slides), various renderers for alternative data views.

### 3. Q&A (Query the Knowledge Base)

Once the wiki reaches sufficient size (~100 articles, ~400K words), you can ask
complex questions and the LLM will research answers across the wiki.

Karpathy's finding: **Fancy RAG is not required at this scale.** The LLM auto-maintains
index files and brief summaries. It reads all important related data fairly easily when
the knowledge base is in the ~hundreds-of-articles range.

### 4. Output

Instead of text/terminal answers, the LLM renders:
- Markdown files
- Slide shows (Marp format)
- Matplotlib/chart images

All viewable in Obsidian. **Critical: file outputs back into the wiki** to enhance it
for further queries. Every exploration and query "adds up" in the knowledge base.

### 5. Linting / Health Checks

Run LLM health checks over the wiki to:
- Find inconsistent data
- Impute missing data (using web search)
- Discover interesting connections for new articles
- Incrementally improve data integrity

LLMs are good at suggesting further questions to investigate.

### 6. Extra Tools

Build additional tools to process the data:
- Search engine over the wiki (web UI for direct use, CLI for LLM tool use)
- Custom CLIs the LLM can invoke for larger queries

### Future: Synthetic Data + Fine-tuning

As the repo grows, explore synthetic data generation and fine-tuning so the LLM
"knows" the data in its weights instead of relying solely on context windows.

---

## Key Principles

1. **LLM owns the wiki.** Human curates sources and asks questions. LLM organizes,
   summarizes, links, and maintains everything.
2. **Compounding loop.** Every output gets filed back into the knowledge base,
   making the next query better.
3. **No fancy infrastructure.** Folders of `.md` files, an LLM, and a viewer
   (Obsidian). No database, no vector store, no RAG pipeline at small scale.
4. **Health checks prevent error compounding.** Regular linting catches mistakes
   before they propagate through the knowledge base.
5. **Tools extend the LLM.** Give the LLM CLI tools (search, web fetch) to
   operate on the wiki at scale.

---

## TLDR

> Raw data from a given number of sources is collected, then compiled by an LLM
> into a .md wiki, then operated on by various CLIs by the LLM to do Q&A and to
> incrementally enhance the wiki, and all of it viewable in Obsidian. You rarely
> ever write or edit the wiki manually, it's the domain of the LLM. I think there
> is room here for an incredible new product instead of a hacky collection of scripts.
>
> — Andrej Karpathy
