---
name: board
description: Opens a local read-only dashboard for backlog, current and past sprints, milestones, story status, areas, and blockers.
disable-model-invocation: true
---

# Board

Find the project directory containing `BACKLOG.md`, `SPRINT.md`, or `MILESTONES.md`. Run the `board.py` file beside this `SKILL.md` with that directory as `--project`; it opens a local browser dashboard and prints the URL. The server runs until stopped. If browser opening is unavailable, use `--no-open` and give the user the printed URL.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/board/board.py" --project .
```

If the path above was not expanded (the skill was copied by hand instead of installed as a plugin), use the `board.py` beside this `SKILL.md`. The dashboard is read-only and refreshes from `MILESTONES.md`, `SPRINT.md`, `sprints/*.md`, `BACKLOG.md`, and the linked plans. `/milestone`, `/sprint`, `/story`, `/pair`, and `/qa` remain responsible for updates. Do not create or change project data just to display the board.
