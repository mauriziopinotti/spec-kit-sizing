---
description: "Approve the exact sizing review after explicit user confirmation"
---

# T-Shirt Sizing — Approve

This command is a **human approval action**. Run it only if the user explicitly invokes this command or gives an unequivocal approval of the *specific* sizing review. A general request to implement is **not** an approval. Do not call it automatically from other commands or hooks.

1. Locate the current feature directory `specs/<feature>` from the current Spec Kit context or `$ARGUMENTS`. If ambiguous, stop and request the directory.
2. Read `size-review.md` and show its `T-Shirt Size` to the user. If the user was expecting a different size or requests changes, do not approve; ask to revise plan/tasks and re-run the estimate.
3. From the repository root run:

```bash
python3 .specify/extensions/sizing/scripts/sizing_gate.py approve "<feature-dir>"
```

4. Only after the command exits successfully, report that this exact review was approved. Do not start implementation automatically; the user should trigger the usual `__SPECKIT_COMMAND_IMPLEMENT__` step.

The script refuses approval if planning documents or the review changed after the last sizing estimate.
