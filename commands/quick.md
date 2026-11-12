---
description: "Estimate a described change without Spec Kit planning documents or approval"
---

# T-Shirt Sizing — Quick Estimate

Run only when explicitly invoked. Use `$ARGUMENTS` as the proposed change, supplemented by relevant conversation context. If no change is described, ask the user to describe it before estimating.

This is a preliminary, advisory estimate. It does not require `.specify/`, a feature branch, a feature directory, `spec.md`, `plan.md`, or `tasks.md`. Do not invoke the Spec Kit planning workflow or the sizing approval gate.

## Assess

Read the description and inspect relevant existing source code, tests, configuration, and contracts to understand the current behavior and likely scope. Do not implement the change or modify any files. If code is unavailable, state that the estimate is based on the description alone and adjust confidence accordingly.

Ask a few focused questions only when the answers could materially change the size. Otherwise, proceed with explicit assumptions. Do not require a full specification, plan, or task list; identify the likely work and validation at a high level.

Use the same sizing criteria as the planned-change estimate:

| Size | Typical scope |
| --- | --- |
| XS | Tiny, straightforward change with minimal reasoning and validation, even when repeated across many files |
| S | Localized behavior change in one component/subsystem with limited implementation and testing effort |
| M | Several interacting behaviors or layers requiring moderate coordination and validation |
| L | Substantial cross-cutting behavior, complex migrations or integrations, and significant validation effort |
| XL | Architectural or multi-phase change with extensive dependencies, design decisions, and validation |

Weigh file roles, change depth, distinct implementation decisions, coupling, compatibility, migrations, and actual validation effort. Include the tests and review work needed. File count is descriptive context, never a sizing threshold; label counts as approximate and omit them if there is insufficient evidence.

Group mechanical repetitions as one conceptual change plus propagation and validation. A simple string replacement across 18 locale files can remain XS; pluralization, interpolation, independently written translations, and layout changes can add real effort. Generated outputs are lightweight only when a reliable generation path exists. A one-file algorithm rewrite or migration can be M or L.

Distinguish implementation size from operational risk: a small security change may be XS and high-risk. Avoid calendar-time estimates unless requested. Identify likely overengineering and the smallest viable approach.

## Output & stop

Return a concise estimate in the conversation:

```markdown
# Preliminary T-Shirt Sizing

T-Shirt Size: [XS/S/M/L/XL]
Confidence: [LOW/MEDIUM/HIGH]

## Summary
[Proposed change and current behavior; mention the code inspected or description-only basis]

## Reasons and expected impact
- [2–5 concrete size drivers, affected components/layers, and distinct work versus repetitions]
- Validation: [likely tests and checks]
- Operational risk: [LOW/MEDIUM/HIGH, with reason]

## Assumptions and uncertainties
- [Scope assumptions, unknowns, and what could change the size]

## Smallest viable approach
[Minimal approach that meets the request]
```

Choose a primary size under the stated assumptions. If a material unknown could change it, describe the conditional alternative (for example, “M; could become L if the API contract must change”). Confidence reflects clarity of scope and evidence from the repository, not size or risk. Do not imply that this preliminary estimate guarantees the final scope.

Do not create or update `size-review.md`, staging markers, approval records, or planning documents. Do not run `sizing_gate.py`, request sizing approval, or start implementation. A later Spec Kit estimate independently assesses the planned work and may confirm or revise this estimate; this result neither grants nor invalidates workflow approval.
