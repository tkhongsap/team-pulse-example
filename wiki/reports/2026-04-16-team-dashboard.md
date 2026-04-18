---
title: "Team Dashboard — 2026-04-16"
tags: [report, dashboard]
sources:
  - "raw/github-daily/2026-04-16-am.md"
  - "raw/github-daily/2026-04-16-pm.md"
  - "raw/github-daily/2026-04-15-am.md"
  - "raw/github-daily/2026-04-12-am.md"
  - "raw/github-daily/2026-04-04-am.md"
created: 2026-04-16
updated: 2026-04-16
---

# Team Dashboard — 2026-04-16

> **Purpose**: Management overview for team leads (wt-project 4.4)
> **Data**: Daily snapshots from raw/github-daily/ (13-day observation, Apr 4–16)
> **Status**: 🔴 CRITICAL — System at terminal saturation. Immediate intervention required.

---

## TEAM HEALTH SCORE: 1.5 / 10

### Factor Breakdown

| Factor | Score | Trend | Alert |
|--------|-------|-------|-------|
| **Velocity** | 0/10 | ↓ Critical | 0 commits, 0 merges (48h running) |
| **Stuck Ratio** | 0.5/10 | ↓ Critical | 78 of 98 PRs (80%) stuck >3d, no reviewer |
| **Workload Balance** | 1/10 | ↓ Critical | 100% of contributors in backlog; 90 awaiting review |
| **Review Responsiveness** | 0/10 | ↓ Critical | Zero active reviewers; avg 5-day wait (target 24h) |
| **Burnout Risk** | 1/10 | ↓ Critical | Maintainers degraded/absent; community disengaging |

**Overall**: The system has progressed from "emerging crisis" (Apr 12) to "terminal state" (Apr 16). The 3-day grace period for intervention (Apr 12-15) was exhausted. Structural recovery is now required.

---

## STATUS DISTRIBUTION

### Per wt-project 4.2 Categorization

| Status | Count | Contributors | Trend |
|--------|-------|---------------|-------|
| **Backlog** | 90 | All contributors with open PRs | ↑ +8 from Apr 12 |
| **In Progress** | 0 | (No activity for 48h) | ↓ None |
| **Stuck** | 98 | (Entire PR queue) | ↑ 78 PRs (80%) exceeded 3d threshold |
| **Ready to Hand Off** | 0 | (No completions in 48h) | ↓ None |

**Interpretation**: The entire system is frozen. No contributors have received feedback, merges, or progress signals in 5+ days. All 90 contributors are classified as "Backlog" despite submitting PRs ranging from 1 to 37 days ago.

---

## WHO NEEDS HELP (Immediate Interventions)

### 🔴 CRITICAL — Maintainer Status

| Role | Name | Status | Evidence | Action |
|------|------|--------|----------|--------|
| **autoresearch Maintainer** | karpathy | **Absent 21 days** | Zero commits/reviews since Mar 26. 40 open PRs, 39 stuck (98%). | Escalate to VP Eng. Establish interim maintainer or co-maintainer. |
| **gstack Maintainer** | garrytan | **Burnout → Degraded Mode** | Inactive Apr 10-12 (3 days), returned Apr 13 but ONLY self-merges (3 versions in 3d, zero community reviews). Zero activity Apr 16. | Manager check-in immediately. Remove community review expectations; focus on well-being. Grant emergency merge access to deputies. |

### 🔴 CRITICAL — Community Reviewers (Blocked)

| Contributor | PRs Stuck | Reason | Action |
|---|---|---|---|
| **voidborne-d** | 6 (most of any) | No reviewer assigned. Proven quality (tokenizer, build fixes). Capable of code review. | **Elevate to reviewer/deputy. Unblock their 6 PRs first.** |
| **TrueCrimeDev** | 1 (Codex workflow) | No reviewer. Deep repo knowledge demonstrated. | **Elevate to reviewer for autoresearch.** |
| **Damin-Lee** | 5 (YAML, tests, skills) | No reviewer. Consistent contributor. | **Elevate to deputy for gstack.** |
| **LewisJEllis** | 1 (landing page, 6d) | No reviewer. Established contributor. | **Elevate to deputy for gstack.** |

### 🟠 HIGH PRIORITY — Security & Fixes

| Issue | PR | Age | Status | Action |
|---|---|---|---|---|
| Security: codex/autoplan no auth gate | gstack#965 | 5d | Open issue. No PR yet. | **Design decision required from lead.** |
| **Security: enforce auth policy (tunnel)** | gstack#1002 | 1d | **Security fix. Highest priority.** | **Review and merge today.** |
| **Security: remove unsafe exec()** | autoresearch#506 | 6d | **Security fix. Stuck 6d.** | **Review and merge today.** |

### 🟠 HIGH PRIORITY — Quick Wins (Batch-Mergeable)

