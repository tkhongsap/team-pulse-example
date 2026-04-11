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
updated: 2026-04-11
---

# autoresearch

Repository: [karpathy/autoresearch](https://github.com/karpathy/autoresearch). Python-based autonomous research framework with 70K+ stars and 10K+ forks. High community interest but effectively stalled due to maintainer inactivity.

## Key Points

- 39 open PRs as of Apr 11, 34 of which are stuck (>3d, no reviewer)
- Zero commits to default branch during Apr 4-11 (last commit: Mar 26)
- Zero PR reviews or merges during observation period
- Sole maintainer [[contributors/karpathy]] inactive since late March
- Active community contributors (e.g., [[contributors/voidborne-d]]) blocked on review
- 3 stuck issues with zero comments (oldest: 13 days)

## Health Trajectory (Apr 4-11)

| Date | Commits | PRs Opened | PRs Merged | Stuck PRs |
|------|---------|------------|------------|-----------|
| Apr 4 | 0 | 2 | 0 | 21 |
| Apr 5 | 0 | 4 | 0 | 21 |
| Apr 6 | 0 | 6 | 0 | 22 |
| Apr 7 | 0 | 5 | 0 | 22 |
| Apr 8 | 0 | 3 | 0 | 21 |
| Apr 9 | 0 | 1 | 0 | 23 |
| Apr 10 | 0 | 1 | 0 | 26 |
| Apr 11 | 0 | 0 | 0 | 34 |

Zero merge throughput. Every new PR adds to the stuck backlog.

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
