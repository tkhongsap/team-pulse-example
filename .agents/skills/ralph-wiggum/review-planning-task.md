# Review Planning Imperium Task

Review a Planning Imperium task against the task authoring constitution and generate a GitHub-ready review report.

## Arguments

- `task_path` (required): Path to the task directory (e.g., `imperium-planning/swebench/tasks/hardbyte-python-can-887`)

## Usage

```
/review-planning-task <task_path>
```

## Output

Creates `review-report.md` in the task directory with:
- Summary assessment
- Critical issues (must fix)
- Minor issues (should fix)
- Checklist pass/fail status

---
<command-name>review-planning-task</command-name>

# Instructions

You are reviewing a Planning Imperium task for quality and compliance with the task authoring constitution.

## Task Path

The user will provide a task path. Read all relevant files from that directory.

## Files to Review

1. **planning_statement.md** - User-facing prompt asking for a plan
2. **golden_plan.md** - Expert-level reference plan
3. **rubric/planning.json** - Criteria to grade plan quality
4. **rubric/execution.json** - Criteria to grade code behavior
5. **golden.patch** - Reference implementation (cross-reference with golden_plan.md)

## Review Checklist

### Planning Statement Checks

| Check | Pass Criteria |
|-------|---------------|
| No file paths | Does not reveal directory structure or specific file locations |
| No variable/function names | Does not mention implementation-specific names from solution |
| No implementation hints | Does not suggest HOW to solve, only WHAT needs to be solved |
| Natural engineer tone | Sounds like a real developer request, not system language |
| Plan-only request | Asks for a plan, not code |

**Automatic fail if contains:**
- Explicit file paths (e.g., `src/utils/helper.py`)
- Function names from golden.patch
- Code snippets or pseudocode
- "The solution should use..." type phrases

### Golden Plan Checks

| Check | Pass Criteria |
|-------|---------------|
| Has "Hard Parts" section | Identifies 1-2 hardest challenges with explanation |
| Has "Alternatives Considered" | Discusses other approaches and why not chosen |
| Not patch-shaped | Structure doesn't mirror golden.patch file-by-file |
| Uses `(e.g., <name>)` | Suggested names are examples, not mandates |
| All patch files mentioned | Every file in golden.patch appears in the plan |
| Reasonable length | 200-300 lines ideal, flag if >400 |

### Planning Rubric Checks (rubric/planning.json)

| Check | Pass Criteria |
|-------|---------------|
| Source field placement | Source ONLY on functional criteria, NOT on robustness/style |
| Valid source values | Only "problem", "prompt", "issue", or "title" |
| Style weights | ALL style criteria have weight: "minor" |
| No stacked criteria | No "and/or" combining independent behaviors |
| Behavior-focused | Tests WHAT (outcome), not HOW (mechanism) |
| Valid JSON | Parses without errors |

### Execution Rubric Checks (rubric/execution.json)

| Check | Pass Criteria |
|-------|---------------|
| Has metadata | Contains language, num_correctness_criteria, num_fail_to_pass, num_pass_to_pass |
| Behavior-focused | Describes observable outcomes, not implementation details |
| Style weights | ALL style criteria have weight: "minor" |
| No stacked criteria | No "and/or" combining independent behaviors |
| Valid JSON | Parses without errors |

### Banned Words (Automatic Minor Issue)

Flag any occurrence of these vague terms in rubric descriptions:
- gracefully
- correctly
- appropriately
- properly
- minimally
- well
- clearly

Replace with specific, observable behavior.

## Severity Classification

### Critical (Must Fix)
- Solution leaks in planning_statement.md
- Stacked criteria in rubrics
- Source field on robustness/style criteria
- Style criteria marked as "major"
- Missing "Hard Parts" section
- Missing "Alternatives Considered" section
- Invalid JSON syntax

### Minor (Should Fix)
- Banned vague words
- Golden plan >400 lines
- Missing patch files in golden_plan.md
- Implementation-specific language (can be improved)

## Output Format

Write the review to `{task_path}/review-report.md`:

```markdown
# Task Review: {task-name}

**Reviewed:** {date}
**Reviewer:** Claude (automated)

## Summary

[1-2 sentences: overall assessment - PASS/NEEDS WORK/MAJOR ISSUES]

## Issues Found

### Critical (Must Fix)

- **[File]**: [Specific issue]
  - Location: [line number or section]
  - Fix: [How to fix]

### Minor (Should Fix)

- **[File]**: [Specific issue]
  - Location: [line number or section]
  - Fix: [How to fix]

## Checklist Results

| File | Status | Notes |
|------|--------|-------|
| planning_statement.md | PASS/FAIL | [brief note] |
| golden_plan.md | PASS/FAIL | [brief note] |
| rubric/planning.json | PASS/FAIL | [brief note] |
| rubric/execution.json | PASS/FAIL | [brief note] |

## Recommendations

[Prioritized list of actions to address issues]
```

## Completion

When the review is complete and `review-report.md` has been written, output:

```
<promise>REVIEW COMPLETE</promise>
```

## Example Ralph Loop Usage

```
/ralph-loop "Review the Planning Imperium task at imperium-planning/swebench/tasks/hardbyte-python-can-887. Follow the review checklist from task_authoring_constitution.md.

## Files to Review
1. planning_statement.md - Check for solution leaks
2. golden_plan.md - Check structure, hard parts, alternatives
3. rubric/planning.json - Check source fields, weights, stacking
4. rubric/execution.json - Check behavior-focus, metadata
5. golden.patch - Cross-reference with golden_plan.md

## Constitution Rules to Check

### NEVER DO Violations
- [ ] Solution leaks in planning_statement.md (file paths, function names)
- [ ] Vague language (appropriately, correctly, gracefully, properly, well)
- [ ] Stacked criteria (and/or combining independent behaviors)
- [ ] Patch-shaped golden plan (mirrors golden.patch structure)
- [ ] Implementation-specific criteria (tests HOW not WHAT)
- [ ] Style criteria marked as 'major'
- [ ] Source field on robustness/style criteria

### ALWAYS DO Checks
- [ ] Observable behaviors in criteria descriptions
- [ ] 'Hard Parts' section in golden_plan.md
- [ ] 'Alternatives Considered' in golden_plan.md
- [ ] High-level checklist items (not detailed)
- [ ] Valid JSON syntax
- [ ] All golden.patch files mentioned in golden_plan.md

## Output Format

Write a file called review-report.md with this structure:

---
## Task Review: <task-name>

### Summary
[1-2 sentences: overall assessment]

### Issues Found

#### Critical (Must Fix)
- **[File]**: [Specific issue] → [How to fix]

#### Minor (Should Fix)
- **[File]**: [Specific issue] → [How to fix]

### Checklist Pass/Fail
- Planning Statement: PASS/FAIL
- Golden Plan: PASS/FAIL
- Planning Rubric: PASS/FAIL
- Execution Rubric: PASS/FAIL

---

When review is complete and review-report.md is written, output:
<promise>REVIEW COMPLETE</promise>
" --completion-promise "REVIEW COMPLETE" --max-iterations 5
```
