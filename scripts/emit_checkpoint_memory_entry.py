#!/usr/bin/env python3
"""Emit a repo-local memory entry for a completed checkpoint."""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MEMORY_ROOT = ROOT / "memory"


def _git_head() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _git_changed_files(commit: str) -> list[str]:
    result = subprocess.run(
        ["git", "show", "--name-only", "--format=", commit],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def _format_list(items: list[str]) -> str:
    if not items:
        return "- none\n"
    return "".join(f"- {item}\n" for item in items)


def _append_entry(path: Path, entry: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8").strip():
        with path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write("\n\n")
            handle.write(entry)
    else:
        path.write_text(entry, encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--title", required=True)
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--commit-hash")
    parser.add_argument("--scope", action="append", default=[])
    parser.add_argument("--validation", action="append", default=[])
    parser.add_argument("--claim-ceiling", action="append", default=[])
    parser.add_argument("--not-claimed", action="append", default=[])
    parser.add_argument("--risk", action="append", default=[])
    parser.add_argument("--allow-no-commit", action="store_true")
    args = parser.parse_args()

    commit_hash = args.commit_hash or _git_head()
    if commit_hash.upper() == "NO_COMMIT" and not args.allow_no_commit:
        print("FAIL emit_checkpoint_memory_entry")
        print("- commit_hash is NO_COMMIT; use --allow-no-commit only for non-binding session notes")
        return 1

    changed_files = [] if commit_hash.upper() == "NO_COMMIT" else _git_changed_files(commit_hash)
    target = MEMORY_ROOT / f"{args.date}.md"
    header = f"# {args.date}\n\n" if not target.exists() or not target.read_text(encoding="utf-8").strip() else ""
    entry = (
        f"{header}## {args.title}\n\n"
        f"session_id: {args.session_id}\n\n"
        "changed_surfaces:\n\n"
        f"{_format_list(args.scope or changed_files)}\n"
        "validation:\n\n"
        f"{_format_list(args.validation)}\n"
        "claim_ceiling:\n\n"
        f"{_format_list(args.claim_ceiling)}\n"
        "not_claimed:\n\n"
        f"{_format_list(args.not_claimed)}\n"
        "risk:\n\n"
        f"{_format_list(args.risk)}\n"
        f"commit_hash: {commit_hash}\n"
    )
    _append_entry(target, entry)
    print(f"PASS emit_checkpoint_memory_entry: {target.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
