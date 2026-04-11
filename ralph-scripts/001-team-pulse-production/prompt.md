# Ralph Agent Instructions

You are an autonomous coding agent working on a software project.

## Your Task

1. Read the PRD at `prd.json` (in the same directory as this file)
2. Read the progress log at `progress.txt` (check Codebase Patterns section first)
3. Check you're on the correct branch from PRD `branchName`. If not, check it out or create from main.
4. Pick the **highest priority** user story where `passes: false`
5. Implement that single user story
6. Run quality checks (e.g., typecheck, lint, test - use whatever your project requires)
7. Update AGENTS.md files if you discover reusable patterns (see below)
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
- Quality gate: `PYTHON=.venv/bin/python make test` must pass before committing

## Stop Condition

After completing a user story, re-read `prd.json` and check if ALL stories have `passes: true`.

If ALL stories are complete and passing, reply with:
<promise>COMPLETE</promise>

## Important

- Work on ONE story per iteration
- Commit frequently
- Keep CI green
- Read the Codebase Patterns section in progress.txt before starting

## Local Learnings

- Use `.venv/bin/python` for running tests; the shell may not have a default `python` binary
- Quality gate: `PYTHON=.venv/bin/python make test` must pass before committing
- Integration tests: `tests/integration/conftest.py` has autouse auth mock + `client` fixture
- Use `dataclasses.asdict()` to serialize dataclass reports to JSON-compatible dicts
- MMM router: `src/platform/api/routers/mmm.py` — register dedicated routes before the generic `/{engine}/{artifact}` catch-all
- Engine protocol: `src/mmm/engines/base.py` — `MmmEngineProtocol`
- Engine registry: `src/mmm/engines/registry.py` — `get_engine(name)`, `list_engines()`
- Validation module: `src/mmm/validation/` — business_sense.py, benchmarks.py, sufficiency.py, diagnostic_interpreter.py, statistical_tests.py
- EDA module: `src/mmm/eda/` — correlations.py, stationarity.py, multicollinearity.py, distributions.py, spec_recommender.py, visualizations.py
- EDA router: `src/platform/api/routers/eda.py` — GET/POST endpoints for EDA artifacts
- Benchmarks: `data/config/benchmarks.json` — top-level metadata object with `benchmarks` array
- Meridian artifacts: `data/mmm/meridian_results/` — roi.json, decomposition.json, diagnostics.json, evaluation_report.json
- Pipeline orchestrator: `src/platform/workflow/pipeline.py` — 10-stage pipeline (BRIEF→REPORT)
- Workflow state: `src/platform/workflow/state_manager.py` — JSON-persisted at data/workflows/
- Supervisor: `src/platform/agents/supervisor.py` — delegation engine with tier routing
- Cleaning pipeline: `src/mmm/cleaning/` — time_alignment.py, outlier_detection.py, missing_data.py, normalisation.py, matrix_builder.py
- Meridian config: `src/mmm/meridian_config.py` — PRIOR_PROFILES, build_prior_distribution(), ADSTOCK_DECAY_RATES
- Schemas: `src/platform/schemas/` — channels.py (CHANNEL_REGISTRY), sources/ (6 families), validation.py
- Experiment schemas: `src/platform/schemas/sources/experiments.py` — GeoliftResultsRow, AttributionPathsRow
- Brand schemas: `src/platform/schemas/sources/brand.py` — BrandTrackingRow
