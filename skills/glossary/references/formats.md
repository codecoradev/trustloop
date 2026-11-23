# Formats

## GLOSSARY.md

```markdown
# <Context name>

<One or two sentences: what this context is and why it exists.>

## Language

**Order**:
A customer's request to buy one or more products, from checkout until delivery or cancellation.
_Avoid_: purchase, transaction

**Customer**:
A person or organisation that places orders.
_Avoid_: client, buyer, account
```

Rules:

- Be opinionated: one word per concept; list the rejected synonyms under _Avoid_.
- One or two sentences per definition. Say what it is, not what it does or how it is built.
- Only terms specific to this project. General programming concepts (timeouts, retries, caches) do not belong, even if the project uses them everywhere.
- Group terms under subheadings once natural clusters appear.

## GLOSSARY-MAP.md (several contexts)

```markdown
# Glossary map

## Contexts
- [Ordering](./src/ordering/GLOSSARY.md): receives and tracks customer orders
- [Billing](./src/billing/GLOSSARY.md): invoices and payments

## Relationships
- **Ordering -> Billing**: Ordering emits OrderPlaced; Billing creates the invoice
```

## ADR (docs/adr/NNNN-slug.md)

```markdown
# <Short title of the decision>

<One to three sentences: the context, what was decided, and why.>
```

That is enough; an ADR can be one paragraph. Add only when useful:

- `Status:` proposed, accepted, deprecated, or superseded by ADR-NNNN.
- Considered options, when the rejected ones are worth remembering.
- Consequences, when the downstream effects are not obvious.

Number by scanning `docs/adr/` for the highest number and adding one.

Good candidates: architectural shape, integration patterns between contexts, technology choices with lock-in, ownership and boundary decisions (including the explicit "no"s), deliberate deviations from the obvious path, and constraints the code does not show (compliance, latency contracts).
