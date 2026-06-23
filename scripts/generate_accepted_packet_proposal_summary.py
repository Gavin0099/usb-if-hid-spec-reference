#!/usr/bin/env python3
"""Generate a summary for accepted-packet proposal artifacts.

Authority ceiling: accepted_packet_proposal_summary_only.
This tool summarizes proposal artifacts only. It does not create accepted
packets, promote entries, or change verification status.
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

from scripts.generate_accepted_packet_preapproval_checklist import _resolve_under_root, list_candidate_ids
from scripts.validate_accepted_packet_proposals import PROPOSAL_DIR, PROPOSAL_MARKDOWN_DIR, validate


SUMMARY_MD = ROOT / "docs" / "evidence" / "accepted_proposal_summary.md"
SUMMARY_JSON = ROOT / "evidence" / "accepted_proposal_summary.json"


def _display_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _proposal_json_path(candidate_id: str, proposal_dir: Path = PROPOSAL_DIR) -> Path:
    return proposal_dir / f"{candidate_id}_accepted_proposal.json"


def _proposal_markdown_path(candidate_id: str, markdown_dir: Path = PROPOSAL_MARKDOWN_DIR) -> Path:
    return markdown_dir / f"{candidate_id}_accepted_proposal.md"


def _load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{_display_path(path)} must contain a JSON object")
    return data


def _accepted_packet_exists(path_text: str) -> bool:
    return (ROOT / path_text).exists()


def build_summary() -> dict[str, Any]:
    errors, receipt = validate()
    if errors:
        raise ValueError("accepted proposal validation must pass before summary generation")

    candidate_ids = list_candidate_ids()
    entries: list[dict[str, Any]] = []
    for candidate_id in candidate_ids:
        proposal = _load_json(_proposal_json_path(candidate_id))
        governed_entry = proposal["governed_entry"]
        source_trace = proposal["source_trace"]
        future_accepted_packet = proposal["future_accepted_packet"]
        entries.append(
            {
                "entry_id": governed_entry["entry_id"],
                "matrix": governed_entry["matrix"],
                "candidate": proposal["candidate"],
                "proposal_markdown": _display_path(_proposal_markdown_path(candidate_id)),
                "proposal_json": _display_path(_proposal_json_path(candidate_id)),
                "preapproval_report": proposal["preapproval_report"],
                "future_accepted_packet": future_accepted_packet,
                "accepted_packet_exists": _accepted_packet_exists(future_accepted_packet),
                "current_claim_level": governed_entry["current_claim_level"],
                "current_evidence_status": governed_entry["current_evidence_status"],
                "source_id": source_trace["source_id"],
                "source_section": source_trace["source_section"],
                "ready_check_count": len(proposal["ready_checks"]),
                "gap_count": len(proposal["remaining_gaps"]),
                "claim_ceiling": proposal["claim_ceiling"],
            }
        )

    accepted_count = sum(1 for entry in entries if entry["accepted_packet_exists"])
    verified_count = sum(1 for entry in entries if entry["current_claim_level"] == "verified")
    return {
        "authority_ceiling": "accepted_packet_proposal_summary_only",
        "candidate_count": len(candidate_ids),
        "proposal_markdown_count": receipt["markdown_proposal_count"],
        "proposal_json_count": receipt["json_proposal_count"],
        "production_accepted_packet_count": accepted_count,
        "verified_entry_count": verified_count,
        "validator_checked_proposal_count": receipt["checked_proposal_count"],
        "entries": entries,
        "claim_ceiling": [
            "accepted_packet_proposal_summary_only",
            "no_production_accepted_packet",
            "no_verified_uplift",
        ],
        "not_claimed": [
            "no accepted evidence packet exists from this summary",
            "no HID entry is verified by this summary",
            "no firmware behavior correctness",
            "no OS input stack behavior",
            "no parser runtime behavior",
        ],
    }


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# HID Accepted Packet Proposal Summary",
        "",
        "> Status: proposal summary only",
        "> Authority ceiling: accepted_packet_proposal_summary_only",
        "",
        "## Totals",
        "",
        f"- candidate packets: {summary['candidate_count']}",
        f"- proposal Markdown artifacts: {summary['proposal_markdown_count']}",
        f"- proposal JSON artifacts: {summary['proposal_json_count']}",
        f"- validator checked proposals: {summary['validator_checked_proposal_count']}",
        f"- production accepted packets: {summary['production_accepted_packet_count']}",
        f"- verified entries: {summary['verified_entry_count']}",
        "",
        "## Entries",
        "",
        "| Entry | Matrix | Source | Current claim | Future accepted packet | Ready | Gaps |",
        "|---|---|---|---|---|---:|---:|",
    ]
    for entry in summary["entries"]:
        source = f"{entry['source_id']} {entry['source_section']}"
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{entry['entry_id']}`",
                    f"`{entry['matrix']}`",
                    f"`{source}`",
                    f"`{entry['current_claim_level']}`",
                    f"`{entry['future_accepted_packet']}`",
                    str(entry["ready_check_count"]),
                    str(entry["gap_count"]),
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
    json_out.write_text(json.dumps(summary, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--markdown-out", default="docs/evidence/accepted_proposal_summary.md")
    parser.add_argument("--json-out", default="evidence/accepted_proposal_summary.json")
    args = parser.parse_args()
    try:
        markdown_out = _resolve_under_root(args.markdown_out)
        json_out = _resolve_under_root(args.json_out)
        summary = build_summary()
        write_summary(summary, markdown_out=markdown_out, json_out=json_out)
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(
        "Generated accepted proposal summary: "
        f"{summary['proposal_json_count']} proposal(s), "
        f"{summary['production_accepted_packet_count']} accepted packet(s), "
        f"{summary['verified_entry_count']} verified entry(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