~15-20 low-risk PRs can clear 78→55 stuck range. Examples:

- Fork additions to Notable Forks (autoresearch: 8-10 PRs, 10-24d old)
- Language translations (zh-CN, Chinese: 2-3 PRs, 5-24d old)
- README / docs updates (gstack/autoresearch: 3-4 PRs, 1-5d old)
- Bug fixes: tokenizer, build tools, CLI (autoresearch: 4-5 PRs, 8-24d old)

**Action**: Grant merge access to 1-2 deputies today. Batch-merge this set by EOD to signal system recovery.

### 🟡 MEDIUM PRIORITY — Idle Contributors (No Action This Week)

**Status**: All 90 contributors are effectively idle — they've submitted work but received zero feedback. No triage action needed; system-level unblocking (reviewer access) solves this.

---

## KEY METRICS

### Today vs 7-Day Average

| Metric | Today | 7-Day Avg | Change | Target |
|--------|-------|-----------|--------|--------|
| **Commits** | 0 | 3 | ↓ -100% | 5+ |
| **PRs Merged** | 0 | 0.4 | ↓ -100% | 3+ |
| **PRs Opened** | 0 | 7 | ↓ -100% | 8+ |
| **Stuck PRs** | 78 | 68 | ↑ +14% | <15 |
| **Avg Days Stuck** | 8.7 | 7.2 | ↑ +20% | <1 |
| **Review Turnaround** | ∞ | 5+ days | ↑ Worse | <24h |
| **Community Activity** | 0 | 6 PRs/day | ↓ -100% | 10+ PRs/day |

**Interpretation**: All velocity metrics are in freefall. The 7-day average masks the severity — Apr 4-10 had positive activity that skews the average. Apr 12-16 (last 5 days) have been near-zero with sustained stuck growth.

---

## WEEK-OVER-WEEK TRENDS

### Stuck PR Growth (13-day trajectory)

| Period | Apr 4 | Apr 11 | Apr 12 | Apr 13 | Apr 14 | Apr 15 | **Apr 16** | Growth |
|--------|-------|--------|--------|--------|--------|--------|-----------|--------|
| **Stuck Count** | 31 | 53 | 66 | 58 | 66 | 75 | **78** | **+152% in 13d** |
| **Stuck %** | 33% | 57% | 66% | 59% | 67% | 77% | **80%** | **+47 ppts** |
| **Daily Change** | — | +22 | **+13** | -8 | +8 | +9 | **+3** | Slowing (ceiling effect) |

**Pattern**: Explosive growth Apr 10-12 (+22/day) is slowing (+3/day Apr 16) **not because of resolution, but because the pool of non-stuck PRs is nearly exhausted**. With only 20 PRs left to age into stuck status, the system will reach 100% within 7 days.

### Community Engagement (5-day decline)

| Date | New PRs | Merges | Community Signal |
|------|---------|--------|------------------|
| Apr 8 | 22 | 3 | Peak activity |
| Apr 9 | 16 | 1 | Still strong |
| Apr 11 | 3 | 1 | Dropping |
| Apr 12 | 5 | 0 | Crisis visible |
| Apr 13-14 | 17 | 1 (self-merge) | Attempting recovery |
| Apr 15 | 8 | 0 | Declining |
| **Apr 16** | **0** | **0** | **Total disengagement** |

**Pattern**: Community PR inflow dropped from 22/day (peak) to 0 (first time ever in 13-day window). This is the **end-stage signal** of review bottleneck. Recovery will require 2-4 weeks of consistent review responsiveness.

---

## RECOMMENDATIONS (Priority Order)

### 1. DECLARE REVIEW EMERGENCY (Today, <1 hour)

**Action**:
- VP Eng / Tech Lead: Post to #engineering Slack: "We are in a review emergency. 78 of 98 PRs are blocked >3 days with no reviewer. Beginning emergency intervention today."
- This signals to the community that leadership is aware and acting.

**Why**: Transparency prevents additional disengagement. Community sees the system is broken but being addressed.

---

### 2. GRANT EMERGENCY MERGE ACCESS (Today, by 10 AM)

**Action**:
- **autoresearch**: Grant merge access to **voidborne-d** and **TrueCrimeDev**
- **gstack**: Grant merge access to **Damin-Lee** and **LewisJEllis**
- These are the highest-output contributors with proven code quality. Temporary escalation (revoke in 2 weeks after system stabilizes).

**Why**: Without reviewer capacity, the queue cannot move. These contributors are already embedded in the codebase and have demonstrated judgment.

---

### 3. BATCH-MERGE LOW-RISK QUEUE (Today, by 2 PM)

**Action**:
- Assign the 2 deputies above to merge all PRs in the "quick wins" category (fork additions, translations, docs, README).
- Expected to clear 15-20 items, reducing stuck from 78→58-63.
- Allocate 2 hours max per deputy.

