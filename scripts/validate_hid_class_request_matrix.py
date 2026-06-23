#!/usr/bin/env python3
"""Validate HID class request scaffold matrix."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX = ROOT / "data" / "hid_class_request_matrix.yaml"

EXPECTED_REQUESTS = {
    "GET_REPORT": {"b_request": "0x01", "direction": "device_to_host"},
    "SET_REPORT": {"b_request": "0x09", "direction": "host_to_device"},
    "GET_IDLE": {"b_request": "0x02", "direction": "device_to_host"},
    "SET_IDLE": {"b_request": "0x0A", "direction": "host_to_device"},
    "GET_PROTOCOL": {"b_request": "0x03", "direction": "device_to_host"},
    "SET_PROTOCOL": {"b_request": "0x0B", "direction": "host_to_device"},
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

    if data.get("matrix_id") != "hid_class_request_matrix":
        errors.append("matrix_id must be hid_class_request_matrix")
    if data.get("status") != "scaffold":
        errors.append("matrix status must be scaffold")

    claim_boundary = data.get("claim_boundary")
    if not isinstance(claim_boundary, dict):
        errors.append("claim_boundary must be a mapping")
        claim_boundary = {}
    boundary_verified = claim_boundary.get("verified_entries")
    if claim_boundary.get("claim_level_default") != "scaffold":
        errors.append("claim_boundary.claim_level_default must be scaffold")

    entries = data.get("entries")
    if not isinstance(entries, list):
        errors.append("entries must be a list")
        entries = []
    if len(entries) != len(EXPECTED_REQUESTS):
        errors.append(f"entries must contain exactly {len(EXPECTED_REQUESTS)} requests")

    seen: set[str] = set()
    required_fields = {
        "request_id",
        "name",
        "b_request",
        "direction",
        "request_type",
        "recipient",
        "purpose",
        "setup_scope",
        "claim_level",
        "evidence_status",
    }
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"entries[{index}] must be a mapping")
            continue
        missing_fields = sorted(required_fields - set(entry))
        if missing_fields:
            errors.append(f"{entry.get('name', f'entries[{index}]')} missing fields: {', '.join(missing_fields)}")

        name = entry.get("name")
        if not isinstance(name, str):
            errors.append(f"entries[{index}].name must be a string")
            continue
        seen.add(name)

        expected = EXPECTED_REQUESTS.get(name)
        if expected is None:
            errors.append(f"unexpected HID class request: {name}")
            continue
        if entry.get("b_request") != expected["b_request"]:
            errors.append(f"{name}.b_request must be {expected['b_request']}")
        if entry.get("direction") != expected["direction"]:
            errors.append(f"{name}.direction must be {expected['direction']}")
        if entry.get("request_type") != "class":
            errors.append(f"{name}.request_type must be class")
        if entry.get("recipient") != "interface":
            errors.append(f"{name}.recipient must be interface")
        if entry.get("claim_level") not in {"scaffold", "reviewed", "verified"}:
            errors.append(f"{name}.claim_level must be scaffold, reviewed, or verified")
        if entry.get("evidence_status") != "not_introduced":
            errors.append(f"{name}.evidence_status must remain not_introduced")

    verified_entries = sum(1 for entry in entries if isinstance(entry, dict) and entry.get("claim_level") == "verified")
    if boundary_verified != verified_entries:
        errors.append(
            f"claim_boundary.verified_entries must match number of verified entries: {boundary_verified} != {verified_entries}"
        )

    missing_requests = sorted(set(EXPECTED_REQUESTS) - seen)
    if missing_requests:
        errors.append(f"missing HID class requests: {', '.join(missing_requests)}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    args = parser.parse_args()

    errors = validate(args.matrix)
    if errors:
        print("FAIL validate_hid_class_request_matrix")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS validate_hid_class_request_matrix")
    return 0


if __name__ == "__main__":
    sys.exit(main())
