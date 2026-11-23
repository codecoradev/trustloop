---
tags: [trustloop]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash, Agent]
---

/trustloop:loop greet("") should return "Hello there" instead of "Hello ". commit it on a branch and write the PR body to pr.md, no remote so don't push.

Input files: greet.py, test_greet.py, docs/agents/trustloop.md, setup-repo.sh
