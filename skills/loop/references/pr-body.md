# PR body

Use the section names from the config (`pr.sections`); the default is below. Write in the configured language. Keep it short: a reviewer should know in one minute what changed, why, how it was proven, and what could go wrong.

```markdown
## What
<One or two sentences on the change. For UI, a before/after screenshot.>

## Why
<The problem and the goal. Link the issue. If the PR is over the size target, say why it cannot be split and what the reviewer may skip.>

## Testing
- Finish condition: <each check and its result>
- Review gate: <verdict line from review-gate, e.g. "cora agent review on 4f2c1ab: 0 blocking, 2 minor fixed">
- Independent verification: <verdict and what the verifier observed>
- Not covered: <what was not tested, and why>

## Risk
<One-way or two-way door. Blast radius: who or what breaks if this is wrong, and how to roll back.>
```

Before you submit, check the title, body and every commit message against the config's `message_rules`. A forbidden line that slipped in gets removed before review, not after merge.
