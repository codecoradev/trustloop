# Flows

Pick the flow that matches the task and copy its steps into your todo list. Every flow sits inside the loop: recall and align come before, review gate, verify, PR and remember come after (except where a flow says otherwise).

## Feature

1. Name the data shape and the interface callers will use, before any logic.
2. Write the first failing test at the outer seam (what a user of the code observes), not at an internal helper.
3. Build one vertical slice that makes it pass end to end. Then the next slice.
4. Walk the feature in the running app or run the real command. Capture what you saw.
5. If the feature sits behind a flag, verify both flag states.

## Bug fix

1. Reproduce first. Write down the exact steps and the observed vs expected result.
2. Turn the reproduction into a failing test (or a script that fails) before touching the fix.
3. Find the first place the system went wrong and fix it there. A guard that hides the symptom is a fix only when the state it handles is legitimate.
4. Show the test going from red to green, and re-run the original reproduction on the real artifact.
5. If two fixes that share one assumption have failed, stop and test the assumption directly before writing a third.

## Refactor

1. State the behavior that must not change and how you will prove it (existing tests, a snapshot of outputs, a recorded run).
2. Remove dead code and redundant layers first, then reshape on the simpler base.
3. Migrate callers and delete the old API in the same change where the size limit allows; otherwise plan the PR stack so each PR stays green on its own.
4. Prove behavior is unchanged with the check from step 1, not by reading the diff.

## Investigation (read-only)

1. Answer the question from evidence: code, git history, PR discussions, logs, measurements. Mark each claim as found, inferred or guessed.
2. Write no code unless the user asks. Skip the review gate and PR.
3. Save the answer with `remember` if it took effort to find and will be asked again.

## Unattended run (user is away)

Before leaving, the run needs a contract. Write it back to the user and get a yes:

- **Goal** and **finish condition** that each iteration can check.
- **Permissions**: what the agent may do alone (commit, push its own branch, open PRs) and what it may not (merge, deploy, anything in `human_gates`). Default: commit and push the task branch yes, merge no.
- **Isolation**: a fresh worktree or a cloud agent, so the run collides with nothing.
- **Escape hatch**: when truly stuck, stop and write a blocker report instead of reinterpreting the goal.

Then loop: check the finish condition, make the smallest justified change, verify it on the real artifact, commit if it helped or discard if not, write one decision-log row, repeat. Never relax the finish condition quietly to declare success.

Decision log: a TSV at `.trustloop/runs/<task-slug>.tsv` with columns `time  phase  decision  reason  evidence  result`. Keep it local by default; commit it when a reviewer needs the trail.

When the user is back, report in review form: what landed, what is waiting on them, and an **Attention** section listing what deserves suspicion, each item pointing at its log rows. If you can, have an agent on a different model family read the log before you write that section.
