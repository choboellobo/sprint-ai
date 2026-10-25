# sprint-ai

A Claude Code plugin for building software with AI **without letting go of the wheel**. Plan a sprint, build vertical user stories, and move work through a visible review flow.

The AI proposes scope, writes code in verified steps, and updates the board. You decide product requirements and sprint scope.

## The flow

```text
/backlog → /milestone → /sprint → /story → /pair → /qa
              optional       |
                          /board (view any time)
```

| Skill | What it does | What it never does |
|---|---|---|
| [`/backlog`](skills/backlog/SKILL.md) | Maintains `BACKLOG.md` with stable story IDs. | Invent requirements or split stories by technical layer. |
| [`/milestone`](skills/milestone/SKILL.md) | Groups product outcomes and their sprints in `MILESTONES.md`. | Declare a goal achieved from story counts alone. |
| [`/sprint`](skills/sprint/SKILL.md) | Selects stories and maintains the board in `SPRINT.md`. | Invent capacity or silently change scope. |
| [`/story`](skills/story/SKILL.md) | Refines one story into criteria, areas, a plan, and verification checks. | Write code. |
| [`/pair`](skills/pair/SKILL.md) | Implements an approved story; bare `/pair` pauses after one check, `/pair ... completa` finishes implementation. | Commit or weaken tests to make them pass. |
| [`/qa`](skills/qa/SKILL.md) | Checks acceptance criteria and records the result. | Mark unverified work `Done` or silently fix it. |
| [`/board`](skills/board/SKILL.md) | Opens a local browser dashboard for the backlog and sprint. | Change stories or status. |

The backlog contains **vertical stories**. Each story can carry several area tags: a login story might be `front, back`. `SPRINT.md` stores the current status; closed sprint snapshots live in `sprints/<ID>.md`. A story moves through `To Do` → `In Progress` → `In QA` → `Done`; `Waiting For` records an external blocker and the state to resume. `/pair` moves work to `In QA`, and `/qa` decides whether the criteria pass. Failed checks return to `In Progress`.

Each skill leaves an artifact for the next: `BACKLOG.md`, optional `MILESTONES.md`, `SPRINT.md`, archived `sprints/<ID>.md`, and approved `plans/<ID>-<name>.md` files. `/story` includes the verification checks in the plan, so `/pair` does not ask for a second approval. Use `/sprint` to close a sprint and `/milestone` to review whether a product goal is truly complete.

For example, `US-001` can be one login story tagged `front, back`. `/sprint` places it in `To Do`; `/story` defines the expected sign-in behavior; `/pair` changes it to `In Progress` and then `In QA`; `/qa` moves it to `Done` if the criteria pass. If a decision about the identity provider is missing, the row becomes `Waiting For` with the question and the state to resume.

## See the board

Run `/sprint-ai:board` after installing the plugin, or start the dashboard directly from a project that contains `BACKLOG.md`, `SPRINT.md`, or `MILESTONES.md`. From this source repository:

```bash
python3 skills/board/board.py --project /path/to/project
# Or preview the included example:
python3 skills/board/board.py --project examples/demo-project
```

The command prints a local URL and opens the browser. The dashboard has views for the current sprint, past sprints, and milestones, with status columns, progress, area filters, blockers, and story criteria. It refreshes every five seconds as the Markdown files change. It is read-only, runs on `127.0.0.1`, and needs only Python 3.9 or newer. Use `--no-open` if you want to open the printed URL yourself; stop the server with Ctrl+C.

## Principles

- **Don't invent.** Missing information gets asked, not filled in.
- **The simplest thing that works.** No abstractions "for the future".
- **Slice vertically and small.** Stories can touch front, back, and sistema; complete and verify one check before starting another.
- **Suggest, don't decide.** Patterns, refactors and commits are your call.
- **Clear checkpoints.** Agree on sprint scope and approve each story and its checks once. Choose interactive pacing or ask `/pair` to complete implementation.

## Install

Install it as a Claude Code plugin. This repository is also its own marketplace:

```text
/plugin marketplace add choboellobo/sprint-ai
/plugin install sprint-ai@sprint-ai
```

Plugin skills are namespaced: `/sprint-ai:backlog`, `/sprint-ai:milestone`, `/sprint-ai:sprint`, `/sprint-ai:story`, `/sprint-ai:pair`, `/sprint-ai:qa`, and `/sprint-ai:board`. They are invoked manually unless your project's own instructions route requests to them. To finish implementation in one turn, use `/sprint-ai:pair ... completa`; use bare `/sprint-ai:pair` to review one check at a time. Then run `/sprint-ai:qa` before treating the story as done.

To try a local checkout without installing it:

```bash
claude --plugin-dir /path/to/sprint-ai
```

---

By Eduardo Muñoz.
