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
DEFAULT_MATRIX = ROOT / "data" / "hid_class_request_matrix.yaml"
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


def expected_counts(matrix_path: Path = DEFAULT_MATRIX) -> dict[str, int]:
    data = load_yaml(matrix_path)
    entries = data.get("entries")
    if not isinstance(entries, list):
        raise ValueError("matrix entries must be a list")
    verified = sum(1 for entry in entries if isinstance(entry, dict) and entry.get("claim_level") == "verified")
    reviewed = sum(1 for entry in entries if isinstance(entry, dict) and entry.get("claim_level") == "reviewed")
    inferred = sum(1 for entry in entries if isinstance(entry, dict) and entry.get("claim_level") == "inferred")
    missing = sum(1 for entry in entries if isinstance(entry, dict) and entry.get("claim_level") == "missing")
    return {
        "tracked": len(entries),
        "verified": verified,
        "reviewed": reviewed,
        "inferred": inferred,
        "missing": missing,
        "evidence_packets": 0,
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


def validate(matrix_path: Path = DEFAULT_MATRIX, status_pages: list[Path] | None = None) -> list[str]:
    errors: list[str] = []
    status_pages = status_pages or DEFAULT_STATUS_PAGES
    expected = expected_counts(matrix_path)
    for page in status_pages:
        rows = parse_rows(page)
        class_requests = rows.get("HID class requests")
        total = rows.get("Total")
        packets = rows.get("evidence_packets")

        if not isinstance(class_requests, dict):
            errors.append(f"{page}: missing HID class requests summary row")
        else:
            for key in ("tracked", "verified", "reviewed", "inferred", "missing"):
                if class_requests.get(key) != expected[key]:
                    errors.append(f"{page}: HID class requests {key} must be {expected[key]}")

        if not isinstance(total, dict):
            errors.append(f"{page}: missing Total summary row")
        else:
            for key in ("tracked", "verified", "reviewed", "inferred", "missing"):
                if total.get(key) != expected[key]:
                    errors.append(f"{page}: Total {key} must be {expected[key]}")

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
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    parser.add_argument("--status-page", action="append", type=Path, dest="status_pages")
    args = parser.parse_args()

    errors = validate(args.matrix, args.status_pages)
    if errors:
        print("FAIL validate_verification_status")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS validate_verification_status")
    return 0


if __name__ == "__main__":
    sys.exit(main())
