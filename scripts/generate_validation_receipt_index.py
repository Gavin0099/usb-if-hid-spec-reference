#!/usr/bin/env python3
"""Generate durable validation receipts for the HID governed surface.

Authority ceiling: validation_receipt_index_only.
This tool records command results. It does not promote entries, import new
authority, or change matrix semantics.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RECEIPT_DIR = ROOT / "evidence" / "validation_receipts" / "hid_current_gate"
DEFAULT_JSON_OUT = ROOT / "evidence" / "validation_receipt_index.json"
DEFAULT_MD_OUT = ROOT / "docs" / "evidence" / "validation_receipt_index.md"


@dataclass(frozen=True)
class GateCommand:
    receipt_id: str
    command: list[str]
    claim_ceiling: str


GATE_COMMANDS = [
    GateCommand(
        "source_authority",
        ["python", "-X", "utf8", "scripts/validate_source_authority.py"],
        "source_authority_structural_validation_only",
    ),
    GateCommand(
        "source_registry",
        [
            "python",
            "-X",
            "utf8",
            "scripts/validate_source_registry.py",
            "--receipt-out",
            "evidence/validation_receipt_source_registry.json",
        ],
        "structural_registry_validation_only",
    ),
    GateCommand(
        "source_authority_import_proposals",
        [
            "python",
            "-X",
            "utf8",
            "scripts/validate_source_authority_import_proposals.py",
            "--receipt-out",
            "evidence/validation_receipt_source_authority_import_proposals.json",
        ],
        "source_authority_import_proposal_validation_only",
    ),
    GateCommand(
        "source_authority_import_proposal_summary",
        [
            "python",
            "-X",
            "utf8",
            "scripts/generate_source_authority_import_proposal_summary.py",
            "--assert-match",
            "evidence/source_authority_proposals/summary.json",
            "--check-only",
            "--receipt-out",
            "evidence/validation_receipt_source_authority_import_proposal_summary.json",
        ],
        "source_authority_import_proposal_summary_only",
    ),
    GateCommand(
        "contract_files",
        [
            "python",
            "-X",
            "utf8",
            "scripts/validate_contract_files.py",
            "--receipt-out",
            "evidence/validation_receipt_contract_files.json",
        ],
        "contract_structural_consistency_only",
    ),
    GateCommand(
        "hid_class_request_matrix",
        ["python", "-X", "utf8", "scripts/validate_hid_class_request_matrix.py"],
        "matrix_identity_validation_only",
    ),
    GateCommand(
        "hid_descriptor_fields_matrix",
        ["python", "-X", "utf8", "scripts/validate_hid_descriptor_fields_matrix.py"],
        "matrix_identity_validation_only",
    ),
    GateCommand(
        "hid_report_descriptor_items_matrix",
        ["python", "-X", "utf8", "scripts/validate_hid_report_descriptor_items_matrix.py"],
        "matrix_identity_validation_only",
    ),
    GateCommand(
        "verification_status",
        ["python", "-X", "utf8", "scripts/validate_verification_status.py"],
        "verification_status_count_consistency_only",
    ),
    GateCommand(
        "evidence_packet_schema",
        [
            "python",
            "-X",
            "utf8",
            "scripts/validate_evidence_packet_schema.py",
            "--receipt-out",
            "evidence/validation_receipt_hid_all_accepted.json",
        ],
        "verified_preflight_contract_only",
    ),
    GateCommand(
        "accepted_packet_proposals",
        [
            "python",
            "-X",
            "utf8",
            "scripts/validate_accepted_packet_proposals.py",
            "--receipt-out",
            "evidence/validation_receipt_accepted_packet_proposals.json",
        ],
        "accepted_packet_proposal_validation_only",
    ),
    GateCommand(
        "accepted_packet_proposal_summary",
        [
            "python",
            "-X",
            "utf8",
            "scripts/generate_accepted_packet_proposal_summary.py",
            "--assert-match",
            "evidence/accepted_proposal_summary.json",
            "--check-only",
            "--receipt-out",
            "evidence/validation_receipt_accepted_packet_proposal_summary.json",
        ],
        "accepted_packet_proposal_summary_only",
    ),
    GateCommand(
        "preapproval_readiness_summary",
        [
            "python",
            "-X",
            "utf8",
            "scripts/generate_preapproval_readiness_summary.py",
            "--receipt-out",
            "evidence/validation_receipt_preapproval_readiness_summary.json",
        ],
        "preapproval_readiness_summary_only",
    ),
    GateCommand(
        "hid_governed_surface_manifest",
        ["python", "-X", "utf8", "scripts/validate_hid_governed_surface_manifest.py"],
        "manifest_structural_integrity_only",
    ),
    GateCommand(
        "table_fingerprint",
        [
            "python",
            "-X",
            "utf8",
            "scripts/probe_table_fingerprint.py",
            "--mode",
            "check",
            "--manifest",
            "exports/hid_governed_surface_manifest.yaml",
            "--baseline-in",
            "evidence/table_fingerprint_baseline.jsonl",
            "--receipt-out",
            "evidence/validation_receipt_table_fingerprint.json",
        ],
        "table_content_fingerprint_drift_only",
    ),
    GateCommand(
        "memory_records",
        [
            "python",
            "-X",
            "utf8",
            "scripts/validate_memory_records.py",
            "--receipt-out",
            "evidence/validation_receipt_memory_records.json",
        ],
        "memory_record_structural_visibility_only",
    ),
    GateCommand(
        "unit_tests",
        ["python", "-B", "-m", "unittest", "discover", "-s", "tests"],
        "regression_test_result_only",
    ),
]


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
        raise ValueError(f"output path must stay under repository root: {path_arg}") from exc
    return resolved


def run_gate(command: GateCommand, *, receipt_dir: Path) -> dict[str, Any]:
    completed = subprocess.run(
        command.command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    receipt = {
        "receipt_id": command.receipt_id,
        "command": command.command,
        "claim_ceiling": command.claim_ceiling,
        "result": "PASS" if completed.returncode == 0 else "FAIL",
        "returncode": completed.returncode,
        "stdout": completed.stdout.splitlines(),
        "stderr": completed.stderr.splitlines(),
    }
    receipt_path = receipt_dir / f"{command.receipt_id}.json"
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    receipt["receipt_path"] = _display_path(receipt_path)
    return receipt


def build_index(receipts: list[dict[str, Any]], *, receipt_dir: Path) -> dict[str, Any]:
    return {
        "validator": "generate_validation_receipt_index.py",
        "authority_ceiling": "validation_receipt_index_only",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "result": "PASS" if all(receipt["result"] == "PASS" for receipt in receipts) else "FAIL",
        "receipt_dir": _display_path(receipt_dir),
        "checked_commands": len(receipts),
        "pass_count": sum(1 for receipt in receipts if receipt["result"] == "PASS"),
        "fail_count": sum(1 for receipt in receipts if receipt["result"] != "PASS"),
        "receipts": [
            {
                "receipt_id": receipt["receipt_id"],
                "result": receipt["result"],
                "returncode": receipt["returncode"],
                "claim_ceiling": receipt["claim_ceiling"],
                "receipt_path": receipt["receipt_path"],
                "command": receipt["command"],
            }
            for receipt in receipts
        ],
        "claim_ceiling": [
            "validation_receipt_index_only",
            "no_new_source_authority_import",
            "no_matrix_semantic_change",
            "no_verified_uplift_by_receipt_index",
            "no_firmware_behavior_claim",
        ],
        "not_claimed": [
            "full HID spec coverage",
            "HID Usage Tables coverage",
            "report descriptor semantic completeness",
            "report payload semantics",
            "firmware behavior correctness",
            "OS input stack behavior",
            "parser/runtime behavior",
            "product-specific HID behavior",
        ],
    }


def render_markdown(index: dict[str, Any]) -> str:
    lines = [
        "# HID Validation Receipt Index",
        "",
        "> Status: validation receipt index only",
        "> Authority ceiling: validation_receipt_index_only",
        "",
        "## Summary",
        "",
        f"- result: {index['result']}",
        f"- checked commands: {index['checked_commands']}",
        f"- pass count: {index['pass_count']}",
        f"- fail count: {index['fail_count']}",
        f"- receipt directory: `{index['receipt_dir']}`",
        "",
        "## Receipts",
        "",
        "| Receipt | Result | Claim ceiling | Path |",
        "|---|---|---|---|",
    ]
    for receipt in index["receipts"]:
        lines.append(
            f"| `{receipt['receipt_id']}` | {receipt['result']} | "
            f"`{receipt['claim_ceiling']}` | `{receipt['receipt_path']}` |"
        )
    lines.extend(
        [
            "",
            "## Claim Ceiling",
            "",
            "- validation receipt index only",
            "- no new source authority import",
            "- no matrix semantic change",
            "- no verified uplift by receipt index",
            "- no firmware behavior claim",
            "",
            "## Not Claimed",
            "",
        ]
    )
    lines.extend(f"- {claim}" for claim in index["not_claimed"])
    return "\n".join(lines) + "\n"


def write_index(index: dict[str, Any], *, json_out: Path, md_out: Path) -> None:
    json_out.parent.mkdir(parents=True, exist_ok=True)
    md_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(index, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    md_out.write_text(render_markdown(index), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt-dir")
    parser.add_argument("--json-out")
    parser.add_argument("--md-out")
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--assert-match")
    args = parser.parse_args()

    try:
        receipt_dir = _resolve_under_root(args.receipt_dir, DEFAULT_RECEIPT_DIR)
        json_out = _resolve_under_root(args.json_out, DEFAULT_JSON_OUT)
        md_out = _resolve_under_root(args.md_out, DEFAULT_MD_OUT)
        assert_match = _resolve_under_root(args.assert_match, json_out) if args.assert_match else None
    except ValueError as exc:
        print(f"FAIL generate_validation_receipt_index: {exc}")
        return 1

    receipts = [run_gate(command, receipt_dir=receipt_dir) for command in GATE_COMMANDS]
    index = build_index(receipts, receipt_dir=receipt_dir)

    if args.check_only:
        if assert_match:
            expected = json.loads(assert_match.read_text(encoding="utf-8"))
            expected_without_time = dict(expected)
            actual_without_time = dict(index)
            expected_without_time.pop("generated_at", None)
            actual_without_time.pop("generated_at", None)
            if expected_without_time != actual_without_time:
                print("FAIL generate_validation_receipt_index: index does not match asserted file")
                return 1
        print(f"{index['result']} generate_validation_receipt_index")
        print(f"- checked commands: {index['checked_commands']}")
        print(f"- pass count: {index['pass_count']}")
        print(f"- fail count: {index['fail_count']}")
        return 0 if index["result"] == "PASS" else 1

    write_index(index, json_out=json_out, md_out=md_out)
    print(f"{index['result']} generate_validation_receipt_index")
    print(f"- wrote: {_display_path(json_out)}")
    print(f"- wrote: {_display_path(md_out)}")
    print(f"- receipt dir: {_display_path(receipt_dir)}")
    return 0 if index["result"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
