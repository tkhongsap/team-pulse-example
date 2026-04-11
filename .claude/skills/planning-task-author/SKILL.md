---
name: planning-task-author
description: Author Planning & Communication tasks for Planning Imperium. Guides creation of planning statements, golden plans, and rubrics from a SWE-Bench task. Use when authoring a planning task, creating a planning statement, writing a golden plan, writing planning/execution rubric criteria, or starting a new Planning Imperium task.
---

## Overview

Author Planning & Communication tasks that evaluate an AI agent's ability to plan before coding.

| Deliverable | Purpose | Target |
|-------------|---------|--------|
| `planning_statement.md` | User-facing prompt asking for a plan | Natural tone, no solution leaks |
| `golden_plan.md` | Expert-level reference plan | Scores >=90% on planning rubric |
| `rubric/planning.json` | Criteria to grade plan quality | Objective, non-stacked |
| `rubric/execution.json` | Criteria to grade code behavior | <60% AI pass rate |

**Calibration targets:**
- Golden patch score on execution rubric: >=85%
- Golden plan score on planning rubric: >=90%
- Frontier model pass rate on execution rubric: <60%

---

## Golden Rules

### NEVER DO

1. **Leak solutions in planning_statement.md** - No file paths, variable names, or implementation hints
2. **Use vague language** - No "appropriately", "correctly", "gracefully", "properly", "minimally", "well", "clearly"
3. **Stack criteria** - Split any criterion with "and/or" testing independent behaviors
4. **Make golden plan patch-shaped** - Don't mirror the golden.patch file-by-file
5. **Use implementation-specific criteria** - Test WHAT (outcome), not HOW (mechanism)
6. **Mark style criteria as "major"** - Style weight is ALWAYS "minor"
7. **Add source field to robustness/style** - Source is only for functional criteria

### ALWAYS DO

1. **Describe observable behaviors** in criteria
2. **Include "Hard Parts" section** in golden_plan.md
3. **Include alternatives considered** in golden_plan.md
4. **Use high-level checklist items** (not detailed sub-sections)
5. **Validate JSON** before committing
6. **Run planning-ci grade** to verify golden plan scores >=90%

### Banned Words in Rubric Criteria

Never use in descriptions: `gracefully`, `correctly`, `appropriately`, `properly`, `minimally`, `well`, `clearly`

Also avoid: `follows existing patterns` (name the pattern), `(e.g., X or Y)` in descriptions (move examples to rationale), specific library names in planning criteria (describe the requirement instead).

---

## Workflow

### Phase 1: Setup

- Download task via `planning download`
- Initialize rubrics via `planning start`
- Create branch, initial commit, draft PR
- Pull AI-generated drafts (planning_statement.md, golden_plan.md, README)

### Phase 2: Viability Check

Read these files before writing anything:
- `prompt_statement.md` - what the user wants
- `problem_statement.md` - full scope and constraints
- `golden.patch` - reference solution OUTCOMES (not implementation)
- `test.patch` - what failures tests catch
- `interface.md` - required function/class names
- `requirements.json` - implementation expectations

**STOP and flag** if: missing tests, broken Docker, unclear/contradictory requirements, or golden patch doesn't solve the problem.

### Phase 3: Understand Codebase

- Find integration points (call sites, reducers, registries, routers, configs)
- Identify repository conventions and patterns
- Find implicit requirements (wiring, naming, file placement, exports)
- Write these down - they become rubric criteria

### Phase 4: Write Deliverables

1. Update `planning_statement.md` (see Writing the Planning Statement)
2. Write `golden_plan.md` (see Writing the Golden Plan)
3. Write `rubric/planning.json` (see Writing the Planning Rubric)
4. Review/improve `rubric/execution.json` (see Reviewing the Execution Rubric)

### Phase 5: Alignment Checks

Run the 3 alignment pairs (see Alignment Checks section).

### Phase 6: Submit

- Validate JSON syntax
- Run `planning-ci grade` (golden plan must score >=90%)
- Commit, push, mark PR ready for review

