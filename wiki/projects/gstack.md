---
title: "gstack"
tags: [project, garrytan]
sources:
  - "raw/github-daily/2026-04-04-am.md"
  - "raw/github-daily/2026-04-05-am.md"
  - "raw/github-daily/2026-04-06-am.md"
  - "raw/github-daily/2026-04-07-am.md"
  - "raw/github-daily/2026-04-08-am.md"
  - "raw/github-daily/2026-04-09-am.md"
  - "raw/github-daily/2026-04-10-am.md"
  - "raw/github-daily/2026-04-11-am.md"
  - "raw/github-daily/2026-04-12-am.md"
  - "raw/github-daily/2026-04-13-am.md"
  - "raw/github-daily/2026-04-14-am.md"
  - "raw/github-daily/2026-04-15-am.md"
  - "raw/github-daily/2026-04-16-am.md"
  - "raw/github-daily/2026-04-17-am.md"
  - "raw/github-daily/2026-04-17-pm.md"
  - "raw/github-daily/2026-04-18-am.md"
created: 2026-04-11
updated: 2026-04-18
---

# gstack

Repository: [garrytan/gstack](https://github.com/garrytan/gstack). TypeScript-based AI agent toolkit with 69K+ stars. High community engagement with a sole maintainer bottleneck. **RECOVERY SUSTAINED: Apr 17-18 show consistent active community mode — 5 commits over 2 days, 4 merges, 20 new PRs flowing. 72 open PRs, 33 stuck (down from 78 on Apr 16 = 58% ratio, healthy from 80%). First sustained improvement since Apr 12 crisis.**

## Key Points

- 72 open PRs as of Apr 18 (stable from Apr 17)
- 33 stuck PRs (>3d, no reviewer) — 46% of open PRs (down from 80% on Apr 16)
- Sole maintainer: [[contributors/garrytan]] — 5-day cycle complete: burnout (Apr 12) → self-merge (Apr 13-15) → silence (Apr 16) → **recovery sustained (Apr 17-18)**
- 15 total merges during Apr 4-18: 9 community PRs (Apr 4-11), 2 self-merges (Apr 13-14), 4 merges (Apr 17-18, mixed community + own)
- 4 versions released in 5 days: v0.16.4.0 (security wave, Apr 13), v0.17.0.0 (UX, Apr 14), v0.18.0.0 (Confusion Protocol, Apr 15), v1.0.0.0 (major, Apr 18)
- Apr 17-18: 20 new community PRs opened across 2 days (recovery from 0 on Apr 16)
- Apr 18: 3 commits ("remove hardcoded author emails", "gstack v1" release, "codex + Apple Silicon hardening v0.18.4.0")

## Health Trajectory (Apr 4-17)

| Date | Commits | PRs Opened | PRs Merged | Stuck PRs | Status |
|------|---------|------------|------------|-----------|--------|
| Apr 4 | 4 | 1 | 0 | ~10 | Baseline |
| Apr 5 | 11 | 5 | 0 | ~11 | Inflow rising |
| Apr 6 | 8 | 10 | 2 | ~12 | Merge catches up |
| Apr 7 | 2 | 17 | 2 | ~14 | Gap widens |
| Apr 8 | 3 | 22 | 3 | ~15 | Inflow peaks |
| Apr 9 | 1 | 16 | 1 | ~17 | Stuck accelerates |
| Apr 10 | 0 | 12 | 0 | ~19 | Zero commits |
| Apr 11 | 1 | 3 | 1 | 19 | Stabilized |
| Apr 12 | 0 | 3 | 0 | 27+ | **garrytan absent — burnout signal** |
| Apr 13 | 1 | 6 | 1 | ~19 | **garrytan returns — self-merge only** |
| Apr 14 | 1 | 11 | 1 | ~27 | Self-merge #1000; 11 new PRs |
| Apr 15 | 0 | 7 | 0 | ~36 | garrytan opens PR but no merge |
| Apr 16 | 0 | 0 | 0 | 39 | **Zero activity — community disengagement** |
| Apr 17 | 2 | 16 | 2 | 33 | RECOVERY: Active community mode; "community wave" merges; +16 PRs |
| **Apr 18** | **3** | **4** | **2** | **33** | **SUSTAINED: v1.0.0.0 release + hardening, healthy merge pace; stuck PRs declining** |

## Key Issues

- [#965](https://github.com/garrytan/gstack/issues/965) — codex/autoplan no auth gate (5d stuck)
- [#961](https://github.com/garrytan/gstack/issues/961) — hooks reference wrong env var; fix PR #968 ready (5d stuck)
- [#971](https://github.com/garrytan/gstack/issues/971) — codex exec stdin deadlock; fix PR #972 ready (4d stuck)
- [#997](https://github.com/garrytan/gstack/issues/997) — Apple Silicon compiled binary SIGKILL (1d)
- [#1006](https://github.com/garrytan/gstack/issues/1006) — headed Chrome auto-terminates (0d)

## Related

- [[contributors/garrytan]] — sole maintainer, self-merge pattern
- [[contributors/voidborne-d]] — expanded to gstack, 3 PRs stuck
- [[contributors/hybirdss]] — security contributor, old PRs batch-resolved
- [[patterns/review-bottleneck]] — community PRs unreviewed
- [[patterns/community-disengagement]] — Apr 16 zero activity
