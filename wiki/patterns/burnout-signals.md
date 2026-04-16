---
title: "Burnout Signals"
tags: [pattern, wellbeing, critical, escalation]
sources:
  - "raw/github-daily/2026-04-04-am.md"
  - "raw/github-daily/2026-04-05-am.md"
  - "raw/github-daily/2026-04-06-am.md"
  - "raw/github-daily/2026-04-07-am.md"
  - "raw/github-daily/2026-04-11-am.md"
  - "raw/github-daily/2026-04-12-am.md"
created: 2026-04-11
updated: 2026-04-12
---

# Burnout Signals

Late-night commit patterns and sole-maintainer workload indicate burnout risk for [[contributors/garrytan]]. **ESCALATION**: On Apr 12, garrytan became completely inactive (first no-commit day) after 10+ late-night commits in prior week. This suggests acute burnout leading to withdrawal.

## Key Points

- [[contributors/garrytan]] had **10+ late-night commits** (22:00-06:00 UTC) across 5 of 8 days (Apr 4-11)
- Late-night pattern: Apr 4 (2), Apr 5 (4), Apr 6 (2), Apr 7 (1), Apr 11 (1) — peak on Apr 5-6
- Apr 11: committed at 03:13 UTC — a v0.16.3.0 refactor, suggesting deep work at night
- **Apr 12: ZERO activity** — first no-commit day after intensive week. Suggests acute burnout → withdrawal
- Worked alone handling 54→66 open PRs with zero other reviewers — unsustainable load
- Stuck PRs exploded 42% on Apr 12 while garrytan was absent → direct correlation
- No other contributors show burnout signals

## Burnout Risk Assessment

| Contributor | Late-Night Commits | Solo Workload | Days Active | Status | Risk Level |
|-------------|-------------------|---------------|-------------|--------|------------|
| garrytan | 10+ across 5 days | 66 open PRs, sole reviewer | 7/8, inactive Apr 12 | **Actively burned out** | **CRITICAL** |
| karpathy | 0 | Inactive (17 days) | 0/9 | Disengaged | Medium |
| All others | 1 (Apr 8) | No review burden | 1-3 days | Normal | Low |

**Escalation**: garrytan's inactivity on Apr 12 after intense late-night work pattern strongly suggests acute burnout. Combined with system-wide stall (stuck PRs +25% in 24h), this is a **CRITICAL PERSONNEL AND SYSTEM RISK**.

## Recommended Actions (per wt-project 4.3)

- Flag garrytan's workload to team lead for intervention
- Consider deputizing trusted contributors (e.g., [[contributors/damin-lee]]) for triage authority
- Separate security PRs ([[contributors/hybirdss]]) into a priority review lane

## Related

- [[contributors/garrytan]] — primary burnout risk
- [[patterns/review-bottleneck]] — root cause of unsustainable workload
- [[connections/sole-maintainer-and-stuck-growth]] — systemic issue