---

## Writing the Planning Statement

The planning statement is what the AI agent sees. It must sound like a real engineer asking for help.

### Must Include

- Natural engineer request tone
- Context about the system/repo
- Asks for a PLAN only, not code
- Encourages thinking about requirements, integration, risks, validation

### Must NOT Include

- File paths or directory structure hints
- Variable/function names from the solution
- Implementation approach hints
- Pseudocode or code snippets

### Tone Check

Bad (system language):
> "Create a comprehensive plan that addresses all functional requirements and integration points..."

Good (real person):
> "Hey, I need to add support for X in our Y system. Can you write up a plan before we start coding? I want to make sure we think through how this integrates with Z and what could go wrong."

### Sanity Check

Run the planning statement in an AI tool (e.g., Cursor) to generate a draft plan. Use this to identify missing constraints and ambiguities before writing the golden plan.

---

## Writing the Golden Plan

The golden plan is the expert reference. Someone following it should implement the solution confidently.

### Required Sections

```
1. Problem Understanding (objectives, constraints, non-goals)
2. Hard Parts (1-2 hardest challenges and why they're hard)
3. Key Integration Points (existing files to modify, where new code plugs in)
4. Design Approach + Alternatives Considered
5. Implementation Steps (5-10 concrete, ordered steps)
6. Risks and Edge Cases
7. Validation Strategy (tests, commands, success/failure criteria)
```

### Existing-vs-New Rule

- **Existing code**: Be exact about file paths and integration points (e.g., `cobbler/validate.py`, existing validator names)
- **New code**: Be outcome-focused (what the code achieves), not implementation-specific, unless the prompt mandates exact naming

Bad: `Add is_str_int(value: str) -> bool helper function`
Good: `Add a helper in cobbler/utils.py to validate whether a string represents a valid integer`

### Golden Plan Must

- Mention ALL files changed in golden.patch (including housekeeping files like .travis.yml, CHANGELOG, docs)
- Use `(e.g., <name>)` for suggested new names rather than prescribing exact identifiers
- Be 200-300 lines (flag if >400)
- Contain no vague statements like "handle appropriately" or "update as needed"

### Verify File Coverage

```bash
grep "^diff --git" golden.patch | sed 's/diff --git a\///' | sed 's/ b\/.*//'
```

Check each file appears in golden_plan.md.

---

## Writing the Planning Rubric

The planning rubric grades the PLAN, not the code. Structure: `functional`, `robustness`, `style`.

### Criterion Template

```json
{
  "id": "<category>-<number>",
  "description": "Single, objective, testable statement",
  "weight": "major|minor",
  "rationale": "Why this matters, with examples if helpful",
  "source": "problem|prompt|issue|title",
  "dependent_on": []
}
```

### Source Field Rules

| Category | Source Field |
|----------|-------------|
| Functional | Required: `"problem"`, `"prompt"`, `"issue"`, or `"title"` |
| Robustness | NOT allowed |
| Style | NOT allowed |

### Category Guidelines

**Functional** - Tests requirements identification, integration points, sequencing, verification strategy:
- One criterion per major requirement
- Require WHERE the change belongs, WHY that location, HOW success is verified
- Must be grounded in repo-specific components (a generic plan should fail)

**Robustness** - Tests edge cases from prompt/problem, error handling, failure modes:
- Edge cases must be task-specific and within scope (not speculative)
- Name specific conditions and expected behaviors
- Weight is "minor" unless failure truly breaks the solution

**Style** - Tests communication quality and repo awareness:
- Must be repo-specific (would fail if copied to a different task)
- Tests anchoring to repo components, technical language, concrete steps
- Weight is ALWAYS "minor"

### Criterion Counts

- Functional: 2-15 criteria
- Robustness: 2-10 criteria
- Style: 2-10 criteria

### Test Planning Criterion

If `test.patch` modifies test files, the planning rubric MUST include a criterion requiring the plan to address test updates.

### Alternative Implementation Test

