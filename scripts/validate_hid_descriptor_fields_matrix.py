#!/usr/bin/env python3
"""Validate HID descriptor fields scaffold matrix."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX = ROOT / "data" / "hid_descriptor_fields_matrix.yaml"

EXPECTED_FIELDS = {
    "bLength",
    "bDescriptorType",
    "bcdHID",
    "bCountryCode",
    "bNumDescriptors",
    "bDescriptorType_subordinate",
    "wDescriptorLength",
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

    if data.get("matrix_id") != "hid_descriptor_fields_matrix":
        errors.append("matrix_id must be hid_descriptor_fields_matrix")
    if data.get("status") != "scaffold":
        errors.append("matrix status must be scaffold")

    claim_boundary = data.get("claim_boundary")
    entries = data.get("entries")
    if not isinstance(entries, list):
        entries = []
    if not isinstance(claim_boundary, dict):
        errors.append("claim_boundary must be a mapping")
        claim_boundary = {}
    if claim_boundary.get("claim_level_default") != "reviewed":
        errors.append("claim_boundary.claim_level_default must be reviewed")
    expected_reviewed = len([entry for entry in entries if isinstance(entry, dict) and entry.get("claim_level") == "reviewed"])
    expected_verified = len([entry for entry in entries if isinstance(entry, dict) and entry.get("claim_level") == "verified"])
    if claim_boundary.get("reviewed_entries") != expected_reviewed:
        errors.append("claim_boundary.reviewed_entries must match count of reviewed entries")
    if claim_boundary.get("verified_entries") != expected_verified:
        errors.append("claim_boundary.verified_entries must match count of verified entries")

    if not isinstance(data.get("entries"), list):
        errors.append("entries must be a list")
    if len(entries) != len(EXPECTED_FIELDS):
        errors.append(f"entries must contain exactly {len(EXPECTED_FIELDS)} fields")

    seen: set[str] = set()
    required_fields = {"field_id", "field_name", "summary", "claim_level", "evidence_status"}
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"entries[{index}] must be a mapping")
            continue
        name = entry.get("field_name")
        if not isinstance(name, str):
            errors.append(f"entries[{index}].field_name must be a string")
            continue
        seen.add(name)
        missing_fields = sorted(required_fields - set(entry))
        if missing_fields:
            errors.append(f"{name} missing fields: {', '.join(missing_fields)}")
        if entry.get("claim_level") not in {"scaffold", "reviewed", "verified"}:
            errors.append(f"{name}.claim_level must be scaffold, reviewed, or verified")
        if entry.get("evidence_status") != "not_verified":
            errors.append(f"{name}.evidence_status must remain not_verified")

        source_anchor = entry.get("source_anchor")
        if not isinstance(source_anchor, dict):
            errors.append(f"{name} must include source_anchor")
            continue
        if source_anchor.get("source_id") != "hid_1_11":
            errors.append(f"{name} source_id must be hid_1_11")
        if source_anchor.get("section") != "6.2.1":
            errors.append(f"{name} source section must be 6.2.1")
        if source_anchor.get("topic") != "HID Descriptor":
            errors.append(f"{name} source topic must be HID Descriptor")

    missing = sorted(EXPECTED_FIELDS - seen)
    if missing:
        errors.append(f"missing HID descriptor fields: {', '.join(missing)}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    args = parser.parse_args()

    errors = validate(args.matrix)
    if errors:
        print("FAIL validate_hid_descriptor_fields_matrix")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS validate_hid_descriptor_fields_matrix")
    return 0


if __name__ == "__main__":
    sys.exit(main())
