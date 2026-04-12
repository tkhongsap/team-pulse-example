---
title: "Q: give me a weekly team health summary for management"
question: "give me a weekly team health summary for management"
consulted:
  - "wiki/patterns/burnout-signals"
  - "wiki/patterns/review-bottleneck"
  - "wiki/patterns/stuck-items-growth"
  - "wiki/connections/sole-maintainer-and-stuck-growth"
  - "wiki/projects/gstack"
  - "wiki/projects/autoresearch"
  - "wiki/contributors/garrytan"
  - "wiki/contributors/karpathy"
sources_read: 8
filed: 2026-04-12
---

# Q: Weekly Team Health Summary (Apr 4–11, 2026)

## Headline

**Team health: CRITICAL.** Two tracked repositories are running on a single-maintainer model that is structurally failing. Stuck PRs grew **71% in one week (31 → 53)**, the gstack maintainer is exhibiting burnout signals, and the autoresearch maintainer has been absent for 16+ days. This is not a productivity issue — it is a capacity and structural risk that requires management intervention this week.

---

## Health Scorecard

| Dimension              | Score | Trend | Notes                                                              |
|------------------------|-------|-------|--------------------------------------------------------------------|
| Velocity               | 3/10  | ↓     | 9 merges across both repos in 8 days vs ~120 PRs opened            |
| Review responsiveness  | 2/10  | ↓     | 53 stuck PRs (>3 days, no reviewer) — 57% of all open PRs          |
| Workload balance       | 1/10  | ↓     | One person carrying 100% of merge throughput on gstack             |
| Burnout risk           | RED   | ↑     | 10+ late-night commits across 5 of 8 days for one contributor      |
| Community engagement   | 9/10  | ↑     | High inflow from quality contributors — bottleneck is review, not contribution |

---

## What's Working

- **Community is healthy.** Both repos are attracting quality PRs from active contributors. Names like [[contributors/damin-lee]], [[contributors/voidborne-d]], [[contributors/hybirdss]], and [[contributors/ignsm]] are all submitting reviewable, well-scoped work. The funnel is full.
- **garrytan is shipping.** Despite the overload, gstack saw 9 merges in 8 days plus a v0.16.3.0 refactor — see [[contributors/garrytan]].
- **No quality regressions** observed in the data.

## What's Broken

### 1. Review throughput cannot keep up with PR inflow
Per [[patterns/review-bottleneck]], the math is unsustainable:

| Repo          | Stuck PRs Apr 4 | Stuck PRs Apr 11 | Growth | Active Reviewers |
|---------------|-----------------|------------------|--------|------------------|
| autoresearch  | 21              | 34               | +62%   | 0                |
| gstack        | 10              | 19               | +90%   | 1 (garrytan)     |
| **Total**     | **31**          | **53**           | **+71%** | **1**          |

- gstack ratio: 9 merges in 8 days vs 54 open PRs = 6:1 backlog
- autoresearch ratio: 0 merges vs 39 open PRs = infinite backlog
- ~3 new stuck items added per day, every day — see [[patterns/stuck-items-growth]]

### 2. Burnout risk on the only person keeping gstack alive
[[patterns/burnout-signals]] flags [[contributors/garrytan]] as **HIGH risk**:
- 10+ late-night commits (22:00–06:00 UTC) on 5 of 8 observation days
- Apr 11 03:13 UTC: deep refactor work in the middle of the night
- Sole reviewer of 54 open PRs with zero deputies
- This is the textbook pattern from `wt-project.md` §4.3

### 3. autoresearch is effectively stalled
[[contributors/karpathy]] has been absent since March 26 (16+ days). Per the wt-project §4.2 definition, the entire project is "Stuck." His own PR #92 (AgentHub) has been open 32 days unreviewed. [[contributors/voidborne-d]]'s 5 tokenizer/build PRs are all blocked.

### 4. The reinforcing cycle
[[connections/sole-maintainer-and-stuck-growth]] documents the feedback loop: community grows → solo reviewer can't keep up → backlog accumulates → maintainer works late → burnout → throughput drops further. The data shows it is already in motion.

---

## Recommended Actions for Management This Week

1. **Deputize co-maintainers on gstack.** Grant merge access (not just review) to a trusted contributor — [[contributors/damin-lee]] is the obvious candidate based on contribution history.
2. **Triage autoresearch.** Reach out to [[contributors/karpathy]] to confirm intent. If he is unable to maintain, identify a successor or archive the project to set community expectations honestly.
3. **Create a security priority lane.** [[contributors/hybirdss]]'s 3 security fix PRs have been unreviewed for 3+ days — these should never sit in the same queue as feature PRs.
4. **Batch the easy PRs.** ~10 of autoresearch's 34 stuck PRs are "add fork to notable forks" — these are accept/reject decisions, not architectural reviews. A 30-minute triage session would clear them.
5. **Track burnout intervention.** Per wt-project §4.3, garrytan's late-night pattern requires explicit conversation, not just observation.

---

## Key Metrics to Watch Next Week

- Stuck PR count (target: ≤45, down from 53)
- garrytan late-night commits (target: 0)
- autoresearch merge count (target: ≥1, up from 0)
- Time-to-first-review on new gstack PRs (target: <48h)

## Sources Consulted

- [[wiki/patterns/burnout-signals]] — quantified late-night pattern and risk levels
- [[wiki/patterns/review-bottleneck]] — throughput vs inflow gap with daily evidence
- [[wiki/patterns/stuck-items-growth]] — 8-day trajectory showing +71% growth
- [[wiki/connections/sole-maintainer-and-stuck-growth]] — root-cause feedback loop
- [[wiki/projects/gstack]] — daily PR/merge/stuck table
- [[wiki/projects/autoresearch]] — zero-throughput evidence and PR categorization
- [[wiki/contributors/garrytan]] — overloaded maintainer detail
- [[wiki/contributors/karpathy]] — absent maintainer detail

## File Back Recommendation

**No new wiki article needed.** This is a synthesis of existing patterns and contributors — the underlying knowledge is already in the wiki. However, two suggestions for compounding:

1. **Create `wiki/reports/2026-04-12-weekly-summary.md`** as a recurring artifact (this answer is the prototype). Weekly executive summaries are a different audience than daily morning briefings and EOD summaries, and management will want to compare week-over-week.
2. **Consider adding a `wiki/patterns/co-maintainer-need.md` pattern** if next week's data shows the recommended interventions did not happen — that would elevate "structural fix not adopted" into a tracked pattern of its own.
