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

## Claude Agent SDK Reference

**Docs:** https://code.claude.com/docs/en/agent-sdk/overview

**Install:** `pip install claude-agent-sdk`

**Auth:** `export ANTHROPIC_API_KEY=your-api-key`

**Core pattern for Team Pulse scripts:**
```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    async for message in query(
        prompt="Your task description here",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Write", "Edit", "Glob", "Grep"],
            setting_sources=["project"],  # auto-loads CLAUDE.md from repo root
        ),
    ):
        if hasattr(message, "result"):
            print(message.result)

asyncio.run(main())
```

**Built-in tools (10):**

| Tool | What it does |
|------|-------------|
| Read | Read any file in the working directory |
| Write | Create new files |
| Edit | Make precise edits to existing files |
| Bash | Run terminal commands, scripts, git operations |
| Monitor | Watch a background script and react to each output line |
| Glob | Find files by pattern (`**/*.ts`, `src/**/*.py`) |
| Grep | Search file contents with regex |
| WebSearch | Search the web for current information |
| WebFetch | Fetch and parse web page content |
| AskUserQuestion | Ask the user clarifying questions with multiple choice |

**Key feature — `setting_sources=["project"]`:**
This makes the Agent SDK automatically read `CLAUDE.md` and `.claude/commands/*.md`
from the repo root. The agent understands the wiki schema, article format, and all
operations without repeating them in the prompt. USE THIS FOR ALL SCRIPTS.

**Sessions (conversation memory):**
```python
from claude_agent_sdk import query, ClaudeAgentOptions, SystemMessage

session_id = None
# First query — capture session ID
async for message in query(prompt="Read the wiki index", options=...):
    if isinstance(message, SystemMessage) and message.subtype == "init":
        session_id = message.data["session_id"]

# Resume with full context
async for message in query(
    prompt="Now find burnout signals",
    options=ClaudeAgentOptions(resume=session_id),
):
    ...
```

**Subagents:**
```python
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

async for message in query(
    prompt="Use the wiki-compiler agent to compile new sources",
    options=ClaudeAgentOptions(
        allowed_tools=["Read", "Glob", "Grep", "Agent"],
        agents={
            "wiki-compiler": AgentDefinition(
                description="Compiles raw sources into wiki articles",
                prompt="Read new raw files, update wiki following CLAUDE.md schema",
                tools=["Read", "Write", "Edit", "Glob", "Grep"],
            )
        },
    ),
):
    ...
```

**Hooks (audit logging example):**
```python
from claude_agent_sdk import query, ClaudeAgentOptions, HookMatcher

async def log_file_change(input_data, tool_use_id, context):
    file_path = input_data.get("tool_input", {}).get("file_path", "unknown")
    with open("./audit.log", "a") as f:
        f.write(f"{datetime.now()}: modified {file_path}\n")
    return {}

options = ClaudeAgentOptions(
    hooks={"PostToolUse": [HookMatcher(matcher="Edit|Write", hooks=[log_file_change])]}
)
```

**Streaming (for web app /api/ask route):**
```python
async for message in query(
    prompt=user_question,
    options=ClaudeAgentOptions(
        allowed_tools=["Read", "Glob", "Grep"],
        setting_sources=["project"],
        resume=session_id,  # conversation memory
    ),
):
    # Stream each message to the frontend via SSE
    yield message
```

**Cost estimates:**
| Operation | Cost |
|-----------|------|
| Compile wiki | ~$0.30-0.50/run |
| Generate report | ~$0.10-0.20/report |
| Q&A query | ~$0.25-0.50/query |
