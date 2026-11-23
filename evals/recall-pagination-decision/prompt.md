---
tags: [trustloop]
max_turns: 30
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Bash]
---

before i touch the orders endpoint: what did we decide about how GET /orders paginates, and is the code actually following it?

Input files: orders_api.py, db.py, docs/agents/trustloop.md, docs/decisions/2026-06-10-orders-pagination.md, docs/decisions/2026-09-02-orders-cursor-pagination.md, setup-repo.sh
