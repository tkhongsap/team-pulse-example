---
title: "Burnout Signals"
tags: [pattern, wellbeing, critical]
sources:
  - "raw/github-daily/2026-04-04-am.md"
  - "raw/github-daily/2026-04-05-am.md"
  - "raw/github-daily/2026-04-06-am.md"
  - "raw/github-daily/2026-04-07-am.md"
  - "raw/github-daily/2026-04-11-am.md"
created: 2026-04-11
updated: 2026-04-11
---

# Burnout Signals

Late-night commit patterns and sole-maintainer workload indicate burnout risk for key contributors, per wt-project 4.3 (Burnout Detection and Workload Balancing).

## Key Points

- [[contributors/garrytan]] had **10+ late-night commits** (22:00-06:00 UTC) across 5 of 8 observation days
- Late-night pattern: Apr 4 (2), Apr 5 (4), Apr 6 (2), Apr 7 (1), Apr 11 (1)
- Apr 11: committed at 03:13 UTC — a v0.16.3.0 refactor, suggesting deep work at night
- garrytan is sole maintainer handling 54 open PRs with zero other reviewers — unsustainable load
- No other contributors show late-night patterns

## Burnout Risk Assessment

| Contributor | Late-Night Commits | Solo Workload | Days Active | Risk Level |
|-------------|-------------------|---------------|-------------|------------|
| garrytan | 10+ across 5 days | 54 open PRs, sole reviewer | 7/8 | **High** |
| karpathy | 0 | Inactive (different concern) | 0/8 | N/A |
| All others | 1 (Jared Friedman, Apr 8) | No review burden | 1-3 days | Low |

## Recommended Actions (per wt-project 4.3)

- Flag garrytan's workload to team lead for intervention
- Consider deputizing trusted contributors (e.g., [[contributors/damin-lee]]) for triage authority
- Separate security PRs ([[contributors/hybirdss]]) into a priority review lane

## Related

- [[contributors/garrytan]] — primary burnout risk
- [[patterns/review-bottleneck]] — root cause of unsustainable workload
- [[connections/sole-maintainer-and-stuck-growth]] — systemic issue
