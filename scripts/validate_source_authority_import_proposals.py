#!/usr/bin/env python3
"""Validate source-authority import proposal artifacts.

Authority ceiling: source_authority_import_proposal_validation_only.
This validator checks proposal structure and non-import boundaries only. It
does not import sources or promote governed entries.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROPOSAL = ROOT / "evidence" / "source_authority_proposals" / "hid_usage_tables_import_proposal.json"
DEFAULT_MARKDOWN = ROOT / "docs" / "evidence" / "source_authority_proposals" / "hid_usage_tables_import_proposal.md"
DEFAULT_CHECKLIST = ROOT / "docs" / "evidence" / "source_authority_proposals" / "hid_usage_tables_import_preapproval_checklist.md"
DEFAULT_EXECUTION_PLAN = ROOT / "evidence" / "source_authority_proposals" / "hid_usage_tables_import_execution_plan.json"
DEFAULT_EXECUTION_PLAN_MARKDOWN = ROOT / "docs" / "evidence" / "source_authority_proposals" / "hid_usage_tables_import_execution_plan.md"
DEFAULT_SOURCE_IDENTITY_PACKET = ROOT / "evidence" / "source_authority_proposals" / "hid_usage_tables_source_identity_selection.json"
DEFAULT_SOURCE_IDENTITY_MARKDOWN = ROOT / "docs" / "evidence" / "source_authority_proposals" / "hid_usage_tables_source_identity_selection.md"
DEFAULT_SOURCE_AUTHORITY = ROOT / "data" / "source_authority.yaml"
DEFAULT_SOURCE_REGISTRY = ROOT / "evidence" / "source_registry.yaml"
DEFAULT_RECEIPT = ROOT / "evidence" / "validation_receipt_source_authority_import_proposals.json"

REQUIRED_CLAIM_CEILING = {
    "source_authority_import_proposal_only",
    "no_source_authority_import",
    "no_usage_tables_coverage",
    "no_verified_uplift",
}
REQUIRED_NOT_CLAIMED = {
    "HID Usage Tables are not imported",
    "Usage Tables entries are not tracked, reviewed, or verified",
    "Report payload semantics are not covered",
    "Firmware behavior correctness is not claimed",
    "OS input stack behavior is not claimed",
    "Parser/runtime behavior is not claimed",
    "Product-specific HID behavior is not claimed",
}
REQUIRED_EXECUTION_NON_CLAIMS = {
    "no direct source authority import in this plan",
    "no Usage Tables governed entries in this plan",
    "no Usage Tables coverage claim in this plan",
    "no verified uplift in this plan",
}
REQUIRED_SOURCE_IDENTITY_FIELDS = {
    "publisher",
    "document_title",
    "publication_version_or_revision",
    "publication_date",
    "canonical_url",
    "imported_scope",
    "excluded_scope",
}
REQUIRED_SOURCE_IDENTITY_NON_CLAIMS = {
    "no selected publication identity in this packet",
    "no source authority import in this packet",
    "no Usage Tables citation authority in this packet",
    "no Usage Tables governed entries in this packet",
}
ALLOWED_FIRST_SLICE_FILES = {
    "data/source_authority.yaml",
    "evidence/source_registry.yaml",
    "docs/source_authority.md",
    "docs/claim_boundary.md",
    "governance/hid_work_queue.yaml",
    "docs/hid_long_running_roadmap.md",
    "docs/hid_long_running_checkpoint_rollup.md",
    "memory/2026-06-23.md",
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


def _write_receipt(path: Path, receipt: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def _usage_tables_source_authority_status(path: Path) -> str | None:
    data = _load_yaml(path)
    for source in data.get("secondary_sources", []):
        if isinstance(source, dict) and source.get("id") == "hid_usage_tables":
            return source.get("status")
    return None


def _usage_tables_registry_sections(path: Path) -> list[Any]:
    data = _load_yaml(path)
    for source in data.get("sources", []):
        if isinstance(source, dict) and source.get("source_id") == "hid_usage_tables":
            sections = source.get("sections", [])
            return sections if isinstance(sections, list) else ["<sections-not-list>"]
    return ["<missing>"]


def validate(
    proposal_path: Path = DEFAULT_PROPOSAL,
    *,
    markdown_path: Path = DEFAULT_MARKDOWN,
    checklist_path: Path = DEFAULT_CHECKLIST,
    execution_plan_path: Path = DEFAULT_EXECUTION_PLAN,
    execution_plan_markdown_path: Path = DEFAULT_EXECUTION_PLAN_MARKDOWN,
    source_identity_path: Path = DEFAULT_SOURCE_IDENTITY_PACKET,
    source_identity_markdown_path: Path = DEFAULT_SOURCE_IDENTITY_MARKDOWN,
    source_authority_path: Path = DEFAULT_SOURCE_AUTHORITY,
    source_registry_path: Path = DEFAULT_SOURCE_REGISTRY,
) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    findings: list[dict[str, str]] = []

    def add_error(code: str, message: str) -> None:
        errors.append(message)
        findings.append({"code": code, "message": message})

    for required_path, code in (
        (proposal_path, "PROPOSAL_JSON_MISSING"),
        (markdown_path, "PROPOSAL_MARKDOWN_MISSING"),
        (checklist_path, "PREAPPROVAL_CHECKLIST_MISSING"),
        (execution_plan_path, "EXECUTION_PLAN_JSON_MISSING"),
        (execution_plan_markdown_path, "EXECUTION_PLAN_MARKDOWN_MISSING"),
        (source_identity_path, "SOURCE_IDENTITY_JSON_MISSING"),
        (source_identity_markdown_path, "SOURCE_IDENTITY_MARKDOWN_MISSING"),
    ):
        if not required_path.exists():
            add_error(code, f"missing required artifact: {_display_path(required_path)}")

    proposal: dict[str, Any]
    try:
        proposal = _load_json(proposal_path)
    except Exception as exc:
        add_error("PROPOSAL_JSON_LOAD_FAILED", str(exc))
        proposal = {}

    source_candidate = proposal.get("source_candidate", {})
    if not isinstance(source_candidate, dict):
        add_error("SOURCE_CANDIDATE_INVALID", "source_candidate must be a mapping")
        source_candidate = {}

    if proposal.get("authority_ceiling") != "source_authority_import_proposal_only":
        add_error("AUTHORITY_CEILING_INVALID", "proposal authority_ceiling must be source_authority_import_proposal_only")
    if proposal.get("proposal_status") != "proposal_only":
        add_error("PROPOSAL_STATUS_INVALID", "proposal_status must be proposal_only")
    if source_candidate.get("source_id") != "hid_usage_tables":
        add_error("SOURCE_ID_INVALID", "source_candidate.source_id must be hid_usage_tables")
    if source_candidate.get("current_status") != "not_imported":
        add_error("CURRENT_STATUS_INVALID", "source_candidate.current_status must be not_imported")
    if proposal.get("production_source_authority_change_created") is not False:
        add_error("PRODUCTION_CHANGE_CREATED", "production_source_authority_change_created must be false")
    if proposal.get("usage_tables_governed_entries_created") is not False:
        add_error("USAGE_TABLE_ENTRIES_CREATED", "usage_tables_governed_entries_created must be false")
    if proposal.get("verified_uplift") is not False:
        add_error("VERIFIED_UPLIFT_CREATED", "verified_uplift must be false")

    gate = proposal.get("required_level3_gate", {})
    if not isinstance(gate, dict):
        add_error("LEVEL3_GATE_INVALID", "required_level3_gate must be a mapping")
        gate = {}
    if gate.get("approval_record") != "TBD_LEVEL3_APPROVAL":
        add_error("APPROVAL_NOT_TBD", "approval_record must remain TBD_LEVEL3_APPROVAL")
    if gate.get("approver") != "TBD_HUMAN_APPROVER":
        add_error("APPROVER_NOT_TBD", "approver must remain TBD_HUMAN_APPROVER")
    if gate.get("direct_import") is not False:
        add_error("DIRECT_IMPORT_NOT_FALSE", "direct_import must be false")
    for key in ("checkpoint_commit", "validation_receipt"):
        value = gate.get(key)
        if not isinstance(value, str) or "TBD" not in value:
            add_error("LEVEL3_GATE_PLACEHOLDER_INVALID", f"{key} must remain a TBD placeholder")

    claim_ceiling = set(proposal.get("claim_ceiling", [])) if isinstance(proposal.get("claim_ceiling"), list) else set()
    missing_claims = sorted(REQUIRED_CLAIM_CEILING - claim_ceiling)
    if missing_claims:
        add_error("CLAIM_CEILING_INCOMPLETE", f"missing claim ceiling(s): {', '.join(missing_claims)}")

    not_claimed = set(proposal.get("not_claimed", [])) if isinstance(proposal.get("not_claimed"), list) else set()
    missing_non_claims = sorted(REQUIRED_NOT_CLAIMED - not_claimed)
    if missing_non_claims:
        add_error("NON_CLAIMS_INCOMPLETE", f"missing non-claim(s): {', '.join(missing_non_claims)}")

    execution_plan: dict[str, Any]
    try:
        execution_plan = _load_json(execution_plan_path)
    except Exception as exc:
        add_error("EXECUTION_PLAN_JSON_LOAD_FAILED", str(exc))
        execution_plan = {}

    if execution_plan.get("authority_ceiling") != "source_authority_import_execution_plan_only":
        add_error(
            "EXECUTION_PLAN_AUTHORITY_CEILING_INVALID",
            "execution plan authority_ceiling must be source_authority_import_execution_plan_only",
        )
    if execution_plan.get("plan_status") != "proposal_only":
        add_error("EXECUTION_PLAN_STATUS_INVALID", "execution plan plan_status must be proposal_only")
    if execution_plan.get("source_id") != "hid_usage_tables":
        add_error("EXECUTION_PLAN_SOURCE_ID_INVALID", "execution plan source_id must be hid_usage_tables")
    if execution_plan.get("production_change_created") is not False:
        add_error("EXECUTION_PLAN_PRODUCTION_CHANGE_CREATED", "execution plan production_change_created must be false")
    if execution_plan.get("direct_import") is not False:
        add_error("EXECUTION_PLAN_DIRECT_IMPORT", "execution plan direct_import must be false")
    if execution_plan.get("usage_tables_governed_entries_created") is not False:
        add_error(
            "EXECUTION_PLAN_USAGE_TABLE_ENTRIES_CREATED",
            "execution plan usage_tables_governed_entries_created must be false",
        )
    if execution_plan.get("verified_uplift") is not False:
        add_error("EXECUTION_PLAN_VERIFIED_UPLIFT", "execution plan verified_uplift must be false")

    proposed_first_slice_files = execution_plan.get("proposed_first_slice_files", [])
    if not isinstance(proposed_first_slice_files, list):
        add_error("EXECUTION_PLAN_FILES_INVALID", "execution plan proposed_first_slice_files must be a list")
        proposed_first_slice_files = []
    unknown_files = sorted(set(proposed_first_slice_files) - ALLOWED_FIRST_SLICE_FILES)
    if unknown_files:
        add_error("EXECUTION_PLAN_FILES_OUT_OF_SCOPE", f"execution plan contains out-of-scope files: {', '.join(unknown_files)}")

    forbidden_first_slice_files = execution_plan.get("forbidden_first_slice_files", [])
    if not isinstance(forbidden_first_slice_files, list):
        add_error("EXECUTION_PLAN_FORBIDDEN_FILES_INVALID", "execution plan forbidden_first_slice_files must be a list")
        forbidden_first_slice_files = []
    if not any("data/hid_" in str(path) and "matrix" in str(path) for path in forbidden_first_slice_files):
        add_error("EXECUTION_PLAN_FORBIDDEN_MATRICES_MISSING", "execution plan must forbid Usage Tables matrix creation in first slice")

    execution_non_claims = (
        set(execution_plan.get("non_claims", [])) if isinstance(execution_plan.get("non_claims"), list) else set()
    )
    missing_execution_non_claims = sorted(REQUIRED_EXECUTION_NON_CLAIMS - execution_non_claims)
    if missing_execution_non_claims:
        add_error(
            "EXECUTION_PLAN_NON_CLAIMS_INCOMPLETE",
            f"execution plan missing non-claim(s): {', '.join(missing_execution_non_claims)}",
        )

    source_identity: dict[str, Any]
    try:
        source_identity = _load_json(source_identity_path)
    except Exception as exc:
        add_error("SOURCE_IDENTITY_JSON_LOAD_FAILED", str(exc))
        source_identity = {}

    if source_identity.get("authority_ceiling") != "source_identity_selection_checklist_only":
        add_error(
            "SOURCE_IDENTITY_AUTHORITY_CEILING_INVALID",
            "source identity authority_ceiling must be source_identity_selection_checklist_only",
        )
    if source_identity.get("packet_status") != "checklist_only":
        add_error("SOURCE_IDENTITY_STATUS_INVALID", "source identity packet_status must be checklist_only")
    if source_identity.get("source_id") != "hid_usage_tables":
        add_error("SOURCE_IDENTITY_SOURCE_ID_INVALID", "source identity source_id must be hid_usage_tables")
    if source_identity.get("selected_publication_identity") != "TBD_LEVEL3_APPROVAL":
        add_error(
            "SOURCE_IDENTITY_SELECTED_TOO_EARLY",
            "source identity selected_publication_identity must remain TBD_LEVEL3_APPROVAL",
        )
    if source_identity.get("source_authority_import_created") is not False:
        add_error("SOURCE_IDENTITY_IMPORT_CREATED", "source identity source_authority_import_created must be false")
    if source_identity.get("citation_authority_enabled") is not False:
        add_error("SOURCE_IDENTITY_CITATION_ENABLED", "source identity citation_authority_enabled must be false")

    required_fields = (
        set(source_identity.get("required_identity_fields", []))
        if isinstance(source_identity.get("required_identity_fields"), list)
        else set()
    )
    missing_identity_fields = sorted(REQUIRED_SOURCE_IDENTITY_FIELDS - required_fields)
    if missing_identity_fields:
        add_error(
            "SOURCE_IDENTITY_FIELDS_INCOMPLETE",
            f"source identity packet missing required field(s): {', '.join(missing_identity_fields)}",
        )

    identity_non_claims = (
        set(source_identity.get("non_claims", [])) if isinstance(source_identity.get("non_claims"), list) else set()
    )
    missing_identity_non_claims = sorted(REQUIRED_SOURCE_IDENTITY_NON_CLAIMS - identity_non_claims)
    if missing_identity_non_claims:
        add_error(
            "SOURCE_IDENTITY_NON_CLAIMS_INCOMPLETE",
            f"source identity packet missing non-claim(s): {', '.join(missing_identity_non_claims)}",
        )

    try:
        source_status = _usage_tables_source_authority_status(source_authority_path)
        if source_status != "not_imported":
            add_error("SOURCE_AUTHORITY_ALREADY_IMPORTED", f"hid_usage_tables status must remain not_imported, got {source_status!r}")
    except Exception as exc:
        add_error("SOURCE_AUTHORITY_LOAD_FAILED", str(exc))
        source_status = None

    try:
        registry_sections = _usage_tables_registry_sections(source_registry_path)
        if registry_sections:
            add_error("SOURCE_REGISTRY_USAGE_TABLES_SECTIONS_PRESENT", "hid_usage_tables registry sections must remain empty")
    except Exception as exc:
        add_error("SOURCE_REGISTRY_LOAD_FAILED", str(exc))
        registry_sections = []

    receipt = {
        "validator": "validate_source_authority_import_proposals.py",
        "authority_ceiling": "source_authority_import_proposal_validation_only",
        "result": "PASS" if not errors else "FAIL",
        "checked_proposal": _display_path(proposal_path),
        "checked_markdown": _display_path(markdown_path),
        "checked_checklist": _display_path(checklist_path),
        "checked_execution_plan": _display_path(execution_plan_path),
        "checked_execution_plan_markdown": _display_path(execution_plan_markdown_path),
        "checked_source_identity_packet": _display_path(source_identity_path),
        "checked_source_identity_markdown": _display_path(source_identity_markdown_path),
        "source_authority_status": source_status,
        "source_registry_sections": registry_sections,
        "error_count": len(errors),
        "errors": errors,
        "findings": findings,
    }
    return errors, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--proposal")
    parser.add_argument("--markdown")
    parser.add_argument("--checklist")
    parser.add_argument("--execution-plan")
    parser.add_argument("--execution-plan-markdown")
    parser.add_argument("--source-identity")
    parser.add_argument("--source-identity-markdown")
    parser.add_argument("--source-authority")
    parser.add_argument("--source-registry")
    parser.add_argument("--receipt-out")
    args = parser.parse_args()

    try:
        proposal = _resolve_under_root(args.proposal, DEFAULT_PROPOSAL)
        markdown = _resolve_under_root(args.markdown, DEFAULT_MARKDOWN)
        checklist = _resolve_under_root(args.checklist, DEFAULT_CHECKLIST)
        execution_plan = _resolve_under_root(args.execution_plan, DEFAULT_EXECUTION_PLAN)
        execution_plan_markdown = _resolve_under_root(args.execution_plan_markdown, DEFAULT_EXECUTION_PLAN_MARKDOWN)
        source_identity = _resolve_under_root(args.source_identity, DEFAULT_SOURCE_IDENTITY_PACKET)
        source_identity_markdown = _resolve_under_root(args.source_identity_markdown, DEFAULT_SOURCE_IDENTITY_MARKDOWN)
        source_authority = _resolve_under_root(args.source_authority, DEFAULT_SOURCE_AUTHORITY)
        source_registry = _resolve_under_root(args.source_registry, DEFAULT_SOURCE_REGISTRY)
        receipt_out = _resolve_under_root(args.receipt_out, DEFAULT_RECEIPT)
    except ValueError as exc:
        print(f"FAIL validate_source_authority_import_proposals: {exc}")
        return 1

    errors, receipt = validate(
        proposal,
        markdown_path=markdown,
        checklist_path=checklist,
        execution_plan_path=execution_plan,
        execution_plan_markdown_path=execution_plan_markdown,
        source_identity_path=source_identity,
        source_identity_markdown_path=source_identity_markdown,
        source_authority_path=source_authority,
        source_registry_path=source_registry,
    )
    if args.receipt_out:
        _write_receipt(receipt_out, receipt)

    if errors:
        print("FAIL validate_source_authority_import_proposals")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS validate_source_authority_import_proposals")
    print(f"- checked proposal: {receipt['checked_proposal']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
