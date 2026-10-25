---
name: story
description: Refines one backlog story into acceptance criteria, area tags, a short plan, and verification checks for approval. Writes no code.
disable-model-invocation: true
---

# Story

We refine a single story, right before building it. You propose and I decide.

## Steps

1. **Read the story** and its ID from `BACKLOG.md` (or the tracker I use). Review the current code and project context. If `SPRINT.md` exists, check whether the story is selected; do not add it to a sprint without my agreement.
2. **Acceptance criteria.** Propose 2–3 in Given/When/Then format. They only describe *what* the user sees or gets, never *how* it's implemented.
3. **If it needs more than 3 criteria, don't bloat it: propose splitting it.** Deliver the new stories in backlog format (`As a…, I want…, so that…`) for me to add to the tracker, and we continue with the first one.
4. **Areas and mini plan.** Mark all affected areas (`front`, `back`, `sistema`, or project-specific tags). A story may have several. In 5 bullets max, describe the smallest end-to-end change; mention files only when needed to make the plan clear. Do not split a vertical story by area.
5. **Verification.** For each criterion, name the observable check, where to run it (UI, API, etc.), and whether it is automated or manual. Include the expected result from the criterion. Do not write tests yet. Use the project's existing test tools; if none exist, state how the browser or another public interface will be checked.
6. **Wait for my approval.** Approval covers the criteria, areas, plan, out-of-scope list, and verification checks together. Save the approved block in `plans/<ID>-<short-name>.md`, then update its link and areas in `BACKLOG.md` and `SPRINT.md` if present. Leave sprint status unchanged.

## Rules

- **Don't invent requirements.** If information is missing, ask me.
- **The simplest thing that meets the criteria.** No abstractions, layers, configuration or patterns "for the future".
- **Suggest, don't decide.** If a pattern could help (Atomic Design, middleware composition, extracting a component…), mention it under "Suggestions" with its why. Only suggest it if there's a concrete signal in the code (for example, something that already repeats), not in advance.
- **Don't write code.**
- **No duplicate approval.** `/pair` uses the approved verification list from this plan; it does not ask me to approve the same list again.
- **Blocked refinement.** If a selected story cannot be refined without an external answer, set its sprint row to `Waiting For`. Record the question, who can answer, and `resume: To Do` in `Next action`.

## Output format

A block to save in `plans/<ID>-<short-name>.md` after approval. `/pair` uses it as input.

```markdown
## Story
ID: US-001
As a <actor>, I want <action>, so that <benefit>.

## Areas
front, back

## Acceptance criteria
- [ ] Given <context>, when <action>, then <result>.
- [ ] ...

## Plan
- ...

## Verification
- [ ] <check name> — <UI/API/etc.; automated/manual>. Expected: <observable result>.

## Out of scope
- <what's left out of this story, so it doesn't sneak in>

## Suggestions (your call)
- <optional>
```
