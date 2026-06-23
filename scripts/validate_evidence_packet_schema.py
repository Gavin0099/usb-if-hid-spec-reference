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
SOURCE_AUTHORITY = ROOT / "data" / "source_authority.yaml"
EVIDENCE_DIR = ROOT / "docs" / "evidence"
CANDIDATE_DIR = EVIDENCE_DIR / "candidates"

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


def _evidence_shell_statuses(evidence_dir: Path = EVIDENCE_DIR) -> dict[str, str]:
    statuses: dict[str, str] = {}
    if not evidence_dir.exists():
        return statuses
    pattern = re.compile(r"^>\s*Status:\s*(.+?)\s*$", re.IGNORECASE | re.MULTILINE)
    for path in sorted(evidence_dir.glob("*_packet.md")):
        text = path.read_text(encoding="utf-8")
        match = pattern.search(text)
        statuses[_display_path(path)] = match.group(1).strip() if match else "missing"
    return statuses


def _display_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _load_candidate_packets(candidate_dir: Path = CANDIDATE_DIR) -> dict[str, dict[str, Any]]:
    packets: dict[str, dict[str, Any]] = {}
    if not candidate_dir.exists():
        return packets
    for path in sorted(candidate_dir.glob("*.yaml")):
        packets[_display_path(path)] = _load_yaml(path)
    return packets


def _default_matrix_paths() -> dict[str, Path]:
    return {
        "hid_class_request_matrix": ROOT / "data" / "hid_class_request_matrix.yaml",
        "hid_descriptor_fields_matrix": ROOT / "data" / "hid_descriptor_fields_matrix.yaml",
        "hid_report_descriptor_items_matrix": ROOT / "data" / "hid_report_descriptor_items_matrix.yaml",
    }


def _entry_index(matrix_paths: dict[str, Path] | None = None) -> dict[tuple[str, str], dict[str, Any]]:
    index: dict[tuple[str, str], dict[str, Any]] = {}
    matrix_paths = matrix_paths or _default_matrix_paths()
    id_fields = ("request_id", "field_id", "item_id")
    for matrix_id, path in matrix_paths.items():
        if not path.exists():
            continue
        data = _load_yaml(path)
        for entry in data.get("entries", []):
            if not isinstance(entry, dict):
                continue
            entry_id = next((entry.get(field) for field in id_fields if isinstance(entry.get(field), str)), None)
            if entry_id:
                index[(matrix_id, entry_id)] = entry
    return index


def _matrix_source_ref_index(matrix_paths: dict[str, Path] | None = None) -> dict[str, set[tuple[str, str]]]:
    refs: dict[str, set[tuple[str, str]]] = {}
    matrix_paths = matrix_paths or _default_matrix_paths()
    for matrix_id, path in matrix_paths.items():
        matrix_refs: set[tuple[str, str]] = set()
        if path.exists():
            data = _load_yaml(path)
            for source_ref in data.get("source_refs", []):
                if not isinstance(source_ref, dict):
                    continue
                source_id = source_ref.get("source_id")
                section = source_ref.get("section")
                if isinstance(source_id, str) and isinstance(section, str):
                    matrix_refs.add((source_id, section))
        refs[matrix_id] = matrix_refs
    return refs


def _source_authority_index(source_authority: Path = SOURCE_AUTHORITY) -> set[tuple[str, str]]:
    if not source_authority.exists():
        return set()
    data = _load_yaml(source_authority)
    allowed: set[tuple[str, str]] = set()
    for source in data.get("primary_sources", []):
        if not isinstance(source, dict) or not isinstance(source.get("id"), str):
            continue
        source_id = source["id"]
        for usage in source.get("current_imported_usage", []):
            if isinstance(usage, dict) and isinstance(usage.get("section"), str):
                allowed.add((source_id, usage["section"]))
    return allowed


