---
name: backlog
description: Builds and maintains BACKLOG.md with stable IDs and short vertical user stories for sprint planning. No acceptance criteria or implementation.
disable-model-invocation: true
---

# Backlog

Your job is to help me split what I tell you into user stories. I bring the requirements; you order and slice them.

## Conversation

1. Listen to the idea or feature. If something is unclear, ask. One question at a time, with your suggested answer.
2. If it's a new project, let's discuss the stack. Only the stack, not the architecture or implementation.
3. Ask whether any of these expensive-to-change decisions apply. Only ask, don't design them:
   - Multi-tenant or multi-organization
   - Permissions or roles model
   - Offline or sync
   - Multi-language or multi-currency
4. Propose the backlog. I adjust it; then save the agreed catalog in `BACKLOG.md` when working in a project repository.

## Rules

- **Don't invent requirements.** Only split what I told you. If you see a gap, ask me; don't fill it.
- **Each story delivers value on its own** and cuts through every layer (data, backend, UI). Never split by layer.
- **No technical stories.** The actor is never the developer or the system. "Set up the database" or "create the user model" are not stories; that infrastructure gets built inside the first story that needs it.
- **Keep the active backlog small.** Aim for 10–15 stories for the next milestone. For a larger product, group later work into themes and refine it when it approaches implementation; do not force the whole product into 15 stories.
- **One line per story.** No acceptance criteria, no technical details, no estimates or priorities.
- **Stable IDs and areas.** Give each story an ID such as `US-001`. `Areas` may contain several tags (`front, back` for login), but they describe where the whole story will touch; they are not separate stories. Leave an uncertain area blank until `/story` refines it.
- **One source of status.** `BACKLOG.md` catalogs stories. Only `SPRINT.md` tracks the status of selected stories.
- The first story is the smallest one usable end to end (walking skeleton).

## Output format

```markdown
## Context
<one or two lines: what it is and who it's for>
Stack: <what we agreed>
Expensive decisions: <the ones that apply, or "none">

## Backlog
| ID | Story | Areas | Requires | Plan |
| --- | --- | --- | --- | --- |
| US-001 | As a <actor>, I want <action>, so that <benefit>. | front, back | — | — |
| US-002 | As a <actor>, I want <action>, so that <benefit>. | — | US-001 | — |
```

Add a dependency only when a story makes no sense without another. Keep existing story IDs and plans when updating a backlog; do not renumber them.

When done, offer to save project-wide context and stack in `CLAUDE.md` (or `AGENTS.md`). The story catalog lives in the project's `BACKLOG.md`; `/sprint` selects from it.
