#!/usr/bin/env python3
"""Validate repo-local HID contract YAML consistency.

Authority ceiling: contract_structural_consistency_only.
Does not validate HID semantics or promote claims.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_DIR = ROOT / "contract"
SOURCE_AUTHORITY = ROOT / "data" / "source_authority.yaml"
MANIFEST = ROOT / "exports" / "hid_governed_surface_manifest.yaml"

REQUIRED_CONTRACTS = {
    "authority_levels.yaml",
    "claim_rules.yaml",
    "evidence_requirements.yaml",
    "version_scope.yaml",
}
REQUIRED_AUTHORITY_LEVELS = {
    "normative_official",
    "official_secondary",
    "official_index",
    "community_reference",
    "excluded",
}
REQUIRED_FORBIDDEN_CLAIMS = {
    "scaffold_as_verified",
    "usage_tables_before_import",
    "os_stack_behavior_from_hid_spec",
    "firmware_correctness_from_reference",
    "hub_class_behavior",
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


def validate() -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    findings: list[dict[str, str]] = []

    def add_error(code: str, message: str) -> None:
        errors.append(message)
        findings.append({"code": code, "message": message})

    missing_contracts = sorted(name for name in REQUIRED_CONTRACTS if not (CONTRACT_DIR / name).exists())
    if missing_contracts:
        add_error("CONTRACT_FILE_MISSING", f"missing contract files: {', '.join(missing_contracts)}")

    docs = {
        name: _load_yaml(CONTRACT_DIR / name)
        for name in REQUIRED_CONTRACTS
        if (CONTRACT_DIR / name).exists()
    }

    authority = docs.get("authority_levels.yaml", {})
    authority_levels = authority.get("authority_levels", {})
    if not isinstance(authority_levels, dict):
        add_error("AUTHORITY_LEVELS_NOT_MAPPING", "authority_levels must be a mapping")
        authority_levels = {}
    missing_levels = sorted(REQUIRED_AUTHORITY_LEVELS - set(authority_levels))
    if missing_levels:
        add_error("AUTHORITY_LEVEL_MISSING", f"missing authority levels: {', '.join(missing_levels)}")

    claim_rules = docs.get("claim_rules.yaml", {})
    forbidden_claims = claim_rules.get("forbidden_claims", [])
    if not isinstance(forbidden_claims, list):
        add_error("FORBIDDEN_CLAIMS_NOT_LIST", "forbidden_claims must be a list")
        forbidden_claim_ids: set[str] = set()
    else:
        forbidden_claim_ids = {
            claim["id"]
            for claim in forbidden_claims
            if isinstance(claim, dict) and isinstance(claim.get("id"), str)
        }
    missing_forbidden = sorted(REQUIRED_FORBIDDEN_CLAIMS - forbidden_claim_ids)
    if missing_forbidden:
        add_error("FORBIDDEN_CLAIM_MISSING", f"missing forbidden claims: {', '.join(missing_forbidden)}")

    evidence = docs.get("evidence_requirements.yaml", {})
    required_entry_fields = evidence.get("required_fields_for_each_governed_entry", [])
    if not isinstance(required_entry_fields, list) or "claim_ceiling" not in required_entry_fields:
        add_error("EVIDENCE_REQUIRED_FIELDS_INCOMPLETE", "evidence requirements must include claim_ceiling")
    claim_level_values = evidence.get("claim_level_values", [])
    if not isinstance(claim_level_values, list) or "scaffold" not in claim_level_values or "verified" not in claim_level_values:
        add_error("CLAIM_LEVEL_VALUES_INCOMPLETE", "claim_level_values must include scaffold and verified")

    version_scope = docs.get("version_scope.yaml", {})
    versions = version_scope.get("versions", {})
    hid11 = versions.get("hid11", {}) if isinstance(versions, dict) else {}
    imported_sections = set(hid11.get("imported_sections", [])) if isinstance(hid11, dict) else set()

    source_authority = _load_yaml(SOURCE_AUTHORITY)
    hid_source = next(
        (
            source
            for source in source_authority.get("primary_sources", [])
            if isinstance(source, dict) and source.get("id") == "hid_1_11"
        ),
        {},
    )
    source_sections = {
        entry.get("section")
        for entry in hid_source.get("current_imported_usage", [])
        if isinstance(entry, dict)
    }
    if imported_sections != source_sections:
        add_error(
            "VERSION_SCOPE_SOURCE_AUTHORITY_MISMATCH",
            f"version_scope hid11 sections {sorted(imported_sections)} != source_authority sections {sorted(source_sections)}",
        )

    manifest = _load_yaml(MANIFEST)
    manifest_ceiling = ((manifest.get("claim_ceiling") or {}).get("default"))
    if manifest_ceiling != hid11.get("claim_ceiling"):
        add_error(
            "MANIFEST_CLAIM_CEILING_MISMATCH",
            f"manifest claim ceiling {manifest_ceiling!r} != version_scope hid11 claim ceiling {hid11.get('claim_ceiling')!r}",
        )

    surface = (manifest.get("authority_surface") or {}).get("hid11", {})
    if surface.get("verified") != 0:
        add_error("HID11_VERIFIED_NOT_ZERO", "HID scaffold manifest must keep verified count at 0")
    if surface.get("scaffold") != surface.get("tracked"):
        add_error("HID11_SCAFFOLD_TRACKED_MISMATCH", "HID scaffold count must equal tracked count")

    receipt = {
        "validator": "validate_contract_files.py",
        "authority_ceiling": "contract_structural_consistency_only",
        "result": "PASS" if not errors else "FAIL",
        "checked_contracts": sorted(docs),
        "checked_authority_levels": sorted(authority_levels),
        "checked_forbidden_claims": sorted(forbidden_claim_ids),
        "source_authority_sections": sorted(source_sections),
        "version_scope_sections": sorted(imported_sections),
        "manifest_claim_ceiling": manifest_ceiling,
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
        print("FAIL validate_contract_files")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS validate_contract_files")
    print(f"- checked contracts: {len(receipt['checked_contracts'])}")
    print(f"- claim ceiling: {receipt['manifest_claim_ceiling']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
