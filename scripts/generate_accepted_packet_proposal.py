#!/usr/bin/env python3
"""Generate a proposal for a future accepted evidence packet.

Authority ceiling: accepted_packet_proposal_only.
This tool creates proposal artifacts only. It does not create accepted packets,
promote entries, or change verification status.
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

from scripts.generate_accepted_packet_preapproval_checklist import (
    _resolve_under_root,
    build_checklist,
)


DEFAULT_CANDIDATE = "hid_get_report"


def build_proposal(candidate_id: str = DEFAULT_CANDIDATE) -> dict[str, Any]:
    checklist = build_checklist(candidate_id=candidate_id)
    governed_entry = checklist["governed_entry"]
    return {
        "authority_ceiling": "accepted_packet_proposal_only",
        "proposal_status": "proposal_only",
        "candidate": checklist["candidate"],
        "preapproval_report": f"docs/evidence/preapproval/{candidate_id}_preapproval_checklist.md",
        "future_accepted_packet": checklist["future_accepted_packet"],
        "production_accepted_packet_created": False,
        "verified_uplift": False,
        "governed_entry": governed_entry,
        "source_trace": checklist["source_trace"],
        "required_level3_acceptance_gate": {
            "previous_packet_status": "candidate",
            "checkpoint_commit": "TBD_LEVEL3_ACCEPTED_PACKET_COMMIT",
            "validation_receipt": "TBD_LEVEL3_VALIDATION_RECEIPT",
            "level3_checkpoint": True,
            "direct_promotion": False,
        },
        "required_approval": {
            "approval_record": "approved",
            "approver": "TBD_HUMAN_APPROVER",
            "requested_approval": "Level 3 approval for accepted packet status only",
        },
        "required_validators": [
            "python -X utf8 scripts/validate_source_authority.py",
            "python -X utf8 scripts/validate_evidence_packet_schema.py",
            "python -X utf8 scripts/validate_hid_governed_surface_manifest.py",
            "python -X utf8 scripts/validate_hid_class_request_matrix.py",
            "python -X utf8 scripts/validate_hid_descriptor_fields_matrix.py",
            "python -X utf8 scripts/validate_hid_report_descriptor_items_matrix.py",
            "python -X utf8 scripts/validate_verification_status.py",
            "python -X utf8 scripts/probe_table_fingerprint.py --mode check --manifest exports/hid_governed_surface_manifest.yaml --baseline-in evidence/table_fingerprint_baseline.jsonl",
            "python -m unittest discover -s tests",
        ],
        "ready_checks": checklist["ready_checks"],
        "remaining_gaps": checklist["gaps"],
        "claim_ceiling": [
            "accepted_packet_proposal_only",
            "no_production_accepted_packet",
            "no_verified_uplift",
        ],
        "not_claimed": [
            "no accepted evidence packet exists from this proposal",
            "no HID entry is verified by this proposal",
            "no firmware behavior correctness",
            "no OS input stack behavior",
            "no parser runtime behavior",
            "no product-specific HID behavior",
        ],
    }


def render_markdown(proposal: dict[str, Any]) -> str:
    gate = proposal["required_level3_acceptance_gate"]
    approval = proposal["required_approval"]
    governed_entry = proposal["governed_entry"]
    lines = [
        "# HID Accepted Packet Proposal",
        "",
        "> Status: proposal only",
        "> Authority ceiling: accepted_packet_proposal_only",
        "",
        f"- Candidate: `{proposal['candidate']}`",
        f"- Pre-approval report: `{proposal['preapproval_report']}`",
        f"- Future accepted packet path: `{proposal['future_accepted_packet']}`",
        "- Production accepted packet created: no",
        "- Verified uplift: no",
        "",
        "## Governed Entry",
        "",
    ]
    for key in ("matrix", "entry_id", "current_claim_level", "current_evidence_status"):
        lines.append(f"- {key}: `{governed_entry.get(key)}`")
    lines.extend(["", "## Required Level 3 Acceptance Gate", ""])
    for key in ("previous_packet_status", "checkpoint_commit", "validation_receipt", "level3_checkpoint", "direct_promotion"):
        value = gate[key]
        if isinstance(value, bool):
            value = str(value).lower()
        lines.append(f"- {key}: `{value}`")
    lines.extend(["", "## Required Approval", ""])
    for key in ("approval_record", "approver", "requested_approval"):
        lines.append(f"- {key}: `{approval[key]}`")
    lines.extend(["", "## Required Validators", ""])
    lines.extend(f"- `{validator}`" for validator in proposal["required_validators"])
    lines.extend(["", "## Remaining Gaps", ""])
    lines.extend(f"- {gap}" for gap in proposal["remaining_gaps"])
    lines.extend(["", "## Claim Ceiling", ""])
    lines.extend(f"- {claim}" for claim in proposal["claim_ceiling"])
    lines.extend(["", "## Not Claimed", ""])
    lines.extend(f"- {claim}" for claim in proposal["not_claimed"])
    lines.append("")
    return "\n".join(lines)


def write_proposal(proposal: dict[str, Any], *, markdown_out: Path, json_out: Path) -> None:
    markdown_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.parent.mkdir(parents=True, exist_ok=True)
    markdown_out.write_text(render_markdown(proposal), encoding="utf-8")
    json_out.write_text(json.dumps(proposal, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", default=DEFAULT_CANDIDATE)
    parser.add_argument("--markdown-out", default="docs/evidence/accepted_proposals/hid_get_report_accepted_proposal.md")
    parser.add_argument("--json-out", default="evidence/accepted_proposals/hid_get_report_accepted_proposal.json")
    args = parser.parse_args()
    try:
        markdown_out = _resolve_under_root(args.markdown_out)
        json_out = _resolve_under_root(args.json_out)
        proposal = build_proposal(candidate_id=args.candidate)
        write_proposal(proposal, markdown_out=markdown_out, json_out=json_out)
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(
        "Generated accepted packet proposal: "
        f"{proposal['governed_entry']['entry_id']}, "
        f"accepted_created={proposal['production_accepted_packet_created']}, "
        f"verified_uplift={proposal['verified_uplift']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