def validate(
    *,
    schema_path: Path = SCHEMA,
    source_authority_path: Path = SOURCE_AUTHORITY,
    evidence_dir: Path = EVIDENCE_DIR,
    candidate_dir: Path = CANDIDATE_DIR,
    matrix_paths: dict[str, Path] | None = None,
) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    findings: list[dict[str, str]] = []

    def add_error(code: str, message: str) -> None:
        errors.append(message)
        findings.append({"code": code, "message": message})

    if not schema_path.exists():
        add_error("SCHEMA_MISSING", f"{_display_path(schema_path)} is missing")
        schema: dict[str, Any] = {}
    else:
        schema = _load_yaml(schema_path)

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

    shell_statuses = _evidence_shell_statuses(evidence_dir)
    for path, status in shell_statuses.items():
        normalized = status.lower()
        if normalized == "accepted":
            add_error("SHELL_PACKET_ACCEPTED", f"{path} is marked accepted but docs/evidence packets are shell artifacts")
        if "verified" in normalized:
            add_error("SHELL_PACKET_VERIFIED", f"{path} status must not contain verified")

    candidate_packets = _load_candidate_packets(candidate_dir)
    entries = _entry_index(matrix_paths)
    matrix_source_refs = _matrix_source_ref_index(matrix_paths)
    source_authority_bindings = _source_authority_index(source_authority_path)
    for path, packet in candidate_packets.items():
        for section in REQUIRED_SECTIONS:
            section_data = packet.get(section)
            if not isinstance(section_data, dict):
                add_error("CANDIDATE_SECTION_MISSING", f"{path} missing section: {section}")
                continue
            for field in required_fields.get(section, []):
                value = section_data.get(field)
                if value in (None, "", []):
                    add_error("CANDIDATE_FIELD_MISSING", f"{path} missing {section}.{field}")

        identity = packet.get("packet_identity", {}) if isinstance(packet.get("packet_identity"), dict) else {}
        status = identity.get("packet_status")
        if status != "candidate":
            add_error("CANDIDATE_STATUS_INVALID", f"{path} packet_identity.packet_status must be candidate")
        if identity.get("target_claim_level") != "verified":
            add_error("CANDIDATE_TARGET_INVALID", f"{path} packet_identity.target_claim_level must be verified")
        if identity.get("review_level") != 3:
            add_error("CANDIDATE_REVIEW_LEVEL_INVALID", f"{path} packet_identity.review_level must be 3")

        binding = packet.get("governed_entry_binding", {}) if isinstance(packet.get("governed_entry_binding"), dict) else {}
        matrix = binding.get("matrix")
        entry_id = binding.get("entry_id")
        entry = entries.get((matrix, entry_id)) if isinstance(matrix, str) and isinstance(entry_id, str) else None
        if entry is None:
            add_error("CANDIDATE_ENTRY_BINDING_INVALID", f"{path} does not bind to a known governed entry")
        else:
            if binding.get("current_claim_level") != entry.get("claim_level"):
                add_error("CANDIDATE_CURRENT_CLAIM_MISMATCH", f"{path} current_claim_level does not match governed entry")
            if binding.get("current_evidence_status") != entry.get("evidence_status"):
                add_error("CANDIDATE_CURRENT_EVIDENCE_MISMATCH", f"{path} current_evidence_status does not match governed entry")

        source_trace = packet.get("source_trace", {}) if isinstance(packet.get("source_trace"), dict) else {}
        source_id = source_trace.get("source_id")
        source_section = source_trace.get("source_section")
        if (source_id, source_section) not in source_authority_bindings:
            add_error(
                "CANDIDATE_SOURCE_AUTHORITY_MISMATCH",
                f"{path} source_trace {source_id!r} section {source_section!r} is not current imported source authority",
            )
        if isinstance(matrix, str) and (source_id, source_section) not in matrix_source_refs.get(matrix, set()):
            add_error(
                "CANDIDATE_MATRIX_SOURCE_REF_MISMATCH",
                f"{path} source_trace {source_id!r} section {source_section!r} does not match {matrix}.source_refs",
            )

        approval = packet.get("approval", {}) if isinstance(packet.get("approval"), dict) else {}
        if approval.get("approval_record") not in {"pending", "rejected"}:
            add_error("CANDIDATE_APPROVAL_INVALID", f"{path} candidate approval_record must remain pending or rejected")

        claim_delta = packet.get("claim_delta", {}) if isinstance(packet.get("claim_delta"), dict) else {}
        cannot_claim = claim_delta.get("cannot_claim_after_acceptance", [])
        if not isinstance(cannot_claim, list) or "firmware behavior correctness" not in cannot_claim:
            add_error("CANDIDATE_NON_CLAIM_INCOMPLETE", f"{path} must preserve firmware behavior correctness as a non-claim")

    receipt = {
        "validator": "validate_evidence_packet_schema.py",
        "authority_ceiling": "verified_preflight_contract_only",
        "result": "PASS" if not errors else "FAIL",
        "schema": _display_path(schema_path),
        "packet_status_values": sorted(status_values),
        "required_sections": sorted(sections),
        "verified_gate": {
            "review_level": gate.get("review_level"),
            "required_packet_status": gate.get("required_packet_status"),
        },
        "checked_shell_packets": shell_statuses,
        "checked_candidate_packets": sorted(candidate_packets),
        "checked_source_authority_bindings": sorted(
            f"{source_id}:{section}"
            for source_id, section in source_authority_bindings
        ),
        "checked_matrix_source_refs": {
            matrix_id: sorted(
                f"{source_id}:{section}"
                for source_id, section in refs
            )
            for matrix_id, refs in sorted(matrix_source_refs.items())
        },
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
    print(f"- checked candidate packets: {len(receipt['checked_candidate_packets'])}")
    print(f"- required sections: {len(receipt['required_sections'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
