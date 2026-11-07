---
description: "Stop implementation unless a matching sizing review was explicitly approved"
---

# T-Shirt Sizing — Pre-Implementation Guard

This command is executed automatically by the `before_implement` hook. It is a **blocking prerequisite in the agent's instruction flow**.

1. Before ANY application-code, test, schema, or configuration change, locate the feature directory `specs/<feature>` targeted by the current implementation. If ambiguous, STOP.
2. From the repository root run:

```bash
python3 .specify/extensions/sizing/scripts/sizing_gate.py check "<feature-dir>"
```

3. If the command fails or returns anything other than `APPROVED`, STOP. Do not edit code, do not work around the check, and explain the missing or outdated approval. Request a fresh sizing estimate and explicit approval.
4. Only if the check succeeds may the standard Spec Kit implementation continue.

A modified `spec.md`, `plan.md`, `tasks.md`, or `size-review.md` invalidates the approval.
