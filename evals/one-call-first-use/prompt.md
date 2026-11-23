---
tags: [trustloop]
max_turns: 60
timeout_seconds: 1500
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash, Agent]
---

/trustloop:loop the CSV export writes duplicate rows when the scheduler retries a job after a timeout. repro first, then fix and verify. there is no remote: don't push or open a real PR, write the PR body to pr.md in the repo root instead.

(When you need an answer from the user, use these, they are what the user would say: memory goes in a new Uteke room called project:trustloop-eval-onecall; no forbidden patterns for commit messages; for anything else take your own recommended answer.)

Input files: export.py, test_export.py, setup-repo.sh
