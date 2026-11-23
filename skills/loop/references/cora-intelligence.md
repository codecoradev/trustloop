# Cora code intelligence in the loop

Cora keeps a local index of the project: symbols, a call graph and a code embedding model. Queries answer in milliseconds and cost no model tokens, so reach for them before grepping or guessing file names. When the `cora-code` skill is installed (by `cora install`), it explains each tool; this page says *when* in the loop each one pays off.

Three ways to call the same tools, in order of preference:

1. **MCP** (server registered by `cora install`; some agents show names with underscores, e.g. `cora_brain_search`).
2. **Bridge**, when the session has no Cora MCP server (it started before `cora install`, or it cannot add servers): `python3 <plugin>/skills/review-gate/scripts/cora_mcp.py call <tool> '<json>'`, run from the repo root.
3. **CLI**: the commands in the table.

Run `cora index` once at the start of a session, or when a tool reports that there is no index. Reviews and scans bring the index up to date themselves, so do not re-index before every query. The index finds candidates; read the files it points to before relying on them.

| Loop step | Question | MCP tool | CLI |
|---|---|---|---|
| Recall / Align | Where is this behaviour implemented? | `cora.brain_search` `{"query": "<words>"}` | `cora brain "<words>"` |
| Recall / Align | Where is this name defined? | `cora.search_symbols` | `cora explore <name>` |
| Align | What does the system look like? | - | `cora arch`, `cora routes` (HTTP endpoints) |
| Build, before changing a symbol | Who calls it? | `cora.find_callers` | `cora callers <symbol>` |
| Build, before changing a symbol | What breaks if it changes? | `cora.find_impact` | `cora impact <symbol>` |
| Build | How does execution reach it? | `cora.query` (`"* -> name"`) | `cora trace <symbol>`, `cora query "* -> name"` |
| Build, refactor | Is the old code now unused? | `cora.dead_code` | `cora dead-code` |
| Verify | Which tests cover the changed files? | `cora.find_affected_tests` | `cora affected` (reads the git diff) or `cora affected <files>` |
| Review gate | Deterministic rules, secrets, index findings | `cora.review_prepare` / `cora.review_finalize` | `cora review --base <branch> --no-llm` |
| Remember / retro | Is quality trending up or down? | `cora.get_debt` | `cora debt` |

How to use the answers:

- **Plan the PR from the impact list.** If `impact` reaches more callers than one PR can hold within the size limits, that is the signal to split by layer or to migrate callers in a follow-up.
- **Targeted tests first, full suite before the PR.** `affected` tells you what to run while iterating; the configured `verify.checks` still run before the review gate.
- **Treat index findings as leads.** In small or dynamic code (Python, JavaScript), "unused import" and "dead code" findings can be false positives; confirm by reading the code. Secret findings are never dismissed without proof that the value is not real.
- **`cora.get_memory` reads the local `uteke` CLI only.** With Uteke Cloud, recall through the Uteke MCP tools (the `recall` skill) instead.
