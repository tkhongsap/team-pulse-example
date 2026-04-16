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
  - "raw/github-daily/2026-04-12-am.md"
  - "raw/github-daily/2026-04-15-am.md"
  - "raw/github-daily/2026-04-16-am.md"
created: 2026-04-11
updated: 2026-04-16
---

# autoresearch

Repository: [karpathy/autoresearch](https://github.com/karpathy/autoresearch). Python-based autonomous research framework with 70K+ stars and 10K+ forks. **Effectively dead: zero merges for 21+ days, 40 open PRs, 39 stuck (98%), maintainer completely absent.**

## Key Points

- 40 open PRs as of Apr 16, 39 stuck (98%) — only 1 PR under 3 days old
- Zero commits to default branch during entire Apr 4-16 observation period
- Zero PR reviews or merges — the only merge activity anywhere was garrytan's gstack self-merges
- Sole maintainer [[contributors/karpathy]] inactive since Mar 26 (21 days)
- New PR on Apr 15: #516 (macOS CPU/MPS support by marketswitch) — last community contribution before Apr 16 silence
- Community activity dropped to zero on Apr 16 — first day with no new PRs or issues
- Oldest stuck PR: #92 (AgentHub) by karpathy himself — 37 days open

## Health Trajectory (Apr 4-16)

| Date | Commits | PRs Opened | PRs Merged | Stuck PRs | Status |
|------|---------|------------|------------|-----------|--------|
| Apr 4 | 0 | 2 | 0 | 21 | Baseline |
| Apr 5 | 0 | 4 | 0 | 21 | Inflow steady |
| Apr 6 | 0 | 6 | 0 | 22 | Inflow peaks |
| Apr 7 | 0 | 5 | 0 | 22 | Continued |
| Apr 8 | 0 | 3 | 0 | 21 | Slight decline |
| Apr 9 | 0 | 1 | 0 | 23 | Minimal |
| Apr 10 | 0 | 1 | 0 | 26 | Stuck grows |
| Apr 11 | 0 | 0 | 0 | 34 | Stuck spike |
| Apr 12 | 0 | 2 | 0 | 39 | Critical |
| Apr 13 | 0 | 0 | 0 | 39 | Flatlined |
| Apr 14 | 0 | 0 | 0 | 39 | Flatlined |
| Apr 15 | 0 | 1 | 0 | 39 | Last community PR |
| Apr 16 | 0 | 0 | 0 | 39 | **Zero activity — dead** |

## PR Categories (approximate, Apr 16)

- "Add fork to notable forks" — ~12 PRs (trivial accept/reject)
- Bug fixes (tokenizer, prepare.py, install) — ~10 PRs (need technical review)
- Feature additions (CLI tools, training, skills) — ~8 PRs (need architecture decisions)
- Documentation (Chinese translation, README) — ~4 PRs (quick merge candidates)
- RFCs / major changes — ~4 PRs (need maintainer direction)

## Related

- [[contributors/karpathy]] — creator and sole maintainer (absent 21 days)
- [[contributors/voidborne-d]] — most active contributor (3 stuck PRs)
- [[patterns/review-bottleneck]] — zero review throughput
- [[patterns/stuck-items-growth]] — stuck count at 98% saturation
- [[patterns/community-disengagement]] — contributor activity dropping to zero
