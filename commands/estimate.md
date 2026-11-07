---
description: "Estimate T-shirt implementation size after tasks, without writing source code"
---

# T-Shirt Sizing — Estimate

This command may be invoked manually or through the `after_tasks` extension hook.

## Locate feature

1. Work from the **repository root** containing `.specify/`.
2. Identify the current feature directory `specs/<feature>`: use the feature handled by the most recent `__SPECKIT_COMMAND_TASKS__` run, otherwise the current feature branch or the user-provided `$ARGUMENTS`. Do not pick an arbitrary feature if more than one is plausible. Ask for the directory if ambiguous.
3. Require `spec.md`, `plan.md` and `tasks.md` inside that directory. If missing, stop and explain.

## Assess

Read the three documents and inspect existing source code that is relevant to the planned change. Do **not** implement, refactor, or modify application code, tests, database schemas, or the three planning documents.

Classify the **total planned change** as XS, S, M, L or XL based on the actual work and distinct implementation decisions. File count is descriptive context, not a sizing threshold. Use these heuristics:

| Size | Typical scope |
| --- | --- |
| XS | Tiny, straightforward change with minimal reasoning and validation, even when repeated across many files |
| S | Localized behavior change in one component/subsystem with limited implementation and testing effort |
| M | Several interacting behaviors or layers requiring moderate coordination and validation |
| L | Substantial cross-cutting behavior, complex migrations or integrations, and significant validation effort |
| XL | Architectural or multi-phase change with extensive dependencies, design decisions, and validation |

### Weigh the actual work

Inspect the role and contents of the affected files, rather than assigning weight solely by extension or counting paths. Consider:

- **File role and change depth:** distinguish application logic, schemas/contracts, configuration, localization resources, documentation, tests/fixtures, and generated artifacts. A one-line text replacement is different from introducing behavior or restructuring a component. JSON or YAML can hold either simple text or complex runtime configuration.
- **Repetition and distinct decisions:** group mechanical repetitions of the same change as one work unit plus the real propagation and validation effort. Do not multiply the conceptual complexity by the number of languages, copies, snapshots, or generated outputs. Report the physical file count separately.
- **Coupling and validation:** weigh dependencies, behavioral changes, integration work, migrations, compatibility, and the tests or manual checks actually needed. Include test changes and any translation/review effort that is part of the planned work. Automation reduces repetition, but does not eliminate validation.
- **Exceptions and uncertainty:** localization work is usually lightweight for a simple repeated string edit, but pluralization, interpolation, ICU syntax, right-to-left layout, encoding, or independently written translations can add real effort. Generated files are lightweight outputs only when a reliable generation path exists; changes to the generator or difficult regeneration count as actual work.

Calibration examples:

- Replacing one simple string in 18 locale files, with no new behavior and straightforward validation, remains **XS**. Report 18 affected files and one repeated lightweight change; do not classify it as L because of the count.
- A small logic fix plus the same string update across 18 locales is sized primarily by the logic fix and its tests, plus the actual localization work.
- A one-file algorithm rewrite or complex database migration can be M or L when its reasoning and validation justify it.

Explain which file groups are lightweight repetitions and which drive the estimate. Do not use a fixed per-file score or automatic size escalation based on file count. Differentiate **effort/size** from **operational risk**; a one-file security change can be XS and high-risk. Avoid estimating calendar time unless the user explicitly asks for it. Highlight any likely overengineering and a smaller viable alternative.

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
- Estimated files: [physical count/range, including repeated/generated outputs]
- Work breakdown: [file roles, change depth, distinct work units, and lightweight repetitions]
- Validation effort: [checks needed, including any locale-specific or regeneration checks]
- Components/layers: [list]
- Database/API/contracts: [changes or none]
- Tests: [expected work]
- Operational risk: LOW/MEDIUM/HIGH

## Reasons for the estimate
[2–5 concrete drivers; explain how file role, repetition, coupling, and validation determine size]

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
