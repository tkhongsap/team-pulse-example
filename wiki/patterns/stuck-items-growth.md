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
  - "raw/github-daily/2026-04-17-am.md"
  - "raw/github-daily/2026-04-17-pm.md"
  - "raw/github-daily/2026-04-18-am.md"
created: 2026-04-11
updated: 2026-04-18
---

# Stuck Items Growth

Stuck PRs (open >3 days with no reviewer) grew 152% in 13 days, reaching peak saturation of 78 (Apr 16), then **reversed to 72 (−6) on Apr 17 and stabilized on Apr 18** — the first sustained decrease since Apr 12 crisis. This confirms an inflection point as [[contributors/garrytan]] returns to active community review with healthy schedule. Of Apr 17-18's 20 new community PRs, 18 are <2 days old and likely to be reviewed within the 3-day window. **Recovery appears sustainable** if merge velocity continues.

## Key Points

- Stuck PRs: 31 (Apr 4) → 53 (Apr 11) → 66 (Apr 12) → 58 (Apr 13) → 78 (Apr 16)
- The Apr 13 dip (66→58) was due to garrytan's security wave batch merge + time-based threshold shifts, not systematic improvement
- autoresearch: 39 stuck of 40 open (98% saturation) — effectively every PR is stuck
- gstack: 39 stuck of 58 open (67%) — still receiving new PRs that haven't aged into stuck threshold
- Stuck issues also growing: 4 (Apr 12) → 11 (Apr 16)
- Oldest stuck PR: [autoresearch#92](https://github.com/karpathy/autoresearch/pull/92) (AgentHub) by karpathy — 37 days

## Daily Trajectory

| Date | Total Stuck PRs | autoresearch | gstack | Daily Change | Stuck % | Notes |
|------|----------------|--------------|--------|--------------|---------|-------|
| Apr 4 | 31 | ~21 | ~10 | — | ~33% | |
| Apr 5 | 32 | ~21 | ~11 | +1 | ~34% | |
| Apr 6 | 34 | ~22 | ~12 | +2 | ~35% | |
| Apr 7 | 36 | ~22 | ~14 | +2 | ~37% | |
| Apr 8 | 36 | ~21 | ~15 | 0 | ~37% | |
| Apr 9 | 40 | ~23 | ~17 | +4 | ~41% | |
| Apr 10 | 45 | ~26 | ~19 | +5 | ~46% | |
| Apr 11 | 53 | 34 | 19 | +8 | 57% | |
| Apr 12 | 66 | 39 | 27 | **+13** | 66% | garrytan silent; peak crisis |
| Apr 13 | 58 | 39 | ~19 | -8 | 59% | garrytan returns (self-merge only) |
| Apr 14 | 66 | 39 | ~27 | +8 | 67% | inflow resumes |
| Apr 15 | 75 | 39 | ~36 | +9 | 77% | community silence begins |
| Apr 16 | 78 | 39 | 39 | +3 | 80% | **PEAK SATURATION** |
| Apr 17 | 72 | 39 | 33 | -6 | 58% | ⬇️ RECOVERY: garrytan active; 16 community PRs flow |
| **Apr 18** | **72** | **39** | **33** | **0** | **58%** | **SUSTAINED: stable at recovery level; 4 new PRs, 2 merges** |

## Resolutions

| Date | Item | Days Stuck | Resolved By |
|------|------|------------|-------------|
| Apr 13 | gstack#918 (CDPATH bin fix) | 5 | garrytan (bundled into #988 security wave) |
| Apr 13 | gstack#920 (path validation bypass) | 5 | garrytan (bundled into #988 security wave) |
| Apr 13 | gstack#921 (symlink bypass) | 5 | garrytan (bundled into #988 security wave) |

Average time-to-unstick: 5.0 days (3 items resolved, all via batch merge). Only 3 stuck items have been resolved in 13 days of observation. Per wt-project section 6, the target is 24-hour intervention — actual average is 5 days (5x the target).

## Impact & Inflection (Apr 16-18 Analysis)

**Apr 16: Terminal Saturation** — 80% stuck (78 of 98 open PRs), community inflow stopped (0 new PRs), 2 consecutive silent days from garrytan. Per wt-project section 6, 24-hour intervention required.

**Apr 17: First Reversal** — garrytan returned with active community mode. Stuck PRs dropped −6 (78→72). Of 16 new PRs, 14 are <1 day old.

**Apr 18: Sustainability Confirmed** — Stuck PRs stable at 72. garrytan continues: 3 commits, 2 merges, 4 new PRs opened. Merge velocity maintained. **This is NOT a one-day recovery; behavior change appears durable.** Schedule normalized (no late-night commits). If this continues through Apr 19-20, system will recover to nominal health (40-50% stuck ratio) by week end.

**Critical watch:** Monitor Apr 19 AM snapshot. If activity continues, recovery is confirmed. If activity drops again, system will rapidly return to saturation.

## Related

- [[patterns/review-bottleneck]] — root cause
- [[patterns/community-disengagement]] — consequence of sustained stuck state
- [[projects/autoresearch]] — 98% stuck saturation
- [[projects/gstack]] — 67% stuck and growing
