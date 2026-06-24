#!/usr/bin/env python3
"""Validate the HID validation receipt index and receipt archive.

Authority ceiling: validation_receipt_index_integrity_only.
This validator checks receipt bookkeeping only. It does not validate HID
semantics, promote entries, or import source authority.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INDEX = ROOT / "evidence" / "validation_receipt_index.json"
DEFAULT_RECEIPT = ROOT / "evidence" / "validation_receipt_validation_receipt_index.json"


def _display_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _resolve_under_root(path_arg: str | None, fallback: Path) -> Path:
    if not path_arg:
        return fallback
    path = Path(path_arg)
    candidate = path if path.is_absolute() else ROOT / path
    resolved_root = ROOT.resolve()
    resolved = candidate.resolve()
    try:
        resolved.relative_to(resolved_root)
    except ValueError as exc:
        raise ValueError(f"path must stay under repository root: {path_arg}") from exc
    return resolved


def _load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{_display_path(path)} must contain a JSON object")
    return data


def _write_receipt(path: Path, receipt: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def validate(index_path: Path = DEFAULT_INDEX) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    findings: list[dict[str, str]] = []

    def add_error(code: str, message: str) -> None:
        errors.append(message)
        findings.append({"code": code, "message": message})

    try:
        index = _load_json(index_path)
    except Exception as exc:
        add_error("INDEX_LOAD_FAILED", str(exc))
        index = {}

    receipt_dir_text = index.get("receipt_dir")
    receipt_dir = ROOT / receipt_dir_text if isinstance(receipt_dir_text, str) else None
    if not receipt_dir_text or receipt_dir is None:
        add_error("RECEIPT_DIR_MISSING", "index receipt_dir must be present")
    elif not receipt_dir.exists() or not receipt_dir.is_dir():
        add_error("RECEIPT_DIR_MISSING_ON_DISK", f"receipt_dir does not exist: {receipt_dir_text}")

    receipts = index.get("receipts", [])
    if not isinstance(receipts, list):
        add_error("RECEIPTS_NOT_LIST", "index receipts must be a list")
        receipts = []

    if index.get("result") != "PASS":
        add_error("INDEX_RESULT_NOT_PASS", f"index result must be PASS, got {index.get('result')!r}")
    if index.get("fail_count") != 0:
        add_error("INDEX_FAIL_COUNT_NONZERO", f"index fail_count must be 0, got {index.get('fail_count')!r}")
    if index.get("checked_commands") != len(receipts):
        add_error(
            "CHECKED_COMMAND_COUNT_MISMATCH",
            f"checked_commands {index.get('checked_commands')!r} != receipt count {len(receipts)}",
        )
    if index.get("pass_count") != len(receipts):
        add_error("PASS_COUNT_MISMATCH", f"pass_count {index.get('pass_count')!r} != receipt count {len(receipts)}")

    seen_ids: set[str] = set()
    indexed_paths: set[Path] = set()
    for receipt_entry in receipts:
        if not isinstance(receipt_entry, dict):
            add_error("RECEIPT_ENTRY_NOT_MAPPING", "receipt entries must be mappings")
            continue

        receipt_id = receipt_entry.get("receipt_id")
        receipt_path_text = receipt_entry.get("receipt_path")
        if not isinstance(receipt_id, str) or not receipt_id:
            add_error("RECEIPT_ID_INVALID", f"invalid receipt_id in index entry: {receipt_entry!r}")
            continue
        if receipt_id in seen_ids:
            add_error("DUPLICATE_RECEIPT_ID", f"duplicate receipt_id: {receipt_id}")
        seen_ids.add(receipt_id)

        if receipt_entry.get("result") != "PASS":
            add_error("INDEXED_RECEIPT_RESULT_NOT_PASS", f"{receipt_id}: index result is not PASS")
        if receipt_entry.get("returncode") != 0:
            add_error("INDEXED_RECEIPT_RETURNCODE_NONZERO", f"{receipt_id}: index returncode is not 0")

        if not isinstance(receipt_path_text, str) or not receipt_path_text:
            add_error("RECEIPT_PATH_INVALID", f"{receipt_id}: receipt_path must be present")
            continue
        try:
            receipt_path = _resolve_under_root(receipt_path_text, ROOT / receipt_path_text)
        except ValueError as exc:
            add_error("RECEIPT_PATH_OUTSIDE_ROOT", f"{receipt_id}: {exc}")
            continue
        indexed_paths.add(receipt_path.resolve())

        if receipt_dir is not None:
            try:
                receipt_path.resolve().relative_to(receipt_dir.resolve())
            except ValueError:
                add_error("RECEIPT_PATH_OUTSIDE_RECEIPT_DIR", f"{receipt_id}: {receipt_path_text}")

        if not receipt_path.exists():
            add_error("RECEIPT_FILE_MISSING", f"{receipt_id}: missing receipt file {receipt_path_text}")
            continue

        try:
            receipt_doc = _load_json(receipt_path)
        except Exception as exc:
            add_error("RECEIPT_FILE_LOAD_FAILED", f"{receipt_id}: {exc}")
            continue

        if receipt_doc.get("receipt_id") != receipt_id:
            add_error(
                "RECEIPT_ID_MISMATCH",
                f"{receipt_id}: file receipt_id {receipt_doc.get('receipt_id')!r} does not match index",
            )
        if receipt_doc.get("result") != "PASS":
            add_error("RECEIPT_FILE_RESULT_NOT_PASS", f"{receipt_id}: file result is not PASS")
        if receipt_doc.get("returncode") != 0:
            add_error("RECEIPT_FILE_RETURNCODE_NONZERO", f"{receipt_id}: file returncode is not 0")

    if receipt_dir is not None and receipt_dir.exists():
        actual_paths = {path.resolve() for path in receipt_dir.glob("*.json")}
        missing_from_index = sorted(actual_paths - indexed_paths)
        missing_from_disk = sorted(indexed_paths - actual_paths)
        for path in missing_from_index:
            add_error("STALE_RECEIPT_FILE", f"stale receipt file not listed in index: {_display_path(path)}")
        for path in missing_from_disk:
            add_error("INDEXED_RECEIPT_FILE_MISSING", f"indexed receipt file missing on disk: {_display_path(path)}")

    receipt = {
        "validator": "validate_validation_receipt_index.py",
        "authority_ceiling": "validation_receipt_index_integrity_only",
        "result": "PASS" if not errors else "FAIL",
        "index": _display_path(index_path),
        "receipt_dir": receipt_dir_text,
        "checked_receipts": len(receipts),
        "error_count": len(errors),
        "errors": errors,
        "findings": findings,
        "claim_ceiling": [
            "validation_receipt_index_integrity_only",
            "no_new_source_authority_import",
            "no_matrix_semantic_change",
            "no_verified_uplift",
        ],
    }
    return errors, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index")
    parser.add_argument("--receipt-out")
    args = parser.parse_args()

    try:
        index_path = _resolve_under_root(args.index, DEFAULT_INDEX)
        receipt_out = _resolve_under_root(args.receipt_out, DEFAULT_RECEIPT)
    except ValueError as exc:
        print(f"FAIL validate_validation_receipt_index: {exc}")
        return 1

    errors, receipt = validate(index_path)
    if args.receipt_out:
        _write_receipt(receipt_out, receipt)

    if errors:
        print("FAIL validate_validation_receipt_index")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS validate_validation_receipt_index")
    print(f"- checked receipts: {receipt['checked_receipts']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
