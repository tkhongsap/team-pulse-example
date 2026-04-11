---
name: llamaparse
description: Extract content from complex PDFs using LlamaParse cloud API. Best for documents with tables, figures, multi-column layouts, and scientific papers where local extraction (pypdf/pdfplumber) falls short.
---

# LlamaParse PDF Extraction

## When to Use

Use LlamaParse (this skill) instead of the `pdf` skill when:
- The PDF has complex layouts (multi-column, nested tables, figures with captions)
- Local extraction produces garbled or incomplete text
- You need high-fidelity markdown output from scientific papers or reports
- The document contains scanned pages that need cloud-based OCR

Use the `pdf` skill for simpler tasks (merging, splitting, form filling, basic text extraction).

## Quick Start

```bash
# Ensure dependencies are installed
.venv/bin/pip install -r llamaindex/requirements.txt

# Extract a single PDF to markdown (default)
.venv/bin/python llamaindex/llamaparse_extract.py document.pdf

# Extract a directory of PDFs to text
.venv/bin/python llamaindex/llamaparse_extract.py docs/ -f text -o results/

# Use a specific parsing tier
.venv/bin/python llamaindex/llamaparse_extract.py paper.pdf --tier agentic_plus -v

# Use a specific vendor multimodal model
.venv/bin/python llamaindex/llamaparse_extract.py paper.pdf --model gemini-2.5-flash -v
```

## API Key

The script reads `LLAMA_CLOUD_API_KEY` from the `.env` file at the repository root. You can also pass it directly:

```bash
.venv/bin/python llamaindex/llamaparse_extract.py doc.pdf --api-key llx-...
```

## Parsing Tiers

| Tier | Best For |
|------|----------|
| `agentic` | Good quality, reasonable speed (default) — 10 credits/page |
| `agentic_plus` | Highest quality, slower — 45 credits/page |
| `cost_effective` | Balance of cost and quality — 3 credits/page |
| `fast` | No AI, spatial text only — 1 credit/page |

## Vendor Multimodal Models

Use `--model` to override the tier's default LLM. Available models:

| Model | Vendor |
|-------|--------|
| `openai-gpt4o` | OpenAI |
| `openai-gpt-4o-mini` | OpenAI |
| `openai-gpt-4-1-nano` | OpenAI |
| `openai-gpt-4-1-mini` | OpenAI |
| `openai-gpt-4-1` | OpenAI |
| `anthropic-sonnet-3.7` | Anthropic |
| `anthropic-sonnet-4.0` | Anthropic |
| `anthropic-sonnet-4.5` | Anthropic (preview) |
| `anthropic-haiku-4.5` | Anthropic (preview) |
| `gemini-2.0-flash` | Google |
| `gemini-2.5-flash` | Google |
| `gemini-2.5-pro` | Google |

Credit costs vary by model (10–90 credits/page). Omit `--model` to use the tier's built-in default.

## CLI Reference

```
llamaparse_extract.py [-h] [-f {markdown,text}] [-o OUTPUT_DIR]
                      [--tier {agentic,agentic_plus,cost_effective,fast}]
                      [--model MODEL] [--api-key API_KEY] [-v]
                      input [input ...]
```

| Flag | Description |
|------|-------------|
| `input` | PDF file(s) or directory |
| `-f, --format` | Output format: `markdown` (default) or `text` |
| `-o, --output-dir` | Where to write output (default: `llamaindex/output/`) |
| `--tier` | Parsing tier (default: `agentic`) |
| `--model` | Vendor multimodal model (overrides tier default) |
| `--api-key` | Override env var API key |
| `-v, --verbose` | Detailed progress output |

## Output

Extracted files are written to `llamaindex/output/` by default:
- `document.md` for markdown format
- `document.txt` for text format

Files are never overwritten; a numeric suffix is appended if needed.

## Project Structure

```
llamaindex/
├── llamaparse_extract.py    # Single extraction script
├── requirements.txt         # Dependencies (llama-parse, python-dotenv)
├── input/                   # PDF input directory
└── output/                  # Default output directory
```
