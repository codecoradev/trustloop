# Feature map format

The map lives next to the verification skill: `features/README.md` plus one file per feature. It describes what a user can do and how to prove it, in the user's terms. Keep implementation details out.

## features/README.md

```markdown
# <App> verification map

Maintained source for verifying the user-facing behavior of <App>. Read this index, then use the matching feature file as the recipe.

## Baseline preconditions
- <how the app is launched for verification, with a disposable data dir>
- <seed data the journeys rely on>
- <doctor check that must pass before driving>
- Never drive an instance this run did not start.

## Driving conventions
- Start every recipe from the baseline unless it says otherwise.
- Prefer stable handles (accessible names, route paths, prompt strings) over position.
- Restore seeded data after a mutation. Never delete proof artifacts during cleanup.

## Proof and skip reporting
- Capture the action and the resulting state, not only the final screen.
- CLI proof: command, stdout, stderr, exit code. UI proof: screenshot plus an accessibility snapshot. Mutation proof: a second, read-only view of the stored value.
- Report an unreachable path with the attempted command and the unmet precondition; never report a skipped entry point as verified through another one.

## Features
- [<Feature>](<feature>.md): <one line>
```

## One file per feature

```markdown
# <Feature>

<One paragraph: what the user can do and see.>

## Sub-features
- <short-id>: <one line per behavior>

## How to get to it (user POV)
- <every entry point a user has: menu, shortcut, command, URL>

## Driving it with <harness>
Preconditions: <state required>
- <user action>: `<exact command>` -> <observable result>

## Gotchas
- <traps that waste or invalidate a run>
```

## Example (CLI)

```markdown
# Export orders

Writes all orders to a CSV file; re-running the same job replaces the file.

## Sub-features
- export-fresh: export to a new file
- export-retry: running the same job again leaves the same file

## How to get to it (user POV)
- `python export.py <path>`

## Driving it with shell
Preconditions: empty scratch directory; sample orders are built in.
- Export once: `python export.py out.csv` -> exit 0; out.csv has a header and 3 rows
- Retry the job: `python export.py out.csv` again -> still a header and 3 rows

## Gotchas
- Running in the repo root leaves output.csv behind; always use a scratch directory.
```
