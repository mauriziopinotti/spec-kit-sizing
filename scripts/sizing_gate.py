#!/usr/bin/env python3
"""Local SHA-256 approval marker for the Spec Kit sizing extension.

Usage (from a Spec Kit project root):
  python3 .specify/extensions/sizing/scripts/sizing_gate.py stage specs/001-example
  python3 .specify/extensions/sizing/scripts/sizing_gate.py approve specs/001-example
  python3 .specify/extensions/sizing/scripts/sizing_gate.py check specs/001-example
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

FILES = ("spec.md", "plan.md", "tasks.md", "size-review.md")
STAGE = ".size-review-stage.json"
APPROVAL = ".size-approval.json"


def fail(message: str) -> None:
    print(f"DENIED: {message}", file=sys.stderr)
    raise SystemExit(1)


def review_metadata(feature: Path) -> tuple[str, str]:
    review = (feature / "size-review.md").read_text(encoding="utf-8")
    fields = {}
    for label, values in (("T-Shirt Size", "XS|S|M|L|XL"), ("Status", "PENDING|APPROVED")):
        lines = [line for line in review.splitlines() if line.startswith(label + ":")]
        if len(lines) != 1:
            fail(f"size-review.md must contain exactly one {label}: field")
        match = re.fullmatch(rf"{label}:[ \t]*({values})[ \t]*", lines[0])
        if not match:
            fail(f"Invalid {label}: expected {values} on the same line")
        fields[label] = match.group(1)
    return fields["T-Shirt Size"], fields["Status"]


def task_content(content: bytes) -> bytes:
    """Ignore only Markdown task completion markers, outside fenced code blocks."""
    lines = []
    fence = None
    for line in content.splitlines(keepends=True):
        marker = re.match(rb"^ {0,3}(`{3,}|~{3,})(.*)", line)
        if fence is None and marker:
            fence = marker.group(1)
        elif fence is not None:
            if marker and marker.group(1)[:1] == fence[:1] and len(marker.group(1)) >= len(fence) and not marker.group(2).strip():
                fence = None
        else:
            line = re.sub(rb"^([ \t]*(?:[-+*]|[0-9]+[.)])[ \t]+)\[[ xX]\](?=[ \t])", rb"\1[ ]", line)
        lines.append(line)
    return b"".join(lines)


def digests(feature: Path) -> dict[str, str]:
    out = {}
    for name in FILES:
        path = feature / name
        if not path.is_file():
            fail(f"Missing required file: {path}")
        content = path.read_bytes()
        if name == "tasks.md":
            content = task_content(content)
        out[name] = hashlib.sha256(content).hexdigest()
    return out


def write_json(path: Path, record: dict) -> None:
    path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict:
    if not path.is_file():
        fail(f"Missing {path.name}; run estimate, then approve")
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(record, dict):
            fail(f"Invalid {path.name}: expected a JSON object")
        return record
    except (ValueError, OSError) as exc:
        fail(f"Invalid {path.name}: {exc}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Sizing approval helper")
    parser.add_argument("action", choices=("stage", "approve", "check"))
    parser.add_argument("feature", help="Feature directory, e.g. specs/001-example")
    args = parser.parse_args()

    feature = Path(args.feature).resolve()
    if not feature.is_dir():
        fail(f"Feature directory does not exist: {feature}")
    # Do not accept a folder outside the project or a parent directory.
    project_root = Path.cwd().resolve()
    if not (project_root / ".specify").is_dir():
        fail("Run this command from the Spec Kit project root")
    if feature.parent != (project_root / "specs").resolve():
        fail("Feature must be an immediate subdirectory of the project's specs/ directory")

    fingerprints = digests(feature)
    size, status = review_metadata(feature)

    if args.action == "stage":
        if status != "PENDING":
            fail("Set Status: PENDING when creating a new estimate")
        write_json(feature / STAGE, {"size": size, "sha256": fingerprints})
        (feature / APPROVAL).unlink(missing_ok=True)
        print(f"PENDING: {size} — awaiting explicit approval for {feature.name}")
        return

    if args.action == "approve":
        staged = read_json(feature / STAGE)
        if status != "PENDING":
            fail("Review is not PENDING; rerun estimate before a new approval")
        if staged.get("size") != size or staged.get("sha256") != fingerprints:
            fail("Documents or review changed since estimate; rerun estimate")
        review_file = feature / "size-review.md"
        review_text = review_file.read_text(encoding="utf-8")
        updated, count = re.subn(r"^Status:[ \t]*PENDING[ \t]*$", "Status: APPROVED", review_text, flags=re.MULTILINE)
        if count != 1:
            fail("Could not update exactly one Status field")
        review_file.write_text(updated, encoding="utf-8")
        if review_metadata(feature) != (size, "APPROVED"):
            fail("Review status was not updated to APPROVED")
        write_json(feature / APPROVAL, {
            "size": size,
            "approved_at_utc": datetime.now(timezone.utc).isoformat(),
            "sha256": digests(feature),
        })
        print(f"APPROVED: {size} — {feature.name}")
        return

    approval = read_json(feature / APPROVAL)
    if status != "APPROVED":
        fail("Sizing review is not approved")
    if approval.get("size") != size or approval.get("sha256") != fingerprints:
        fail("Approval is stale: a reviewed document changed after approval")
    print(f"APPROVED: {size} — {feature.name}; fingerprints match")


if __name__ == "__main__":
    try:
        main()
    except (OSError, UnicodeError) as exc:
        fail(f"Cannot read or write sizing artifacts: {exc}")
