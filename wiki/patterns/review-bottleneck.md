---
title: "Review Bottleneck"
tags: [pattern, critical]
sources:
  - "raw/github-daily/2026-04-04-am.md"
  - "raw/github-daily/2026-04-11-am.md"
created: 2026-04-11
updated: 2026-04-11
---

# Review Bottleneck

Both tracked repositories have a single-maintainer review bottleneck where PR inflow consistently exceeds review throughput, causing stuck items to accumulate daily.

## Key Points

- **gstack**: [[contributors/garrytan]] is the sole reviewer for 54 open PRs. Merged 9 PRs in 8 days while 40+ new PRs arrived. Net: stuck PRs grew from ~10 to 19.
- **autoresearch**: [[contributors/karpathy]] is the sole reviewer and has been inactive since Mar 26. Zero PRs reviewed. Stuck PRs grew from 21 to 34.
- Combined: **53 stuck PRs** across both repos as of Apr 11 (57% of all open PRs)
- Security PRs ([[contributors/hybirdss]]) treated the same as feature PRs — no priority lane
- Community contributors like [[contributors/voidborne-d]] and [[contributors/damin-lee]] are actively contributing but blocked

## Evidence

| Repo | Stuck PRs (Apr 4) | Stuck PRs (Apr 11) | Growth | Reviewers |
|------|-------------------|-------------------|--------|-----------|
| autoresearch | 21 | 34 | +62% | 0 active |
| gstack | 10 | 19 | +90% | 1 (garrytan) |
| **Total** | **31** | **53** | **+71%** | **1 active** |

## Impact

Per wt-project 4.2, "Stuck" is defined as "no movement for 3+ days." 53 stuck PRs exceeds the 24-hour intervention target (wt-project section 6). If this were an internal team, this would require immediate resource reallocation.

## Related

- [[projects/gstack]] — 19 stuck PRs, sole maintainer
- [[projects/autoresearch]] — 34 stuck PRs, inactive maintainer
- [[patterns/stuck-items-growth]] — stuck count trajectory
- [[connections/sole-maintainer-and-stuck-growth]] — root cause analysis
