# Changelog

## [Unreleased]

### Fixed
- Limit automatic sizing and approval checks to the active Spec Kit workflow; ordinary edit requests do not activate the gate
- Clarify that existing planning artifacts and past reviews do not impose sizing on unrelated requests

## [0.1.2] - 2026-11-07

### Changed
- Size changes by file role, change depth, distinct work, coupling, and validation effort
- Treat mechanical localization and generated-file repetitions as lightweight propagation, not independent complexity
- Remove file-count sizing thresholds and include a work breakdown in sizing reviews

## [0.1.1] - 2026-11-07

### Fixed
- Preserve approval when completing or reopening tasks; scope changes still invalidate it
- Reject malformed and duplicate review metadata before approval
- Reject non-object JSON markers with a clear denial instead of a traceback
- Verify that approval updates the review status successfully

### Changed
- Document release installation, upgrade behavior, and Python 3.11 requirement
- Require Spec Kit 1.3.1, the verified CLI version
- Add regression tests for approval and stale-document checks

## [0.1.0] - 2026-11-07

### Added
- T-Shirt sizing estimates (XS, S, M, L, XL)
- Automatic sizing review after tasks
- Explicit human approval
- Pre-implementation approval guard
- SHA-256 validation of planning artifacts
