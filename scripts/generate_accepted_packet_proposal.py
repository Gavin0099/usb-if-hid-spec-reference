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
    _display_path,
    _resolve_under_root,
    build_checklist,
    list_candidate_ids,
)


DEFAULT_CANDIDATE = "hid_get_report"
DEFAULT_MARKDOWN_DIR = ROOT / "docs" / "evidence" / "accepted_proposals"
DEFAULT_JSON_DIR = ROOT / "evidence" / "accepted_proposals"


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


def stale_proposal_artifacts(
    *,
    markdown_dir: Path = DEFAULT_MARKDOWN_DIR,
    json_dir: Path = DEFAULT_JSON_DIR,
) -> list[Path]:
    expected = {f"{candidate_id}_accepted_proposal" for candidate_id in list_candidate_ids()}
    stale: list[Path] = []
    if markdown_dir.exists():
        stale.extend(
            path
            for path in sorted(markdown_dir.glob("*_accepted_proposal.md"))
            if path.stem not in expected
        )
    if json_dir.exists():
        stale.extend(
            path
            for path in sorted(json_dir.glob("*_accepted_proposal.json"))
            if path.stem not in expected
        )
    return stale


def write_all_proposals(
    *,
    markdown_dir: Path = DEFAULT_MARKDOWN_DIR,
    json_dir: Path = DEFAULT_JSON_DIR,
    prune_stale: bool = False,
) -> int:
    stale = stale_proposal_artifacts(markdown_dir=markdown_dir, json_dir=json_dir)
    if stale and not prune_stale:
        paths = ", ".join(_display_path(path) for path in stale)
        raise ValueError(f"stale accepted-packet proposal artifact(s) found: {paths}")
    for stale_path in stale:
        stale_path.unlink()
    markdown_dir.mkdir(parents=True, exist_ok=True)
    json_dir.mkdir(parents=True, exist_ok=True)
    candidate_ids = list_candidate_ids()
    for candidate_id in candidate_ids:
        proposal = build_proposal(candidate_id=candidate_id)
        write_proposal(
            proposal,
            markdown_out=markdown_dir / f"{candidate_id}_accepted_proposal.md",
            json_out=json_dir / f"{candidate_id}_accepted_proposal.json",
        )
    return len(candidate_ids)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", default=DEFAULT_CANDIDATE)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--markdown-out", default="docs/evidence/accepted_proposals/hid_get_report_accepted_proposal.md")
    parser.add_argument("--json-out", default="evidence/accepted_proposals/hid_get_report_accepted_proposal.json")
    parser.add_argument("--markdown-dir", default="docs/evidence/accepted_proposals")
    parser.add_argument("--json-dir", default="evidence/accepted_proposals")
    parser.add_argument("--prune-stale", action="store_true")
    args = parser.parse_args()
    try:
        if args.all:
            markdown_dir = _resolve_under_root(args.markdown_dir)
            json_dir = _resolve_under_root(args.json_dir)
            count = write_all_proposals(
                markdown_dir=markdown_dir,
                json_dir=json_dir,
                prune_stale=args.prune_stale,
            )
            print(
                "Generated accepted packet proposal batch: "
                f"{count} proposal(s), accepted_created=false, verified_uplift=false"
            )
            return 0
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
