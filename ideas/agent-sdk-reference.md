# Claude Agent SDK — Reference for Team Pulse

> Source: https://code.claude.com/docs/en/agent-sdk/overview
> Date captured: 2026-04-11

## What It Is

The Claude Agent SDK gives you the same tools, agent loop, and context management
that power Claude Code — programmable in Python and TypeScript. Claude autonomously
reads files, runs commands, edits code, and more.

## Install

```bash
pip install claude-agent-sdk          # Python
npm install @anthropic-ai/claude-agent-sdk  # TypeScript
```

## Auth

```bash
export ANTHROPIC_API_KEY=your-api-key   # from platform.claude.com
```

Also supports Bedrock, Vertex AI, and Azure.

## Core Pattern

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    async for message in query(
        prompt="Your task here",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Write", "Edit", "Glob", "Grep"],
        ),
    ):
        if hasattr(message, "result"):
            print(message.result)

asyncio.run(main())
```

## Built-in Tools

| Tool | What it does |
|------|-------------|
| Read | Read any file in the working directory |
| Write | Create new files |
| Edit | Make precise edits to existing files |
| Bash | Run terminal commands, scripts, git operations |
| Glob | Find files by pattern |
| Grep | Search file contents with regex |
| WebSearch | Search the web |
| WebFetch | Fetch and parse web pages |
| Agent | Spawn subagents for delegation |
| AskUserQuestion | Ask the user clarifying questions |
| Monitor | Watch a background script |

## Key Feature: setting_sources

```python
options=ClaudeAgentOptions(
    setting_sources=["project"],  # reads CLAUDE.md automatically!
)
```

This makes the Agent SDK read `CLAUDE.md` and `.claude/commands/` — the agent
understands our wiki schema, article format, and operations without us repeating
them in the prompt.

## Sessions (Conversation Memory)

```python
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

Sessions persist context. Follow-up questions work naturally.

## Subagents

```python
options=ClaudeAgentOptions(
    allowed_tools=["Read", "Glob", "Grep", "Agent"],
    agents={
        "wiki-compiler": AgentDefinition(
            description="Compiles raw sources into wiki articles",
            prompt="Read new raw files, update wiki following CLAUDE.md schema",
            tools=["Read", "Write", "Edit", "Glob", "Grep"],
        )
    },
)
```

## Hooks

```python
async def log_file_change(input_data, tool_use_id, context):
    file_path = input_data.get("tool_input", {}).get("file_path", "unknown")
    with open("./audit.log", "a") as f:
        f.write(f"{datetime.now()}: modified {file_path}\n")
    return {}

options=ClaudeAgentOptions(
    hooks={
        "PostToolUse": [
            HookMatcher(matcher="Edit|Write", hooks=[log_file_change])
        ]
    },
)
```

Available hooks: PreToolUse, PostToolUse, Stop, SessionStart, SessionEnd, UserPromptSubmit.

## How This Maps to Team Pulse

| Team Pulse Need | Agent SDK Implementation |
|---|---|
| `/compile-wiki` | `query(prompt="Compile new sources...", allowed_tools=["Read","Write","Edit","Glob","Grep"])` |
| `/morning-briefing` | `query(prompt="Generate morning briefing...", allowed_tools=["Read","Glob","Grep","Write"])` |
| `/eod-summary` | `query(prompt="Generate EOD summary...", allowed_tools=["Read","Glob","Grep","Write"])` |
| `/ask` (Q&A) | `query(prompt=user_question, allowed_tools=["Read","Glob","Grep"])` + sessions for follow-ups |
| Wiki health check | `query(prompt="Lint the wiki...", allowed_tools=["Read","Glob","Grep"])` |

With `setting_sources=["project"]`, the agent reads CLAUDE.md automatically —
it knows the wiki schema, article format, and everything about the system.

## CLI vs SDK

| Use case | Best choice |
|---|---|
| Interactive development | CLI (Claude Code) |
| CI/CD pipelines | SDK |
| Custom applications | SDK |
| One-off tasks | CLI |
| Production automation | SDK |

## Cost

API billing (per token), not Claude subscription. Estimated:
- Compile: ~$0.30-0.50/run (reads many files)
- Report generation: ~$0.10-0.20/report
- Q&A query: ~$0.25-0.50/query (depends on articles read)
