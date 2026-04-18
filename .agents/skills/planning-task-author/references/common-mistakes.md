# Common Mistakes Reference

Quick reference for the 10 most frequent rubric mistakes and 7 task-level issues.

---

## Quick Reference Table

| # | Mistake | One-Line Check |
|---|---------|----------------|
| 1 | Stacked criteria | Does "and/or" join independent behaviors? |
| 2 | Vague language | Contains banned words? |
| 3 | Implementation details | Describes HOW instead of WHAT outcome? |
| 4 | Not self-contained | Requires external context to understand? |
| 5 | Undefined standards | References conventions without defining them? |
| 6 | Not measurable | Could an autograder verify this? |
| 7 | Edge cases not defined | Says "edge cases" without naming them? |
| 8 | Weight assignment | Is weight appropriate for engineering reality? |
| 9 | References to tests | References test files in non-correctness criteria? |
| 10 | References to golden.patch | Mentions golden.patch in criterion text? |

---

## 10 Rubric Mistakes

### 1. Stacked Criteria

**Problem:** Single criterion evaluates multiple independent behaviors.
**Identify:** Look for "and" or "or" in descriptions. Triple-check each conjunction.
**Fix:** Split into separate criteria unless conditions describe one indivisible outcome.

Bad: `API supports GET /groups to return device groups, and each group includes an updated_at timestamp`
Good: Split into two criteria (endpoint exists + timestamp field present)

**Exception:** "The interface includes all fields: X, Y, Z" is acceptable (single completeness check).

### 2. Vague Language

**Problem:** Criteria open to multiple interpretations.
**Identify:** Search for: `gracefully`, `correctly`, `minimally`, `appropriately`, `clearly`, `properly`, `well`
**Fix:** Replace with observable condition + expected output.

Bad: `Handles invalid inputs gracefully`
Good: `Returns 400 Bad Request with error message when invalid input is provided`

### 3. Implementation Details

**Problem:** Describes HOW something was implemented, not WHAT was achieved.
**Identify:** Ask "Does this describe the mechanism or the outcome?"
**Fix:** Focus on observable outcomes.

Bad: `Uses a for loop to iterate through the array`
Good: `Processes all items in the array and returns the transformed result`

### 4. Not Self-Contained

**Problem:** Requires external context to understand.
**Identify:** "If an LLM evaluated this 10 times, would it get the same answer?"
**Fix:** Add necessary context to description or use dependent_on array.

Bad: `Adheres to Go language conventions`
Good: `All function names use camelCase`

### 5. Undefined Standards

**Problem:** References conventions without defining them.
**Identify:** Search for: `conventions`, `standards`, `best practices`, `idiomatic`
**Fix:** Name the specific standard being checked.

Bad: `Follows REST conventions`
Good: `Returns 201 for resource creation with Location header`

### 6. Not Measurable

**Problem:** Cannot be verified by an autograder.
**Identify:** Ask "How would an autograder determine this?"
**Fix:** Make binary pass/fail.

Bad: `Scales to large datasets`
Good: `Code does not include nested for loops`

### 7. Edge Cases Not Defined

**Problem:** Says "edge cases" without naming them.
**Identify:** Search for "edge case" without specifics following.
**Fix:** Name specific conditions and expected behaviors.

Bad: `Handles edge cases for SHOW VARIABLES queries`
Good: `Returns default value of 0 when userPreferences state is undefined`

### 8. Weight Assignment

**Problem:** Weights don't reflect engineering reality.
**Identify:** Style criteria marked "major", obvious follow-on behaviors marked "major".
**Fix:** Style = always minor. Follow-on behaviors = minor. Core functionality = major.

Rule: If behavior naturally follows from another criterion, it's "minor".

### 9. References to Tests

**Problem:** Non-correctness criteria reference test files.
**Identify:** Search for `test_`, `.py test`, `pytest` in functional/robustness/style criteria.
**Fix:** Describe the behavior being tested, not the test itself.

Bad: `Passes test_user_authentication.py`
Good: `User authentication validates credentials and returns session token`

### 10. References to golden.patch

**Problem:** Criteria mention golden.patch directly.
**Identify:** Search for `golden.patch`, `patch` in criterion text.
**Fix:** Describe observable outcomes, not the patch.

Bad: `Implementation matches golden.patch`
Good: `API endpoint returns paginated results with next_page_token`

---

## 7 Task-Level Issues

### Issue 1: Golden Plan Is Patch-Shaped

**Problem:** Plan mirrors golden.patch line-by-line (exact function names, error strings, control flow).

Bad: `Add is_str_int(value: str) -> bool helper function and raise TypeError('value needs to be of type string')`
Good: `Add a helper in cobbler/utils.py to validate whether a string represents a valid integer`

**Rule:** Be exact about EXISTING integration points. Be outcome-focused about NEW code.

### Issue 2: Planning Rubric Derives From Single Implementation

**Problem:** Rubric criteria copy golden plan specifics verbatim, penalizing valid alternatives.

Bad: `Plans to create is_str_int() and is_str_float() helpers in cobbler/utils.py`
Good: `Plans to add shared helpers in cobbler/utils.py to validate or convert numeric string inputs`

**Fix:** Focus on WHERE the logic goes and WHAT it achieves.

### Issue 3: Missing Test Update Criteria

**Problem:** test.patch modifies test files but planning rubric has no test planning criterion.

**Fix:** Add criterion when test.patch shows changes:
`Plans to update or add unit tests in tests/validate_test.py to verify numeric string handling`

### Issue 4: Execution Rubric Uses Vague Language

**Problem:** Criteria use "handles correctly", "works as expected", "properly validates".

**Fix:** Specify observable behavior:
- CLI behavior (output format, error messages)
- Return types (returns float, raises TypeError)
- Specific errors (ValueError for invalid input)

### Issue 5: Execution Rubric Tests Implementation

**Problem:** Criteria reference mechanisms ("Uses try/except", "Calls $ifNull operator").

**Fix:** Focus on outcomes:
- Bad: `Uses try/except ValueError to catch conversion errors`
- Good: `Rejects non-numeric strings with clear error message`

### Issue 6: Examples Inside Criteria Descriptions

**Problem:** Descriptions contain inline examples that belong in rationale.

Bad: `Plans to validate inputs (e.g., checking for non-strings, rejecting floats)`
Good: Description: `Plans to validate that inputs are strings representing valid integers`
Rationale: `Validation prevents runtime errors. For example, non-string inputs and float strings should be rejected.`

### Issue 7: Infrastructure Problems

- **Dockerfile**: Don't overwrite repo with `pip install <package>` (use `-e /workspace/repo --no-deps`)
- **run_test.sh**: Don't use `sudo` (container runs as root)
- **README**: Include `--privileged` if tests need hardware access
- **test_metadata.json**: PASS_TO_PASS must include ALL passing tests (not just some)
- **golden_plan.md**: Must mention all files in golden.patch (including housekeeping files)

---

## Client QA Rejection Categories

Criteria are also rejected by Client QA for these patterns:

| Category | What QA Checks | Quick Fix |
|----------|---------------|-----------|
| Professionalism | Too generic, no technical depth | Add repo-specific file paths, class names, config keys |
| Verifiability | Vague terms, not gradable | Replace with observable condition + expected output |
| Label Accuracy | Wrong category | Functional=exists/works, Robustness=error handling, Style=conventions |
| Customization | Template rubric, applies anywhere | Ground every criterion in task-specific details |
