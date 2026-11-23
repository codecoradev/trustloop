---
base_branch: main
pr:
  language: English
  sections: [What, Why, Testing]
  files_ceiling: 20
  lines_ceiling: 1500
  agent_may_merge: false
memory:
  backend: none
reviewer:
  tool: cora
  severity_blocking: [critical, major]
verify:
  run: ""
  checks: ["python -m unittest"]
  journeys:
    - price_with_discount(200, 15) returns 170.0
human_gates: [deploy to production, push a release tag, rewrite git history]
message_rules:
  forbidden_patterns: []
---
