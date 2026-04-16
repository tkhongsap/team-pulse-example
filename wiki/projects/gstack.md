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
created: 2026-04-11
updated: 2026-04-12
---

# gstack

Repository: [garrytan/gstack](https://github.com/garrytan/gstack). TypeScript-based AI agent toolkit with 69K+ stars and 9.7K forks. High community engagement with a sole maintainer bottleneck. **ESCALATING: 66 open PRs (Apr 12), 27+ stuck, zero merges in 24 hours.**

## Key Points

- 66 open PRs as of Apr 12 (up from 54 on Apr 11) — inflow accelerating
- Sole maintainer: [[contributors/garrytan]] — only person merging PRs; **inactive on Apr 12**
- 27+ stuck PRs (>3d, no reviewer) as of Apr 12, up from 19 on Apr 11 (+42% in 24h)
- 9 PRs merged during Apr 4-11, all by garrytan; **zero merges Apr 11-12**
- 3 new PRs opened Apr 12 (xogjs #981, guos88065-tech #979, others)
- Active community: 100+ unique PR authors (growing)
- Major areas: browse module fixes, host support, skill additions, security patches

## Health Trajectory (Apr 4-12)

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
| Apr 12 | 0 | 3 | 0 | 27+ | **CRITICAL: inactivity + stuck spike** |

PR inflow consistently exceeds merge throughput. Gap has widened significantly.

## Key Issues

- [#965](https://github.com/garrytan/gstack/issues/965) — codex/autoplan shell out with no auth gate
- [#961](https://github.com/garrytan/gstack/issues/961) — hooks reference wrong env variable (fix PR [#968](https://github.com/garrytan/gstack/pull/968) ready)
- [#949](https://github.com/garrytan/gstack/issues/949) — /ship command too expensive
- [#943](https://github.com/garrytan/gstack/issues/943) — watchdog kills browse server mid-workflow

## Related

- [[contributors/garrytan]] — sole maintainer
- [[contributors/damin-lee]] — consistent contributor
- [[contributors/hybirdss]] — security contributor
- [[contributors/ignsm]] — docs contributor
- [[patterns/review-bottleneck]] — PR review throughput < inflow
- [[patterns/stuck-items-growth]] — stuck count growing daily
