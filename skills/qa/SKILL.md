---
name: qa
description: Reviews a completed story against its acceptance criteria and verification checks, then updates the sprint board with the evidence-based result.
disable-model-invocation: true
---

# QA

Review one implemented story, normally in `In QA`. Read its approved plan, implementation, and `SPRINT.md` if present. Use a fresh check of observable behavior; do not treat `/pair`'s report as proof. Do not implement fixes in this skill.

## Check

1. Run the project's relevant automated tests and the plan's manual checks. Compare each result with the criterion's expected behavior. Note any check you could not perform.
2. If all criteria pass, mark their checkboxes in the plan and move the sprint row to `Done`. Clear `Next action` or record a concise completion note.
3. If behavior fails, leave the criterion unchecked, move the row to `In Progress`, and put the concrete failure in `Next action` for `/pair` to fix.
4. If an external decision, environment, or dependency prevents checking, set `Waiting For` and record what is needed, from whom, and `resume: In QA`. Do not call an unverified story `Done`.

If there is no sprint board, report the same findings without creating one. Do not change the approved acceptance criteria to make implementation pass. Never commit.

## Report

List passed, failed, and unverified criteria with the command or manual action used. State the resulting status and the next action. Keep the report short enough for the user to decide what to do next.
