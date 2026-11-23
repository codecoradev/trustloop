---
base_branch: main
memory:
  backend: none
reviewer:
  tool: cora
verify:
  checks: ["python -m unittest"]
human_gates: [deploy to production, push a release tag, rewrite git history]
---
