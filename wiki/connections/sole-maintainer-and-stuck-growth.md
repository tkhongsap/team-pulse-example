---
title: "Connection: Sole Maintainer, Burnout, and System Collapse"
tags: [connection, critical]
connects:
  - "patterns/review-bottleneck"
  - "patterns/stuck-items-growth"
  - "patterns/burnout-signals"
sources:
  - "raw/github-daily/2026-04-04-am.md"
  - "raw/github-daily/2026-04-11-am.md"
  - "raw/github-daily/2026-04-12-am.md"
created: 2026-04-11
updated: 2026-04-12
---

# Connection: Sole Maintainer, Burnout, and System Collapse

## The Connection

The single-maintainer model in both repos creates a reinforcing cycle that has now reached critical breaking point: sole reviewer overloaded → works late nights → stuck items accumulate → burnout intensifies → maintainer becomes inactive → system completely stalls. **This cycle completed in 9 days (Apr 4-12).**

## Key Insight: System Collapse Timeline

This is a **structural system failure**, not a contributor problem. Both repos have active communities submitting quality PRs. The bottleneck was review capacity (garrytan) — not contribution quality. The system hit its breaking point on Apr 12.

**The cycle:**
1. **Apr 4-7**: Community submits ~15-20 PRs/day. garrytan merges ~2/day, works normal hours. Stuck items grow slowly (~2-3/day).
2. **Apr 8-11**: Inflow peaks (~20+ PRs/day). garrytan increases late-night work (10+ after-hours commits in 5 days). Merges stall (1/day). Stuck items accelerate (~4-5/day).
3. **Apr 11 midnight**: garrytan completes last merge + refactor commit (03:13 UTC). System at 53 stuck PRs (57% of total).
4. **Apr 12**: garrytan goes completely inactive. Zero commits, zero reviews. Without him, autoresearch has zero reviewers. gstack has zero active reviewers. Community continues submitting PRs (3 new ones), but none can be reviewed or merged.
5. **Result**: Stuck PRs spike 25% in 24 hours (53 → 66). System functionally stalled.

## Evidence

**Apr 4-11 Period:**
- gstack: 9 merges in 8 days vs 54 open PRs = 6:1 backlog ratio
- autoresearch: 0 merges vs 39 open PRs = infinite backlog ratio
- garrytan late-night commits: 5 of 8 days (10+ commits)
- Stuck growth: accelerating, 2-5 new stuck items per day, totaling +22 in 8 days

**Apr 12 (Critical Day):**
- System-wide merges: **0** (garrytan inactive)
- New PRs opened: 3 (all unreviewed)
- Stuck PR spike: +13 in 24 hours (+25%)
- Stuck ratio: 66 / 100 = 66% of all open PRs now stuck

**Single Point of Failure Impact:**
- Apr 11: With garrytan active, stuck PRs = 53 (57% of 93 total)
- Apr 12: Without garrytan, stuck PRs = 66 (66% of 100 total) — 9 percentage point increase in one day

## Urgent: Intervention Required Within 24 Hours

Per wt-project 4.3 and section 6 (24-hour intervention SLA), this has crossed into **CRITICAL** territory.

**Immediate actions:**
1. **Get garrytan status**: Confirm he's okay (burnout concern). If unavailable >24 hours, escalate to management.
2. **Emergency triage**: Fast-track the ~35 "add fork to notable forks" PRs in autoresearch (auto-mergeable?). This alone could clear ~10-15 stuck items.
3. **Temporary deputies**: Grant merge access to trusted contributors:
   - [[contributors/damin-lee]] for gstack (has 4 quality PRs; proven competent)
   - [[contributors/voidborne-d]] for autoresearch (has 3 quality tokenizer fixes; blocked by same person)
4. **Security priority lane**: [[contributors/hybirdss]] has 3 security fixes in stuck queue — review these first.
5. **Auto-merge for docs**: Chinese translation and README updates should not require deep review.

**Long-term structural fix** (after emergency is over):
- Add 2-3 co-maintainers with full merge access
- Establish triage bot for low-risk PRs (translations, fork additions, docs)
- Set review SLA: triage within 24h, merge within 5 days for non-blocked items

## Related

- [[patterns/review-bottleneck]] — the throughput gap
- [[patterns/stuck-items-growth]] — the accumulation effect
- [[patterns/burnout-signals]] — the human cost
- [[contributors/garrytan]] — overloaded maintainer
- [[contributors/karpathy]] — absent maintainer
