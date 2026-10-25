---
name: sprint
description: Plans and tracks a sprint in SPRINT.md using backlog stories, area tags, and explicit workflow states. Does not implement stories.
disable-model-invocation: true
---

# Sprint

Use `BACKLOG.md` as the story catalog and `SPRINT.md` as the single source of truth for the current sprint's status. Work in the user's project, not in the `sprint-ai` distribution repository.

## Start a sprint

1. Read project context, `BACKLOG.md`, existing plans, `MILESTONES.md` if present, and any current `SPRINT.md`. Do not replace an active sprint silently.
2. Propose a sprint goal and a small set of story IDs that fit it. Check dependencies. Ask for a date or capacity only when it affects selection; never invent estimates or deadlines.
3. Let the user adjust the scope. Once agreed, assign a stable sprint ID (`SP-001`, then `SP-002`, etc.) and write `SPRINT.md` with the goal, optional dates, optional milestone ID, and board below. New rows start in `To Do`.
4. If linked to a milestone, append the sprint ID to that row's `Sprints` field in `MILESTONES.md` and set it `Active`. Do not invent a milestone or change its goal.
5. Keep story text and dependencies in `BACKLOG.md`; link each row to its plan if one exists. `SPRINT.md` owns status so it is never copied into the backlog.

```markdown
# Sprint: <name>

ID: SP-001
Goal: <user-visible outcome>
Dates: <only if agreed>
Milestone: M-001

## Board
| ID | Story | Areas | Status | Plan | Next action |
| --- | --- | --- | --- | --- | --- |
| US-001 | As a user, I want to sign in... | front, back | To Do | — | Refine with /story |
```

`Areas` are multi-value tags for the work a **whole vertical story** touches: `front`, `back`, `sistema`, or project-specific terms. A login story can be `front, back`; do not split it into separate stories by layer.

## States

- `To Do`: selected for this sprint, not started.
- `In Progress`: implementation has begun.
- `In QA`: implementation checks pass; acceptance review is pending.
- `Waiting For`: an external decision or dependency blocks progress. In `Next action`, record who or what is awaited and the state to resume (`To Do`, `In Progress`, or `In QA`).
- `Done`: `/qa` has confirmed every acceptance criterion.

`/pair` moves a story to `In Progress`, then `In QA`; `/qa` moves it to `Done` or back to `In Progress`. `/story`, `/pair`, and `/qa` may set `Waiting For` for a genuine external blocker. A failing test is work to fix, not a blocker. When the blocker clears, restore the recorded state. Never mark `Done` merely because code was written.

## Inspect or close

When asked for status, read the board and report counts, blockers, and the next actionable story. Suggest `/board` when the user wants a visual dashboard. On sprint close, show completed and unfinished IDs. With the user's chosen carry-over scope, archive the exact final board as `sprints/<ID>.md`, then create the next `SPRINT.md` with a new ID. Never overwrite an archived sprint or discard unfinished work. A carried story may appear in both files; the newer sprint records its current status.