**Why**: Quick wins send a recovery signal to the community. Clears 20% of the backlog in one action.

---

### 4. SECURITY PRIORITY LANE (Today, by EOD)

**Action**:
- Security lead or designated reviewer: Review and merge **gstack#1002** (auth policy) and **autoresearch#506** (remove unsafe exec()).
- These are correctness/security fixes that should never be in a general queue.

**Why**: Security fixes delay impacts user safety and increases CVE risk.

---

### 5. ESTABLISH PERMANENT CO-MAINTAINER MODEL (This Week)

**Action**:
- For autoresearch: Designate interim maintainer (recommend voidborne-d or TrueCrimeDev) pending karpathy's return or formal escalation.
- For gstack: Establish 2-person review team to handle community PRs while garrytan focuses on strategic features.
- Create an SLA: Triage PRs within 24h of submission (decision on direction, not necessarily merge).

**Why**: The single-maintainer model is structurally broken. It creates burnout and blocks the entire system. A team of 2-3 reviewers per repo distributes load and prevents individual burnout.

---

### 6. RESTORE COMMUNITY TRUST (Next 2 Weeks)

**Action**:
- Resume regular merges (target: 70%+ of PRs merged within 5 days, 95%+ within 10 days)
- Post weekly public summary: "This week we merged X PRs, Y contributors unblocked, Z pending triage."
- Respond to open issues (even if the answer is "We'll prioritize this in Q2").

**Why**: Community trust takes months to build and days to destroy. Sustained review responsiveness is the only path back.

---

## SUCCESS METRICS TRACKER

### Per wt-project Section 6 — Target vs Actual

| Metric | Target | Actual (Apr 16) | Status |
|--------|--------|-----------------|--------|
| **Copilot Daily Active Users** | >90% | N/A (not applicable) | — |
| **Stand-up Meeting Time Reduction** | 50% | N/A | — |
| **Stuck Task Resolution SLA** | 24h intervention | 5+ days (5x over) | 🔴 FAILED |
| **Stuck Detection Speed** | 3d threshold | 3d threshold met (but unresolved) | 🟡 PARTIAL |
| **Review Turnaround** | <24h | 5-37 days | 🔴 FAILED |
| **Tool Cost Reduction** | ClickUp sunsetted M6 | On track (not evaluated weekly) | — |
| **Employee Wellbeing** | Reduce burnout/turnover | garrytan: burnout signals; karpathy: absent | 🔴 CRITICAL |
| **Team Migration** | 100% to GitHub by M6 | N/A (org-level, outside repos) | — |

**Summary**: The two operationalized KPIs for this dashboard (stuck resolution SLA, review turnaround) are both failed. The system is performing at ~10% of target across both dimensions.

---

## DAILY DELTA (Apr 15 PM → Apr 16 AM)

| Change | Impact |
|--------|--------|
| **Commits**: 0 | No progress on any feature |
| **PRs Opened**: 0 | First day with zero community inflow |
| **PRs Merged**: 0 | 48 hours with no resolution |
| **Stuck PRs**: 78 (+3 from Apr 15) | Saturation continuing |
| **Stuck Issues**: 11 (+0 from Apr 15) | Stable but unresolved |
| **Community Activity**: 0 | End-stage disengagement signal |

**Comparison to Apr 15 (24h prior)**:
- Apr 15 AM: 75 stuck (77%), 8 PRs expected that day
- Apr 16 AM: 78 stuck (80%), 0 PRs received that entire day

---

## CONFIDENCE & CAVEATS

**Data Quality**: Excellent. Daily snapshots capture all GitHub activity (commits, PRs, issues) across both repos.

**Scope**: autoresearch (karpathy) and gstack (garrytan) — the two primary repositories tracked.

**Observation Window**: Apr 4–16 (13 days). Sufficient to establish trend confidence.

**Blind Spots**:
- Personal/well-being signals (e.g., is garrytan on personal leave?) rely on inference from activity, not first-person reporting
- External blockers (platform outages, merging tool failures) would not be visible in this data
- Scheduled maintenance or code freezes would not be annotated

---

## NEXT ACTIONS FOR THIS DASHBOARD

1. **Tomorrow (Apr 17)**: Repeat snapshot. Expected result: If interventions from #1-4 above are executed, stuck count should drop to ~60-65. If no action: stuck → 85+.
2. **Weekly (Apr 23)**: Update metrics. Re-evaluate burnout signals for garrytan (if activity resumes, condition improving; if continued silence, escalate to manager/HR).
3. **Ongoing**: Track community PR inflow recovery. Baseline Apr 8 = 22 PRs/day. Milestone: return to 15+ by May 1 (2-week recovery window).

---

*Generated by: Team Pulse management analyst*
*Dashboard Type: Executive decision support (wt-project 4.4)*
*Next update: 2026-04-17*
