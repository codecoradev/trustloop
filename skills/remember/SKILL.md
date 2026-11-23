---
name: remember
description: Save what a coding session learned to long-term project memory so the next agent or teammate starts ahead - decisions with their reasons, non-obvious gotchas, procedures and handoffs - one fact per entry, de-duplicated and superseding stale entries, in Uteke when connected or in decision files otherwise. Use after a decision is made, a hard bug is understood, a task lands, work is handed over, or the user says "remember this", "save this decision" or "note this for next time".
---

# remember

Memory is only useful if the next reader can trust it. Save less, save it precisely, and keep it current.

## What is worth saving

- **Decision**: what was chosen, the reason, and the alternatives rejected. "Use cursor pagination for /orders, because offset scans time out above 1M rows; page numbers rejected because clients scroll rather than jump to a page."
- **Gotcha**: a non-obvious failure and how to avoid it, with the evidence. "CI review returns an empty result for PRs to main unless base-branch is set to the PR base."
- **Procedure**: steps that worked and will be repeated.
- **Status change**: a recorded decision was implemented, reverted or found not followed by the code. Update or supersede the decision entry so recall stops reporting a plan as if it were shipped.
- **Handoff**: when work stops mid-way: current state, next step, blockers, branch and PR links.

Do not save what the code or git history already says plainly, routine progress chatter, guesses that were not checked, or anything secret: no tokens, keys, passwords, connection strings, personal data. If a fact needs a secret to be useful, save where the secret lives, not its value.

## How to write an entry

One fact per entry, readable on its own months later: what, why, when (absolute date), and a pointer to evidence (PR, commit, file, measurement). Write it in the language your team reads.

## Uteke (backend `uteke`)

1. Search before writing: `uteke_room_recall` on the room with the fact as the query. If an entry already says it, stop. If one says something now wrong, write the new entry and call `uteke_supersede` so recall flags the old one, rather than leaving two answers.
2. Write with `uteke_remember`: `content`, `type` (`decision`, `insight` for a gotcha, `procedure`, `context` for a handoff, or `fact`), the configured `room` and `tags`, and `author` from `memory.author` (default `claude-code`), so every entry from this repo's agents carries the same name. Always pass `type` when you pass `room`: with a room and no type, Uteke stores the entry as `fact`. Pin (`uteke_pin`) only what every future session must see.
3. An ADR or glossary change in the repo gets a one-line memory pointing to the file (path and commit), not a copy, so there is one source of truth. Longer material that does not belong in the repo (a design, a runbook, a research summary) goes in a document: `uteke_doc_create`, then `uteke_room_add_document` to link it to the room. Memories stay short and point to the document.

Details on tools and conventions: `references/uteke.md`.

## Files (backend `files`, or Uteke unreachable)

Append to `<memory.files_dir>/YYYY-MM-DD-<slug>.md` with a heading per entry, or the team's ADR format if one exists. Superseding: edit the old entry's status line to "Superseded by <file>", do not delete it. These files are repo-visible: keep internal-only notes out of public repositories.

## When

Save right after the decision or discovery during long runs, so a crash loses nothing; for a short task, one pass at the end is enough. At light rigor, save only if something was decided. Add a handoff only if something remains open.

Report what you saved in one line per entry with its id, so the user can correct it.
