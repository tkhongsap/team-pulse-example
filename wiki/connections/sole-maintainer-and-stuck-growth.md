---
title: "Connection: Sole Maintainer and Stuck Growth"
tags: [connection]
connects:
  - "patterns/review-bottleneck"
  - "patterns/stuck-items-growth"
  - "patterns/burnout-signals"
sources:
  - "raw/github-daily/2026-04-04-am.md"
  - "raw/github-daily/2026-04-11-am.md"
created: 2026-04-11
updated: 2026-04-11
---

# Connection: Sole Maintainer and Stuck Growth

## The Connection

The single-maintainer model in both repos creates a reinforcing cycle: as community activity grows, the sole reviewer can't keep up, stuck items accumulate, and the maintainer works longer hours to compensate — increasing burnout risk, which eventually reduces throughput further.

## Key Insight

This is not a contributor problem — it's a structural problem. Both repos have active communities submitting quality PRs. The bottleneck is review capacity, not contribution quality. gstack has garrytan working late nights to keep up and still falling behind. autoresearch has karpathy absent entirely, creating a complete blockage.

The data shows the cycle clearly:
1. Community submits ~15 PRs/day across both repos
2. garrytan merges ~1/day; karpathy merges 0
3. Net: ~14 PRs/day join the stuck backlog
4. garrytan compensates with late-night work (10+ after-hours commits in 8 days)
5. Despite effort, stuck items grew 71% (31 → 53)

## Evidence

- gstack: 9 merges in 8 days vs 54 open PRs = 6:1 backlog ratio
- autoresearch: 0 merges vs 39 open PRs = infinite backlog ratio
- garrytan late-night commits: 5 of 8 days
- Stuck growth: linear, ~3 new stuck items per day

## Recommended Structural Fix

Per wt-project 4.3, this requires management intervention:
- Add co-maintainers with merge access (not just reviewers)
- Create triage labels to batch similar PRs (e.g., "add fork to notable forks")
- Establish a security priority lane for PRs like [[contributors/hybirdss]]'s fixes

## Related

- [[patterns/review-bottleneck]] — the throughput gap
- [[patterns/stuck-items-growth]] — the accumulation effect
- [[patterns/burnout-signals]] — the human cost
- [[contributors/garrytan]] — overloaded maintainer
- [[contributors/karpathy]] — absent maintainer
