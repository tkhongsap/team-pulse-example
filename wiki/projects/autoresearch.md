---
title: "autoresearch"
tags: [project, karpathy]
sources:
  - "raw/github-daily/2026-04-04-am.md"
  - "raw/github-daily/2026-04-05-am.md"
  - "raw/github-daily/2026-04-06-am.md"
  - "raw/github-daily/2026-04-07-am.md"
  - "raw/github-daily/2026-04-08-am.md"
  - "raw/github-daily/2026-04-09-am.md"
  - "raw/github-daily/2026-04-10-am.md"
  - "raw/github-daily/2026-04-11-am.md"
created: 2026-04-11
updated: 2026-04-12
---

# autoresearch

Repository: [karpathy/autoresearch](https://github.com/karpathy/autoresearch). Python-based autonomous research framework with 70K+ stars and 10K+ forks. High community interest but effectively stalled due to maintainer inactivity. **WORSENING: 100 open PRs (Apr 12), 39+ stuck, zero maintainer engagement.**

## Key Points

- 100 open PRs as of Apr 12 (up from 39 on Apr 11) — +156% in 24 hours
- 39+ open PRs are stuck (>3d, no reviewer) as of Apr 12, up from 34 (+15% in 24h)
- Zero commits to default branch during Apr 4-12 (last commit: Mar 26 — 17 days ago)
- Zero PR reviews or merges during entire observation period (Apr 4-12)
- Sole maintainer [[contributors/karpathy]] inactive since late March
- Active community contributors (e.g., [[contributors/voidborne-d]]) blocked on review
- 4 stuck issues with zero comments (oldest: 17 days; new issue #505 added Apr 12)

## Health Trajectory (Apr 4-12)

| Date | Commits | PRs Opened | PRs Merged | Stuck PRs | Status |
|------|---------|------------|------------|-----------|--------|
| Apr 4 | 0 | 2 | 0 | 21 | Baseline |
| Apr 5 | 0 | 4 | 0 | 21 | Inflow steady |
| Apr 6 | 0 | 6 | 0 | 22 | Inflow peaks |
| Apr 7 | 0 | 5 | 0 | 22 | Continued inflow |
| Apr 8 | 0 | 3 | 0 | 21 | Slight decline |
| Apr 9 | 0 | 1 | 0 | 23 | Minimal inflow |
| Apr 10 | 0 | 1 | 0 | 26 | Stuck grows |
| Apr 11 | 0 | 0 | 0 | 34 | Stuck spike |
| Apr 12 | 0 | 1 | 0 | 39+ | **CRITICAL: stuck doubles in 2d** |

Zero merge throughput for 17 days. Every PR automatically becomes stuck.

## PR Categories (approximate)

- "Add fork to notable forks" — ~10 PRs (quick accept/reject decisions)
- Bug fixes (tokenizer, prepare.py, install) — ~8 PRs (need technical review)
- Feature additions (CLI tools, training, skills) — ~6 PRs (need architecture decisions)
- Documentation (Chinese translation, README) — ~3 PRs (quick merge candidates)

## Related

- [[contributors/karpathy]] — creator and sole maintainer (inactive)
- [[contributors/voidborne-d]] — most active community contributor (blocked)
- [[patterns/review-bottleneck]] — zero review throughput
- [[patterns/stuck-items-growth]] — stuck count growing from 21 to 34
