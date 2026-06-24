#!/usr/bin/env python3
"""Validate Usage Tables matrix proposal artifacts.

Authority ceiling: usage_tables_matrix_schema_proposal_validation_only.
This validator checks proposal structure and non-production boundaries only. It
does not import Usage Tables or create governed matrix entries.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROPOSAL = ROOT / "evidence" / "usage_tables_matrix_proposals" / "usage_page_identity_matrix_proposal.json"
DEFAULT_MARKDOWN = ROOT / "docs" / "evidence" / "usage_tables_matrix_proposals" / "usage_page_identity_matrix_proposal.md"
DEFAULT_USAGE_ID_PROPOSAL = (
    ROOT / "evidence" / "usage_tables_matrix_proposals" / "usage_id_identity_matrix_proposal.json"
)
DEFAULT_USAGE_ID_MARKDOWN = (
    ROOT / "docs" / "evidence" / "usage_tables_matrix_proposals" / "usage_id_identity_matrix_proposal.md"
)
DEFAULT_SOURCE_AUTHORITY = ROOT / "data" / "source_authority.yaml"
DEFAULT_RECEIPT = ROOT / "evidence" / "validation_receipt_usage_tables_matrix_proposals.json"

MATRIX_REQUIREMENTS = {
    "usage_page_identity_matrix": {
        "required_schema_fields": {
            "entry_id",
            "usage_page_id",
            "usage_page_name",
            "source_id",
            "source_section",
            "status",
            "claim_level",
            "notes",
        },
        "future_matrix_path": "data/hid_usage_page_identity_matrix.yaml",
    },
    "usage_id_identity_matrix": {
        "required_schema_fields": {
            "entry_id",
            "usage_page_id",
            "usage_id",
            "usage_id_name",
            "source_id",
            "source_section",
            "status",
            "claim_level",
            "notes",
        },
        "future_matrix_path": "data/hid_usage_id_identity_matrix.yaml",
    },
}
REQUIRED_NON_CLAIMS = {
    "no Usage Tables source authority import in this proposal",
    "no Usage Tables matrix exists in this proposal",
    "no Usage Tables entries are tracked in this proposal",
    "no Usage Tables coverage claim in this proposal",
    "no verified uplift in this proposal",
    "no report payload semantics in this proposal",
}


def _display_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _resolve_under_root(path_arg: str | None, fallback: Path) -> Path:
    if not path_arg:
        return fallback
    path = Path(path_arg)
    candidate = path if path.is_absolute() else ROOT / path
    resolved_root = ROOT.resolve()
    resolved = candidate.resolve()
    try:
        resolved.relative_to(resolved_root)
    except ValueError as exc:
        raise ValueError(f"path must stay under repository root: {path_arg}") from exc
    return resolved


def _load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{_display_path(path)} must contain a JSON object")
    return data


def _load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{_display_path(path)} must contain a YAML mapping")
    return data


def _usage_tables_status(path: Path) -> str | None:
    data = _load_yaml(path)
    for source in data.get("secondary_sources", []):
        if isinstance(source, dict) and source.get("id") == "hid_usage_tables":
            return source.get("status")
    return None


def _write_receipt(path: Path, receipt: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def validate(
    proposal_path: Path = DEFAULT_PROPOSAL,
    *,
    markdown_path: Path = DEFAULT_MARKDOWN,
    source_authority_path: Path = DEFAULT_SOURCE_AUTHORITY,
) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    findings: list[dict[str, str]] = []

    def add_error(code: str, message: str) -> None:
        errors.append(message)
        findings.append({"code": code, "message": message})

    for required_path, code in (
        (proposal_path, "PROPOSAL_JSON_MISSING"),
        (markdown_path, "PROPOSAL_MARKDOWN_MISSING"),
    ):
        if not required_path.exists():
            add_error(code, f"missing required artifact: {_display_path(required_path)}")

    try:
        proposal = _load_json(proposal_path)
    except Exception as exc:
        add_error("PROPOSAL_JSON_LOAD_FAILED", str(exc))
        proposal = {}

    if proposal.get("authority_ceiling") != "usage_tables_matrix_schema_proposal_only":
        add_error("AUTHORITY_CEILING_INVALID", "authority_ceiling must be usage_tables_matrix_schema_proposal_only")
    if proposal.get("proposal_status") != "proposal_only":
        add_error("PROPOSAL_STATUS_INVALID", "proposal_status must be proposal_only")
    if proposal.get("source_id") != "hid_usage_tables":
        add_error("SOURCE_ID_INVALID", "source_id must be hid_usage_tables")
    if proposal.get("source_authority_status_required") != "not_imported":
        add_error("SOURCE_STATUS_REQUIREMENT_INVALID", "source_authority_status_required must be not_imported")
    matrix_id = proposal.get("matrix_id")
    matrix_requirements = MATRIX_REQUIREMENTS.get(matrix_id)
    if matrix_requirements is None:
        add_error(
            "MATRIX_ID_INVALID",
            f"matrix_id must be one of: {', '.join(sorted(MATRIX_REQUIREMENTS))}",
        )
    if matrix_requirements is not None:
        if proposal.get("future_matrix_path") != matrix_requirements["future_matrix_path"]:
            add_error(
                "FUTURE_MATRIX_PATH_INVALID",
                f"future_matrix_path must be {matrix_requirements['future_matrix_path']}",
            )
    if proposal.get("matrix_created") is not False:
        add_error("MATRIX_CREATED", "matrix_created must be false")
    if proposal.get("usage_tables_entries_created") is not False:
        add_error("USAGE_TABLES_ENTRIES_CREATED", "usage_tables_entries_created must be false")
    if proposal.get("verified_uplift") is not False:
        add_error("VERIFIED_UPLIFT", "verified_uplift must be false")
    if proposal.get("proposed_initial_status") != "scaffold":
        add_error("INITIAL_STATUS_INVALID", "proposed_initial_status must be scaffold")

    schema_fields = (
        set(proposal.get("proposed_schema_fields", []))
        if isinstance(proposal.get("proposed_schema_fields"), list)
        else set()
    )
    required_fields = set(
        matrix_requirements["required_schema_fields"] if matrix_requirements is not None else set()
    )
    missing_fields = sorted(required_fields - schema_fields)
    if missing_fields:
        add_error("SCHEMA_FIELDS_INCOMPLETE", f"missing schema field(s): {', '.join(missing_fields)}")

    non_claims = set(proposal.get("non_claims", [])) if isinstance(proposal.get("non_claims"), list) else set()
    missing_non_claims = sorted(REQUIRED_NON_CLAIMS - non_claims)
    if missing_non_claims:
        add_error("NON_CLAIMS_INCOMPLETE", f"missing non-claim(s): {', '.join(missing_non_claims)}")

    source_status = _usage_tables_status(source_authority_path)
    if source_status != "not_imported":
        add_error("SOURCE_AUTHORITY_IMPORTED", f"hid_usage_tables status must remain not_imported, got {source_status!r}")

    future_matrix = ROOT / str(proposal.get("future_matrix_path", ""))
    future_matrix_exists = future_matrix.exists()
    if future_matrix_exists:
        add_error("FUTURE_MATRIX_EXISTS", f"production matrix must not exist yet: {_display_path(future_matrix)}")

    receipt = {
        "validator": "validate_usage_tables_matrix_proposals.py",
        "authority_ceiling": "usage_tables_matrix_schema_proposal_validation_only",
        "result": "PASS" if not errors else "FAIL",
        "checked_proposal": _display_path(proposal_path),
        "checked_markdown": _display_path(markdown_path),
        "source_authority_status": source_status,
        "future_matrix_exists": future_matrix_exists,
        "error_count": len(errors),
        "errors": errors,
        "findings": findings,
    }
    return errors, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--proposal")
    parser.add_argument("--markdown")
    parser.add_argument("--source-authority")
    parser.add_argument("--receipt-out")
    args = parser.parse_args()

    try:
        proposal = _resolve_under_root(args.proposal, DEFAULT_PROPOSAL)
        markdown = _resolve_under_root(args.markdown, DEFAULT_MARKDOWN)
        source_authority = _resolve_under_root(args.source_authority, DEFAULT_SOURCE_AUTHORITY)
        receipt_out = _resolve_under_root(args.receipt_out, DEFAULT_RECEIPT)
    except ValueError as exc:
        print(f"FAIL validate_usage_tables_matrix_proposals: {exc}")
        return 1

    errors, receipt = validate(proposal, markdown_path=markdown, source_authority_path=source_authority)
    if args.receipt_out:
        _write_receipt(receipt_out, receipt)

    if errors:
        print("FAIL validate_usage_tables_matrix_proposals")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS validate_usage_tables_matrix_proposals")
    print(f"- checked proposal: {receipt['checked_proposal']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
