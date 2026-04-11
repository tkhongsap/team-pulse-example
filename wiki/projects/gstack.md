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
updated: 2026-04-11
---

# gstack

Repository: [garrytan/gstack](https://github.com/garrytan/gstack). TypeScript-based AI agent toolkit with 69K+ stars and 9.7K forks. High community engagement with a sole maintainer bottleneck.

## Key Points

- 54 open PRs as of Apr 11, growing steadily throughout the week
- Sole maintainer: [[contributors/garrytan]] — only person merging PRs or pushing to default branch
- 19 stuck PRs (>3d, no reviewer) as of Apr 11, up from ~10 at start of week
- 9 PRs merged during Apr 4-11, all by garrytan
- Active community: 108+ unique PR authors during the observation period
- Major areas of contribution: browse module fixes, host support, skill additions, security patches

## Health Trajectory (Apr 4-11)

| Date | Commits | PRs Opened | PRs Merged | Stuck PRs |
|------|---------|------------|------------|-----------|
| Apr 4 | 4 | 1 | 0 | ~10 |
| Apr 5 | 11 | 5 | 0 | ~11 |
| Apr 6 | 8 | 10 | 2 | ~12 |
| Apr 7 | 2 | 17 | 2 | ~14 |
| Apr 8 | 3 | 22 | 3 | ~15 |
| Apr 9 | 1 | 16 | 1 | ~17 |
| Apr 10 | 0 | 12 | 0 | ~19 |
| Apr 11 | 1 | 3 | 1 | 19 |

PR inflow consistently exceeds merge throughput. The gap widens each day.

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
