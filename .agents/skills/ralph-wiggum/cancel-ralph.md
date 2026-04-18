# Cancel Ralph Loop

Cancel an active Ralph Wiggum loop.

## Usage

```
/cancel-ralph
```

---
<command-name>cancel-ralph</command-name>

# Instructions

When the user invokes this command, acknowledge the cancellation:

```
[Ralph Loop] Cancellation requested.

To cancel a Ralph loop:
1. If running in terminal: Press Ctrl+C
2. If running via script: Kill the process with `pkill -f ralph`
3. If in Claude Code session: The loop will stop at the end of the current iteration

Note: Any work completed so far should be saved in output files.
Check the task directory for partial results.
```

If the user is running a loop within the current Claude Code session, acknowledge that loops are designed to complete when the completion promise is found or max iterations are reached. Manual cancellation requires user intervention (Ctrl+C or process termination).