For each criterion ask: "Would a valid different implementation fail this criterion?" If yes, the criterion is too implementation-specific.

See `references/rubric-rules.md` for per-category checklists and weight distribution details.
See `references/examples.md` for good/bad criterion examples.

---

## Reviewing the Execution Rubric

The execution rubric grades CODE behavior. Categories in order: `correctness`, `functional`, `robustness`, `style`.

### Key Differences from Planning Rubric

- Includes `correctness` category (auto-generated from test results)
- Functional criteria require `source` field
- Calibrated for <60% AI pass rate (harder than planning rubric)
- No criterion should reference test files (those belong in correctness only)

### Required Metadata

```json
{
  "metadata": {
    "language": "python",
    "num_correctness_criteria": 2,
    "num_fail_to_pass": 2,
    "num_pass_to_pass": 4
  }
}
```

Get counts from `test_metadata.json`.

### Review Each Criterion For

1. **Objective** - True/false, no interpretation
2. **Self-contained** - Understandable without external context
3. **Non-stacked** - One behavior per criterion
4. **Implementation-agnostic** - Tests WHAT, not HOW
5. **No vague language** - No banned words
6. **No test references** - In non-correctness categories
7. **Correct weights** - Style always "minor", robustness mostly "minor"

### Clarify Ambiguous Alternatives

When using "or" in criteria, always clarify when each alternative applies:

Bad: `Exceptions are re-raised or logged`
Good: `Unrecoverable exceptions are re-raised; recoverable exceptions are logged`

See `references/common-mistakes.md` for the 10 most frequent rubric mistakes.

---

## Alignment Checks

### Golden Plan <-> Planning Rubric

- [ ] Golden plan scores >=90% on planning rubric
- [ ] Every major requirement in planning_statement.md appears in golden_plan.md
- [ ] Every functional criterion verifiable by reading golden_plan.md
- [ ] Robustness criteria reflect edge cases/risks in golden_plan.md
- [ ] No orphan criteria (testing things not in plan)

### Golden Plan <-> Golden Patch

- [ ] Same solution approach (not necessarily identical)
- [ ] ALL files in golden.patch mentioned in golden_plan.md
- [ ] Integration points align
- [ ] Edge cases match

### Execution Rubric <-> Golden Patch

- [ ] Tests outcomes/behaviors, not implementation details
- [ ] Functional criteria verify end-to-end feature behavior
- [ ] Robustness criteria test edge cases grounded in prompt/problem
- [ ] Style criteria reference actual repo conventions

---

## Pre-Submit Checklist

### Planning Statement
- [ ] No solution/implementation leaks
- [ ] Natural engineer tone
- [ ] Asks for plan only

### Golden Plan
- [ ] Has "Hard Parts" section
- [ ] Has "Alternatives Considered" section
- [ ] All golden.patch files mentioned
- [ ] 200-300 lines (flag if >400)
- [ ] No vague statements

### Planning Rubric
- [ ] Source only on functional criteria
- [ ] All style weights = "minor"
- [ ] No stacked criteria
- [ ] Would pass alternative valid implementations
- [ ] 2-15 functional, 2-10 robustness, 2-10 style

### Execution Rubric
- [ ] Has metadata with test counts
- [ ] Behavior-focused (WHAT not HOW)
- [ ] All style weights = "minor"
- [ ] No stacked criteria
- [ ] No test references outside correctness

### Validation
- [ ] JSON validates: `python3 -m json.tool rubric/planning.json && python3 -m json.tool rubric/execution.json`
- [ ] Golden plan scores >=90%: `planning-ci grade-agent-plan --task-name <task-name> --mode golden-only`

---

## Reference Files

| File | When to Read |
|------|-------------|
| `references/rubric-rules.md` | When writing or reviewing rubric criteria (per-category rules, weight guide, quality checklist) |
| `references/common-mistakes.md` | When checking rubrics before submission (10 mistake patterns + 7 task-level issues) |
| `references/examples.md` | When unsure about criterion quality (good/bad pairs, JSON templates, stacking examples) |
