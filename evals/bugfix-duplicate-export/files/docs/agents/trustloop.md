---
base_branch: main
pr:
  language: English
  sections: [What, Why, Testing, Risk]
  files_ceiling: 20
  lines_ceiling: 1500
  agent_may_merge: false
memory:
  backend: files
  files_dir: docs/decisions
reviewer:
  tool: cora
  severity_blocking: [critical, major]
verify:
  run: "python export.py output.csv"
  checks: ["python -m unittest"]
  journeys:
    - run `python export.py output.csv` twice in a row; output.csv has a header and exactly 3 data rows
human_gates: [deploy to production, push a release tag, delete data]
message_rules:
  forbidden_patterns: []
---
