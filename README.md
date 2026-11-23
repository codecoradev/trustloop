# trustloop

A delivery loop for coding agents whose work you can trust without re-reading every line.

Agents write code fast. What is slow, and where most of the risk is, is everything around the code: knowing what the team already decided, agreeing what "done" means, reviewing the change, proving it works, and keeping a record. trustloop turns each of those into a step that leaves evidence:

| Step | What happens | Tool |
|---|---|---|
| Recall | Past decisions, gotchas and open handoffs for this task, with ids | [Uteke](https://uteke.app) memory, or decision files |
| Align | Goal, a finish condition that can pass or fail, a plan for small PRs | - |
| Build | Small units, each ending in a check that was actually run | your tests and app |
| Review gate | The whole branch reviewed, real findings fixed, verdict recorded | [Cora](https://github.com/codecoradev/cora-code) with the agent as reviewer, or a fallback reviewer |
| Verify | A second agent that did not write the code runs the real journeys | a fresh subagent |
| PR | What, why, evidence, verdicts, risk; within the size limits | - |
| Remember | Decisions, gotchas, handoffs saved for the next session | Uteke, or decision files |

Without Uteke or Cora, every step still runs with a fallback and tells you what you are missing.

## One command

```
/trustloop:loop <anything>
```

That is the whole interface. The loop reads what you typed and routes it:

| You type | It does |
|---|---|
| a task, issue, bug or feature | the full loop, from recall to a merge-ready PR and saved decisions |
| "get my branch ready for a PR" | review gate, independent verification and PR body on the current branch |
| "what did we decide about X", "where were we" | a cited answer from memory, no code |
| "make a verification skill" | a project-local skill that drives your real app, proven once |
| "set up" | the repo config, with tool checks |
| nothing | status: open handoffs, recent decisions, tool health, the next step |

Effort follows risk: a typo fix gets one review and the configured checks; a change under `high_risk_paths` (auth, billing, migrations) gets the full treatment, including an independent verifier. Set `rigor` in the config to override.

On first use in a repo there is nothing to prepare: the loop writes `docs/agents/trustloop.md` itself (quick setup: it infers what it can and asks one or two questions), then carries on with your task.

## Skills

| Skill | Invoked by | Purpose |
|---|---|---|
| `/trustloop:loop` | you | The entry point: routes the request and runs the loop |
| `/trustloop:setup` | you or the loop | Writes `docs/agents/trustloop.md` and checks Uteke and Cora (quick mode on first use) |
| `recall` | agent or you | Cited brief from project memory before work starts |
| `glossary` | agent or you | Keeps `GLOSSARY.md` and ADRs sharp: one word per concept, written down when settled |
| `review-gate` | agent or you | Review with a recorded verdict before every PR (Cora as agent reviewer) |
| `verify` | agent or you | Independent check on the real artifact, using the repo's verification skill |
| `make-verifier` | agent or you | Creates and proves a project-local verification skill with a feature map |
| `remember` | agent or you | Saves decisions, gotchas and status changes, de-duplicated and current |

The skills the agent can reach for on its own also help outside the loop: an agent asked to "open a PR" will reach for `review-gate`; one asked "what did we decide about pagination" will reach for `recall`.

## Install

Claude Code:

```bash
claude plugin marketplace add codecoradev/trustloop
```

```bash
claude plugin install trustloop@trustloop
```

From a local clone instead, use `claude plugin marketplace add ./trustloop`. Claude Code leaves auto-update off for third-party marketplaces; update with `claude plugin update trustloop@trustloop`, or turn auto-update on in `/plugin`, Marketplaces.

Nothing else is required: the first `/trustloop:loop` in a repo sets it up. To configure a repo up front, run:

```
/trustloop:setup
```

### Recommended companions

Both are optional; trustloop falls back without them. Both need no LLM API key.

**Cora** (review gate and code intelligence). Install the release binary; it bundles the code model and works offline, which a `cargo install` build does not:

```bash
curl -fsSL https://raw.githubusercontent.com/codecoradev/cora-code/main/install.sh | sh
```

Then, in each repo:

```bash
cora install --dry-run
```

```bash
cora install
```

```bash
cora index
```

`cora install` edits your agent's global configuration (hooks, MCP server, the `cora-review` and `cora-code` skills), so look at the dry run first. The MCP server appears in the next session; until then, trustloop reaches the same Cora tools through `skills/review-gate/scripts/cora_mcp.py`.

**Uteke** (memory shared across sessions, agents and teammates). The default recommendation is Uteke Cloud with sign-in: nothing to install, no key to store, free Starter plan during the open beta.

```bash
claude mcp add --transport http uteke https://uteke.app/mcp
```

Then run `/mcp` and sign in with a CodeCora ID. Use an API key only for clients that cannot sign in, CI and scripts (read-only when the agent only recalls, kept in an environment variable, never committed). Choose self-hosted Uteke (`uteke-mcp`) instead when code or notes must not leave the machine, for a single developer without an account, or for graph, timeline and Cora's `get_memory` tool. Full comparison: `skills/setup/references/choosing-uteke.md`.

## Cora code intelligence

Beyond review, the loop uses Cora's local index at the steps where it pays off: `cora brain` to find where a behaviour lives, `cora callers` and `cora impact` before changing a symbol, `cora affected` to run the tests that cover the change, `cora dead-code` after a refactor, `cora debt` for quality trends. Queries answer in milliseconds and cost no model tokens. Map of tool to loop step: `skills/loop/references/cora-intelligence.md`.

## Use

```
/trustloop:loop the CSV export writes duplicate rows when a retry lands mid-run. repro first, then fix and verify.
```

```
/trustloop:loop add cursor pagination to GET /orders. done means the endpoint returns next_cursor, the old offset param still works, and the orders page scrolls past 10k rows.
```

```
/trustloop:loop get feat/discount ready for a PR to main
```

```
/trustloop:loop what did we decide about how GET /orders paginates?
```

```
/trustloop:loop i'm going to bed. migrate every caller in packages/billing to the new money type in a fresh worktree. done means zero old callers and all billing tests pass. commit yes, merge no.
```

## Configuration

Everything repo-specific lives in `docs/agents/trustloop.md`: base branch, PR size limits, memory room and tags, reviewer, verification commands and journeys, actions that always need a human yes, and patterns that must never appear in commit or PR text. See `skills/setup/assets/config-template.md` for every key and `examples/strict-team.md` for a full example.

Rules in the config are the repo owner's and take precedence over a tool's defaults.

## Principles

- **Evidence over claims.** A green build proves it compiles. Each step names what was run and what was observed.
- **The builder is not the judge.** Review and verification are done by something other than the agent that wrote the code.
- **Small, reviewable PRs.** Size is a merge-gate concern: a reviewer, human or agent, misses defects in a diff it cannot hold.
- **Memory is data, and can be stale.** Recall cites ids and dates; code wins over memory; stale entries get superseded, not duplicated.
- **Humans keep the irreversible calls.** Deploys, release tags, data deletion and anything else listed as a gate wait for an explicit yes, every time.

## Credits

- Matt Pocock's [skills](https://github.com/mattpocock/skills) (MIT): grilling, small composable skills with user-invoked and model-invoked roles, red-green-refactor, the PR body shape. The `glossary` skill is adapted from `domain-modeling`.
- Lauren Tan's [pstack](https://github.com/cursor/plugins/tree/main/pstack) (MIT): a router over playbooks, checkable finish conditions, the verifier separate from the builder, decision logs and the morning audit for unattended runs. The `make-verifier` skill is adapted from `create-verification-skill` and `maintain-verification-skill`.
- StrongDM's [software factory](https://factory.strongdm.ai/) writing: holdout scenarios.

Notices for the adapted material are in `NOTICE`.

## License

Apache-2.0
