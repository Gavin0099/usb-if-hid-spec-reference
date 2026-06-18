#!/usr/bin/env python3
"""Validate HID source registry against repo-local contract scaffolds.

Authority ceiling: structural_registry_validation_only.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_AUTHORITY_FILE = ROOT / "contract" / "authority_levels.yaml"
DEFAULT_REGISTRY_FILE = ROOT / "evidence" / "source_registry.yaml"
DEFAULT_SOURCE_AUTHORITY_FILE = ROOT / "data" / "source_authority.yaml"

VALID_SOURCE_SCOPES = {
    "hid11",
    "hid_usage_tables",
    "hid_over_i2c",
    "os_input_stack_behavior",
    "firmware_handler_correctness",
    "hub_class_behavior",
    "report_payload_semantics_beyond_identity_scaffold",
}
REQUIRED_SOURCE_FIELDS = {
    "source_id",
    "title",
    "authority_level",
    "source_scope",
    "topics",
    "sections",
    "url",
    "url_type",
    "monitor_status",
    "claim_usage",
}
CLAIM_USAGE_POLICY = {
    "normative_official": {"scaffold_identity_reference_only", "verified_semantic_claim"},
    "official_secondary": {"not_imported", "secondary_lookup_after_import"},
    "official_index": {"discovery_only"},
    "community_reference": {"non_authoritative_cross_check"},
    "excluded": {"excluded"},
}


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return data


def _resolve_path(path_arg: str | None, fallback: Path) -> Path:
    if not path_arg:
        return fallback
    path = Path(path_arg)
    return path if path.is_absolute() else ROOT / path


def _write_receipt(path: Path, receipt: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def _source_authority_ids(path: Path) -> set[str]:
    data = _load_yaml(path)
    ids: set[str] = set()
    for key in ("primary_sources", "secondary_sources", "excluded_sources"):
        entries = data.get(key, [])
        if isinstance(entries, list):
            ids.update(
                entry["id"]
                for entry in entries
                if isinstance(entry, dict) and isinstance(entry.get("id"), str)
            )
    return ids


def validate(
    authority_file: Path = DEFAULT_AUTHORITY_FILE,
    registry_file: Path = DEFAULT_REGISTRY_FILE,
    source_authority_file: Path = DEFAULT_SOURCE_AUTHORITY_FILE,
) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    findings: list[dict[str, str]] = []

    def add_error(code: str, message: str) -> None:
        errors.append(message)
        findings.append({"code": code, "message": message})

    authority_doc = _load_yaml(authority_file)
    authority_levels = authority_doc.get("authority_levels", {})
    if not isinstance(authority_levels, dict) or not authority_levels:
        add_error("AUTHORITY_LEVELS_MISSING", "contract/authority_levels.yaml missing authority_levels")
        authority_level_keys: set[str] = set()
    else:
        authority_level_keys = set(authority_levels)

    source_authority_ids = _source_authority_ids(source_authority_file)
    registry_doc = _load_yaml(registry_file)
    sources = registry_doc.get("sources", [])
    if not isinstance(sources, list):
        add_error("SOURCES_NOT_LIST", "evidence/source_registry.yaml sources must be a list")
        sources = []

    registry_ids: set[str] = set()
    for index, source in enumerate(sources):
        location = f"sources[{index}]"
        if not isinstance(source, dict):
            add_error("SOURCE_NOT_MAPPING", f"{location} must be a mapping")
            continue

        source_id = str(source.get("source_id", f"<missing@{index}>"))
        registry_ids.add(source_id)
        missing_fields = [field for field in REQUIRED_SOURCE_FIELDS if field not in source]
        if missing_fields:
            add_error("REQUIRED_FIELD_MISSING", f"{source_id}: missing fields: {', '.join(sorted(missing_fields))}")

        title = source.get("title")
        if not isinstance(title, str) or not title.strip():
            add_error("TITLE_INVALID", f"{source_id}: title must be a non-empty string")

        authority_level = source.get("authority_level")
        if authority_level not in authority_level_keys:
            add_error("UNKNOWN_AUTHORITY_LEVEL", f"{source_id}: unknown authority_level {authority_level!r}")

        scopes = source.get("source_scope", [])
        if not isinstance(scopes, list) or not scopes:
            add_error("SOURCE_SCOPE_EMPTY", f"{source_id}: source_scope must be a non-empty list")
        else:
            invalid_scopes = [scope for scope in scopes if scope not in VALID_SOURCE_SCOPES]
            if invalid_scopes:
                add_error("SOURCE_SCOPE_INVALID", f"{source_id}: invalid source_scope values: {', '.join(invalid_scopes)}")

        topics = source.get("topics", [])
        if not isinstance(topics, list) or not topics:
            add_error("TOPICS_EMPTY", f"{source_id}: topics must be a non-empty list")

        sections = source.get("sections", [])
        if not isinstance(sections, list):
            add_error("SECTIONS_NOT_LIST", f"{source_id}: sections must be a list")
        if source_id == "hid_1_11" and set(sections) != {"7.2", "6.2.1"}:
            add_error("HID11_SECTIONS_MISMATCH", "hid_1_11 sections must be exactly 7.2 and 6.2.1")
        if source_id != "hid_1_11" and sections:
            add_error("NON_IMPORTED_SOURCE_HAS_SECTIONS", f"{source_id}: non-imported source must not list sections")

        url = source.get("url")
        url_type = source.get("url_type")
        if authority_level == "excluded":
            if url != "out_of_scope" or url_type != "out_of_scope":
                add_error("EXCLUDED_URL_INVALID", f"{source_id}: excluded sources must use out_of_scope url and url_type")
        elif not isinstance(url, str) or not url.startswith("https://"):
            add_error("URL_INVALID", f"{source_id}: url must start with https://")

        allowed_claim_usages = CLAIM_USAGE_POLICY.get(str(authority_level), set())
        claim_usage = source.get("claim_usage")
        if claim_usage not in allowed_claim_usages:
            add_error(
                "CLAIM_USAGE_NOT_ALLOWED",
                f"{source_id}: claim_usage {claim_usage!r} not allowed for authority_level {authority_level!r}",
            )

    missing_from_registry = sorted(source_authority_ids - registry_ids)
    if missing_from_registry:
        add_error(
            "SOURCE_AUTHORITY_ID_MISSING_FROM_REGISTRY",
            f"source registry missing data/source_authority ids: {', '.join(missing_from_registry)}",
        )

    receipt = {
        "validator": "validate_source_registry.py",
        "authority_ceiling": "structural_registry_validation_only",
        "result": "PASS" if not errors else "FAIL",
        "checked_authority_levels": len(authority_level_keys),
        "checked_sources": len(sources),
        "source_authority_ids": sorted(source_authority_ids),
        "registry_ids": sorted(registry_ids),
        "error_count": len(errors),
        "errors": errors,
        "findings": findings,
    }
    return errors, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--authority-file")
    parser.add_argument("--registry-file")
    parser.add_argument("--source-authority-file")
    parser.add_argument("--receipt-out")
    args = parser.parse_args()

    authority_file = _resolve_path(args.authority_file, DEFAULT_AUTHORITY_FILE)
    registry_file = _resolve_path(args.registry_file, DEFAULT_REGISTRY_FILE)
    source_authority_file = _resolve_path(args.source_authority_file, DEFAULT_SOURCE_AUTHORITY_FILE)
    errors, receipt = validate(authority_file, registry_file, source_authority_file)

    if args.receipt_out:
        _write_receipt(_resolve_path(args.receipt_out, ROOT / "evidence" / "validation_receipt_source_registry.json"), receipt)

    if errors:
        print("FAIL validate_source_registry")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS validate_source_registry")
    print(f"- checked authority levels: {receipt['checked_authority_levels']}")
    print(f"- checked sources: {receipt['checked_sources']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
