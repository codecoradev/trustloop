---
base_branch: main
pr:
  language: English
  sections: [What, Why, Testing]
memory:
  backend: none
reviewer:
  tool: fallback
verify:
  checks: ["python -m unittest"]
message_rules:
  forbidden_patterns:
    - "(?i)^co-authored-by:"
    - "(?i)generated with"
    - "(?i)claude-session:"
---
