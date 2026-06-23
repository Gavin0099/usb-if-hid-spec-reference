#!/usr/bin/env python3
"""Generate a pre-approval checklist for a future accepted evidence packet.

Authority ceiling: accepted_preapproval_gap_report_only.
This tool reads candidate packets and governance contracts only. It does not
create accepted packets, promote entries, or change verification status.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_DIR = ROOT / "docs" / "evidence" / "candidates"
ACCEPTED_DIR = ROOT / "docs" / "evidence" / "accepted"
SCHEMA = ROOT / "contract" / "evidence_packet_schema.yaml"

REQUIRED_ACCEPTANCE_GATE_FIELDS = (
    "previous_packet_status",
    "checkpoint_commit",
    "validation_receipt",
    "level3_checkpoint",
    "direct_promotion",
)
REQUIRED_VALIDATION_FIELDS = (
    "source_authority_validator",
    "matrix_validator",
    "verification_status_validator",
    "evidence_packet_validator",
    "unit_tests",
)
REQUIRED_NON_CLAIMS = (
    "firmware_implementation_correctness",
    "os_input_stack_behavior",
    "parser_runtime_behavior",
    "product_specific_hid_behavior",
)


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return data


def _display_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _candidate_path(candidate_id: str, candidate_dir: Path) -> Path:
    candidate = Path(candidate_id)
    if candidate.suffix:
        return candidate if candidate.is_absolute() else ROOT / candidate
    return candidate_dir / f"{candidate_id}_candidate.yaml"


def _accepted_path_for_candidate(candidate_path: Path, accepted_dir: Path) -> Path:
    name = candidate_path.name
    if not name.endswith("_candidate.yaml"):
        return accepted_dir / f"{candidate_path.stem}_accepted.yaml"
    return accepted_dir / f"{name[:-len('_candidate.yaml')]}_accepted.yaml"


def build_checklist(
    *,
    candidate_id: str,
    candidate_dir: Path = CANDIDATE_DIR,
    accepted_dir: Path = ACCEPTED_DIR,
    schema_path: Path = SCHEMA,
) -> dict[str, Any]:
    candidate_path = _candidate_path(candidate_id, candidate_dir)
    candidate = _load_yaml(candidate_path)
    schema = _load_yaml(schema_path)
    accepted_path = _accepted_path_for_candidate(candidate_path, accepted_dir)

    identity = candidate.get("packet_identity", {}) if isinstance(candidate.get("packet_identity"), dict) else {}
    approval = candidate.get("approval", {}) if isinstance(candidate.get("approval"), dict) else {}
    validation = candidate.get("validation", {}) if isinstance(candidate.get("validation"), dict) else {}
    non_claims = candidate.get("non_claims", {}) if isinstance(candidate.get("non_claims"), dict) else {}
    binding = candidate.get("governed_entry_binding", {}) if isinstance(candidate.get("governed_entry_binding"), dict) else {}
    source_trace = candidate.get("source_trace", {}) if isinstance(candidate.get("source_trace"), dict) else {}

    ready_checks: list[str] = []
    gaps: list[str] = []

    if identity.get("packet_status") == "candidate":
        ready_checks.append("candidate packet status is candidate")
    else:
        gaps.append("candidate packet must remain packet_status: candidate before acceptance")

    if identity.get("review_level") == 3:
        ready_checks.append("candidate packet is marked review_level 3")
    else:
        gaps.append("candidate packet must be marked review_level: 3")

    if identity.get("target_claim_level") == "verified":
        ready_checks.append("candidate packet targets verified claim level for future review")
    else:
        gaps.append("candidate packet target_claim_level must be verified")

    if approval.get("approval_record") == "pending" and approval.get("approver") == "pending":
        ready_checks.append("candidate approval is still pending as expected")
    else:
        gaps.append("candidate approval must remain pending before accepted packet creation")

    for field in REQUIRED_VALIDATION_FIELDS:
        if validation.get(field):
            ready_checks.append(f"validation command present: {field}")
        else:
            gaps.append(f"validation command missing: {field}")

    for field in REQUIRED_NON_CLAIMS:
        if non_claims.get(field) == "not_claimed":
            ready_checks.append(f"non-claim preserved: {field}")
        else:
            gaps.append(f"non-claim must be not_claimed: {field}")

    if binding.get("matrix") and binding.get("entry_id"):
        ready_checks.append("governed matrix binding is present")
    else:
        gaps.append("governed matrix binding must be present")

    if source_trace.get("source_id") and source_trace.get("source_section"):
        ready_checks.append("source trace binding is present")
    else:
        gaps.append("source trace source_id/source_section must be present")

    accepted_location = schema.get("accepted_packet_location", {})
    expected_directory = accepted_location.get("directory", "docs/evidence/accepted")
    if _display_path(accepted_dir).endswith(expected_directory):
        ready_checks.append(f"future accepted packet directory is {expected_directory}")
    else:
        gaps.append(f"future accepted packet directory must end with {expected_directory}")

    for field in REQUIRED_ACCEPTANCE_GATE_FIELDS:
        gaps.append(f"future accepted packet must add acceptance_gate.{field}")

    gaps.extend(
        [
            "human approver must be recorded before acceptance",
            "approval_record must change to approved only in the accepted packet",
            "checkpoint_commit must reference the accepted-packet checkpoint commit",
            "validation_receipt must reference a durable receipt for the accepted-packet checkpoint",
            "level3_checkpoint must be true only after Level 3 approval",
            "direct_promotion must be false",
            "accepted packet file must be reviewed before any later verified promotion slice",
        ]
    )

    return {
        "authority_ceiling": "accepted_preapproval_gap_report_only",
        "candidate": _display_path(candidate_path),
        "future_accepted_packet": _display_path(accepted_path),
        "governed_entry": {
            "matrix": binding.get("matrix"),
            "entry_id": binding.get("entry_id"),
            "current_claim_level": binding.get("current_claim_level"),
            "current_evidence_status": binding.get("current_evidence_status"),
        },
        "source_trace": {
            "source_id": source_trace.get("source_id"),
            "source_section": source_trace.get("source_section"),
        },
        "ready_checks": ready_checks,
        "gaps": gaps,
        "claim_ceiling": [
            "preapproval_checklist_only",
            "no_production_accepted_packet",
            "no_verified_uplift",
        ],
        "not_claimed": [
            "no accepted evidence packet exists from this report",
            "no HID entry is verified",
            "no firmware behavior correctness",
            "no OS input stack behavior",
            "no parser runtime behavior",
        ],
    }


def render_markdown(checklist: dict[str, Any]) -> str:
    lines = [
        "# HID Accepted Packet Pre-Approval Checklist",
        "",
        "> Status: gap report only",
        "> Authority ceiling: accepted_preapproval_gap_report_only",
        "",
        f"- Candidate: `{checklist['candidate']}`",
        f"- Future accepted packet path: `{checklist['future_accepted_packet']}`",
        "- Production accepted packet created: no",
        "- Verified uplift: no",
        "",
        "## Governed Entry",
        "",
    ]
    governed_entry = checklist["governed_entry"]
    for key in ("matrix", "entry_id", "current_claim_level", "current_evidence_status"):
        lines.append(f"- {key}: `{governed_entry.get(key)}`")
    lines.extend(["", "## Source Trace", ""])
    source_trace = checklist["source_trace"]
    for key in ("source_id", "source_section"):
        lines.append(f"- {key}: `{source_trace.get(key)}`")
    lines.extend(["", "## Ready Checks", ""])
    lines.extend(f"- {item}" for item in checklist["ready_checks"])
    lines.extend(["", "## Gaps Before Accepted Packet", ""])
    lines.extend(f"- {item}" for item in checklist["gaps"])
    lines.extend(["", "## Claim Ceiling", ""])
    lines.extend(f"- {item}" for item in checklist["claim_ceiling"])
    lines.extend(["", "## Not Claimed", ""])
    lines.extend(f"- {item}" for item in checklist["not_claimed"])
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", default="hid_get_report")
    parser.add_argument("--out")
    args = parser.parse_args()

    checklist = build_checklist(candidate_id=args.candidate)
    output = render_markdown(checklist)
    if args.out:
        out = ROOT / args.out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
