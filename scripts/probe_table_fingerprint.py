#!/usr/bin/env python3
"""Fingerprint baseline and drift check probe for governed HID tables.

Authority ceiling: table_content_fingerprint_drift_only.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "exports" / "hid_governed_surface_manifest.yaml"
DEFAULT_BASELINE = ROOT / "evidence" / "table_fingerprint_baseline.jsonl"

GOVERNANCE_METADATA = {
    "time_bound": True,
    "observation_only": True,
    "does_not_change_claim_level": True,
}


def _utc_now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def _sha256_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _load_manifest(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        doc = yaml.safe_load(handle) or {}
    tables = doc.get("governed_tables", [])
    if not isinstance(tables, list):
        raise ValueError(f"{path} governed_tables must be a list")
    return [table for table in tables if isinstance(table, dict)]


def _load_baseline(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    latest: dict[str, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        entry = json.loads(line)
        table_id = entry.get("table_id", "")
        if table_id:
            latest[table_id] = entry
    return latest


def _load_baseline_entries(path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if not path.exists():
        return [], [{"error": "BASELINE_NOT_FOUND", "path": str(path)}]

    entries: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append({"line": line_no, "error": "INVALID_JSON", "detail": str(exc)})
            continue
        if not entry.get("table_id"):
            errors.append({"line": line_no, "error": "MISSING_TABLE_ID"})
            continue
        entries.append(entry)
    return entries, errors


def _append_jsonl(path: Path, obj: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(obj, ensure_ascii=True) + "\n")


def _write_jsonl(path: Path, entries: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(json.dumps(entry, ensure_ascii=True) + "\n" for entry in entries)
    path.write_text(text, encoding="utf-8")


def _resolve_table_path(table_entry: dict[str, Any], manifest_path: Path) -> Path:
    raw = str(table_entry.get("path", ""))
    path = Path(raw)
    if path.is_absolute():
        return path
    candidate = ROOT / path
    if candidate.exists():
        return candidate
    return manifest_path.parent / path


def run_baseline(args: argparse.Namespace) -> int:
    manifest_path = Path(args.manifest)
    baseline_path = Path(args.baseline_out)
    receipt_path = Path(args.receipt_out) if args.receipt_out else None

    tables = _load_manifest(manifest_path)
    recorded_at = _utc_now_iso()
    entries: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []

    for table in tables:
        table_id = str(table.get("id") or table.get("table_id", ""))
        table_path = _resolve_table_path(table, manifest_path)
        if not table_path.exists():
            errors.append({"table_id": table_id, "path": str(table_path), "error": "FILE_NOT_FOUND"})
            continue
        relative_path = str(table_path.relative_to(ROOT)) if table_path.is_relative_to(ROOT) else str(table_path)
        entry = {
            "table_id": table_id,
            "path": relative_path,
            "content_hash": _sha256_file(table_path),
            "recorded_at": recorded_at,
            **GOVERNANCE_METADATA,
        }
        _append_jsonl(baseline_path, entry)
        entries.append(entry)

    receipt: dict[str, Any] = {
        "probe": "probe_table_fingerprint.py",
        "authority_ceiling": "table_content_fingerprint_drift_only",
        "mode": "baseline",
        "result": "PASS" if not errors else "PARTIAL",
        "recorded_at": recorded_at,
        "tables_fingerprinted": len(entries),
        "entries": entries,
        "errors": errors,
        **GOVERNANCE_METADATA,
    }
    if receipt_path:
        receipt_path.parent.mkdir(parents=True, exist_ok=True)
        receipt_path.write_text(json.dumps(receipt, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    print(f"Baseline recorded: {len(entries)} table(s) -> {baseline_path}")
    for error in errors:
        print(f"  ERROR: {error['table_id']} -> {error['error']}: {error['path']}")
    return 0 if not errors else 1


def run_check(args: argparse.Namespace) -> int:
    manifest_path = Path(args.manifest)
    baseline_path = Path(args.baseline_in)
    receipt_path = Path(args.receipt_out) if args.receipt_out else None

    tables = _load_manifest(manifest_path)
    baseline = _load_baseline(baseline_path)
    checked_at = _utc_now_iso()
    findings: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []

    for table in tables:
        table_id = str(table.get("id") or table.get("table_id", ""))
        table_path = _resolve_table_path(table, manifest_path)
        if not table_path.exists():
            errors.append({"table_id": table_id, "path": str(table_path), "error": "FILE_NOT_FOUND"})
            continue
        if table_id not in baseline:
            errors.append({"table_id": table_id, "error": "NOT_IN_BASELINE"})
            continue

        current_hash = _sha256_file(table_path)
        baseline_hash = baseline[table_id].get("content_hash")
        if current_hash != baseline_hash:
            relative_path = str(table_path.relative_to(ROOT)) if table_path.is_relative_to(ROOT) else str(table_path)
            findings.append({
                "table_id": table_id,
                "path": relative_path,
                "impact": "drift_detected",
                "baseline_hash": baseline_hash,
                "current_hash": current_hash,
                "baseline_recorded_at": baseline[table_id].get("recorded_at"),
                "checked_at": checked_at,
                "required_action": "review_required",
            })

    drift_count = len(findings)
    error_count = len(errors)
    if drift_count:
        result = "DRIFT_DETECTED"
    elif error_count:
        result = "ERROR"
    else:
        result = "PASS"

    receipt: dict[str, Any] = {
        "probe": "probe_table_fingerprint.py",
        "authority_ceiling": "table_content_fingerprint_drift_only",
        "mode": "check",
        "result": result,
        "checked_at": checked_at,
        "tables_checked": len(tables) - error_count,
        "drift_count": drift_count,
        "error_count": error_count,
        "findings": findings,
        "errors": errors,
        **GOVERNANCE_METADATA,
    }
    if receipt_path:
        receipt_path.parent.mkdir(parents=True, exist_ok=True)
        receipt_path.write_text(json.dumps(receipt, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    if result == "PASS":
        print(f"Table fingerprint check PASSED: {receipt['tables_checked']} table(s), 0 drift")
        return 0

    print(f"Table fingerprint check {result}: {drift_count} drift, {error_count} error(s)")
    for finding in findings:
        print(f"  [drift] {finding['table_id']}: {finding['baseline_hash']} -> {finding['current_hash']}")
    for error in errors:
        print(f"  [error] {error['table_id']}: {error['error']}")
    return 1


def run_compact(args: argparse.Namespace) -> int:
    baseline_in = Path(args.baseline_in)
    baseline_out = Path(args.baseline_out)
    receipt_path = Path(args.receipt_out) if args.receipt_out else None
    compacted_at = _utc_now_iso()

    entries, errors = _load_baseline_entries(baseline_in)
    latest: dict[str, dict[str, Any]] = {}
    for entry in entries:
        latest[str(entry["table_id"])] = entry
    compacted_entries = [latest[table_id] for table_id in sorted(latest)]

    if not errors:
        _write_jsonl(baseline_out, compacted_entries)

    receipt = {
        "probe": "probe_table_fingerprint.py",
        "authority_ceiling": "table_content_fingerprint_drift_only",
        "mode": "compact",
        "result": "PASS" if not errors else "ERROR",
        "compacted_at": compacted_at,
        "baseline_in": str(baseline_in),
        "baseline_out": str(baseline_out),
        "input_entries": len(entries),
        "entries_retained": len(compacted_entries),
        "entries_removed": len(entries) - len(compacted_entries),
        "errors": errors,
        **GOVERNANCE_METADATA,
    }
    if receipt_path:
        receipt_path.parent.mkdir(parents=True, exist_ok=True)
        receipt_path.write_text(json.dumps(receipt, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    if errors:
        print(f"Table fingerprint compact ERROR: {len(errors)} error(s)")
        for error in errors:
            print(f"  [error] line {error.get('line', '-')}: {error['error']}")
        return 1

    print(
        "Table fingerprint compact PASSED: "
        f"{len(entries)} input, {len(compacted_entries)} retained, {len(entries) - len(compacted_entries)} removed"
    )
    return 0


def main() -> int:
    return main_with_args()


def main_with_args(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Fingerprint governed HID tables for drift detection.")
    parser.add_argument("--mode", choices=["baseline", "check", "compact"], required=True)
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    parser.add_argument("--baseline-out", default=str(DEFAULT_BASELINE))
    parser.add_argument("--baseline-in", default=str(DEFAULT_BASELINE))
    parser.add_argument("--receipt-out")
    args = parser.parse_args(argv)

    if args.mode == "baseline":
        return run_baseline(args)
    if args.mode == "compact":
        return run_compact(args)
    return run_check(args)


if __name__ == "__main__":
    sys.exit(main())
