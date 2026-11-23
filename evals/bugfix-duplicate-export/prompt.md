---
tags: [trustloop]
max_turns: 60
timeout_seconds: 1200
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash, Agent]
---

/trustloop:loop the CSV export writes duplicate rows when the scheduler retries a job after a timeout. repro first, then fix and verify. there is no remote: don't push or open a real PR, write the PR body to pr.md in the repo root instead.

Input files: export.py, test_export.py, docs/agents/trustloop.md, docs/decisions/2026-11-01-export-writes.md, setup-repo.sh
