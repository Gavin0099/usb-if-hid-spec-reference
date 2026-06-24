#!/usr/bin/env python3
"""Generate a summary for source-authority import proposal artifacts.

Authority ceiling: source_authority_import_proposal_summary_only.
This tool summarizes proposal/readiness state only. It does not import source
authority, populate source registry sections, or create Usage Tables entries.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.validate_source_authority_import_proposals import (
    DEFAULT_CHECKLIST,
    DEFAULT_EXECUTION_PLAN,
    DEFAULT_EXECUTION_PLAN_MARKDOWN,
    DEFAULT_MARKDOWN,
    DEFAULT_SOURCE_IDENTITY_MARKDOWN,
    DEFAULT_SOURCE_IDENTITY_PACKET,
    DEFAULT_PROPOSAL,
    DEFAULT_SOURCE_AUTHORITY,
    DEFAULT_SOURCE_REGISTRY,
    _display_path,
    _load_json,
    _resolve_under_root,
    _usage_tables_registry_sections,
    _usage_tables_source_authority_status,
    validate,
)


SUMMARY_MD = ROOT / "docs" / "evidence" / "source_authority_proposals" / "summary.md"
SUMMARY_JSON = ROOT / "evidence" / "source_authority_proposals" / "summary.json"
DEFAULT_RECEIPT = ROOT / "evidence" / "validation_receipt_source_authority_import_proposal_summary.json"


def _compare_summary(expected: dict[str, Any], actual: dict[str, Any]) -> list[str]:
    mismatches: list[str] = []
    fields = [
        "authority_ceiling",
        "proposal_count",
        "checklist_count",
        "execution_plan_count",
        "source_identity_packet_count",
        "source_authority_status",
        "source_registry_section_count",
        "production_source_authority_change_count",
        "usage_tables_governed_entry_count",
        "verified_uplift_count",
        "ready_for_level3_import",
        "remaining_gap_count",
    ]
    for field in fields:
        if expected.get(field) != actual.get(field):
            mismatches.append(
                f"summary field mismatch {field}: expected {expected.get(field)!r}, got {actual.get(field)!r}"
            )

    for field in ("claim_ceiling", "not_claimed"):
        expected_values = sorted(expected.get(field, [])) if isinstance(expected.get(field), list) else []
        actual_values = sorted(actual.get(field, [])) if isinstance(actual.get(field), list) else []
        if expected_values != actual_values:
            mismatches.append(f"summary field mismatch {field}: {expected_values!r} != {actual_values!r}")

    expected_proposals = expected.get("proposals", [])
    actual_proposals = actual.get("proposals", [])
    if expected_proposals != actual_proposals:
        mismatches.append("summary proposals mismatch")
    return mismatches


def _build_receipt(assert_match: str | None, summary: dict[str, Any], mismatches: list[str]) -> dict[str, Any]:
    return {
        "validator": "generate_source_authority_import_proposal_summary.py",
        "authority_ceiling": "source_authority_import_proposal_summary_only",
        "result": "PASS" if not mismatches else "FAIL",
        "assert_match": assert_match,
        "proposal_count": summary["proposal_count"],
        "source_authority_status": summary["source_authority_status"],
        "source_registry_section_count": summary["source_registry_section_count"],
        "ready_for_level3_import": summary["ready_for_level3_import"],
        "error_count": len(mismatches),
        "errors": mismatches,
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def build_summary() -> dict[str, Any]:
    errors, _receipt = validate()
    if errors:
        raise ValueError("source authority import proposal validation must pass before summary generation")

    proposal = _load_json(DEFAULT_PROPOSAL)
    gate = proposal["required_level3_gate"]
    gaps = proposal["remaining_gaps"] if isinstance(proposal.get("remaining_gaps"), list) else []
    registry_sections = _usage_tables_registry_sections(DEFAULT_SOURCE_REGISTRY)
    source_status = _usage_tables_source_authority_status(DEFAULT_SOURCE_AUTHORITY)
    ready_for_level3_import = (
        source_status == "not_imported"
        and len(registry_sections) == 0
        and gate.get("approval_record") == "TBD_LEVEL3_APPROVAL"
        and gate.get("direct_import") is False
        and proposal.get("production_source_authority_change_created") is False
        and proposal.get("usage_tables_governed_entries_created") is False
        and proposal.get("verified_uplift") is False
    )
    return {
        "authority_ceiling": "source_authority_import_proposal_summary_only",
        "proposal_count": 1,
        "checklist_count": 1 if DEFAULT_CHECKLIST.exists() else 0,
        "execution_plan_count": 1 if DEFAULT_EXECUTION_PLAN.exists() and DEFAULT_EXECUTION_PLAN_MARKDOWN.exists() else 0,
        "source_identity_packet_count": 1
        if DEFAULT_SOURCE_IDENTITY_PACKET.exists() and DEFAULT_SOURCE_IDENTITY_MARKDOWN.exists()
        else 0,
        "source_authority_status": source_status,
        "source_registry_section_count": len(registry_sections),
        "production_source_authority_change_count": 1
        if proposal.get("production_source_authority_change_created") is True
        else 0,
        "usage_tables_governed_entry_count": 1 if proposal.get("usage_tables_governed_entries_created") is True else 0,
        "verified_uplift_count": 1 if proposal.get("verified_uplift") is True else 0,
        "ready_for_level3_import": ready_for_level3_import,
        "remaining_gap_count": len(gaps),
        "proposals": [
            {
                "source_id": proposal["source_candidate"]["source_id"],
                "current_status": proposal["source_candidate"]["current_status"],
                "proposed_next_status": proposal["source_candidate"]["proposed_next_status"],
                "proposal_json": _display_path(DEFAULT_PROPOSAL),
                "proposal_markdown": _display_path(DEFAULT_MARKDOWN),
                "preapproval_checklist": _display_path(DEFAULT_CHECKLIST),
                "execution_plan_json": _display_path(DEFAULT_EXECUTION_PLAN),
                "execution_plan_markdown": _display_path(DEFAULT_EXECUTION_PLAN_MARKDOWN),
                "source_identity_json": _display_path(DEFAULT_SOURCE_IDENTITY_PACKET),
                "source_identity_markdown": _display_path(DEFAULT_SOURCE_IDENTITY_MARKDOWN),
                "approval_record": gate["approval_record"],
                "approver": gate["approver"],
                "direct_import": gate["direct_import"],
                "remaining_gap_count": len(gaps),
            }
        ],
        "claim_ceiling": [
            "source_authority_import_proposal_summary_only",
            "no_source_authority_import",
            "no_usage_tables_coverage",
            "no_verified_uplift",
        ],
        "not_claimed": [
            "HID Usage Tables are not imported",
            "Usage Tables entries are not tracked, reviewed, or verified",
            "Usage Tables source version is not selected",
            "Report payload semantics are not covered",
            "Firmware behavior correctness is not claimed",
            "OS input stack behavior is not claimed",
            "Parser/runtime behavior is not claimed",
            "Product-specific HID behavior is not claimed",
        ],
    }


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# HID Source Authority Import Proposal Summary",
        "",
        "> Status: proposal summary only",
        "> Authority ceiling: source_authority_import_proposal_summary_only",
        "",
        "## Totals",
        "",
        f"- proposal artifacts: {summary['proposal_count']}",
        f"- preapproval checklists: {summary['checklist_count']}",
        f"- execution plans: {summary['execution_plan_count']}",
        f"- source identity packets: {summary['source_identity_packet_count']}",
        f"- source authority status: `{summary['source_authority_status']}`",
        f"- source registry Usage Tables sections: {summary['source_registry_section_count']}",
        f"- production source authority changes: {summary['production_source_authority_change_count']}",
        f"- Usage Tables governed entries: {summary['usage_tables_governed_entry_count']}",
        f"- verified uplift count: {summary['verified_uplift_count']}",
        f"- ready for Level 3 import approval: {str(summary['ready_for_level3_import']).lower()}",
        f"- remaining gaps: {summary['remaining_gap_count']}",
        "",
        "## Proposals",
        "",
        "| Source | Current status | Proposed next status | Approval | Direct import | Gaps |",
        "|---|---|---|---|---|---:|",
    ]
    for proposal in summary["proposals"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{proposal['source_id']}`",
                    f"`{proposal['current_status']}`",
                    f"`{proposal['proposed_next_status']}`",
                    f"`{proposal['approval_record']}`",
                    f"`{proposal['direct_import']}`",
                    str(proposal["remaining_gap_count"]),
                ]
            )
            + " |"
        )

    lines.extend(["", "## Claim Ceiling", ""])
    lines.extend(f"- {item}" for item in summary["claim_ceiling"])
    lines.extend(["", "## Not Claimed", ""])
    lines.extend(f"- {item}" for item in summary["not_claimed"])
    lines.append("")
    return "\n".join(lines)


def write_summary(summary: dict[str, Any], *, markdown_out: Path, json_out: Path) -> None:
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.write_text(render_markdown(summary), encoding="utf-8")
    _write_json(json_out, summary)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--markdown-out", default="docs/evidence/source_authority_proposals/summary.md")
    parser.add_argument("--json-out", default="evidence/source_authority_proposals/summary.json")
    parser.add_argument("--assert-match")
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--receipt-out")
    args = parser.parse_args()
    if args.check_only and not args.assert_match:
        parser.error("--check-only requires --assert-match")

    try:
        markdown_out = _resolve_under_root(args.markdown_out, SUMMARY_MD)
        json_out = _resolve_under_root(args.json_out, SUMMARY_JSON)
        summary = build_summary()
        mismatches: list[str] = []
        if args.assert_match:
            expected_path = _resolve_under_root(args.assert_match, SUMMARY_JSON)
            expected = _load_json(expected_path)
            mismatches = _compare_summary(expected, summary)
        if args.receipt_out:
            receipt_out = _resolve_under_root(args.receipt_out, DEFAULT_RECEIPT)
            _write_json(receipt_out, _build_receipt(args.assert_match, summary, mismatches))
        if mismatches:
            print("FAIL source authority import proposal summary")
            for mismatch in mismatches:
                print(f"- {mismatch}")
            return 1
        if not args.check_only:
            write_summary(summary, markdown_out=markdown_out, json_out=json_out)
            print(f"Wrote {_display_path(markdown_out)}")
            print(f"Wrote {_display_path(json_out)}")
        elif args.assert_match:
            print(f"PASS source authority import proposal summary matches {args.assert_match}")
        return 0
    except Exception as exc:
        print(f"FAIL generate_source_authority_import_proposal_summary: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
