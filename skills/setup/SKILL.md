---
name: setup
description: Configure a repository for trustloop - base branch, PR size limits, Uteke memory room, Cora reviewer, verification commands, human approval gates and message rules - by writing docs/agents/trustloop.md and checking that Uteke and Cora are reachable. Use when docs/agents/trustloop.md is missing and trustloop is about to run, when the user types /trustloop:setup, or asks to set up or reconfigure trustloop in a repo.
---

# trustloop setup

Writes one file, `docs/agents/trustloop.md`, that every other trustloop skill reads. Run it once per repo; run it again to change a value. The file is plain Markdown with a YAML block on top, so humans can edit it directly too.

Two modes:

- **Quick** (when the loop finds no config on first use): infer everything, ask only the must-ask questions below, write the config, and hand back to the task in a couple of minutes. Offer the optional extras (a verification skill, CI review job) as one line at the end instead of doing them.
- **Full** (when the user asks for setup): the same, plus every question whose answer you could not infer, and the optional extras if the user wants them.

## 1. Read what is already known

Before asking anything, gather what the repo already says, so the user only confirms:

- Base branch: the remote default branch (`git symbolic-ref refs/remotes/origin/HEAD`), and whether a `develop` branch receives PRs.
- Checks: test, lint and type-check commands from `package.json`, `Makefile`, `justfile`, `Cargo.toml`, CI workflow files.
- How to run the app: README, `docker-compose.yml`, dev scripts.
- Existing conventions: `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, a PR template.
- An existing `docs/agents/trustloop.md`: start from it rather than the template.

## 2. Check the tools

**Uteke** (memory). Call `uteke_room_list` (or `uteke_stats`). If it answers, memory is available. If the tool does not exist, Uteke is not connected: recommend one option using `references/choosing-uteke.md`, give the user the exact steps, and continue with `memory.backend: files` meanwhile. The new server appears in the agent's next session.

**Cora** (review gate and code intelligence). Run `cora --version`, then check for the `cora` MCP server and the `cora-review` and `cora-code` skills. If Cora is missing, set `reviewer.tool: fallback` for now and recommend installing it:

1. The release binary, which bundles the code model and works offline (a `cargo install` build does not): `curl -fsSL https://raw.githubusercontent.com/codecoradev/cora-code/main/install.sh | sh`. The installer verifies the SHA-256 checksum, and the Sigstore signature when `cosign` is present.
2. `cora install --dry-run`, shown to the user, because `cora install` edits the agent's global configuration (hooks, MCP server, skills, instructions file). Then `cora install` once they agree.
3. `cora index` in the repo root.

Cora needs no API key: the agent is the reviewer. Until the agent restarts with the new MCP server, the review gate uses the bridge script `../review-gate/scripts/cora_mcp.py`.

Report what was found in two lines. Never print tokens, keys or the content of credential files while checking.

## 3. Ask only what you could not infer

Use the template in `assets/config-template.md`. Ask the user one question at a time, each with your recommended answer, only for values you could not find. In quick mode, ask only the questions marked **must-ask**; take the recommended answer for the rest and list them in the summary so the user can change them later.

1. **Must-ask when Uteke is connected and no room was named.** Which Uteke room holds this project's memory? Search first with `uteke_room_search` so you do not create a duplicate. If none fits, offer to create one (`uteke_room_create`) with an id of the form `project:<repo-name>` (lowercase, one colon); Uteke recommends `category:title` ids and will require them later.
2. Which actions need a human yes every time (`human_gates`)? Start from the template list. In the same question, propose `high_risk_paths` from what the repo has (auth, payments or billing, migrations, permissions, infrastructure); these always get full rigor.
3. **Must-ask.** Any patterns that must never appear in commit messages or PR text (`message_rules.forbidden_patterns`)? Some teams forbid certain trailers or footers; record them here, not in prose files.
4. May the agent merge after a clean review and verification (`pr.agent_may_merge`)? Default no.

## 4. Optional extras

- **Verification skill**: if the repo has a user-facing app and no scripted way to drive it, offer `make-verifier`; it makes every later `verify` step real.
- **CI review job**: if CI has no Cora review on pull requests, offer to add one (`../review-gate/references/cora.md`, section CI) as its own PR.
- **Glossary**: do not create an empty `GLOSSARY.md`; the `glossary` skill creates it when the first term is settled.

## 5. Write and confirm

Write `docs/agents/trustloop.md`, show the user the YAML block, and ask them to commit it with their next change. If the repo has an `AGENTS.md` or `CLAUDE.md`, offer to add one line pointing to the config: "Agent workflow config: docs/agents/trustloop.md". Keep internal policy text out of repo-visible files; the config holds values, not explanations of internal rules.

Add `.trustloop/` to `.gitignore` (it holds local decision logs) unless the user wants run logs committed.

If memory is on, save one memory in the room: the setup decisions (base branch, gates, reviewer), tagged with the configured tags.
