---
# trustloop config. Agents read this file at the start of every loop.
# Defaults are shown; delete a key to keep its default.

base_branch: main            # branch PRs target and diffs are taken against

rigor: auto                  # auto | light | standard | full: how much review and verification a change gets
high_risk_paths: []          # globs that always get full rigor, e.g. ["src/auth/**", "migrations/**", "billing/**"]

pr:
  language: English          # language of PR titles, bodies and commit messages
  sections: [What, Why, Testing, Risk]
  files_target: 15           # ideal number of changed files per PR
  files_ceiling: 20          # above this, split or write a reason in the PR
  lines_target: 1000         # ideal changed lines (added + deleted), lockfiles and generated code excluded
  lines_ceiling: 1500
  agent_may_merge: false     # true lets the agent merge after a clean review and verification

memory:
  backend: uteke             # uteke | files | none
  room: ""                   # Uteke room for this project, e.g. "project:acme-web"; empty = ask once, then save here
  tags: []                   # tags added to every memory, e.g. ["project:acme-web"]
  files_dir: docs/decisions  # used when backend is files, or as a fallback when Uteke is unreachable
  author: claude-code        # author name on every memory, so recall can tell who wrote what

reviewer:
  tool: cora                 # cora | fallback
  severity_blocking: [critical, major]
  ci_job: ""                 # name of the CI review job whose verdict gates merge, if any

verify:
  run: ""                    # how to start the app or the system under test, e.g. "pnpm dev"
  checks: []                 # commands that must pass, e.g. ["pnpm test", "pnpm lint"]
  journeys: []               # main user journeys to walk, in plain words
  scenarios_dir: ""          # optional holdout scenarios the builder must not read; only the verifier does

models: {}                   # optional model per role, e.g. {verify: sonnet, recall: haiku}; empty = session model

human_gates:                 # actions that always wait for an explicit yes from a human, every time
  - deploy to production
  - push a release tag
  - force-push a shared branch
  - rewrite git history (rebase, squash or filter commits already shared or reviewed)
  - delete data
  - send messages to customers

message_rules:
  forbidden_patterns: []     # regexes that must never appear in commit messages, PR titles, bodies or comments
---

# trustloop notes for this repo

Free text the agent should know: services to start, test accounts, known flaky tests, who approves what.
