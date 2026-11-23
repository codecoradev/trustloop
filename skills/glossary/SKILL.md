---
name: glossary
description: Keep a project's shared language sharp - challenge vague or conflicting terms against GLOSSARY.md, stress-test them with concrete edge cases, check the code agrees, and write each resolved term (and, rarely, an ADR for a hard-to-reverse decision) the moment it is settled. Use when the user or a spec uses project-specific terms, when two words seem to mean the same thing (or one word two things), when naming new concepts, types or modules, or when the user mentions GLOSSARY.md, domain terms, ubiquitous language or ADRs.
---

# glossary

Agents dropped into a project guess at its jargon and use twenty words where one would do. A shared glossary fixes that: the user, the code and every agent use the same word for the same thing, names in the code follow it, and conversations get shorter. This skill is for *changing* the language; merely reading `GLOSSARY.md` before work is a habit every skill has.

Adapted from the `domain-modeling` skill in Matt Pocock's skills (MIT).

## Where it lives

- One context: `GLOSSARY.md` at the repo root.
- Several contexts: `GLOSSARY-MAP.md` at the root lists each context and where its `GLOSSARY.md` lives; pick the context the topic belongs to, and ask if it is unclear.
- Decisions: `docs/adr/0001-<slug>.md`, numbered sequentially.

Create files lazily, only when there is a first term or a first ADR to write. The glossary stays in the repo, where every agent and teammate reads it; memory (Uteke) points to it rather than copying it.

## During the work

- **Challenge conflicts.** When a term clashes with the glossary, say so at once: "The glossary defines Cancellation as a whole order; you seem to mean one line. Which is it?"
- **Sharpen fuzzy words.** Offer a precise term for a vague one: "Account: do you mean the Customer or the User? They are different here."
- **Use scenarios.** Probe boundaries with concrete edge cases until the definition holds.
- **Check the code.** When someone states how something works, see whether the code agrees and surface contradictions.
- **Write it down now.** When a term is resolved, update the glossary in the same step, not at the end. Format: `references/formats.md`.
- **Name things by it.** New types, functions, files and test names use the glossary term; renames that align old code are a separate, small PR.

The glossary is a glossary only: definitions of what a thing *is*, with the words to avoid. No implementation details, no specs, no todo lists.

## ADRs, sparingly

Offer an ADR only when all three hold: the decision is hard to reverse, a future reader would be surprised by it without context, and it was a real trade-off between alternatives. Otherwise skip it; a decision that is easy to reverse or obvious needs no record. Format: `references/formats.md`. When memory is on, the `remember` skill saves a one-line pointer to the ADR, not a copy.
