# Cora for trustloop

Cora (cora-code) is a native CLI for code review and code intelligence. With no LLM configured, the coding agent itself is the reviewer: Cora supplies deterministic checks and review prompts, the agent judges, Cora validates and records the verdict. Source: https://github.com/codecoradev/cora-code

## Install

Use the release binary. It bundles the code embedding model and works offline; a `cargo install` build does not carry the model and downloads it on first use, which fails in sandboxed agent environments.

```bash
curl -fsSL https://raw.githubusercontent.com/codecoradev/cora-code/main/install.sh | sh
```

Pin a version with `CORA_VERSION=vX.Y.Z` before `sh`. The installer verifies the SHA-256 checksum, and the Sigstore signature when `cosign` is installed. Then, in the repo:

```bash
cora install
```

```bash
cora index
```

`cora install` sets up hooks, the MCP server and the `cora-review` and `cora-code` skills for Claude Code and other agents. `cora index` builds the symbol and meaning index the review uses. Re-run both after upgrading Cora (`cora upgrade`).

`cora install` writes to your agent's global configuration (for Claude Code: hooks in `~/.claude/settings.json`, the MCP server, skills under `~/.claude/skills/`, and a section in `~/.claude/CLAUDE.md`). Run `cora install --dry-run` first and show the user what it will change. A new MCP server becomes available in the next session; until then, use the bridge script `scripts/cora_mcp.py`.

For headless runs (`claude -p`), MCP tools ask for permission; the read-only intelligence tools can be allowed up front: `mcp__cora__cora_brain_search`, `mcp__cora__cora_search_symbols`, `mcp__cora__cora_find_callers`, `mcp__cora__cora_find_impact`, `mcp__cora__cora_find_affected_tests`.

If `which -a cora` shows more than one binary, remove the stale one; hooks run whichever is first on `PATH`.

## Agent review paths

Cora runs its deterministic checks and hands you review prompts with code intelligence; you judge with your own model; Cora validates, merges and records the verdict for the exact diff under `.git/cora/validations/`. Pass the same, unmodified diff to prepare and finalize. Index once per session (`cora index`); reviews refresh it.

1. **`cora-review` skill**: follow it.
2. **MCP server**: `cora.review_prepare` with `{"diff": "<diff>"}`; answer its `user_prompt` following its `system_prompt` as a JSON array shaped like `response_schema`, only for files in `valid_files`, without repeating `deterministic_findings`; then `cora.review_finalize` with the same diff and your array as `issues`. Read `should_block` and `commit_gate`.
3. **Bridge script** (Cora installed, no MCP server in this session), from the repo root:

   ```bash
   git diff <base>...HEAD > /tmp/review.diff
   ```

   ```bash
   python3 <plugin>/skills/review-gate/scripts/cora_mcp.py prepare /tmp/review.diff --compact
   ```

   Judge, write your findings as a JSON array to a file, then:

   ```bash
   python3 <plugin>/skills/review-gate/scripts/cora_mcp.py finalize /tmp/review.diff /tmp/issues.json
   ```

   From the second round on, add `--skip-system-prompt` to `prepare` when you still have the first round's reviewer instructions; it prints only their hash, which must match the first round's.
4. **CLI**: `cora review --base <base>` with a configured LLM, or `--no-llm` for the deterministic checks only, then judge yourself and say so.

## Before the first review: ignore noise

Dependencies, build output, generated code and snapshots add noise, cost and untrusted text to the review. Cora ignores the common ones; add project-specific paths to `.cora.yaml` before the first review.

## Useful commands

| Command | Use |
|---|---|
| `cora review --base <branch>` | Review the branch against its base |
| `cora review` | Review staged changes |
| `cora review --no-llm` | Deterministic checks only |
| `cora scan` | Audit the whole project (not a PR gate) |
| `cora brain "<question>"` | Find code by meaning while working |
| `cora callers`, `cora impact`, `cora affected` | Who calls a symbol, what a change can break, which tests to run (see `cora <command> --help`) |

## CI

Run a Cora review job on every pull request (GitHub: `codecoradev/cora-review-action`; Gitea, GitLab and Bitbucket examples in the Cora docs). Three rules keep it honest:

- The job fails when its required secrets are empty, instead of passing silently.
- Diff against the PR's own base branch (for example `origin/${{ github.base_ref }}`), not a fixed branch; a fixed `origin/develop` returns an empty review for PRs to `main`.
- In `pull_request_target` workflows, read `.cora.yaml` from the base branch, never from the PR.

## Pitfalls seen in practice

- The verdict is tied to the exact diff. Staging or editing anything afterwards needs a new review.
- With git worktrees, the MCP server records verdicts in the git directory of the checkout it runs in, while `cora hook verify` in a worktree reads `.git/worktrees/<name>/cora/validations/` (seen with cora 0.20). If the pre-commit hook does not see a verdict you just recorded, copy the validation file there; the hook still recomputes the fingerprint, so the gate is not weakened.
- Index findings ("unused import", "potentially dead code") were seen as false positives on a small Python module whose imports were used (cora 0.21.1). Confirm before acting.
- An LLM reviewer can be wrong about fast-moving frameworks (for example, flagging a config file that a newer major version removed). Check the installed package's types or docs, add a comment in the code explaining the choice, and record the reasoning in the PR.
- Very large diffs take long and produce noisy deterministic findings that hide real ones. Keep PRs within the configured size.
