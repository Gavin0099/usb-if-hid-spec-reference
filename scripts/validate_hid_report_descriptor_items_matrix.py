#!/usr/bin/env python3
"""Validate HID report descriptor item import-prep matrix."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX = ROOT / "data" / "hid_report_descriptor_items_matrix.yaml"

EXPECTED_ITEMS = {
    "short_item_prefix",
    "long_item_prefix",
    "main_item_type",
    "global_item_type",
    "local_item_type",
    "reserved_item_type",
}


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return data


def validate(path: Path = DEFAULT_MATRIX) -> list[str]:
    errors: list[str] = []
    data = load_yaml(path)

    if data.get("matrix_id") != "hid_report_descriptor_items_matrix":
        errors.append("matrix_id must be hid_report_descriptor_items_matrix")
    if data.get("status") != "import_prep":
        errors.append("matrix status must be import_prep")

    source_refs = data.get("source_refs")
    if not isinstance(source_refs, list) or len(source_refs) != 1:
        errors.append("source_refs must contain exactly one HID 1.11 section 6.2.2 reference")
        source_refs = []
    if source_refs:
        source_ref = source_refs[0]
        if not isinstance(source_ref, dict):
            errors.append("source_refs[0] must be a mapping")
        else:
            if source_ref.get("source_id") != "hid_spec_1_11":
                errors.append("source_refs[0].source_id must be hid_spec_1_11")
            if source_ref.get("section") != "6.2.2":
                errors.append("source_refs[0].section must be 6.2.2")

    claim_boundary = data.get("claim_boundary")
    if not isinstance(claim_boundary, dict):
        errors.append("claim_boundary must be a mapping")
        claim_boundary = {}
    if claim_boundary.get("current_imported_usage") is not False:
        errors.append("claim_boundary.current_imported_usage must be false")
    if claim_boundary.get("claim_level_default") != "scaffold":
        errors.append("claim_boundary.claim_level_default must be scaffold")
    if claim_boundary.get("evidence_status_default") != "not_imported":
        errors.append("claim_boundary.evidence_status_default must be not_imported")
    if claim_boundary.get("verified_entries") != 0:
        errors.append("claim_boundary.verified_entries must remain 0")
    if claim_boundary.get("reviewed_entries") != 0:
        errors.append("claim_boundary.reviewed_entries must remain 0")

    entries = data.get("entries")
    if not isinstance(entries, list):
        errors.append("entries must be a list")
        entries = []
    if len(entries) != len(EXPECTED_ITEMS):
        errors.append(f"entries must contain exactly {len(EXPECTED_ITEMS)} report descriptor item shells")

    seen: set[str] = set()
    required_fields = {"item_id", "item_name", "item_kind", "summary", "claim_level", "evidence_status", "source_anchor"}
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"entries[{index}] must be a mapping")
            continue
        name = entry.get("item_name")
        if not isinstance(name, str):
            errors.append(f"entries[{index}].item_name must be a string")
            continue
        seen.add(name)
        missing_fields = sorted(required_fields - set(entry))
        if missing_fields:
            errors.append(f"{name} missing fields: {', '.join(missing_fields)}")
        if entry.get("item_kind") not in {"item_prefix", "item_type"}:
            errors.append(f"{name}.item_kind must be item_prefix or item_type")
        if entry.get("claim_level") != "scaffold":
            errors.append(f"{name}.claim_level must remain scaffold")
        if entry.get("evidence_status") != "not_imported":
            errors.append(f"{name}.evidence_status must remain not_imported")

        source_anchor = entry.get("source_anchor")
        if not isinstance(source_anchor, dict):
            errors.append(f"{name} must include source_anchor")
            continue
        if source_anchor.get("source_id") != "hid_spec_1_11":
            errors.append(f"{name} source_id must be hid_spec_1_11")
        if source_anchor.get("section") != "6.2.2":
            errors.append(f"{name} source section must be 6.2.2")
        if not isinstance(source_anchor.get("topic"), str) or not source_anchor.get("topic"):
            errors.append(f"{name} source topic must be present")

    missing = sorted(EXPECTED_ITEMS - seen)
    if missing:
        errors.append(f"missing HID report descriptor item shells: {', '.join(missing)}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    args = parser.parse_args()

    errors = validate(args.matrix)
    if errors:
        print("FAIL validate_hid_report_descriptor_items_matrix")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS validate_hid_report_descriptor_items_matrix")
    return 0


if __name__ == "__main__":
    sys.exit(main())
