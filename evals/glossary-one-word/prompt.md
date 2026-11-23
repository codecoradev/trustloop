---
tags: [trustloop]
max_turns: 60
timeout_seconds: 1500
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash, Agent]
---

/trustloop:loop add a way for support staff to cancel a placed order so it does not ship. this codebase already says cancel, void and abort for what is the same thing to our customers; pick one word for it and make sure everyone uses it from now on. commit on a branch, no remote, write the PR body to pr.md.

Input files: orders.py, test_orders.py, docs/agents/trustloop.md, setup-repo.sh
