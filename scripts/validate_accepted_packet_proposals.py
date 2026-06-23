#!/usr/bin/env python3
"""Validate accepted-packet proposal artifacts.

Authority ceiling: accepted_packet_proposal_validation_only.
This validator checks proposal structure and claim ceilings only. It does not
create accepted packets, promote entries, or change verification status.
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

from scripts.generate_accepted_packet_preapproval_checklist import list_candidate_ids


PROPOSAL_DIR = ROOT / "evidence" / "accepted_proposals"
PROPOSAL_MARKDOWN_DIR = ROOT / "docs" / "evidence" / "accepted_proposals"
REQUIRED_AUTHORITY_CEILING = "accepted_packet_proposal_only"
REQUIRED_CLAIM_CEILING = {
    "accepted_packet_proposal_only",
    "no_production_accepted_packet",
    "no_verified_uplift",
}
REQUIRED_NOT_CLAIMED = {
    "no accepted evidence packet exists from this proposal",
    "no HID entry is verified by this proposal",
    "no firmware behavior correctness",
    "no OS input stack behavior",
    "no parser runtime behavior",
}


def _display_path(path: Path, root: Path = ROOT) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _load_json(path: Path, root: Path = ROOT) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{_display_path(path, root)} must contain a JSON object")
    return data


def _resolve_under_root(path_arg: str, *, root: Path = ROOT) -> Path:
    path = Path(path_arg)
    candidate = path if path.is_absolute() else root / path
    resolved_root = root.resolve()
    resolved = candidate.resolve()
    try:
        resolved.relative_to(resolved_root)
    except ValueError as exc:
        raise ValueError(f"output path must stay under repository root: {path_arg}") from exc
    return resolved


def _write_receipt(path: Path, receipt: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def _proposal_base_from_json(path: Path) -> str:
    name = path.name
    if name.endswith("_accepted_proposal.json"):
        return name[: -len("_accepted_proposal.json")]
    return path.stem


def _proposal_base_from_markdown(path: Path) -> str:
    name = path.name
    if name.endswith("_accepted_proposal.md"):
        return name[: -len("_accepted_proposal.md")]
    return path.stem


def validate(
    proposal_dir: Path = PROPOSAL_DIR,
    *,
    markdown_dir: Path = PROPOSAL_MARKDOWN_DIR,
    root: Path = ROOT,
) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    findings: list[dict[str, str]] = []

    def add_error(code: str, message: str) -> None:
        errors.append(message)
        findings.append({"code": code, "message": message})

    candidate_ids = set(list_candidate_ids(root / "docs" / "evidence" / "candidates"))
    json_paths = sorted(proposal_dir.glob("*_accepted_proposal.json")) if proposal_dir.exists() else []
    markdown_paths = sorted(markdown_dir.glob("*_accepted_proposal.md")) if markdown_dir.exists() else []
    json_bases = {_proposal_base_from_json(path) for path in json_paths}
    markdown_bases = {_proposal_base_from_markdown(path) for path in markdown_paths}

    missing_json = sorted(candidate_ids - json_bases)
    if missing_json:
        add_error("PROPOSAL_JSON_COVERAGE_INCOMPLETE", f"missing JSON proposal(s): {', '.join(missing_json)}")
    missing_markdown = sorted(candidate_ids - markdown_bases)
    if missing_markdown:
        add_error("PROPOSAL_MARKDOWN_COVERAGE_INCOMPLETE", f"missing Markdown proposal(s): {', '.join(missing_markdown)}")
    stale_json = sorted(json_bases - candidate_ids)
    if stale_json:
        add_error("PROPOSAL_JSON_STALE", f"stale JSON proposal(s): {', '.join(stale_json)}")
    stale_markdown = sorted(markdown_bases - candidate_ids)
    if stale_markdown:
        add_error("PROPOSAL_MARKDOWN_STALE", f"stale Markdown proposal(s): {', '.join(stale_markdown)}")
    missing_markdown_for_json = sorted(json_bases - markdown_bases)
    if missing_markdown_for_json:
        add_error("PROPOSAL_MARKDOWN_JSON_MISMATCH", f"JSON proposal(s) without matching Markdown proposal: {', '.join(missing_markdown_for_json)}")
    missing_json_for_markdown = sorted(markdown_bases - json_bases)
    if missing_json_for_markdown:
        add_error("PROPOSAL_MARKDOWN_JSON_MISMATCH", f"Markdown proposal(s) without matching JSON proposal: {', '.join(missing_json_for_markdown)}")

    proposals: dict[str, dict[str, Any]] = {}
    if proposal_dir.exists():
        for path in json_paths:
            proposals[_display_path(path, root)] = _load_json(path, root)

    for path, proposal in proposals.items():
        proposal_base = _proposal_base_from_json(Path(path))
        if proposal.get("authority_ceiling") != REQUIRED_AUTHORITY_CEILING:
            add_error("PROPOSAL_AUTHORITY_CEILING_INVALID", f"{path} authority_ceiling must be {REQUIRED_AUTHORITY_CEILING}")
        if proposal.get("proposal_status") != "proposal_only":
            add_error("PROPOSAL_STATUS_INVALID", f"{path} proposal_status must be proposal_only")
        if proposal.get("production_accepted_packet_created") is not False:
            add_error("PROPOSAL_ACCEPTED_CREATED_INVALID", f"{path} production_accepted_packet_created must be false")
        if proposal.get("verified_uplift") is not False:
            add_error("PROPOSAL_VERIFIED_UPLIFT_INVALID", f"{path} verified_uplift must be false")

        future = proposal.get("future_accepted_packet")
        if not isinstance(future, str) or not future.startswith("docs/evidence/accepted/") or not future.endswith("_accepted.yaml"):
            add_error("PROPOSAL_FUTURE_ACCEPTED_PATH_INVALID", f"{path} future_accepted_packet must be under docs/evidence/accepted/")
        elif (root / future).exists():
            add_error("PROPOSAL_FUTURE_ACCEPTED_PATH_EXISTS", f"{path} future accepted packet path must not exist: {future}")

        candidate = proposal.get("candidate")
        if not isinstance(candidate, str) or not candidate.startswith("docs/evidence/candidates/") or not candidate.endswith("_candidate.yaml"):
            add_error("PROPOSAL_CANDIDATE_PATH_INVALID", f"{path} candidate must be under docs/evidence/candidates/")
        elif candidate != f"docs/evidence/candidates/{proposal_base}_candidate.yaml":
            add_error("PROPOSAL_CANDIDATE_BINDING_MISMATCH", f"{path} candidate must match proposal basename: {proposal_base}")
        elif not (root / candidate).exists():
            add_error("PROPOSAL_CANDIDATE_MISSING", f"{path} candidate does not exist: {candidate}")

        preapproval = proposal.get("preapproval_report")
        if not isinstance(preapproval, str) or not preapproval.startswith("docs/evidence/preapproval/") or not preapproval.endswith("_preapproval_checklist.md"):
            add_error("PROPOSAL_PREAPPROVAL_PATH_INVALID", f"{path} preapproval_report must be under docs/evidence/preapproval/")
        elif preapproval != f"docs/evidence/preapproval/{proposal_base}_preapproval_checklist.md":
            add_error("PROPOSAL_PREAPPROVAL_BINDING_MISMATCH", f"{path} preapproval_report must match proposal basename: {proposal_base}")
        elif not (root / preapproval).exists():
            add_error("PROPOSAL_PREAPPROVAL_MISSING", f"{path} preapproval report does not exist: {preapproval}")

        if isinstance(future, str) and future.startswith("docs/evidence/accepted/") and future.endswith("_accepted.yaml"):
            expected_future = f"docs/evidence/accepted/{proposal_base}_accepted.yaml"
            if future != expected_future:
                add_error("PROPOSAL_FUTURE_ACCEPTED_BINDING_MISMATCH", f"{path} future_accepted_packet must match proposal basename: {proposal_base}")

        governed_entry = proposal.get("governed_entry", {})
        if not isinstance(governed_entry, dict) or governed_entry.get("current_claim_level") == "verified":
            add_error("PROPOSAL_CURRENT_CLAIM_INVALID", f"{path} governed entry must not be currently verified")

        gate = proposal.get("required_level3_acceptance_gate", {})
        if not isinstance(gate, dict):
            add_error("PROPOSAL_GATE_MISSING", f"{path} required_level3_acceptance_gate must be a mapping")
            gate = {}
        expected_gate = {
            "previous_packet_status": "candidate",
            "level3_checkpoint": True,
            "direct_promotion": False,
        }
        for key, expected in expected_gate.items():
            if gate.get(key) != expected:
                add_error("PROPOSAL_GATE_INVALID", f"{path} required_level3_acceptance_gate.{key} must be {expected!r}")
        if not isinstance(gate.get("checkpoint_commit"), str) or "TBD" not in gate.get("checkpoint_commit", ""):
            add_error("PROPOSAL_GATE_CHECKPOINT_NOT_PLACEHOLDER", f"{path} checkpoint_commit must remain a TBD placeholder")
        if not isinstance(gate.get("validation_receipt"), str) or "TBD" not in gate.get("validation_receipt", ""):
            add_error("PROPOSAL_GATE_RECEIPT_NOT_PLACEHOLDER", f"{path} validation_receipt must remain a TBD placeholder")

        claim_ceiling = set(proposal.get("claim_ceiling", []))
        missing_claims = sorted(REQUIRED_CLAIM_CEILING - claim_ceiling)
        if missing_claims:
            add_error("PROPOSAL_CLAIM_CEILING_INCOMPLETE", f"{path} missing claim ceiling: {', '.join(missing_claims)}")

        not_claimed = set(proposal.get("not_claimed", []))
        missing_not_claimed = sorted(REQUIRED_NOT_CLAIMED - not_claimed)
        if missing_not_claimed:
            add_error("PROPOSAL_NOT_CLAIMED_INCOMPLETE", f"{path} missing not_claimed: {', '.join(missing_not_claimed)}")

    receipt = {
        "validator": "validate_accepted_packet_proposals.py",
        "authority_ceiling": "accepted_packet_proposal_validation_only",
        "result": "PASS" if not errors else "FAIL",
        "checked_proposals": sorted(proposals),
        "checked_proposal_count": len(proposals),
        "candidate_count": len(candidate_ids),
        "markdown_proposal_count": len(markdown_bases),
        "json_proposal_count": len(json_bases),
        "error_count": len(errors),
        "errors": errors,
        "findings": findings,
    }
    return errors, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt-out")
    args = parser.parse_args()

    errors, receipt = validate()
    if args.receipt_out:
        try:
            receipt_path = _resolve_under_root(args.receipt_out)
        except ValueError as exc:
            print("FAIL validate_accepted_packet_proposals")
            print(f"- {exc}")
            return 1
        _write_receipt(receipt_path, receipt)

    if errors:
        print("FAIL validate_accepted_packet_proposals")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS validate_accepted_packet_proposals")
    print(f"- checked proposals: {receipt['checked_proposal_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
