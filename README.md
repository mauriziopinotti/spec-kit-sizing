# Spec Kit T-Shirt Sizing Gate

A standalone local Spec Kit extension that adds an AI sizing review after tasks and a pre-implementation approval guard.

## Installation

From an existing Spec Kit project root (must contain `.specify/`):

```bash
specify version
specify extension add --dev /absolute/path/to/spec-kit-sizing
specify extension list
```

For GitHub Copilot in skills layout, the invocations are:
- `/speckit-sizing-estimate`
- `/speckit-sizing-approve`
- `/speckit-sizing-guard`

Other agents may render commands differently. Check the installed integration and its generated command files.

## Routine

1. Run `speckit.specify`, `speckit.plan`, `speckit.tasks` normally.
2. `after_tasks` runs the estimate and creates `specs/<feature>/size-review.md` and `.size-review-stage.json`.
3. Review the proposed XS/S/M/L/XL estimate. If acceptable, explicitly invoke the approval command in your coding-agent chat.
4. `approve` stores `.size-approval.json` and stamps `Status: APPROVED`.
5. Run `speckit.implement`. `before_implement` calls `check`, which rejects missing or stale approval.

The stage and approval JSON files should be tracked with feature artifacts in Git. They contain SHA-256 digests of the four review documents, not application secrets. SHA-256 checks detect accidental planning changes; they are not a security boundary against an agent that ignores instructions or edits the approval files.

## Reinstall after editing extension source

```bash
specify extension add --dev /absolute/path/to/spec-kit-sizing --force
```

Edit the separately maintained source directory, not generated Spec Kit command files. Reinstall into each project when needed.

## Limitations

Extension hooks are instructions surfaced to the coding agent, not an independently enforced runtime execution gate. An agent can ignore them. For strict workflow-engine enforcement consider Spec Kit workflow gates; for OS-level protections use CI or repository controls.

Requires Python 3 and a compatible Spec Kit extension-capable CLI. This package does not modify core Spec Kit source files.
