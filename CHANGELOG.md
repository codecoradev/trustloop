# Changelog

## 0.4.0 (2026-11-23)

Smaller and faster, measured against 0.3.0 with the same eval cases.

- Rigor by risk: `rigor: auto | light | standard | full` and `high_risk_paths` in the config. Light changes get one review and no separate verification pass; high-risk paths always get full rigor.
- One review per branch, on the final diff, instead of per commit; re-review only after a change to the diff.
- Shorter instructions: the loop and review-gate skills were rewritten; exact Cora commands moved to `review-gate/references/cora.md`, read only when needed; recall starts with one Uteke call.
- Bridge: `cora_mcp.py prepare --compact` prints plain text with only the fields a reviewer needs (about 14 percent smaller), and `--skip-system-prompt` from the second round on (about 48 percent smaller).
- Verify reuses a full-suite result already obtained on the same commit; optional `models.verify` for a cheaper verifier model.
- Memory: `memory.author` gives every entry the same author name.
- The loop no longer proposes rewriting history to add or remove tool-appended commit lines.
- Light rigor now covers small changes (under ~50 lines in one module) pinned by a red-then-green test, not only changes without a behaviour change; `cora index` runs once at the start of the session.

## 0.3.0 (2026-11-23)

- One command: `/trustloop:loop` routes any request (task, ready-up a branch, question about the past, make a verifier, setup, or nothing for status) and runs setup in quick mode on first use instead of asking the user to run it.
- New `make-verifier` skill (adapted from pstack, MIT): creates a project-local verification skill with launch, doctor, drive, evidence and cleanup sections plus a feature map, and proves it by running it once. `verify` uses it when present and keeps the map current.
- New `glossary` skill (adapted from Matt Pocock's domain-modeling, MIT): GLOSSARY.md and ADRs, written lazily when a term or hard-to-reverse decision is settled.
- Setup: quick and full modes, must-ask questions only, optional extras (verification skill, CI review job). Setup is now model-invocable so the loop can call it.
- Remember: ADR and glossary changes are saved as pointers, not copies.
- NOTICE file with the MIT notices for the adapted material.

## 0.2.0 (2026-11-23)

- Review gate: tested against Cora 0.21.1. Added `skills/review-gate/scripts/cora_mcp.py`, a bridge that calls Cora's MCP tools (`review_prepare`, `review_finalize` and the intelligence tools) over stdio when the session has no Cora MCP server; the verdict is recorded the same way.
- Review gate: explicit path order (cora-review skill, MCP, bridge, CLI, fallback); guidance on deterministic findings (secrets are real until proven otherwise; index findings can be false positives).
- Loop: Cora code intelligence at each step (brain, callers, impact, affected, dead-code, debt) in `skills/loop/references/cora-intelligence.md`; defers to Cora's `cora-code` and `cora-review` skills when installed.
- Verify: run the tests Cora maps to the changed files.
- Setup: install recommendations for Cora (release binary, `cora install --dry-run` first) and a guide to choosing Uteke Cloud or self-hosted Uteke, including API key handling.
- Remember: record status changes of decisions (implemented, reverted, not followed).
- Config: new default human gate for rewriting shared git history; room ids of the form `project:<name>`.
- Evals: fixture scaffolds no longer commit their setup script; new case for message rules.

## 0.1.0 (2026-11-23)

- First version: loop, setup, recall, review-gate, verify, remember.
