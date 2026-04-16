---
title: "Stuck Items Growth"
tags: [pattern, velocity, critical]
sources:
  - "raw/github-daily/2026-04-04-am.md"
  - "raw/github-daily/2026-04-11-am.md"
  - "raw/github-daily/2026-04-12-am.md"
  - "raw/github-daily/2026-04-13-am.md"
  - "raw/github-daily/2026-04-14-am.md"
  - "raw/github-daily/2026-04-15-am.md"
  - "raw/github-daily/2026-04-16-am.md"
created: 2026-04-11
updated: 2026-04-16
---

# Stuck Items Growth

Stuck PRs (open >3 days with no reviewer) grew 152% in 13 days, from 31 (Apr 4) to 78 (Apr 16). Growth has reached near-saturation: 78 of 98 open PRs (80%) are now stuck. The rate is slowing only because the pool of non-stuck PRs is nearly exhausted.

## Key Points

- Stuck PRs: 31 (Apr 4) → 53 (Apr 11) → 66 (Apr 12) → 58 (Apr 13) → 78 (Apr 16)
- The Apr 13 dip (66→58) was due to garrytan's security wave batch merge + time-based threshold shifts, not systematic improvement
- autoresearch: 39 stuck of 40 open (98% saturation) — effectively every PR is stuck
- gstack: 39 stuck of 58 open (67%) — still receiving new PRs that haven't aged into stuck threshold
- Stuck issues also growing: 4 (Apr 12) → 11 (Apr 16)
- Oldest stuck PR: [autoresearch#92](https://github.com/karpathy/autoresearch/pull/92) (AgentHub) by karpathy — 37 days

## Daily Trajectory

| Date | Total Stuck PRs | autoresearch | gstack | Daily Change | Stuck % |
|------|----------------|--------------|--------|--------------|---------|
| Apr 4 | 31 | ~21 | ~10 | — | ~33% |
| Apr 5 | 32 | ~21 | ~11 | +1 | ~34% |
| Apr 6 | 34 | ~22 | ~12 | +2 | ~35% |
| Apr 7 | 36 | ~22 | ~14 | +2 | ~37% |
| Apr 8 | 36 | ~21 | ~15 | 0 | ~37% |
| Apr 9 | 40 | ~23 | ~17 | +4 | ~41% |
| Apr 10 | 45 | ~26 | ~19 | +5 | ~46% |
| Apr 11 | 53 | 34 | 19 | +8 | 57% |
| Apr 12 | 66 | 39 | 27 | **+13** | 66% |
| Apr 13 | 58 | 39 | ~19 | -8 | 59% |
| Apr 14 | 66 | 39 | ~27 | +8 | 67% |
| Apr 15 | 75 | 39 | ~36 | +9 | 77% |
| **Apr 16** | **78** | **39** | **39** | **+3** | **80%** |

## Resolutions

| Date | Item | Days Stuck | Resolved By |
|------|------|------------|-------------|
| Apr 13 | gstack#918 (CDPATH bin fix) | 5 | garrytan (bundled into #988 security wave) |
| Apr 13 | gstack#920 (path validation bypass) | 5 | garrytan (bundled into #988 security wave) |
| Apr 13 | gstack#921 (symlink bypass) | 5 | garrytan (bundled into #988 security wave) |

Average time-to-unstick: 5.0 days (3 items resolved, all via batch merge). Only 3 stuck items have been resolved in 13 days of observation. Per wt-project section 6, the target is 24-hour intervention — actual average is 5 days (5x the target).

## Impact

The system is approaching **terminal saturation**. With 80% of PRs stuck, the growth rate appears to slow (+3/day on Apr 16 vs +13/day on Apr 12), but this is a ceiling effect — there are only 20 non-stuck PRs left. Without intervention, the system will reach 100% stuck within days as new PRs age past the 3-day threshold.

## Related

- [[patterns/review-bottleneck]] — root cause
- [[patterns/community-disengagement]] — consequence of sustained stuck state
- [[projects/autoresearch]] — 98% stuck saturation
- [[projects/gstack]] — 67% stuck and growing
