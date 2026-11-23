---
name: verify
description: Independently verify that a change actually works before it is merged - a fresh agent that did not write the code re-runs the finish condition and the main user journeys on the real artifact (running app, real command, stored value, measurement), optionally against holdout scenarios the builder never saw, and reports what it observed as PASS, ISSUES or BLOCKED. Use after implementation and review and before calling a PR ready, when the user asks "does this really work", "verify the fix", "prove it", or when a builder's own "tests pass" is the only evidence.
---

# verify

The agent that wrote the code is the worst judge of it: it knows what it meant, not what it did, and its tests can be written to pass. Verification is done by someone else, on the real thing.

Read `docs/agents/trustloop.md` for `verify.*`, `rigor` and `models.verify`.

How much to run depends on the rigor the loop chose: **light** needs no separate pass (the builder's configured checks are the evidence); **standard** runs the journeys and the affected tests, and reuses the full-suite result when it already passed on this same commit; **full** runs everything, including holdout scenarios, by an independent agent whenever the harness allows one.

## 1. Brief a fresh verifier

Spawn a new subagent with a fresh context (not a fork of the builder's conversation), on the model named in `models.verify` if set. Give it only:

- the goal and the finish condition, in the words agreed with the user;
- the branch or commit to check out, and how to run the system: the repo's verification skill (`.claude/skills/verify-*/`, made by `make-verifier`) when one exists, with its feature map, otherwise `verify.run`;
- the checks and journeys from the config, plus any journey this change adds;
- the tests that cover the changed files, when Cora is installed (`cora affected` against the base branch), and the full-suite result if it already passed on this commit;
- the path to holdout scenarios in `verify.scenarios_dir`, if configured. The builder must not have read these; that is what makes them a fair test.

Tell it not to change code, and to report observations, not opinions. Do not pass the builder's summary or its claims; they are what is being checked.

No subagents available: do the pass yourself as a separate step, from the brief alone, and label the result "self-verified, not independent".

## 2. Match the evidence to the change

| Change | Evidence that counts |
|---|---|
| CLI or script | The real command, its exit code and output |
| UI | The changed flow walked in the running app, with screenshots of before and after states |
| API | Real requests and responses, including an error path |
| Storage or migration | The value read back from storage; a replay of real or realistic input |
| Performance | Before and after measurements under the same conditions, with what limits the number |
| Bug fix | The original reproduction now behaving correctly, plus the new test failing on the old code |

A passing build, a type check, or "the tests are green" are inputs, not verification.

## 3. Report

The verifier returns, and you pass on unchanged:

```
Verify on <short sha>: PASS | ISSUES | BLOCKED
Checked:   <each check or journey> -> <observed result, with command/output or screenshot path>
Issues:    <what went wrong, steps to reproduce>
Not checked: <what could not be run, and why>
```

If a journey in the feature map no longer matches the app (renamed control, new entry point, removed command), report it as ISSUES and update the map with the change, per `make-verifier`.

ISSUES go back to the builder as a fix round; after the fix, verify again on the new commit with a fresh verifier. BLOCKED (cannot start the app, missing access) is reported to the user as is; never turn a blocked check into an assumption that it works.

The final verdict line goes into the PR's Testing section.
