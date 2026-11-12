# Spec Kit T-Shirt Sizing Gate

A Spec Kit extension that adds an AI sizing review after tasks and a pre-implementation approval guard.

## Installation

Requires **Spec Kit 1.3.1 or later**, **Python 3.11 or later** available as `python3`, and an installed coding-agent integration.

From an existing Spec Kit project root (must contain `.specify/`), install the published release:

```bash
specify version
specify extension add sizing --from https://github.com/mauriziopinotti/spec-kit-sizing/archive/refs/tags/v0.1.2.zip
specify extension list
```

The release command requires the `v0.1.2` tag to be published in the [official repository](https://github.com/mauriziopinotti/spec-kit-sizing).

For GitHub Copilot in skills layout, the invocations are:

- `/speckit-sizing-estimate`
- `/speckit-sizing-approve`
- `/speckit-sizing-guard`

Other agents may render commands differently. Check the installed integration and its generated command files.

## How sizing works

Sizing weighs file roles, change depth, distinct implementation decisions, coupling, and validation effort. File count is reported for visibility and does not set the size. For example, the same simple string update across 18 locale files remains XS when it introduces no behavior and needs only straightforward validation. Complex localization rules, logic changes, or migrations are weighed by their actual implementation and testing effort.

## Routine

Sizing applies only to the Spec Kit flow (`specify` → `plan` → `tasks` → `implement`), or to explicitly invoked sizing commands. Ordinary requests to change code, tests, configuration, or documentation do not require sizing or approval. Existing Spec Kit files, feature branches, and past reviews do not activate the gate on their own. The gate applies to the feature being implemented through Spec Kit and does not carry over to unrelated requests.

1. Run `speckit.specify`, `speckit.plan`, `speckit.tasks` normally.
2. `after_tasks` runs the estimate and creates `specs/<feature>/size-review.md` and `.size-review-stage.json`.
3. Review the proposed XS/S/M/L/XL estimate. If acceptable, explicitly invoke the approval command in your coding-agent chat.
4. `approve` stores `.size-approval.json` and stamps `Status: APPROVED`.
5. Run `speckit.implement`. `before_implement` calls `check`, which rejects missing or stale approval.

The stage and approval JSON files should be tracked with feature artifacts in Git. They contain SHA-256 digests of the four review documents, not application secrets. Task completion markers (`[ ]`, `[x]`, `[X]`) in Markdown task lists in `tasks.md` are normalized before hashing, so completing or reopening tasks preserves approval. Task descriptions, IDs, ordering, additions/removals, and fenced code examples remain significant. All content in the other three documents is significant.

SHA-256 checks detect accidental planning changes; they are not a security boundary against an agent that ignores instructions or edits the approval files.

## Local development

```bash
git clone https://github.com/mauriziopinotti/spec-kit-sizing.git
# From the Spec Kit project root, with the clone in ./spec-kit-sizing:
specify extension add --dev ./spec-kit-sizing --force
```

Edit the separately maintained source directory, not generated Spec Kit command files. Reinstall into each project when needed.

## Limitations

Extension hooks are instructions surfaced to the coding agent, not an independently enforced runtime execution gate. An agent can ignore them. For strict workflow-engine enforcement consider Spec Kit workflow gates; for OS-level protections use CI or repository controls.

This package does not modify core Spec Kit source files.

Version 0.1.1 changes task fingerprinting. After upgrading from 0.1.0, run a fresh estimate and explicitly approve it once before resuming implementation.

## Validation

Run the helper regression tests from this extension repository:

```bash
python3 -m unittest discover -s tests -v
```

The manifest and local installation are checked with Spec Kit 1.3.1. Release-archive installation and a full coding-agent workflow in a real project should also be verified before catalog submission.
