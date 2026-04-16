---
title: "Community Disengagement"
tags: [pattern, critical, new]
sources:
  - "raw/github-daily/2026-04-12-pm.md"
  - "raw/github-daily/2026-04-13-am.md"
  - "raw/github-daily/2026-04-14-am.md"
  - "raw/github-daily/2026-04-15-am.md"
  - "raw/github-daily/2026-04-16-am.md"
created: 2026-04-16
updated: 2026-04-16
---

# Community Disengagement

Community contribution activity is declining and reached zero on Apr 16 — the first day with no new PRs, commits, or issues across both repos. This is the predictable end-stage of sustained review unresponsiveness (see [[patterns/review-bottleneck]]).

## Key Points

- **Apr 16: Zero activity** — no PRs opened, no commits, no issues. First time in the 13-day observation period.
- PR inflow declined steadily: 22 (Apr 8) → 3 (Apr 12) → 6 (Apr 13) → 11 (Apr 14) → 8 (Apr 15) → **0 (Apr 16)**
- autoresearch community inflow: dried up first (0 new PRs since Apr 15; last was #516 by marketswitch)
- gstack community inflow: followed — 7 new PRs on Apr 15, then 0 on Apr 16
- Despite garrytan releasing 3 new versions (v0.16.4.0, v0.17.0.0, v0.18.0.0) during Apr 13-15, community response was declining, not increasing
- 90 unique contributors have open PRs across both repos — all in "Backlog" status with zero feedback

## Community PR Inflow Trajectory

| Date | New PRs (autoresearch) | New PRs (gstack) | Total | Merged |
|------|----------------------|-----------------|-------|--------|
| Apr 8 | 3 | 19 | 22 | 3 |
| Apr 9 | 1 | 15 | 16 | 1 |
| Apr 10 | 1 | 11 | 12 | 0 |
| Apr 11 | 0 | 3 | 3 | 1 |
| Apr 12 | 2 | 3 | 5 | 0 |
| Apr 13 | 0 | 6 | 6 | 1 (self) |
| Apr 14 | 0 | 11 | 11 | 1 (self) |
| Apr 15 | 1 | 7 | 8 | 0 |
| **Apr 16** | **0** | **0** | **0** | **0** |

## Why This Matters

Community contributions are the primary value driver for both repos (70K+ and 69K+ stars respectively). When contributors stop submitting PRs, the repos lose:
- Bug fixes and security patches from real-world users
- Feature diversity from community perspectives
- Translation and documentation improvements
- Fork visibility and ecosystem growth

Per wt-project section 6, employee wellbeing includes monitoring for disengagement. While these are external contributors, the same signal applies: **when productive people stop contributing, the system has failed them**.

## Recovery Difficulty

Community trust is harder to rebuild than to maintain. Contributors who submitted PRs 10-20 days ago with zero feedback are unlikely to return quickly even if the review bottleneck is resolved. Expected recovery timeline: 2-4 weeks of consistent review responsiveness to restore submission rates to Apr 8 levels.

## Related

- [[patterns/review-bottleneck]] — root cause (zero community PR reviews)
- [[patterns/stuck-items-growth]] — 80% stuck rate drives disengagement
- [[connections/sole-maintainer-and-stuck-growth]] — structural failure chain
- [[contributors/voidborne-d]] — highest-output contributor, 6 PRs stuck
