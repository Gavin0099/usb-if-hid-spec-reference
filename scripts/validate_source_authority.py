#!/usr/bin/env python3
"""Validate HID source authority lock."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_AUTHORITY = ROOT / "data" / "source_authority.yaml"

REQUIRED_EXCLUDED = {
    "hid_over_i2c",
    "os_input_stack_behavior",
    "firmware_handler_correctness",
    "hub_class_behavior",
    "report_payload_semantics_beyond_identity_scaffold",
}


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return data


def validate(path: Path = DEFAULT_AUTHORITY) -> list[str]:
    errors: list[str] = []
    data = load_yaml(path)

    if data.get("status") != "locked":
        errors.append("source_authority.status must be locked")

    primary_sources = data.get("primary_sources")
    if not isinstance(primary_sources, list):
        errors.append("primary_sources must be a list")
        primary_sources = []

    hid_1_11 = next(
        (source for source in primary_sources if isinstance(source, dict) and source.get("id") == "hid_1_11"),
        None,
    )
    if hid_1_11 is None:
        errors.append("primary_sources must include hid_1_11")
    else:
        if hid_1_11.get("version") != "1.11":
            errors.append("hid_1_11.version must be 1.11")
        if hid_1_11.get("role") != "primary":
            errors.append("hid_1_11.role must be primary")
        usage = hid_1_11.get("current_imported_usage")
        if not isinstance(usage, list) or len(usage) != 1:
            errors.append("hid_1_11.current_imported_usage must contain exactly one entry")
        else:
            usage_entry = usage[0]
            if not isinstance(usage_entry, dict):
                errors.append("hid_1_11.current_imported_usage[0] must be a mapping")
            else:
                if usage_entry.get("section") != "7.2":
                    errors.append("hid_1_11 imported section must be 7.2")
                if usage_entry.get("topic") != "Class-Specific Requests":
                    errors.append("hid_1_11 imported topic must be Class-Specific Requests")
                if usage_entry.get("status") != "scaffolded":
                    errors.append("hid_1_11 imported usage status must be scaffolded")

    secondary_sources = data.get("secondary_sources")
    if not isinstance(secondary_sources, list):
        errors.append("secondary_sources must be a list")
        secondary_sources = []

    usage_tables = next(
        (source for source in secondary_sources if isinstance(source, dict) and source.get("id") == "hid_usage_tables"),
        None,
    )
    if usage_tables is None:
        errors.append("secondary_sources must include hid_usage_tables")
    elif usage_tables.get("status") != "not_imported":
        errors.append("hid_usage_tables.status must remain not_imported")

    excluded_sources = data.get("excluded_sources")
    if not isinstance(excluded_sources, list):
        errors.append("excluded_sources must be a list")
        excluded_sources = []
    excluded_ids = {
        source.get("id")
        for source in excluded_sources
        if isinstance(source, dict) and isinstance(source.get("id"), str)
    }
    missing = sorted(REQUIRED_EXCLUDED - excluded_ids)
    if missing:
        errors.append(f"excluded_sources missing required ids: {', '.join(missing)}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--authority", type=Path, default=DEFAULT_AUTHORITY)
    args = parser.parse_args()

    errors = validate(args.authority)
    if errors:
        print("FAIL validate_source_authority")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS validate_source_authority")
    return 0


if __name__ == "__main__":
    sys.exit(main())
