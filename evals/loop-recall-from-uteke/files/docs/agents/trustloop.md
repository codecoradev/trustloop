---
base_branch: main
pr:
  language: English
  sections: [What, Why, Testing, Risk]
memory:
  backend: uteke
  room: "project:trustloop-eval-recall"
  tags: ["project:orders-export"]
reviewer:
  tool: cora
verify:
  run: "python export.py output.csv"
  checks: ["python -m unittest"]
  journeys:
    - run `python export.py output.csv` twice in a row; output.csv has a header and exactly 3 data rows
human_gates: [deploy to production, push a release tag, rewrite git history]
message_rules:
  forbidden_patterns: []
---
