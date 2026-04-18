# Ralph Loop Skill

Start a Ralph Wiggum loop in the current session with a specific prompt and completion promise.

## Arguments

- `prompt` (required): The full prompt to execute in a loop
- `--completion-promise` (required): String that signals completion (e.g., "DONE", "REVIEW COMPLETE")
- `--max-iterations` (optional): Maximum iterations before stopping (default: 5)

## Usage

```
/ralph-loop "<prompt>" --completion-promise "<promise>" --max-iterations <n>
```

## How It Works

1. Executes the prompt in fresh context
2. Checks output for `<promise>COMPLETION_STRING</promise>`
3. If found, stops and reports success
4. If not found, continues to next iteration (up to max)
5. Reports final status

## Example

```
/ralph-loop "Analyze the codebase and output <promise>DONE</promise> when complete" --completion-promise "DONE" --max-iterations 3
```

---
<command-name>ralph-loop</command-name>

# Instructions

You are executing a Ralph Wiggum loop. Parse the user's arguments and execute the loop pattern.

## Parse Arguments

Extract from the user's command:
1. **prompt**: The quoted string after `/ralph-loop`
2. **completion_promise**: The value after `--completion-promise`
3. **max_iterations**: The value after `--max-iterations` (default: 5)

## Loop Execution

For each iteration (1 to max_iterations):

1. **Announce iteration**: `[Ralph Loop] Iteration {n} of {max}`
2. **Execute the prompt**: Treat the prompt as instructions and execute them
3. **Check for completion**: Look for `<promise>{completion_promise}</promise>` in your output
4. **If complete**: Report success and stop
5. **If not complete**: Continue to next iteration

## Completion Detection

When you complete the task described in the prompt, you MUST output:
```
<promise>{COMPLETION_PROMISE}</promise>
```

This signals the loop to stop.

## Example Output Flow

```
[Ralph Loop] Iteration 1 of 5
[Executing prompt...]
...work output...
[No completion signal found, continuing...]

[Ralph Loop] Iteration 2 of 5
[Executing prompt...]
...more work output...
<promise>DONE</promise>

[Ralph Loop] Complete! Finished in 2 iterations.
```

## Important Notes

- Fresh context each iteration (read files again, don't assume state)
- Write outputs to files for persistence between iterations
- The completion promise must match EXACTLY (case-sensitive)
- If max iterations reached without completion, report status and exit
