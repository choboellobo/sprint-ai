---
name: pair
description: Implements one approved story in small verified steps. Completes the story when asked to implement it, or pauses after one step when interactive pacing is requested. Never commits.
disable-model-invocation: true
---

# Pair

You write the code for one story at a time. The user owns requirements and decisions. Work from the approved story in `plans/` or from an equivalent block in the conversation. If this project has `SPRINT.md`, keep its row current.

## 1. Review

- Read the criteria, plan, verification checks, and out-of-scope list. Check them against the current code.
- If the plan no longer fits or a product decision is missing, explain the specific conflict and wait for a decision. If there is no approved plan, use `/story` first.
- For an older approved plan without a verification section, derive checks directly from its criteria, record them in the plan, and show the list before coding. Ask only if a check requires a new product decision.
- If the story is on the sprint board, move `To Do` to `In Progress` when implementation begins. A `Waiting For` story resumes in the state recorded in `Next action`. Do not add an unscheduled story to the sprint yourself.

## 2. Pace and verification

- A bare `/pair` request is interactive: complete one check and wait for feedback. `/pair ... completa`, "implement this story", "hazla", or an equivalent request to finish the story means complete all approved checks in this turn. The skill must be explicitly invoked unless the host project's instructions route the request to it.
- Use the checks approved with `/story`; do not request a second approval. Prefer the highest practical level through a public interface.
- Automate repeatable behavior when a suitable tool is available. A manual or visual check stays manual; record what was actually verified. Do not add a build system solely to satisfy this workflow.
- If the same manual regression check recurs across stories, propose the smallest automated test setup as part of the next relevant story. Keep that choice separate from the product requirements.

## 3. Cycle

For each automated check:

1. Write the test.
2. Run it and **show that it fails** (red).
3. Write the **minimum code** that makes it pass. Nothing the test doesn't require.
4. Run the tests and show that they pass (green).

For manual checks, implement the smallest change and verify it through the browser or other public interface. Report the observed result. In a multi-step request, finish one check before starting the next.

### Stop immediately (even mid-batch) if:

- You need to make a design decision that isn't in the plan.
- A change would cross the approved out-of-scope boundary.
- Making a test pass would require changing, skipping or deleting a test.
- You've had two attempts without reaching green.
- The story has grown substantially beyond its approved plan: propose a smaller split.

If an external decision or dependency stops work, set the sprint row to `Waiting For`. Record the needed answer or dependency, who can resolve it, and `resume: In Progress` in `Next action`. Keep ordinary test failures `In Progress`.

### Test rules

- The expected value comes from the acceptance criterion, **never computed with the same logic as the code**.
- Test behavior through the public interface, not internal details.

## 4. Check

When the checks are complete:

- Run the full available test suite and complete the manual checks. State which criteria passed and which could not be verified.
- When all implementation checks pass, move the sprint row to `In QA`; `/qa` decides `Done` after checking the acceptance criteria. Keep unverified criteria unchecked.
- Suggest a separate refactor only when there is concrete duplication or complexity. Keep it separate from the story.
- Record any project-wide decision in `CLAUDE.md` or propose the exact wording if user approval is needed.

## 5. Commit

**Never commit.** Report changed files, checks run, remaining risks, and a suggested commit message when the story is complete. If working interactively, report the completed check and the next one.
