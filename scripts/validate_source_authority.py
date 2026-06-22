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
    usage = []

    if hid_1_11 is None:
        errors.append("primary_sources must include hid_1_11")
    else:
        if hid_1_11.get("version") != "1.11":
            errors.append("hid_1_11.version must be 1.11")
        if hid_1_11.get("role") != "primary":
            errors.append("hid_1_11.role must be primary")

        usage = hid_1_11.get("current_imported_usage", [])
        if not isinstance(usage, list):
            errors.append("hid_1_11.current_imported_usage must be a list")
            usage = []
        elif len(usage) != 3:
            errors.append("hid_1_11.current_imported_usage must contain exactly three entries")
        else:
            used_sections = {
                entry.get("section")
                for entry in usage
                if isinstance(entry, dict)
            }
            usage_by_section = {
                entry.get("section"): entry
                for entry in usage
                if isinstance(entry, dict)
            }

            class_request_entry = usage_by_section.get("7.2")
            if class_request_entry is None:
                errors.append("hid_1_11.current_imported_usage must include section 7.2")
            else:
                if class_request_entry.get("topic") != "Class-Specific Requests":
                    errors.append("section 7.2 topic must be Class-Specific Requests")
                if class_request_entry.get("status") != "scaffolded":
                    errors.append("section 7.2 status must be scaffolded")

            descriptor_entry = usage_by_section.get("6.2.1")
            if descriptor_entry is None:
                errors.append("hid_1_11.current_imported_usage must include section 6.2.1")
            else:
                if descriptor_entry.get("topic") != "HID Descriptor":
                    errors.append("section 6.2.1 topic must be HID Descriptor")
                if descriptor_entry.get("status") != "scaffolded":
                    errors.append("section 6.2.1 status must be scaffolded")

            report_descriptor_entry = usage_by_section.get("6.2.2")
            if report_descriptor_entry is None:
                errors.append("hid_1_11.current_imported_usage must include section 6.2.2")
            else:
                if report_descriptor_entry.get("topic") != "Report Descriptor item types":
                    errors.append("section 6.2.2 topic must be Report Descriptor item types")
                if report_descriptor_entry.get("status") != "scaffolded":
                    errors.append("section 6.2.2 status must be scaffolded")

            if used_sections != {"7.2", "6.2.1", "6.2.2"}:
                errors.append("hid_1_11.current_imported_usage sections must be 7.2, 6.2.1, and 6.2.2 only")

        future_usage = hid_1_11.get("future_authorized_usage")
        if future_usage is None:
            errors.append("future_authorized_usage must exist")
        elif not isinstance(future_usage, list):
            errors.append("future_authorized_usage must be a list")
        else:
            seen_sections: set[str] = set()
            for index, entry in enumerate(future_usage):
                if not isinstance(entry, dict):
                    errors.append(f"future_authorized_usage[{index}] must be a mapping")
                    continue
                section = entry.get("section")
                topic = entry.get("topic")
                status = entry.get("status")
                if not isinstance(section, str) or not section.strip():
                    errors.append(f"future_authorized_usage[{index}].section must be a non-empty string")
                if not isinstance(topic, str) or not topic.strip():
                    errors.append(f"future_authorized_usage[{index}].topic must be a non-empty string")
                if not isinstance(status, str) or not status.strip():
                    errors.append(f"future_authorized_usage[{index}].status must be a non-empty string")
                if isinstance(section, str) and section in seen_sections:
                    errors.append(f"future_authorized_usage contains duplicate section {section}")
                if isinstance(section, str):
                    seen_sections.add(section)

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
