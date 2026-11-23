# AGENTS.md — trustloop

trustloop is a Claude Code plugin made of Markdown skills (`skills/<name>/SKILL.md`, with `references/`, `assets/` and `scripts/` beside them) and one Python helper (`skills/review-gate/scripts/cora_mcp.py`, standard library only).

## Working on this repo

- Validate the plugin after any change to a manifest or a skill's frontmatter: `claude plugin validate . --strict`.
- Keep each `SKILL.md` short; move detail an agent needs only sometimes into `references/` and point to it from the step that needs it.
- Evals live in `evals/<case>/` (prompt, case.yaml, graders, fixture files). Run them with `claude plugin eval . --allow-tools Write,Edit,Bash --scaffold`; they are real, billed model runs.
- Fixtures must not contain real secrets or live-looking keys in their source; assemble test values at scaffold time (see `evals/review-gate-before-pr/files/setup-repo.sh`).
- Adapted third-party material keeps its notice in `NOTICE`.
- Update `CHANGELOG.md` and the version in `.claude-plugin/plugin.json` with every release.

## Session start (continuity ritual)

- New session: read and understand the team knowledge rooms before any work.
- Save every decision or important outcome back to the responsible room during or at the end of the session.
- Handing over mid-task: leave a [HANDOFF] entry (state, next step, blockers).

## Workflow summary

Issue → branch from develop → code + pre-commit checks → push → PR to develop (## What / ## Why / ## Testing, English) → CI green + review verdict → merge → cleanup → release (bump + CHANGELOG + tag). 1 issue = 1 branch = 1 PR.
