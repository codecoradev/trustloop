---
name: loop
description: The single entry point to trustloop. Give it anything - a task ("fix the duplicate export rows"), a branch to get ready for a PR, a question about past decisions, "set up", or nothing at all - and it routes to the right flow, sets the repo up on first use, and carries the work end to end - recall memory, agree a checkable finish condition, build in small verified units, pass an agent review gate (Cora), verify independently, open a small evidence-backed PR, and save what was decided (Uteke). Use when the user types /trustloop:loop.
disable-model-invocation: true
---

# trustloop

One command for delivery you can trust without re-reading every line: memory before work, a finish condition before code, a review verdict before the PR, an independent check, a record after. This skill routes; the skills it calls hold the detail. Read a skill or reference only when its step comes up, so small tasks stay cheap.

## 1. Route

Say the route in one line ("Route: bug fix, full loop, rigor standard.").

| The user gave | Route |
|---|---|
| Nothing | **Status**: `recall` brief, open handoffs, config and tool health, next step. Stop. |
| "set up", "configure" | **Setup**: the `setup` skill. Stop. |
| A question about the past | **Ask**: `recall` (plus git history or `cora brain` if memory is thin). Answer with ids. No code. |
| "review", "ready for a PR", "check my branch" | **Ready-up**: steps 6 to 8 on the current branch. |
| "make a verification skill" | **Verifier**: `make-verifier`. |
| A task, issue, bug, feature, refactor, overnight run | **Full loop**: steps 2 to 8. |

Mixed requests take the widest route. If the wanted outcome is unclear, ask one question with your recommended answer.

## 2. Config and first use

Read `docs/agents/trustloop.md`. If missing, run `setup` in quick mode (infer everything, ask only its must-ask questions), then continue. If nobody can answer, use the defaults in `../setup/assets/config-template.md` and say so. Config rules win over tool defaults, including lines a tool would append to commit messages; never propose rewriting history just to add or remove such a line.

## 3. Rigor

Match the effort to the risk (`rigor` in the config; `auto` decides per change):

| Level | When (auto) | Review gate | Verify |
|---|---|---|---|
| **light** | outside `high_risk_paths`, and either docs, comments or config values, or a small change (under ~50 changed lines in one module) whose new behaviour is pinned by a test that fails without it; a small bug fix with a red-then-green test qualifies | once, on the final diff | the configured checks only; no separate pass |
| **standard** | everything else | once on the final diff, again only after fixes | journeys plus affected tests; reuse check results already run on the same commit |
| **full** | touches `high_risk_paths`, data migrations, auth, money, deletion; or the user asks | as standard, with fresh judgement on every round | independent agent required when the harness allows; holdout scenarios if configured |

Decide after the plan, revisit after the build (a change that grew moves up, never down below what it touches), and state the level in the PR.

## 4. Recall, locate, align

Run `recall` with the task as the query. Code is authoritative over memory; report conflicts. With Cora installed, run `cora index` once at the start of the session (reviews and queries on a missing index give empty or false findings), then find code with `cora brain "<task>"` and check reach with `cora callers`/`cora impact` (`references/cora-intelligence.md` if you need the full map). Use the words in `GLOSSARY.md`; when terms are vague or clash, use the `glossary` skill.

Then write back, before code: the **goal** and the smallest change that meets it; a **finish condition** that can pass or fail (not a duration); the **flow** (feature, bug fix, refactor, investigation, unattended; read `references/flows.md` for refactor and unattended runs, the others follow step 5); and a **PR plan** within the size limits. Ask only decisions that are the user's and that an experiment cannot settle, one question at a time with your recommendation. Keep a short checklist: `recall, align, build, review, verify, PR, remember`.

## 5. Build in verifiable units

Bug fix: reproduce first, turn it into a failing test, fix the first place it goes wrong. Feature: name the data shape, test at the outer seam, one vertical slice at a time. Each unit ends in a check you ran (a test going green, a command and its output, a value read back); a green build is not proof. Commit units that move the finish condition; discard ones that did not help. Run the tests that cover the change while iterating (`cora affected`), the full configured checks once before the review gate. One worker per worktree.

## 6. Review gate

Run `review-gate` once on the whole branch against the base, after the build is done; not per commit. Fix real findings (logic bugs get a failing test first) and re-review only what changed. Keep the verdict line.

## 7. Verify

Run `verify` at the level from step 3. If the change is user-facing and the repo has no way to drive the app, offer `make-verifier` once; do not block on it.

## 8. PR, then remember

Check the size (`git diff --stat <base>...HEAD`), write the PR with `references/pr-body.md`, apply the config's message rules to the title, body and every commit message. Stop at merge-ready unless the config allows merging; `human_gates` wait for an explicit yes every time.

Run `remember` for decisions, non-obvious gotchas, status changes of recorded decisions, and a handoff if work remains. At light rigor, only if something was decided.

## Reporting back

Lead with what changed for the user; evidence or a label (measured, inferred, guess) for each claim; the checklist with results; then what waits on the user, each with your recommendation.
