---
name: milestone
description: Plans and tracks product milestones in MILESTONES.md, linking them to one or more sprints without replacing story-level status.
disable-model-invocation: true
---

# Milestone

Use a milestone for a user-visible product outcome that may require several sprints. `MILESTONES.md` is the milestone catalog; `SPRINT.md` and `sprints/` hold the actual story status. Work in the user's project, not in the `sprint-ai` distribution repository.

## Create or update

1. Read project context, `BACKLOG.md`, `SPRINT.md`, archived `sprints/`, and existing `MILESTONES.md`.
2. Propose a stable ID (`M-001`), a short name, and an outcome that can be checked. Ask for a target date only if the user wants one; do not invent dates or capacity.
3. After the user agrees, add or update one row. New milestones start `Planned`. Keep IDs stable and preserve existing sprint links.
4. When `/sprint` starts a sprint for the milestone, append that sprint ID to `Sprints` in chronological order and set the milestone `Active`. A sprint may belong to one milestone; a milestone may span many sprints.
5. Mark `Done` only after checking the milestone goal with the user and confirming the necessary stories. Story count alone is not proof that the product outcome works.

```markdown
# Milestones

| ID | Name | Goal | Status | Target | Sprints |
| --- | --- | --- | --- | --- | --- |
| M-001 | Acceso personal | El usuario puede entrar y consultar sus tareas. | Active | — | SP-001, SP-002 |
```

Statuses are `Planned`, `Active`, and `Done`. `Target` is optional. Do not duplicate each story's status here. `/board` shows milestones, linked current and archived sprints, and progress based on the latest status of each story across those sprints. Never commit.
