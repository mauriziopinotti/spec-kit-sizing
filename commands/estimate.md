---
description: "Estimate T-shirt implementation size after tasks, without writing source code"
---

# T-Shirt Sizing — Estimate

This command may be invoked manually or through the `after_tasks` extension hook.

## Locate feature

1. Work from the **repository root** containing `.specify/`.
2. Identify the current feature directory `specs/<feature>`: use the feature handled by the most recent `/speckit.tasks` run, otherwise the current feature branch or the user-provided `$ARGUMENTS`. Do not pick an arbitrary feature if more than one is plausible. Ask for the directory if ambiguous.
3. Require `spec.md`, `plan.md` and `tasks.md` inside that directory. If missing, stop and explain.

## Assess

Read the three documents and inspect existing source code that is relevant to the planned change. Do **not** implement, refactor, or modify application code, tests, database schemas, or the three planning documents.

Classify the **total planned change** as XS, S, M, L or XL. Use these as heuristics, not rigid rules:

| Size | Typical scope |
| --- | --- |
| XS | Trivial isolated edit, normally 1–2 files, no meaningful cross-component dependency |
| S | Localized change, normally 3–5 files, one component/subsystem |
| M | Several components/layers, normally 6–12 files, moderate coordination or tests |
| L | Cross-cutting change, normally 13–25 files, complex migrations/integrations |
| XL | Architectural or multi-phase change, often more than 25 files |

Include test changes in the estimate. Give complexity and coupling more weight than file count. Differentiate **effort/size** from **operational risk**; a one-file security change can be XS and high-risk. Avoid estimating calendar time unless the user explicitly asks for it. Highlight any likely overengineering and a smaller viable alternative.

## Write the review

Create or replace `<feature-dir>/size-review.md` with exactly these machine-readable top lines, followed by a concise human-readable review:

```markdown
# T-Shirt Sizing Review

T-Shirt Size: M
Status: PENDING
Confidence: MEDIUM

## Summary
[What needs to change]

## Expected impact
- Estimated files: [approximate count/range]
- Components/layers: [list]
- Database/API/contracts: [changes or none]
- Tests: [expected work]
- Operational risk: LOW/MEDIUM/HIGH

## Reasons for the estimate
[2–5 concrete drivers]

## Smallest viable approach
[Whether scope could be smaller and how]

## Uncertainties
[Missing information or "None"]
```

Replace the example size/confidence with your actual estimate. Keep the top three fields `T-Shirt Size:`, `Status:` and `Confidence:` in the same format; `Status` must be `PENDING`.

Next, from the repository root **run**:

```bash
python3 .specify/extensions/sizing/scripts/sizing_gate.py stage "<feature-dir>"
```

Replace `<feature-dir>` with the real path, e.g. `specs/001-example`. If this command fails, report the error and do not claim the review is ready.

## Output & stop

Present the size, confidence, main reasons, changed components, risk, and smallest viable approach. Clearly state **NOT APPROVED — implementation must not begin**.

Tell the user to explicitly invoke `__SPECKIT_COMMAND_SIZING_APPROVE__` after reviewing, or ask for a smaller plan. Never run approval automatically. Do not start implementation in this command.
