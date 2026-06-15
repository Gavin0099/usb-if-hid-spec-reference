#!/usr/bin/env python3
"""Validate visible verification status counts against HID scaffold data."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRICES = [
    ROOT / "data" / "hid_class_request_matrix.yaml",
    ROOT / "data" / "hid_descriptor_fields_matrix.yaml",
]
DEFAULT_STATUS_PAGES = [
    ROOT / "specs" / "verification_status.md",
    ROOT / "specs" / "en" / "verification_status.md",
]

SUMMARY_ROW_RE = re.compile(
    r"^\|\s*(?P<area>\*{0,2}[^|]+?\*{0,2})\s*\|\s*\*{0,2}(?P<tracked>\d+)\*{0,2}\s*\|"
    r"\s*\*{0,2}(?P<verified>\d+)\*{0,2}\s*\|\s*\*{0,2}(?P<reviewed>\d+)\*{0,2}\s*\|"
    r"\s*\*{0,2}(?P<inferred>\d+)\*{0,2}\s*\|\s*\*{0,2}(?P<missing>\d+)\*{0,2}\s*\|$"
)
EVIDENCE_PACKET_RE = re.compile(r"^\|\s*Entry verification packets\s*\|\s*(?P<count>\d+)\s*\|")


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return data


def expected_counts(matrix_paths: list[Path] | None = None) -> dict[str, int]:
    matrix_paths = matrix_paths or DEFAULT_MATRICES
    area_tracked: dict[str, int] = {
        "HID descriptors": 0,
        "HID report descriptors": 0,
        "HID class requests": 0,
        "Report / boot / idle semantics": 0,
    }

    verified = reviewed = inferred = missing = 0

    for matrix_path in matrix_paths:
        data = load_yaml(matrix_path)
        entries = data.get("entries")
        if not isinstance(entries, list):
            raise ValueError(f"{matrix_path} entries must be a list")

        matrix_id = data.get("matrix_id")
        if matrix_id == "hid_class_request_matrix":
            area_tracked["HID class requests"] = len(entries)
        elif matrix_id == "hid_descriptor_fields_matrix":
            area_tracked["HID descriptors"] = len(entries)
        else:
            raise ValueError(f"{matrix_path} matrix_id is not recognized")

        verified += sum(1 for entry in entries if isinstance(entry, dict) and entry.get("claim_level") == "verified")
        reviewed += sum(1 for entry in entries if isinstance(entry, dict) and entry.get("claim_level") == "reviewed")
        inferred += sum(1 for entry in entries if isinstance(entry, dict) and entry.get("claim_level") == "inferred")
        missing += sum(1 for entry in entries if isinstance(entry, dict) and entry.get("claim_level") == "missing")

    tracked = sum(area_tracked.values())
    return {
        "tracked": tracked,
        "verified": verified,
        "reviewed": reviewed,
        "inferred": inferred,
        "missing": missing,
        "evidence_packets": 0,
        "area_tracked": area_tracked,
    }


def parse_rows(path: Path) -> dict[str, dict[str, int] | int]:
    rows: dict[str, dict[str, int] | int] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        row = SUMMARY_ROW_RE.match(line)
        if row:
            area = row.group("area").strip().strip("*")
            rows[area] = {
                "tracked": int(row.group("tracked")),
                "verified": int(row.group("verified")),
                "reviewed": int(row.group("reviewed")),
                "inferred": int(row.group("inferred")),
                "missing": int(row.group("missing")),
            }
            continue

        packet = EVIDENCE_PACKET_RE.match(line)
        if packet:
            rows["evidence_packets"] = int(packet.group("count"))
    return rows


def validate(matrix_paths: list[Path] | None = None, status_pages: list[Path] | None = None) -> list[str]:
    errors: list[str] = []
    status_pages = status_pages or DEFAULT_STATUS_PAGES
    expected = expected_counts(matrix_paths)

    for page in status_pages:
        rows = parse_rows(page)

        for area, expected_tracked in expected["area_tracked"].items():
            row = rows.get(area)
            if not isinstance(row, dict):
                errors.append(f"{page}: missing {area} summary row")
                continue
            for key in ("tracked", "verified", "reviewed", "inferred", "missing"):
                if key == "tracked":
                    if row.get(key) != expected_tracked:
                        errors.append(f"{page}: {area} {key} must be {expected_tracked}")
                else:
                    if row.get(key) != expected[key]:
                        errors.append(f"{page}: {area} {key} must be {expected[key]}")

        total = rows.get("Total")
        if not isinstance(total, dict):
            errors.append(f"{page}: missing Total summary row")
        else:
            for key in ("tracked", "verified", "reviewed", "inferred", "missing"):
                expected_value = expected["tracked"] if key == "tracked" else expected[key]
                if total.get(key) != expected_value:
                    errors.append(f"{page}: Total {key} must be {expected_value}")

        packets = rows.get("evidence_packets")
        if packets != expected["evidence_packets"]:
            errors.append(f"{page}: evidence packet count must be {expected['evidence_packets']}")

        text = page.read_text(encoding="utf-8")
        if "Source authority status: locked." not in text:
            errors.append(f"{page}: missing source authority locked status")
        if "HID Usage Tables | not imported" not in text:
            errors.append(f"{page}: HID Usage Tables must remain not imported")
        if "Firmware handler correctness | excluded" not in text:
            errors.append(f"{page}: firmware handler correctness must remain excluded")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix", type=Path, action="append", dest="matrices")
    parser.add_argument("--status-page", action="append", type=Path, dest="status_pages")
    args = parser.parse_args()

    matrices = args.matrices or DEFAULT_MATRICES
    errors = validate(matrix_paths=matrices, status_pages=args.status_pages)
    if errors:
        print("FAIL validate_verification_status")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS validate_verification_status")
    return 0


if __name__ == "__main__":
    sys.exit(main())
