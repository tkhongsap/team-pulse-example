# Ralph Wiggum Help

Explain the Ralph Wiggum technique and available commands.

## Usage

```
/help
```

---
<command-name>help</command-name>

# Instructions

Explain the Ralph Wiggum technique to the user:

## What is Ralph Wiggum?

Ralph Wiggum is an autonomous loop pattern for AI agents that enables long-running, iterative tasks. Named after the Simpsons character, it follows a simple philosophy:

> "Constrained context, backpressure, autonomous action, and human oversight over the loop - not in it."

## Core Concepts

### Fresh Context Each Iteration
Each loop iteration starts with fresh context. State is persisted through files (like `review-report.md`), not memory. This prevents context drift and keeps the AI in its "smart zone."

### Completion Promises
The loop continues until it sees a specific completion signal:
```
<promise>COMPLETION_STRING</promise>
```

This ensures the agent knows when work is truly done.

### File-Based State
- Write outputs to files for persistence
- Read files at the start of each iteration
- Don't assume state from previous iterations

## Available Commands

| Command | Description |
|---------|-------------|
| `/ralph-loop` | Start a Ralph loop with a custom prompt |
| `/review-planning-task` | Review a Planning Imperium task |
| `/cancel-ralph` | Cancel an active Ralph loop |
| `/help` | Show this help message |

## Example Usage

### Start a Ralph Loop
```
/ralph-loop "Analyze the codebase and write findings to analysis.md. Output <promise>DONE</promise> when complete." --completion-promise "DONE" --max-iterations 5
```

### Review a Planning Task
```
/review-planning-task imperium-planning/swebench/tasks/hardbyte-python-can-887
```

## Best Practices

1. **Be specific in prompts** - Include what files to read/write
2. **Set appropriate max iterations** - Default is 5, increase for complex tasks
3. **Use clear completion signals** - Make sure the promise is unambiguous
4. **Check output files** - Results are written to files, not just displayed

## Reference

For more details on the Ralph methodology, see:
- `ralph-instruction/ralph-playbook.md` - Full Ralph methodology
- `ralph/ralph.sh` - Shell script implementation
