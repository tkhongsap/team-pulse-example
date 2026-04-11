# Morning Briefing — 2026-04-11

> Generated from: docs/daily/2026-04-11-am.md
> Purpose: What needs attention today (wt-project 4.1 + 4.2)

---

## 1. Top Priorities Today

### P1: Security PRs on gstack need immediate review
Two security-related PRs from **Hybirdss** have been open for 2 days with no reviewer:
- [gstack#920](https://github.com/garrytan/gstack/pull/920) — path validation bypass in upload and cookie-import
- [gstack#921](https://github.com/garrytan/gstack/pull/921) — validateOutputPath bypassed via symlinks

**Owner:** garrytan (maintainer)
**Action:** Review and merge or request changes today. Security fixes should not sit unreviewed.

### P2: PR review backlog is critical — 53 stuck PRs, 57% of all open PRs
93 PRs are open across both repos. **53 have been open 3+ days with no reviewer assigned.** This is the single biggest process bottleneck. The autoresearch repo has essentially no review activity — 34 PRs stuck with zero reviewers.

**Owner:** karpathy (autoresearch), garrytan (gstack)
**Action:** Batch-triage stuck PRs. For autoresearch, decide which community PRs to accept/close — many are "add fork to notable forks" PRs that could be bulk-processed. For gstack, prioritize the bug fixes (security, browse watchdog, CDPATH).

### P3: Browse watchdog bug — 4 duplicate PRs trying to fix the same issue
Multiple contributors have independently submitted fixes for the parent-process watchdog killing the browse server:
- [gstack#869](https://github.com/garrytan/gstack/pull/869) by zzyyfff (4d)
- [gstack#857](https://github.com/garrytan/gstack/pull/857) by schobiDotDev (4d)
- [gstack#944](https://github.com/garrytan/gstack/pull/944) by navin-statisfy (1d)
- [gstack#959](https://github.com/garrytan/gstack/pull/959) by garrett-fox (0d)

**Owner:** garrytan
**Action:** Pick the best implementation, merge it, close the duplicates. Leaving all four open wastes contributor goodwill.

### P4: garrytan committed at 03:13 UTC (10:13 AM Bangkok) — monitor workload
garrytan merged [#941](https://github.com/garrytan/gstack/pull/941) (AI slop reduction refactor) and is the sole active maintainer handling 54 open gstack PRs. This is a heavy, solo workload.

**Owner:** Team lead
**Action:** Check if garrytan needs review help. Consider deputizing a trusted contributor for triage.

### P5: Issue #961 — hooks referencing wrong env variable
ivansamartino filed [gstack#961](https://github.com/garrytan/gstack/issues/961) AND submitted [gstack#968](https://github.com/garrytan/gstack/pull/968) with the fix. Issue + PR are matched and ready for quick review/merge.

**Owner:** garrytan
**Action:** Quick win — review and merge #968 to close #961 today.

---

## 2. Status Board

### autoresearch

| Contributor | Status | Evidence | Action Needed |
|---|---|---|---|
| karpathy | **Stuck** | Own PR [#92](https://github.com/karpathy/autoresearch/pull/92) (AgentHub) open 32d. Last commit to default branch was Mar 26. 34 community PRs with no review. | Triage community PRs or delegate review. |
| voidborne-d | **In Progress** | 3 open PRs ([#498](https://github.com/karpathy/autoresearch/pull/498), [#484](https://github.com/karpathy/autoresearch/pull/484), [#482](https://github.com/karpathy/autoresearch/pull/482)) — active tokenizer/install fixes over past 5 days. | Needs reviewer assigned — all 3 PRs stuck waiting. |
| ademeure | **In Progress** | PR [#504](https://github.com/karpathy/autoresearch/pull/504) — PyTorch 2.11 + FlexAttention, 2d old. | Monitor — significant performance PR. |

### gstack

| Contributor | Status | Evidence | Action Needed |
|---|---|---|---|
| garrytan | **In Progress** | 1 commit + 1 PR merged today. 2 own PRs stuck ([#78](https://github.com/garrytan/gstack/pull/78) 26d, [#416](https://github.com/garrytan/gstack/pull/416) 17d). | Heavy workload — sole maintainer of 54 open PRs. |
| ivansamartino | **In Progress** | Opened PR [#968](https://github.com/garrytan/gstack/pull/968) fixing hooks env var. Also filed issue [#961](https://github.com/garrytan/gstack/issues/961). | PR ready for review — quick merge. |
| rvdlaar | **In Progress** | Opened PR [#967](https://github.com/garrytan/gstack/pull/967) fixing ngrok build externalization. | Needs review. |
| bjohnson135 | **In Progress** | Opened PR [#966](https://github.com/garrytan/gstack/pull/966) adding Windsurf host. | Needs review. |
| Damin-Lee | **In Progress** | 3 open PRs ([#834](https://github.com/garrytan/gstack/pull/834) 5d, [#917](https://github.com/garrytan/gstack/pull/917) 2d, [#905](https://github.com/garrytan/gstack/pull/905) 2d, [#950](https://github.com/garrytan/gstack/pull/950) 0d). Consistent contributor. | #834 stuck at 5d — prioritize review. |
| Hybirdss | **In Progress** | 3 security-related PRs ([#920](https://github.com/garrytan/gstack/pull/920), [#921](https://github.com/garrytan/gstack/pull/921), [#918](https://github.com/garrytan/gstack/pull/918)). | **Security PRs — review urgently.** |
| ignsm | **Ready to Hand Off** | 3 docs/cleanup PRs ([#952](https://github.com/garrytan/gstack/pull/952), [#953](https://github.com/garrytan/gstack/pull/953), [#951](https://github.com/garrytan/gstack/pull/951)). README alignment. | Merge — low risk, docs only. |

---

## 3. Review Queue

Sorted by age, highest priority items only (53 total stuck — showing top actionable ones):

| Priority | PR | Author | Age | Why Urgent |
|---|---|---|---|---|
| **SECURITY** | [gstack#920](https://github.com/garrytan/gstack/pull/920) | Hybirdss | 2d | Path validation bypass — security vuln |
| **SECURITY** | [gstack#921](https://github.com/garrytan/gstack/pull/921) | Hybirdss | 2d | Symlink bypass — security vuln |
| Quick win | [gstack#968](https://github.com/garrytan/gstack/pull/968) | ivansamartino | 0d | Fixes reported issue #961, ready |
| Quick win | [gstack#876](https://github.com/garrytan/gstack/pull/876) | quanru | 3d | YAML parsing fix — small, clear |
| Quick win | [gstack#950](https://github.com/garrytan/gstack/pull/950) | Damin-Lee | 0d | YAML quoting fix — small, clear |
| Dedup needed | [gstack#869](https://github.com/garrytan/gstack/pull/869) | zzyyfff | 4d | Watchdog fix — pick one of 4 dupes |
| Bug fix | [gstack#834](https://github.com/garrytan/gstack/pull/834) | Damin-Lee | 5d | OpenClaw YAML parsing |
| Bug fix | [gstack#836](https://github.com/garrytan/gstack/pull/836) | Gujiassh | 5d | CDPATH-safe bin root detection |
| Feature | [autoresearch#504](https://github.com/karpathy/autoresearch/pull/504) | ademeure | 2d | PyTorch 2.11 + FlexAttention — high impact |
| Stale | [autoresearch#92](https://github.com/karpathy/autoresearch/pull/92) | karpathy | 32d | Own PR — decide: continue or close |

---

## 4. Stuck Items Triage

### Critical Stuck Items

**autoresearch — 34 stuck PRs, repo-wide review drought**
- **Root cause:** karpathy appears to be the sole reviewer and hasn't reviewed community PRs since late March. No other maintainers with merge access are active.
- **Recommended action:** Batch-process community PRs into categories:
  - "Add fork to notable forks" PRs (~10): quick accept/reject decision
  - Bug fix PRs (~8): need technical review
  - Feature PRs (~6): need architecture decision
  - Docs PRs (~3): quick merge candidates
- **Who:** karpathy or a designated co-maintainer

**gstack — 19 stuck PRs, maintainer bottleneck**
- **Root cause:** garrytan is sole active reviewer. PR volume (54 open) exceeds one person's review capacity.
- **Recommended action:** Identify 2-3 trusted contributors (Damin-Lee, ignsm, Hybirdss have track records) and grant limited review/triage permissions.
- **Who:** garrytan

### Stuck Issues (3)

| Issue | Age | Likely Reason | Action |
|---|---|---|---|
| [autoresearch#437](https://github.com/karpathy/autoresearch/issues/437) | 13d, 0 comments | Low priority fork listing request | Close or respond with timeline |
| [autoresearch#445](https://github.com/karpathy/autoresearch/issues/445) | 11d, 0 comments | Hybrid inference question — may need research | Respond with current status or label as "needs investigation" |
| [autoresearch#476](https://github.com/karpathy/autoresearch/issues/476) | 7d, 0 comments | CLI analysis tool request — has matching PR [#475](https://github.com/karpathy/autoresearch/pull/475) | Review PR #475 to close this issue |

---

## 5. Overnight Activity

**gstack (active overnight):**
- garrytan merged PR [#941](https://github.com/garrytan/gstack/pull/941) — AI slop reduction refactor (v0.16.3.0) at 03:13 UTC
- 3 new PRs opened: #968 (hooks fix), #967 (ngrok build), #966 (Windsurf host)
- No new issues filed today

**autoresearch (quiet):**
- No commits, no new PRs, no new issues
- Last commit to default branch was March 26 (16 days ago)

**Immediate attention needed:** None of the overnight items are urgent beyond the security PRs already flagged above.

---

## wt-project Success Metrics Check

| Metric | Target | Current State | Status |
|---|---|---|---|
| Stuck Task Resolution | Within 24h of alert | 53 PRs stuck, oldest 32d | **Behind** |
| Stuck Detection Speed | Flagged at 3+ days | Working — script flags correctly | **On Track** |
| Stand-up Replacement | AI summary replaces manual checks | This briefing serves that role | **On Track** |

**Key concern for wt-project 4.2 (Status Categorization):** The status board shows a healthy pattern for gstack (multiple contributors in progress) but a stalled pattern for autoresearch (single maintainer, no review flow). If this were a team repo, 34 stuck PRs would require immediate intervention per the 24h resolution target.
