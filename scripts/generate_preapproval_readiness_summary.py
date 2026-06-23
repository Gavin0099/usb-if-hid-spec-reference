#!/usr/bin/env python3
"""Generate readiness summaries for accepted-packet pre-approval reports.

Authority ceiling: preapproval_readiness_summary_only.
This tool summarizes candidate/pre-approval gaps only. It does not create
accepted packets, promote entries, or change verification status.
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
    PREAPPROVAL_DIR,
    ROOT,
    _resolve_under_root,
    build_checklist,
    list_candidate_ids,
    stale_preapproval_reports,
)


SUMMARY_MD = ROOT / "docs" / "evidence" / "preapproval_summary.md"
SUMMARY_JSON = ROOT / "evidence" / "preapproval_summary.json"


def _display_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _preapproval_report_path(candidate_id: str, preapproval_dir: Path = PREAPPROVAL_DIR) -> Path:
    return preapproval_dir / f"{candidate_id}_preapproval_checklist.md"


def _accepted_packet_exists(path_text: str) -> bool:
    path = ROOT / path_text
    return path.exists()


def build_summary() -> dict[str, Any]:
    stale_reports = stale_preapproval_reports()
    candidate_ids = list_candidate_ids()
    entries: list[dict[str, Any]] = []
    for candidate_id in candidate_ids:
        checklist = build_checklist(candidate_id=candidate_id)
        governed_entry = checklist["governed_entry"]
        future_accepted_packet = checklist["future_accepted_packet"]
        entries.append(
            {
                "entry_id": governed_entry["entry_id"],
                "matrix": governed_entry["matrix"],
                "candidate": checklist["candidate"],
                "preapproval_report": _display_path(_preapproval_report_path(candidate_id)),
                "future_accepted_packet": future_accepted_packet,
                "accepted_packet_exists": _accepted_packet_exists(future_accepted_packet),
                "current_claim_level": governed_entry["current_claim_level"],
                "current_evidence_status": governed_entry["current_evidence_status"],
                "ready_check_count": len(checklist["ready_checks"]),
                "gap_count": len(checklist["gaps"]),
                "missing_acceptance_gate_fields": [
                    gap.removeprefix("future accepted packet must add acceptance_gate.")
                    for gap in checklist["gaps"]
                    if gap.startswith("future accepted packet must add acceptance_gate.")
                ],
                "requires_human_approval": any("human approver" in gap for gap in checklist["gaps"]),
                "requires_validation_receipt": any("validation_receipt" in gap for gap in checklist["gaps"]),
                "claim_ceiling": checklist["claim_ceiling"],
            }
        )

    accepted_count = sum(1 for entry in entries if entry["accepted_packet_exists"])
    verified_count = sum(1 for entry in entries if entry["current_claim_level"] == "verified")
    return {
        "authority_ceiling": "preapproval_readiness_summary_only",
        "candidate_count": len(candidate_ids),
        "preapproval_report_count": len(entries),
        "production_accepted_packet_count": accepted_count,
        "verified_entry_count": verified_count,
        "stale_preapproval_report_count": len(stale_reports),
        "entries": entries,
        "claim_ceiling": [
            "preapproval_readiness_summary_only",
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
        "# HID Accepted Packet Pre-Approval Readiness Summary",
        "",
        "> Status: readiness summary only",
        "> Authority ceiling: preapproval_readiness_summary_only",
        "",
        "## Totals",
        "",
        f"- candidate packets: {summary['candidate_count']}",
        f"- pre-approval reports: {summary['preapproval_report_count']}",
        f"- production accepted packets: {summary['production_accepted_packet_count']}",
        f"- verified entries: {summary['verified_entry_count']}",
        f"- stale pre-approval reports: {summary['stale_preapproval_report_count']}",
        "",
        "## Entries",
        "",
        "| Entry | Matrix | Candidate | Pre-approval report | Future accepted packet | Ready | Gaps | Missing acceptance gate fields |",
        "|---|---|---|---|---|---:|---:|---|",
    ]
    for entry in summary["entries"]:
        missing = ", ".join(entry["missing_acceptance_gate_fields"])
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{entry['entry_id']}`",
                    f"`{entry['matrix']}`",
                    f"`{entry['candidate']}`",
                    f"`{entry['preapproval_report']}`",
                    f"`{entry['future_accepted_packet']}`",
                    str(entry["ready_check_count"]),
                    str(entry["gap_count"]),
                    missing,
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
    parser.add_argument("--markdown-out", default="docs/evidence/preapproval_summary.md")
    parser.add_argument("--json-out", default="evidence/preapproval_summary.json")
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
        "Generated pre-approval readiness summary: "
        f"{summary['preapproval_report_count']} report(s), "
        f"{summary['production_accepted_packet_count']} accepted packet(s), "
        f"{summary['verified_entry_count']} verified entry(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
