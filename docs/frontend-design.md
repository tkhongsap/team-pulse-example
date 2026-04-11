# Team Pulse Frontend Design Spec

**Design reference:** claude.ai chat interface
**Framework:** Next.js + Tailwind CSS + shadcn/ui

---

## Layout: Three-Panel Design (claude.ai style)

```
┌─────────────────────────────────────────────────────────────────────────┐
│ ┌──────────────┐ ┌────────────────────────────────────────────────────┐ │
│ │              │ │  Header Bar                                        │ │
│ │   Sidebar    │ │  [Team Pulse]        [garrytan ▾]  [⚙]  [🌙/☀]  │ │
│ │   (280px)    │ ├────────────────────────────────────────────────────┤ │
│ │              │ │                                                    │ │
│ │ [+ New Chat] │ │                                                    │ │
│ │              │ │             Main Content Area                      │ │
│ │ ── Today ──  │ │                                                    │ │
│ │ 💬 Who is..  │ │   (Chat messages OR Dashboard view)                │ │
│ │ 💬 Busiest.. │ │                                                    │ │
│ │              │ │                                                    │ │
│ │ ── Reports ──│ │                                                    │ │
│ │ 📋 Morning   │ │                                                    │ │
│ │ 📋 EOD       │ │                                                    │ │
│ │ 📋 Dashboard │ │                                                    │ │
│ │              │ │                                                    │ │
│ │ ── Wiki ──   │ │                                                    │ │
│ │ 👤 Contrib.  │ │                                                    │ │
│ │ 📁 Projects  │ │                                                    │ │
│ │ 🔍 Patterns  │ │                                                    │ │
│ │              │ ├────────────────────────────────────────────────────┤ │
│ │              │ │                                                    │ │
│ │              │ │  [Ask anything about your team...]        [Send ➤] │ │
│ │              │ │                                                    │ │
│ └──────────────┘ └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 1. Sidebar (Left Panel)

**Width:** 280px (collapsible on mobile)
**Background:** `#f9fafb` light / `#1a1a2e` dark
**Border:** 1px right border `#e5e7eb`

### Sections

**New Chat Button** (top)
- Full-width button, `+ New Chat`
- Like claude.ai's new conversation button
- Opens empty chat in main area

**Quick Actions** (pinned)
- `📊 Morning Briefing` → generates/shows today's morning briefing
- `📋 EOD Summary` → generates/shows today's EOD summary
- `📈 Team Dashboard` → shows team health dashboard

**Chat History** (scrollable, grouped by date)
- Today / Yesterday / This Week / Earlier
- Each item: truncated question text, timestamp
- Click to load that conversation
- Same as claude.ai's conversation list

**Wiki Browser** (collapsible sections)
- `👤 Contributors` → garrytan, karpathy, damin-lee, ...
- `📁 Projects` → gstack, autoresearch
- `🔍 Patterns` → review-bottleneck, burnout-signals, stuck-items-growth
- `🔗 Connections` → sole-maintainer-and-stuck-growth
- Click any article to view in main area

**Reports Archive** (collapsible)
- Browse by date: `Apr 11`, `Apr 10`, `Apr 9`, ...
- Each date expands to show: Morning Briefing, EOD Summary

---

## 2. Header Bar

**Height:** 56px
**Background:** white / `#16213e` dark

```
[☰ (mobile)]  Team Pulse  |  Apr 11, 2026        [garrytan ▾]  [⚙]  [🌙]
```

- **Left:** Logo + "Team Pulse" text
- **Center:** Current date (clickable date picker to browse other days)
- **Right:** User avatar/name dropdown, settings gear, dark mode toggle

---

## 3. Main Content Area

This area switches between two modes:

### Mode A: Chat (default, like claude.ai)

```
┌────────────────────────────────────────────────────────────┐
│                                                            │
│   You                                           10:30 AM   │
│   ┌──────────────────────────────────────────────────┐     │
│   │ Who is at highest burnout risk?                  │     │
│   └──────────────────────────────────────────────────┘     │
│                                                            │
│   Team Pulse                                     10:30 AM   │
│   ┌──────────────────────────────────────────────────┐     │
│   │ Based on wiki data, **garrytan** is at highest   │     │
│   │ burnout risk.                                    │     │
│   │                                                  │     │
│   │ Evidence from [[contributors/garrytan]]:         │     │
│   │ - 10+ late-night commits across 5 of 8 days     │     │
│   │ - Sole reviewer for 54 open PRs                  │     │
│   │ - 15-hour work window on Apr 5 (03:59-18:43)    │     │
│   │                                                  │     │
│   │ Sources: garrytan.md, burnout-signals.md         │     │
│   └──────────────────────────────────────────────────┘     │
│                                                            │
│                                                            │
├────────────────────────────────────────────────────────────┤
│  [📎]  Ask anything about your team...          [Send ➤]   │
│         Model: Claude Sonnet  ▾                             │
└────────────────────────────────────────────────────────────┘
```

**Message styling (like claude.ai):**
- User messages: right-aligned or left with "You" label, light bg `#f3f4f6`
- AI messages: left-aligned with "Team Pulse" label, white bg
- Markdown rendering: headers, tables, bold, code blocks, lists
- Wiki links `[[contributors/garrytan]]` render as clickable chips
- Source citations shown at bottom of each response
- Streaming: text appears word-by-word as the Agent SDK streams

**Input area (bottom, like claude.ai):**
- Rounded text input, auto-expanding height
- Send button (right side)
- Attachment button (left side, for uploading docs to raw/)
- Model selector dropdown (optional)
- Suggested questions when chat is empty:
  - "Who is at highest burnout risk?"
  - "What should we address in tomorrow's stand-up?"
  - "Compare gstack and autoresearch health"
  - "Show me this week's trends"

