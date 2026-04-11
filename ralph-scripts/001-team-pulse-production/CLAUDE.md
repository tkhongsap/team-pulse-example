# Ralph Agent Instructions

You are an autonomous coding agent working on a software project.

## Your Task

1. Read the PRD at `prd.json` (in the same directory as this file)
2. Read the progress log at `progress.txt` (check Codebase Patterns section first)
3. Check you're on the correct branch from PRD `branchName`. If not, check it out or create from main.
4. Pick the **highest priority** user story where `passes: false`
5. Implement that single user story
6. Run quality checks (e.g., typecheck, lint, test - use whatever your project requires)
7. Update CLAUDE.md files if you discover reusable patterns (see below)
8. If checks pass, commit ALL changes with message: `feat: [Story ID] - [Story Title]`
9. Update the PRD to set `passes: true` for the completed story
10. Append your progress to `progress.txt`

## Progress Report Format

APPEND to progress.txt (never replace, always append):

```
## [Date/Time] - [Story ID]
- What was implemented
- Files changed
- **Learnings for future iterations:**
  - Patterns discovered
  - Gotchas encountered
  - Useful context
---
```

## Consolidate Patterns

If you discover a **reusable pattern** that future iterations should know, add it to the `## Codebase Patterns` section at the TOP of progress.txt (create it if it doesn't exist).

## Quality Requirements

- ALL commits must pass your project's quality checks
- Do NOT commit broken code
- Keep changes focused and minimal
- Follow existing code patterns
- For Python scripts: `python scripts/team_pulse.py --help` must not error
- For web app: `cd web && npm run build` must pass (once web/ exists)

## Stop Condition

After completing a user story, re-read `prd.json` and check if ALL stories have `passes: true`.

If ALL stories are complete and passing, reply with:
<promise>COMPLETE</promise>

## Important

- Work on ONE story per iteration
- Commit frequently
- Keep CI green
- Read the Codebase Patterns section in progress.txt before starting

## Project Context

- **System schema:** Read CLAUDE.md in the repo root — it describes the three-layer architecture (raw/, wiki/, outputs/)
- **Existing extraction script:** scripts/team_pulse.py — uses `gh` CLI to pull GitHub data
- **Existing commands:** .claude/commands/*.md — prompt templates for compile, briefing, EOD, dashboard, ask
- **Frontend design spec:** docs/frontend-design.md — claude.ai-style three-panel layout
- **Agent SDK reference:** ideas/agent-sdk-reference.md — SDK tools, code examples, costs
- **PRD details:** docs/prd-team-pulse-production.md — full product requirements
- **Wiki data:** wiki/ has 11 compiled articles + 9 reports from the PoC
