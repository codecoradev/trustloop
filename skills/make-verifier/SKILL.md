---
name: make-verifier
description: Create (or repair) a project-local verification skill that drives this repo's real app the way a user does - launch, health check, drive, capture evidence, clean up - plus a feature map of the main user journeys, and prove it by running it once. Works for web, CLI, API, desktop or library projects in any language. Use when a repo has no scripted way to prove behavior, when the verify step had nothing real to run, when a feature map has drifted from the app, or when the user asks to "make a verification skill", "make the agent able to test the app", or "set up verification".
---

# make-verifier

Agents claim a change works; a verification skill lets them prove it, every time, the same way. This skill writes one for the repo at `.claude/skills/verify-<app>/` (or the harness's project skill folder, for example `.agents/skills/` or `.cursor/skills/`). Write it for the next agent, who will read it cold, mid-task, having never seen the app.

Adapted from the `create-verification-skill` and `maintain-verification-skill` skills in Lauren Tan's pstack (MIT).

## 1. Learn the repo, not the user

Answer from the code; ask the user only what you cannot observe:

- **Surface**: what a user touches (web UI, CLI or TUI, API, desktop, mobile, library). Pick the primary one; note the rest.
- **Run**: the repo's own dev command (package scripts, Makefile, README). Ports, environment variables, seed data, auth, test accounts.
- **Drive**: existing harnesses first (Playwright or Cypress specs, HTTP examples, PTY or expect scripts). Otherwise a generic recipe: a browser driver for web, a PTY or tmux session for CLI and TUI, plain HTTP for services, a short script for libraries.
- **Observe**: screenshots, terminal transcripts, response bodies, exit codes, logs, stored values.
- **Isolate**: can two instances run side by side (ports, data dirs)? If not, the skill must refuse to drive an instance it did not start.

If the checkout does not build or start, fix that or report it precisely first; a skill written against a broken base teaches wrong steps. With Cora installed, `cora routes` lists HTTP endpoints and `cora arch` the module layout, which speeds up this step.

## 2. Write the skill

`.claude/skills/verify-<app>/SKILL.md` with frontmatter (`name: verify-<app>` and a description naming the app, its surface and when to use it; without frontmatter it never loads) and these sections, each filled from what step 1 found, with no placeholders left:

- **Launch**: the exact command, how to tell it is ready (usable, not just a process answering), starting from an empty data dir with migrations and seed data. For a short CLI: build once, then run each check in its own isolated directory.
- **Doctor**: one read-only check: is this instance ours, the right build, ready to drive?
- **Drive**: real commands and stable handles from this repo (accessible names, data attributes, route paths, prompt strings), not examples and not coordinates.
- **Evidence**: what to capture and where it is kept. Exercise the real user path, not test-only setters; capture the action and the resulting state; check side effects (files written, rows stored, messages sent) as well as what is visible.
- **Cleanup**: stop what this run started (never kill by process name) and remove scratch state; keep the evidence.
- **Helpers**: any script it ships is executable and its invocation is written in the skill.

## 3. Seed the feature map

`.claude/skills/verify-<app>/features/README.md` (baseline preconditions, driving conventions, how to report a proof or a skip, and an index) plus one file per user-facing feature, the top 3 to 5 to start. Format: `references/feature-map.md`. If seed data lacks a precondition a journey needs, the journey fails and the reason goes in that feature's Gotchas; never weaken a journey to make it pass.

## 4. Prove it before handing it over

Run the generated skill once, end to end: launch, doctor, drive one mapped feature, capture evidence, clean up, then confirm the evidence still exists. Fix what fails and run cleanup after every failed attempt. A verification skill that was never run is a draft.

## 5. Wire it in

If `docs/agents/trustloop.md` exists, set `verify.run` and `verify.journeys` to point at the new skill (for example `verify.run: "see .claude/skills/verify-<app>"`). Tell the user the skill exists and that the `verify` step will use it.

## Maintaining it

When `verify` finds that a journey no longer matches the app (a renamed button, a new entry point, a removed command), update the feature map in the same PR as the change that caused it, prove the changed journey once, and say so in the PR. Keep one source of truth: the map, not notes scattered in PR descriptions.
