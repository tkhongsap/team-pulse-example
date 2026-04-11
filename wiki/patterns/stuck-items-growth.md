---
title: "Stuck Items Growth"
tags: [pattern, velocity]
sources:
  - "raw/github-daily/2026-04-04-am.md"
  - "raw/github-daily/2026-04-11-am.md"
created: 2026-04-11
updated: 2026-04-11
---

# Stuck Items Growth

Stuck PRs (open >3 days with no reviewer) grew 71% in one week, from 31 to 53 across both tracked repos. This is the most concerning velocity metric in the observation period.

## Key Points

- Stuck PRs: 31 (Apr 4) → 53 (Apr 11), a net increase of 22 in 8 days
- Stuck issues: stable at 2-3 (less concerning)
- autoresearch accounts for the majority: 21 → 34 (+62%), driven by zero review activity
- gstack grew from ~10 → 19 (+90%), despite garrytan actively merging 9 PRs
- The oldest stuck PR is [autoresearch#92](https://github.com/karpathy/autoresearch/pull/92) (AgentHub) by karpathy himself — 32 days

## Daily Trajectory

| Date | Total Stuck PRs | autoresearch | gstack |
|------|----------------|--------------|--------|
| Apr 4 | 31 | ~21 | ~10 |
| Apr 5 | 32 | ~21 | ~11 |
| Apr 6 | 34 | ~22 | ~12 |
| Apr 7 | 36 | ~22 | ~14 |
| Apr 8 | 36 | ~21 | ~15 |
| Apr 9 | 40 | ~23 | ~17 |
| Apr 10 | 45 | ~26 | ~19 |
| Apr 11 | 53 | 34 | 19 |

## Impact

Per wt-project section 6, the target is "Leads intervene within 24 hours of AI alert." With 53 items stuck, the system is far behind this target. The growth rate suggests the problem will worsen without intervention.

## Related

- [[patterns/review-bottleneck]] — root cause
- [[projects/autoresearch]] — 34 stuck (zero reviewers)
- [[projects/gstack]] — 19 stuck (one reviewer, insufficient throughput)
