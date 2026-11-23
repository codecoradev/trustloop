---
tags: [trustloop]
max_turns: 60
timeout_seconds: 1500
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash, Agent]
---

/trustloop:setup

(When you need an answer from the user, use these, they are what the user would say: memory goes in a new Uteke room called project:trustloop-eval-setup; commit messages and PR text must never contain lines matching co-authored-by, generated with, or claude-session; for anything else take your own recommended answer.)

Input files: export.py, test_export.py, setup-repo.sh
