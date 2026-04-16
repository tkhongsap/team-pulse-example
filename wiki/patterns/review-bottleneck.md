---
title: "Review Bottleneck"
tags: [pattern, critical, escalation]
sources:
  - "raw/github-daily/2026-04-04-am.md"
  - "raw/github-daily/2026-04-11-am.md"
  - "raw/github-daily/2026-04-12-am.md"
  - "raw/github-daily/2026-04-13-am.md"
  - "raw/github-daily/2026-04-14-am.md"
  - "raw/github-daily/2026-04-16-am.md"
created: 2026-04-11
updated: 2026-04-16
---

# Review Bottleneck

Both tracked repositories have a single-maintainer review bottleneck where PR inflow exceeds review throughput. **REVISED ASSESSMENT (Apr 13-16)**: garrytan returned to gstack but shifted to self-merge-only mode. The bottleneck is now behavioral, not availability-based. autoresearch remains at zero throughput (karpathy absent 21 days).

## Key Points

- **gstack**: [[contributors/garrytan]] returned Apr 13 but only merges self-authored PRs. Community PRs remain unreviewed. 39 stuck PRs.
- **autoresearch**: [[contributors/karpathy]] absent since Mar 26 (21 days). Zero PRs reviewed. 39 stuck PRs (98% of open).
- Combined: **78 stuck PRs** across both repos as of Apr 16 (80% of 98 total open)
- garrytan's post-return merges: #988 (self-authored batch of community fixes, 33m TTM) and #1000 (self-authored feature, 1.6h TTM) — both fast self-merges
- Security PRs: Hybirdss's 3 old PRs were bundled into garrytan's #988 rather than merged directly. New security PR #1002 still pending.
- **Zero community PRs directly merged** since Apr 11

## Evidence

| Repo | Stuck PRs (Apr 4) | Stuck PRs (Apr 12) | Stuck PRs (Apr 16) | Total Growth | Reviewers |
|------|-------------------|-------------------|-------------------|--------------|-----------|
| autoresearch | 21 | 39 | 39 | +86% | 0 active |
| gstack | 10 | 27 | 39 | +290% | 1 (self-merge only) |
| **Total** | **31** | **66** | **78** | **+152%** | **0 reviewing community PRs** |

## Bottleneck Type Shift

- **Apr 4-11**: Capacity bottleneck — garrytan merging 1-2 community PRs/day but inflow was 5-10/day
- **Apr 12**: Availability bottleneck — garrytan absent, zero throughput
- **Apr 13-16**: **Behavioral bottleneck** — garrytan active but only self-merging. Released v0.16.4.0, v0.17.0.0, v0.18.0.0 while 39 community PRs languished. This is worse than absence because it demonstrates active choice to skip community review.

## Impact

Per wt-project 4.2, "Stuck" = no movement for 3+ days. 78 stuck PRs far exceeds the 24-hour intervention SLA (wt-project section 6). Community contributors are beginning to disengage (Apr 16: zero new PRs).

## Related

- [[projects/gstack]] — 39 stuck, maintainer self-merging only
- [[projects/autoresearch]] — 39 stuck, maintainer absent
- [[patterns/stuck-items-growth]] — stuck count trajectory
- [[patterns/community-disengagement]] — consequence
- [[connections/sole-maintainer-and-stuck-growth]] — systemic analysis
