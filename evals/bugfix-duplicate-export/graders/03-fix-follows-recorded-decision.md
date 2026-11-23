---
type: llm
focus: trace
weight: 1
---

The fix writes to a temporary file and replaces the target (or otherwise never appends), consistent with docs/decisions/2026-11-01-export-writes.md, and the agent mentions that decision.
