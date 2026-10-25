# Repository Guidelines

## Project Structure & Module Organization

`sprint-ai` is a Claude Code plugin with seven skills in `skills/`: `backlog`, `milestone`, `sprint`, `story`, `pair`, `qa`, and `board`. `.claude-plugin/` holds the plugin and marketplace manifests. `README.md` explains the workflow and installation. The consuming project stores `BACKLOG.md`, `MILESTONES.md`, `SPRINT.md`, archived `sprints/`, and approved `plans/`. `skills/board/board.py` and `skills/board/ui/` provide a local, read-only dashboard. Keep examples generic across stacks.

## Build, Test, and Development Commands

No build or package installation is required. Run `python3 -m unittest discover -s tests` for board parsing tests and `python3 skills/board/board.py --project examples/demo-project --no-open` to preview the dashboard. Run `git diff --check` for whitespace errors. Walk a sample story through `/backlog`, `/milestone`, `/sprint`, `/story`, `/pair`, and `/qa` when changing the workflow.

## Writing Style & Naming Conventions

Use Markdown headings, short imperative instructions, and concrete examples. Keep the YAML front matter at the top of each `SKILL.md` with the skill's `name`, `description`, and invocation setting. Directory names match slash commands: `skills/story/` defines `/story`. Preserve the skill names when editing. There is no formatter or linter; follow the existing Markdown style.

## Verification Guidelines

Check that `/story` outputs criteria, areas, a plan, verification checks, and out-of-scope items. `/pair` moves an active story to `In QA`; `/qa` alone marks it `Done`. Keep current status in `SPRINT.md` and preserve closed snapshots in `sprints/`. Test the dashboard against table and legacy numbered backlogs, archived sprints, and milestones. Review the README whenever a skill changes.

## Commit & Pull Request Guidelines

Recent commits use short English subjects, such as `Add MIT license` and `To english`. Keep commits focused on one workflow change. Pull requests should explain the user-facing behavior, link any related issue, show a before-and-after example when instructions change, and state how the workflow was checked. Do not edit installed copies in another project's `.claude/skills/` as a substitute for changing this repository.
