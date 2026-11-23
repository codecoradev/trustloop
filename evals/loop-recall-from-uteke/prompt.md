---
tags: [trustloop]
max_turns: 60
timeout_seconds: 1500
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash, Agent]
---

/trustloop:loop the CSV export writes duplicate rows when the scheduler retries a job after a timeout. repro first, then fix and verify. there is no remote: don't push or open a real PR, write the PR body to pr.md in the repo root instead.

Input files: export.py, test_export.py, docs/agents/trustloop.md, setup-repo.sh
