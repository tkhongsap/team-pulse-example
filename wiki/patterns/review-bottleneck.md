---
title: "Review Bottleneck"
tags: [pattern, critical, escalation]
sources:
  - "raw/github-daily/2026-04-04-am.md"
  - "raw/github-daily/2026-04-11-am.md"
  - "raw/github-daily/2026-04-12-am.md"
created: 2026-04-11
updated: 2026-04-12
---

# Review Bottleneck

Both tracked repositories have a single-maintainer review bottleneck where PR inflow consistently exceeds review throughput, causing stuck items to accumulate daily. **ESCALATION**: The sole active reviewer (garrytan) became inactive on Apr 12, triggering a system-wide stall.

## Key Points

- **gstack**: [[contributors/garrytan]] was sole reviewer for 54+ open PRs. Merged 9 PRs in 8 days while 50+ new PRs arrived. **Became inactive on Apr 12 → stuck PRs spiked 42% in 24h (19→27+).**
- **autoresearch**: [[contributors/karpathy]] is sole reviewer and inactive since Mar 26 (17 days). Zero PRs reviewed. Stuck PRs grew from 21 to 34 to 39+ in 8 days.
- Combined: **66 stuck PRs** across both repos as of Apr 12 (66% of 100 total open PRs) — system is 2/3 stalled
- Security PRs ([[contributors/hybirdss]]) treated same as feature PRs — no priority lane
- Community contributors ([[contributors/voidborne-d]], [[contributors/damin-lee]]) actively contributing but blocked
- **CRITICAL**: Only 1 reviewer total (garrytan) was active, and he's now inactive. Zero backup capacity.

## Evidence

| Repo | Stuck PRs (Apr 4) | Stuck PRs (Apr 11) | Stuck PRs (Apr 12) | Total Growth | Reviewers |
|------|-------------------|-------------------|-------------------|--------------|-----------|
| autoresearch | 21 | 34 | 39+ | +86% | 0 active |
| gstack | 10 | 19 | 27+ | +170% | 1 (inactive as of Apr 12) |
| **Total** | **31** | **53** | **66+** | **+113%** | **0 active** |

**Status change**: As of Apr 12, garrytan became inactive (zero commits, zero reviews). The single active reviewer is now inactive, leaving two repos with zero active reviewers.

## Impact

Per wt-project 4.2, "Stuck" is defined as "no movement for 3+ days." 53 stuck PRs exceeds the 24-hour intervention target (wt-project section 6). If this were an internal team, this would require immediate resource reallocation.

## Related

- [[projects/gstack]] — 19 stuck PRs, sole maintainer
- [[projects/autoresearch]] — 34 stuck PRs, inactive maintainer
- [[patterns/stuck-items-growth]] — stuck count trajectory
- [[connections/sole-maintainer-and-stuck-growth]] — root cause analysis
