# Examples Reference

Good/bad pairs, JSON templates, and concrete patterns for Planning Imperium rubric criteria.

---

## Implementation vs Behavior

| Implementation (Bad) | Behavior (Good) |
|----------------------|-----------------|
| "Uses inter-process mutex" | "Concurrent access does not fail" |
| "Catches socket.error exception" | "Handles socket errors without crashing" |
| "Uses try/except ValueError" | "Rejects non-numeric strings with clear error" |
| "Calls `$ifNull` operator" | "Handles missing fields without query failures" |
| "Creates `is_str_int()` helper" | "Adds shared helper to validate numeric inputs" |
| "Uses `strings.HasPrefix`" | "Detects and processes prefixed strings" |
| "Filters channels using capability check" | "Enumerates channels without failing on non-CAN types" |
| "Re-raises as CanError" | "Errors expose diagnostic context to callers" |

---

## Vague vs Specific

| Vague (Bad) | Specific (Good) |
|-------------|-----------------|
| "Handles conversion correctly" | "Converts '123' to int 123, rejects '123.45' with ValueError" |
| "Properly validates input" | "Raises TypeError when non-string input provided" |
| "Works as expected" | "Returns float type for virt_file_size field" |
| "Handles edge cases for SHOW VARIABLES" | "Returns default 0 when userPreferences state is undefined" |
| "SEO friendly component" | "Includes `<title>`, `<meta description>`, and Open Graph tags" |

---

## Planning Criteria: Too-Specific vs Flexible

| Too Specific (Bad) | Flexible (Good) |
|--------------------|-----------------|
| "Plans to create `is_str_int()` in `utils.py`" | "Plans to add shared helpers in `utils.py` for numeric validation" |
| "Uses filelock library" | "Plans for inter-process synchronization mechanism" |
| "Plans to add `_stop_task()` method" | "Plan addresses stopping individual periodic tasks" |
| "Plan includes updating `CyclicSendTaskABC`" | "Plan identifies the base class for periodic task management needs changes" |
| "Plan identifies `__getattr__` needs modification" | "Plan identifies the recursive attribute access causing infinite loops" |

---

## Full JSON Examples

### Functional Criterion (Execution)

```json
{
  "id": "functional-1",
  "description": "The userPreferences reducer is integrated into the root reducer via app/redux/rootReducer.ts using the correct namespace key.",
  "weight": "major",
  "rationale": "The reducer must be properly combined with existing reducers (emissions, budget) for the state to be accessible and the feature to function.",
  "source": "problem",
  "dependent_on": []
}
```

Why it's good: Concrete, repo-specific, checks integration that shallow solutions miss.

### Robustness Criterion (Execution)

```json
{
  "id": "robustness-1",
  "description": "The getAcceptedTermsOfUseVersion selector returns a default value of 0 when the userPreferences state is undefined or missing, ensuring first-time users see the intro screen.",
  "weight": "major",
  "rationale": "For existing users upgrading the app (who have no prior acceptedTermsOfUseVersion in persisted state), the selector must safely return 0 so they are prompted to accept terms."
}
```

Why it's good: Names exact missing-state case and exact required behavior. No vague language.

### Style Criterion (Execution)

```json
{
  "id": "style-1",
  "description": "Follow the existing ducks pattern: keep actions, reducer, namespace, and selectors in dedicated files and export them via app/ducks/index.ts for consistency.",
  "weight": "minor",
  "rationale": "Maintains the project's expected module structure so future contributors know where to find user preference logic."
}
```

Why it's good: Points to explicit repo pattern and specific export location, not generic "conventions".

### Functional Criterion (Planning)

```json
{
  "id": "functional-1",
  "description": "Plan identifies that user preferences state must be added to the Redux store via rootReducer.ts",
  "weight": "major",
  "rationale": "Without root reducer integration, the state slice is inaccessible and the feature fails silently",
  "source": "problem",
  "dependent_on": []
}
```

---

## Stacking Examples

### Bad (Stacked - Two Independent Behaviors)

```json
{
  "description": "The API supports GET /groups/v1/locations/{location_id}/groups to return device groups for a location, and each group includes an updated_at timestamp parsed into a datetime object."
}
```

Problem: Endpoint existence and timestamp parsing are independent - split into two criteria.

### Acceptable (Single Indivisible Outcome)

```json
{
  "description": "PATCH endpoint returns 400 Bad Request with error message when JSON Patch operation targets non-existent path"
}
```

Why acceptable: Status code + error message describe a single unified endpoint behavior.

### Acceptable (Completeness Check)

```json
{
  "description": "The interface includes all of the fields: emissionType, emissionModelType, value, creationDate, and isMitigated"
}
```

Why acceptable: Single completeness check. Uses "all" to indicate the criterion passes only if every field exists.

---

## Planning Statement Tone

### Bad (System Language)

> "Create a comprehensive plan that addresses all functional requirements and integration points, ensuring proper handling of edge cases and validation strategies."

### Good (Real Engineer)

> "Hey, I need to add support for X in our Y system. Can you write up a plan before we start coding? I want to make sure we think through how this integrates with Z and what could go wrong."

### Bad (Leaks Solution)

> "The core files are in `can/` with `message.py` and `bus.py` being central."

### Good (No Leaks)

> "Before jumping into code, put together a plan."

---

## Golden Plan: Existing vs New Code

### Referencing Existing Code (Be Exact)

> "Modify the existing `validate_value` function in `cobbler/validate.py` to handle the new input type."

> "Wire the new reducer into `app/redux/rootReducer.ts` alongside the existing emissions and budget reducers."

### Describing New Code (Be Outcome-Focused)

> "Add a helper in `cobbler/utils.py` to validate whether a string represents a valid integer (reject non-strings, allow exact round-trip conversion), then reuse it in validators."

> "Create a new selector that safely returns a default value when the preferences state is missing."

---

## Category Decision Tree

```
Is it about WHETHER something exists or works?  -> Functional
Is it about WHAT HAPPENS when things go wrong?  -> Robustness
Is it about HOW code is written/organized?      -> Style
```

Common misclassifications:
- "Plan includes validation section" -> Functional (not Style)
- "UI includes length selector" -> Functional (not Robustness)
- "Code handles null input" -> Robustness (not Functional)
- "Uses kebab-case for filenames" -> Style (not Functional)
