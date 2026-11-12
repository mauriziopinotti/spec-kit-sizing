---
description: "Check sizing approval for the current Spec Kit implementation"
---

# T-Shirt Sizing — Pre-Implementation Guard

This command is executed by the `before_implement` hook **only within the Spec Kit workflow**, when the user invokes `__SPECKIT_COMMAND_IMPLEMENT__` or explicitly asks to resume that workflow's implementation of a feature prepared through specify, plan, and tasks. It can also be invoked explicitly to check a feature's approval.

Ordinary requests to edit code, tests, schemas, configuration, or documentation do not activate this guard. The presence of `.specify/`, a feature branch, planning documents, or an old sizing review does not by itself mean the current request uses Spec Kit. Outside the workflow, continue the user's request without running sizing commands, requesting sizing approval, or asking for a feature directory. Do not carry this gate over to unrelated requests after a Spec Kit command ends.

For an active Spec Kit implementation or an explicit guard invocation:

1. Locate the feature directory `specs/<feature>` targeted by that invocation. If ambiguous, STOP and request the directory. Require `spec.md`, `plan.md`, and `tasks.md` for that feature; if missing, explain that the Spec Kit planning steps must be completed before implementation.
2. From the repository root run:

```bash
python3 .specify/extensions/sizing/scripts/sizing_gate.py check "<feature-dir>"
```

3. If the command fails or returns anything other than `APPROVED`, STOP. Do not edit code, do not work around the check, and explain the missing or outdated approval. Request a fresh sizing estimate and explicit approval.
4. Only if the check succeeds may the standard Spec Kit implementation continue.

A modified `spec.md`, `plan.md`, `tasks.md`, or `size-review.md` invalidates the approval.

Task completion checkbox changes in `tasks.md` are ignored; changes to task descriptions, IDs, ordering, or other document content require a fresh estimate and approval.
