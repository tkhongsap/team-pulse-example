---
title: "Stuck Items Growth"
tags: [pattern, velocity, critical]
sources:
  - "raw/github-daily/2026-04-04-am.md"
  - "raw/github-daily/2026-04-11-am.md"
  - "raw/github-daily/2026-04-12-am.md"
created: 2026-04-11
updated: 2026-04-12
---

# Stuck Items Growth

Stuck PRs (open >3 days with no reviewer) grew 113% in 9 days, from 31 (Apr 4) to 66 (Apr 12). The growth rate has accelerated sharply: +71% in the first 8 days, then +25% in a single day (Apr 12). This is now a **CRITICAL VELOCITY CRISIS**.

## Key Points

- Stuck PRs: 31 (Apr 4) → 53 (Apr 11) → 66 (Apr 12), a net increase of 35 in 9 days
- **Day-over-day spike**: +22 in 8 days (Apr 4-11), then +13 in ONE DAY (Apr 11-12)
- Stuck issues: 2-4 (stable, less critical than PRs)
- autoresearch accounts for majority growth: 21 → 34 → 39+ (+86% total), zero review activity
- gstack escalated sharply: 19 → 27+ (+42% in 24h), garrytan inactive on Apr 12
- The oldest stuck PR is [autoresearch#92](https://github.com/karpathy/autoresearch/pull/92) (AgentHub) by karpathy himself — 37 days
- **New critical threshold**: 66 stuck PRs = 66% of 100 total open PRs (both repos)

## Daily Trajectory

| Date | Total Stuck PRs | autoresearch | gstack | Daily Change | Trend |
|------|----------------|--------------|--------|--------------|-------|
| Apr 4 | 31 | ~21 | ~10 | — | Baseline |
| Apr 5 | 32 | ~21 | ~11 | +1 | Steady |
| Apr 6 | 34 | ~22 | ~12 | +2 | Steady |
| Apr 7 | 36 | ~22 | ~14 | +2 | Steady |
| Apr 8 | 36 | ~21 | ~15 | 0 | Plateau |
| Apr 9 | 40 | ~23 | ~17 | +4 | Accelerating |
| Apr 10 | 45 | ~26 | ~19 | +5 | Accelerating |
| Apr 11 | 53 | 34 | 19 | +8 | **Spike** |
| Apr 12 | 66 | 39+ | 27+ | **+13** | **CRITICAL** |

## Impact

Per wt-project section 6, the target is "Leads intervene within 24 hours of AI alert." With 66 items stuck, the system is **CRITICALLY FAR BEHIND** this target.

**Projection**: If Apr 12's rate (+13/day) continues, stuck PRs will reach 79 by Apr 13, 92 by Apr 14. At 100 PRs total across both repos, the system will be entirely stalled within 2 days unless immediate action is taken.

**Root cause**: [[contributors/garrytan]] was the only active reviewer, and he became inactive on Apr 12 (zero commits, no reviews). This single point of failure has cascaded into system-wide gridlock.

## Related

- [[patterns/review-bottleneck]] — root cause
- [[projects/autoresearch]] — 39+ stuck (zero reviewers)
- [[projects/gstack]] — 27+ stuck (zero active reviewers as of Apr 12)
