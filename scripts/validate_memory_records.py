#!/usr/bin/env python3
"""Validate repo-local memory records.

Authority ceiling: memory_record_structural_visibility_only.
This validator is warning-only by default. Use --strict to make warnings fail.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MEMORY_ROOT = ROOT / "memory"
COMMIT_RE = re.compile(r"^[0-9a-fA-F]{5,40}$")
DATE_FILE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}\.md$")


@dataclass(frozen=True)
class MemorySection:
    file: Path
    title: str
    start_line: int
    end_line: int
    text: str


def _write_receipt(path: Path, receipt: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def _resolve_path(path_arg: str | None, fallback: Path) -> Path:
    if not path_arg:
        return fallback
    path = Path(path_arg)
    return path if path.is_absolute() else ROOT / path


def _daily_memory_files(memory_root: Path) -> list[Path]:
    if not memory_root.exists():
        return []
    return sorted(
        path
        for path in memory_root.iterdir()
        if path.is_file() and DATE_FILE_RE.match(path.name)
    )


def _sections(path: Path) -> list[MemorySection]:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [
        (index, line[3:].strip())
        for index, line in enumerate(lines)
        if line.startswith("## ")
    ]
    sections: list[MemorySection] = []
    for position, (start, title) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        sections.append(
            MemorySection(
                file=path,
                title=title,
                start_line=start + 1,
                end_line=end,
                text="\n".join(lines[start:end]),
            )
        )
    return sections


def _field_value(section: MemorySection, field: str) -> str | None:
    pattern = re.compile(rf"^\s*{re.escape(field)}\s*:\s*(.+?)\s*$", re.IGNORECASE | re.MULTILINE)
    match = pattern.search(section.text)
    return match.group(1).strip() if match else None


def _git_commits_since(since: str) -> set[str]:
    try:
        result = subprocess.run(
            ["git", "log", f"--since={since}", "--format=%h"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return set()
    return {line.strip() for line in result.stdout.splitlines() if line.strip()}


def _display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def validate(memory_root: Path = MEMORY_ROOT, check_git_since: str | None = None) -> tuple[list[str], dict[str, Any]]:
    warnings: list[str] = []
    findings: list[dict[str, str]] = []

    def add_warning(code: str, message: str) -> None:
        warnings.append(message)
        findings.append({"severity": "warning", "code": code, "message": message})

    files = _daily_memory_files(memory_root)
    if not files:
        add_warning("missing_memory_root_entries", f"{memory_root} has no daily memory files")

    sections: list[MemorySection] = []
    for file in files:
        file_sections = _sections(file)
        if not file_sections:
            add_warning("memory_file_has_no_sections", f"{file.relative_to(ROOT)} has no ## sections")
        sections.extend(file_sections)

    bound_commits: set[str] = set()
    for section in sections:
        rel = _display_path(section.file)
        session_id = _field_value(section, "session_id")
        commit_hash = _field_value(section, "commit_hash") or _field_value(section, "commit hash")

        if not session_id:
            add_warning("memory_session_id_missing", f"{rel}:{section.start_line} {section.title!r} missing session_id")
        if not commit_hash:
            add_warning("memory_commit_hash_missing", f"{rel}:{section.start_line} {section.title!r} missing commit_hash")
            continue
        normalized = commit_hash.lower()
        if normalized in {"no_commit", "pending", "none"}:
            add_warning("memory_unbound_commit", f"{rel}:{section.start_line} {section.title!r} has commit_hash: {commit_hash}")
            continue
        if not COMMIT_RE.match(commit_hash):
            add_warning("memory_commit_hash_invalid", f"{rel}:{section.start_line} {section.title!r} has invalid commit_hash: {commit_hash}")
            continue
        bound_commits.add(commit_hash[:7].lower())

    recent_commits = _git_commits_since(check_git_since) if check_git_since else set()
    for commit in sorted(recent_commits - bound_commits):
        add_warning("git_commit_missing_memory", f"git commit {commit} has no matching daily memory entry")

    result = "PASS" if not warnings else "PASS_WITH_WARNINGS"
    receipt = {
        "validator": "validate_memory_records.py",
        "authority_ceiling": "memory_record_structural_visibility_only",
        "result": result,
        "memory_root": _display_path(memory_root),
        "checked_files": [_display_path(path) for path in files],
        "checked_sections": len(sections),
        "bound_commits": sorted(bound_commits),
        "check_git_since": check_git_since,
        "recent_git_commits": sorted(recent_commits),
        "warning_count": len(warnings),
        "warnings": warnings,
        "findings": findings,
    }
    return warnings, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory-root")
    parser.add_argument("--check-git-since")
    parser.add_argument("--receipt-out")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    memory_root = _resolve_path(args.memory_root, MEMORY_ROOT)
    warnings, receipt = validate(memory_root, args.check_git_since)

    if args.receipt_out:
        _write_receipt(_resolve_path(args.receipt_out, ROOT / "evidence" / "validation_receipt_memory_records.json"), receipt)

    if warnings:
        print("PASS_WITH_WARNINGS validate_memory_records")
        for warning in warnings:
            print(f"- {warning}")
        return 1 if args.strict else 0

    print("PASS validate_memory_records")
    print(f"- checked files: {len(receipt['checked_files'])}")
    print(f"- checked sections: {receipt['checked_sections']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
