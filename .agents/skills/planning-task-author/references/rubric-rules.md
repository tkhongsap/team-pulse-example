# Rubric Rules Reference

Per-category rules, weight distribution, and quality checklists for Planning Imperium rubrics.

---

## Planning Rubric Categories

The planning rubric grades the PLAN. Categories: `functional`, `robustness`, `style`.

### Functional (Planning)

**What it checks:** Requirements identification, integration points, sequencing, verification strategy.

| Aspect | What to Check |
|--------|---------------|
| Requirements | Task-specific requirements and expected outcomes (what must change / what must not) |
| Integration | Repo-specific integration points (modules/files/entrypoints) grounded in codebase |
| Sequencing | Work ordered by dependencies (what happens first and why) |
| Behavior | End-to-end behavior for this specific problem |
| Validation | Verification strategy: what pass/fail looks like |

**Rule of thumb:** A good functional-planning criterion requires at least one of:
1. WHERE in the system the change belongs
2. WHY that spot is the right place
3. HOW success is verified

**Checklist:**
- [ ] Does criterion require WHERE the change belongs?
- [ ] Does criterion require WHY that location is correct?
- [ ] Does criterion require HOW success is verified?
- [ ] Is criterion grounded in repo-specific components?
- [ ] Would a generic plan fail this criterion?

### Robustness (Planning)

**What it checks:** Edge cases, failure modes, risks WITHIN current scope (not speculation).

| Aspect | What to Check |
|--------|---------------|
| Edge Cases | Task-specific edge cases/failure modes within scope |
| Expected Behavior | Specific behavior for each case (not "handles properly") |
| Failure Points | Where things can break (parsing, state, formatting, invalid output) |
| Mitigations | Rollbacks or recovery if relevant |

**Checklist:**
- [ ] Does criterion name specific edge cases from the task?
- [ ] Does criterion specify expected behavior?
- [ ] Is the edge case within scope of prompt/problem?
- [ ] Are failure points specific to this task's pipeline/flow?

### Style (Planning)

**What it checks:** Communication quality, concreteness, repo awareness.

NOT: validation criteria, generic formatting rules.

| Aspect | What to Check |
|--------|---------------|
| Actionable | Clear, actionable steps (no filler) |
| Anchored | Steps anchored to repo components (files/modules/functions) |
| Technical | Concrete technical language from task/repo |

**Checklist:**
- [ ] Does criterion require anchoring to repo-specific components?
- [ ] Would this criterion fail if copied to a different task?
- [ ] Is it checking communication quality (not validation strategy)?
- [ ] Does it avoid generic formatting requirements?

---

## Execution Rubric Categories

The execution rubric grades the CODE. Categories in order: `correctness`, `functional`, `robustness`, `style`.

### Correctness (Execution)

Auto-generated from test results. No manual authoring needed.

### Functional (Execution)

**What it checks:** Core requirements work - feature exists, produces correct output.

- Source field REQUIRED: `"problem"`, `"prompt"`, `"issue"`, or `"title"`
- One criterion per major requirement
- Must be implementation-agnostic and observable
- May overlap what tests cover, but should test the behavior aspect

**Checklist:**
- [ ] Does criterion describe observable behavior?
- [ ] Is source field present?
- [ ] Does criterion test WHAT code does, not HOW?
- [ ] Would a different valid implementation still pass?

### Robustness (Execution)

**What it checks:** Edge cases and error handling.

- Source field NOT allowed
- Weight is "minor" unless failure truly breaks the solution
- Base on realistic scenarios from the codebase
- Name specific error conditions and expected responses

**Checklist:**
- [ ] Does criterion specify exact error condition?
- [ ] Does criterion specify exact expected response?
- [ ] Is weight "minor" (unless truly solution-breaking)?
- [ ] No source field present?

### Style (Execution)

**What it checks:** Code conventions and repo-specific patterns.

- Source field NOT allowed
- Weight is ALWAYS "minor" (never "major")
- Must reference repo-specific patterns (not generic style rules)
- Avoid restating formatter/linter rules

**Checklist:**
- [ ] Is weight "minor"?
- [ ] Does criterion reference repo-specific patterns?
- [ ] No source field present?
- [ ] Would this criterion fail on a different repo?

---

## Source Field Rules

| Category | Source Field | Allowed Values |
|----------|-------------|----------------|
| Functional | Required | `"problem"`, `"prompt"`, `"issue"`, `"title"` |
| Robustness | NOT allowed | - |
| Style | NOT allowed | - |

Never use `"approach"` as a source value.

---

## Weight Distribution Guide

| Category | Major | Minor |
|----------|-------|-------|
| Functional | Core requirements, critical integration | Nice-to-have, follow-on behaviors |
| Robustness | ONLY if failure truly breaks the solution | Edge cases, graceful degradation |
| Style | NEVER | ALWAYS |

**Planning-specific weights:**
- Major: correctness, integration, hard parts, edge cases, test planning
- Minor: structure, naming, validation clarity

---

## Criterion Quality Requirements

Every criterion must satisfy all 6:

1. **Objective** - True/false, no interpretation needed
2. **Self-contained** - Understandable without external context (with dependent_on)
3. **Non-stacked** - Evaluates exactly one behavior
4. **Implementation-agnostic** - Tests outcome, not mechanism
5. **Measurable** - An autograder can verify it
6. **Task-specific** - Would fail if copied to a different task/repo

**Litmus test:** If an LLM read the criterion 10 times, it should understand the same behavior every time.

---

## Criterion Counts

| Category | Min | Max |
|----------|-----|-----|
| Functional | 2 | 15 |
| Robustness | 2 | 10 |
| Style | 2 | 10 |

---

## Planning vs Execution Separation

| Planning Rubric | Execution Rubric |
|-----------------|------------------|
| "Plan identifies..." | "Code does..." |
| "Plan includes..." | "API returns..." |
| "Plan addresses..." | "Function outputs..." |
| Tests plan quality | Tests code behavior |

Never write execution-style criteria ("X returns Y") in the planning rubric. Use "Plan addresses..." or "Plan includes..." phrasing.

---

## Common Planning Rubric Issues

| Issue | Fix |
|-------|-----|
| Restates requirements ("mentions X") | Require integration/sequencing/verification, not just mention |
| Missing test-planning criterion | Add criterion for verification strategy |
| Planning vs execution confusion | Rewrite as "Plan addresses..." |
| Stacked criteria (contains "and/or") | Split into separate criteria |
| Wrong weights (style marked major) | Style is always minor |
| Overfitted to golden.patch | Ground in prompt/problem, not patch specifics |
