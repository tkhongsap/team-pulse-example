# Data Sources Registry

This file documents all data sources feeding into the Team Pulse knowledge base.
When adding a new source, add an entry here following the format below.

---

## github-daily

| Field | Value |
|-------|-------|
| **Directory** | `raw/github-daily/` |
| **Format** | Markdown (AM/PM snapshot pairs) |
| **Filename pattern** | `YYYY-MM-DD-am.md`, `YYYY-MM-DD-pm.md` |
| **Schedule** | Twice daily — 07:00 AM and 18:00 PM Bangkok time (UTC+7) |
| **Extraction script** | `scripts/team_pulse.py` |
| **Repos tracked** | `karpathy/autoresearch`, `garrytan/gstack` |
| **Data captured** | Commits, PRs (opened/merged/open), issues (opened/closed/open), contributor activity, stuck items |
| **Size per file** | ~30 KB |
| **Immutable** | Yes — never modified after writing |

**How to extract:**
```bash
python scripts/team_pulse.py --period am          # morning snapshot
python scripts/team_pulse.py --period pm          # evening snapshot
python scripts/team_pulse.py --date 2026-04-11    # specific date
```

**How to add new repos:**
```bash
python scripts/team_pulse.py --repos owner/repo1 owner/repo2
```

---

## Adding a New Data Source

1. Create a subdirectory under `raw/` (e.g., `raw/slack/`, `raw/google-docs/`)
2. Add an entry to this file documenting the source
3. Write or configure an extraction script in `scripts/`
4. Update the `/compile-wiki` command to include the new source format
5. Run `/compile-wiki` to integrate the new data into the wiki
