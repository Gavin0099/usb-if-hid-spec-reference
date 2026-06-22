#!/usr/bin/env python3
"""Validate the HID verified evidence packet preflight schema.

Authority ceiling: verified_preflight_contract_only.
This validator checks governance structure only and does not promote entries.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "contract" / "evidence_packet_schema.yaml"
EVIDENCE_DIR = ROOT / "docs" / "evidence"

REQUIRED_STATUS_VALUES = {"shell", "candidate", "accepted", "rejected"}
REQUIRED_SECTIONS = {
    "packet_identity",
    "governed_entry_binding",
    "source_trace",
    "claim_delta",
    "evidence_body",
    "non_claims",
    "validation",
    "approval",
    "residual_risk",
}
REQUIRED_GATE_FLAGS = {
    "requires_human_approval",
    "requires_registered_source_authority",
    "requires_governed_entry_binding",
    "requires_validation_pass",
}


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return data


def _write_receipt(path: Path, receipt: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def _evidence_shell_statuses() -> dict[str, str]:
    statuses: dict[str, str] = {}
    if not EVIDENCE_DIR.exists():
        return statuses
    pattern = re.compile(r"^>\s*Status:\s*(.+?)\s*$", re.IGNORECASE | re.MULTILINE)
    for path in sorted(EVIDENCE_DIR.glob("*_packet.md")):
        text = path.read_text(encoding="utf-8")
        match = pattern.search(text)
        statuses[str(path.relative_to(ROOT))] = match.group(1).strip() if match else "missing"
    return statuses


def validate() -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    findings: list[dict[str, str]] = []

    def add_error(code: str, message: str) -> None:
        errors.append(message)
        findings.append({"code": code, "message": message})

    if not SCHEMA.exists():
        add_error("SCHEMA_MISSING", f"{SCHEMA.relative_to(ROOT)} is missing")
        schema: dict[str, Any] = {}
    else:
        schema = _load_yaml(SCHEMA)

    if schema.get("authority_ceiling") != "verified_preflight_contract_only":
        add_error("AUTHORITY_CEILING_INVALID", "authority_ceiling must be verified_preflight_contract_only")

    status_values = set(schema.get("packet_status_values", []))
    missing_statuses = sorted(REQUIRED_STATUS_VALUES - status_values)
    if missing_statuses:
        add_error("PACKET_STATUS_VALUES_INCOMPLETE", f"missing packet status values: {', '.join(missing_statuses)}")

    sections = set(schema.get("required_sections", []))
    missing_sections = sorted(REQUIRED_SECTIONS - sections)
    if missing_sections:
        add_error("REQUIRED_SECTIONS_INCOMPLETE", f"missing required sections: {', '.join(missing_sections)}")

    required_fields = schema.get("required_fields", {})
    if not isinstance(required_fields, dict):
        add_error("REQUIRED_FIELDS_NOT_MAPPING", "required_fields must be a mapping")
        required_fields = {}
    for section in REQUIRED_SECTIONS:
        fields = required_fields.get(section)
        if not isinstance(fields, list) or not fields:
            add_error("REQUIRED_SECTION_FIELDS_MISSING", f"{section} must define at least one required field")

    gate = schema.get("verified_gate", {})
    if not isinstance(gate, dict):
        add_error("VERIFIED_GATE_NOT_MAPPING", "verified_gate must be a mapping")
        gate = {}
    if gate.get("review_level") != 3:
        add_error("VERIFIED_GATE_REVIEW_LEVEL_INVALID", "verified_gate.review_level must be 3")
    if gate.get("required_packet_status") != "accepted":
        add_error("VERIFIED_GATE_STATUS_INVALID", "verified_gate.required_packet_status must be accepted")
    for flag in sorted(REQUIRED_GATE_FLAGS):
        if gate.get(flag) is not True:
            add_error("VERIFIED_GATE_FLAG_INVALID", f"verified_gate.{flag} must be true")

    non_claims = set(gate.get("requires_non_claims", []))
    for required in ("firmware implementation correctness", "OS input stack behavior"):
        if required not in non_claims:
            add_error("VERIFIED_GATE_NON_CLAIM_MISSING", f"verified gate must preserve non-claim: {required}")

    forbidden_promotions = schema.get("forbidden_promotions", [])
    forbidden_ids = {
        item.get("id")
        for item in forbidden_promotions
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    for required in ("shell_to_verified", "candidate_without_approval", "missing_source_trace", "missing_human_approval"):
        if required not in forbidden_ids:
            add_error("FORBIDDEN_PROMOTION_MISSING", f"missing forbidden promotion: {required}")

    shell_statuses = _evidence_shell_statuses()
    for path, status in shell_statuses.items():
        normalized = status.lower()
        if normalized == "accepted":
            add_error("SHELL_PACKET_ACCEPTED", f"{path} is marked accepted but docs/evidence packets are shell artifacts")
        if "verified" in normalized:
            add_error("SHELL_PACKET_VERIFIED", f"{path} status must not contain verified")

    receipt = {
        "validator": "validate_evidence_packet_schema.py",
        "authority_ceiling": "verified_preflight_contract_only",
        "result": "PASS" if not errors else "FAIL",
        "schema": str(SCHEMA.relative_to(ROOT)),
        "packet_status_values": sorted(status_values),
        "required_sections": sorted(sections),
        "verified_gate": {
            "review_level": gate.get("review_level"),
            "required_packet_status": gate.get("required_packet_status"),
        },
        "checked_shell_packets": shell_statuses,
        "error_count": len(errors),
        "errors": errors,
        "findings": findings,
    }
    return errors, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt-out")
    args = parser.parse_args()

    errors, receipt = validate()
    if args.receipt_out:
        _write_receipt(ROOT / args.receipt_out, receipt)

    if errors:
        print("FAIL validate_evidence_packet_schema")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS validate_evidence_packet_schema")
    print(f"- checked shell packets: {len(receipt['checked_shell_packets'])}")
    print(f"- required sections: {len(receipt['required_sections'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
