---
# Example: a team that integrates on develop, releases from main,
# keeps PRs small, and gates every merge on a CI review job.
# Copy to docs/agents/trustloop.md and adjust.

base_branch: develop

pr:
  language: English
  sections: [What, Why, Testing]
  files_target: 15
  files_ceiling: 20
  lines_target: 1000
  lines_ceiling: 1500
  agent_may_merge: false

memory:
  backend: uteke
  room: "project:acme-web"
  tags: ["project:acme-web"]
  files_dir: docs/decisions

reviewer:
  tool: cora
  severity_blocking: [critical, major]
  ci_job: "Cora Review"

verify:
  run: "docker compose up -d && pnpm dev"
  checks: ["pnpm test", "pnpm lint", "pnpm typecheck"]
  journeys:
    - sign in, create an order, pay with the test card, see the receipt
    - export orders as CSV twice in a row; the file has no duplicate rows
  scenarios_dir: ""

human_gates:
  - deploy to production
  - push a release tag
  - bump a version number
  - force-push a shared branch
  - rewrite git history (rebase, squash or filter commits already shared or reviewed)
  - delete data
  - send messages to customers

message_rules:
  forbidden_patterns:
    - "(?i)^co-authored-by:"
---

# Notes

- One issue = one branch = one PR. Squash merge with an explicit message.
- Staging is deployed from develop; verify there before asking for a release.