### Mode B: Dashboard View

When user clicks a report or wiki article from sidebar:

```
┌────────────────────────────────────────────────────────────┐
│  ← Back to Chat          Morning Briefing — Apr 11, 2026   │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  # Morning Briefing — 2026-04-11                           │
│                                                            │
│  ## 1. Top Priorities Today                                │
│                                                            │
│  ### P1: Security PRs need immediate review                │
│  Two security PRs from Hybirdss open 2 days...             │
│                                                            │
│  ## 2. Status Board                                        │
│  ┌─────────────┬─────────────┬──────────────┐              │
│  │ Contributor │ Status      │ Action       │              │
│  ├─────────────┼─────────────┼──────────────┤              │
│  │ garrytan    │ In Progress │ Heavy load   │              │
│  │ karpathy    │ Stuck       │ Inactive 16d │              │
│  └─────────────┴─────────────┴──────────────┘              │
│                                                            │
│  ...rendered markdown continues...                         │
│                                                            │
├────────────────────────────────────────────────────────────┤
│  [📎]  Ask a follow-up about this report...     [Send ➤]   │
└────────────────────────────────────────────────────────────┘
```

**Key:** The input bar stays at the bottom in dashboard mode too — you can ask follow-up questions about what you're viewing.

---

## 4. Color Palette

### Light Mode (default)
| Element | Color | Hex |
|---------|-------|-----|
| Background | White | `#ffffff` |
| Sidebar bg | Light gray | `#f9fafb` |
| User message bg | Light gray | `#f3f4f6` |
| AI message bg | White | `#ffffff` |
| Primary accent | Indigo | `#4f46e5` |
| Text primary | Dark gray | `#111827` |
| Text secondary | Medium gray | `#6b7280` |
| Border | Light border | `#e5e7eb` |
| Stuck/alert | Red | `#ef4444` |
| In Progress | Green | `#22c55e` |
| Backlog | Yellow | `#eab308` |
| Idle | Gray | `#9ca3af` |

### Dark Mode
| Element | Color | Hex |
|---------|-------|-----|
| Background | Dark navy | `#0f172a` |
| Sidebar bg | Darker navy | `#1e293b` |
| User message bg | Dark slate | `#334155` |
| AI message bg | Dark navy | `#1e293b` |
| Primary accent | Light indigo | `#818cf8` |
| Text primary | White | `#f1f5f9` |
| Text secondary | Slate | `#94a3b8` |

---

## 5. Typography

| Element | Font | Size | Weight |
|---------|------|------|--------|
| Body text | Inter (or system) | 15px | 400 |
| Headings (h1) | Inter | 24px | 600 |
| Headings (h2) | Inter | 20px | 600 |
| Sidebar items | Inter | 14px | 400 |
| Code blocks | JetBrains Mono | 13px | 400 |
| Input placeholder | Inter | 15px | 400 |
| Status badges | Inter | 12px | 500 |
| Timestamps | Inter | 12px | 400 |

---

## 6. Key Components

### Status Badge
```
[● In Progress]  — green dot + green text + light green bg
[● Stuck]        — red dot + red text + light red bg
[● Backlog]      — yellow dot + yellow text + light yellow bg
[● Idle]         — gray dot + gray text + light gray bg
```

### Wiki Link Chip
When `[[contributors/garrytan]]` appears in a response:
```
[👤 garrytan]  — clickable pill/chip, indigo border, navigates to article
```

### Source Citation Block
At bottom of each AI response:
```
┌─ Sources ──────────────────────────────────────┐
│ 📄 garrytan.md  📄 burnout-signals.md  📄 gstack.md │
└────────────────────────────────────────────────┘
```
Each source is clickable — opens the article in dashboard mode.

### Suggested Questions (empty state)
When chat is empty, show 4 cards like claude.ai:
```
┌─────────────────────┐  ┌─────────────────────┐
│ 🔥 Who needs help?  │  │ 📊 Weekly summary   │
│ Burnout risk and    │  │ for management      │
│ stuck contributors  │  │                     │
└─────────────────────┘  └─────────────────────┘
┌─────────────────────┐  ┌─────────────────────┐
│ 📋 Today's brief    │  │ 🔍 Compare repos    │
│ Morning priorities  │  │ gstack vs           │
│ and action items    │  │ autoresearch        │
└─────────────────────┘  └─────────────────────┘
```

---

## 7. Responsive Design

### Desktop (>1024px)
- Sidebar visible (280px) + main area (remaining)

### Tablet (768px-1024px)
- Sidebar collapsed to icons only (60px), expandable on tap

### Mobile (<768px)
- Sidebar hidden, hamburger menu to open as overlay
- Full-width chat
- Input bar fixed at bottom

---

## 8. Tech Stack

| Component | Library |
|-----------|---------|
| Framework | Next.js 14+ (App Router) |
| Styling | Tailwind CSS |
| Components | shadcn/ui |
| Markdown | react-markdown + remark-gfm |
| Chat streaming | Vercel AI SDK or direct Agent SDK streaming |
| Auth | NextAuth.js (GitHub OAuth) |
| State | React context or Zustand |
| Deployment | Vercel |

---

## 9. Page Routes

```
/                    → Chat interface (default, like claude.ai)
/chat/:id            → Specific conversation
/reports             → Browse reports by date
/reports/:date/:type → Specific report (morning-briefing, eod-summary)
/wiki/contributors   → List contributors
/wiki/contributors/:name → Contributor article
/wiki/projects/:name → Project article
/wiki/patterns/:name → Pattern article
/settings            → User preferences, notifications
```
