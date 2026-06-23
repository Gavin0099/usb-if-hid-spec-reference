#!/usr/bin/env python3
"""Generate a production accepted evidence packet from a prepared candidate.

Authority ceiling: accepted_packet_production_candidate_transition_only.

This script performs the mechanical candidate->accepted transition and requires
explicit Level 3 acceptance context (approver, checkpoint commit, and
validation receipt). It does not promote claims, does not modify matrices, and
does not perform verification status updates.
"""

from __future__ import annotations

import argparse
import copy
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_DIR = ROOT / "docs" / "evidence" / "candidates"
ACCEPTED_DIR = ROOT / "docs" / "evidence" / "accepted"


def _display_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _resolve_under_root(path_value: str) -> Path:
    path = Path(path_value)
    resolved = path.resolve() if path.is_absolute() else (ROOT / path).resolve()
    root = ROOT.resolve()
    if resolved != root and root not in resolved.parents:
        raise ValueError(f"output path must stay under repository root: {path_value}")
    return resolved


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{_display_path(path)} must contain a YAML mapping")
    return data


def _candidate_path(candidate_id: str, candidate_dir: Path = CANDIDATE_DIR) -> Path:
    candidate = Path(candidate_id)
    if candidate.suffix:
        return candidate if candidate.is_absolute() else ROOT / candidate
    return candidate_dir / f"{candidate_id}_candidate.yaml"


def _candidate_base(candidate_path: Path) -> str:
    name = candidate_path.name
    if name.endswith("_candidate.yaml"):
        return name[:-len("_candidate.yaml")]
    return candidate_path.stem


def _accepted_path_for_candidate(
    candidate_path: Path,
    accepted_dir: Path = ACCEPTED_DIR,
) -> Path:
    return accepted_dir / f"{_candidate_base(candidate_path)}_accepted.yaml"


def list_candidate_ids(candidate_dir: Path = CANDIDATE_DIR) -> list[str]:
    return [_candidate_base(path) for path in sorted(candidate_dir.glob("*_candidate.yaml"))]


def stale_accepted_artifacts(
    *,
    candidate_dir: Path = CANDIDATE_DIR,
    accepted_dir: Path = ACCEPTED_DIR,
) -> list[Path]:
    expected = {f"{candidate_id}_accepted.yaml" for candidate_id in list_candidate_ids(candidate_dir)}
    if not accepted_dir.exists():
        return []
    return [path for path in sorted(accepted_dir.glob("*_accepted.yaml")) if path.name not in expected]


def _as_yaml_dump(data: dict[str, Any]) -> str:
    return yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=120)


def build_accepted_packet(
    *,
    candidate_id: str,
    approver: str,
    checkpoint_commit: str,
    validation_receipt: str,
    candidate_dir: Path = CANDIDATE_DIR,
    level3_checkpoint: bool = True,
    direct_promotion: bool = False,
) -> dict[str, Any]:
    approver_value = approver.strip()
    if not approver_value or approver_value.lower() in {"", "pending", "none"}:
        raise ValueError("approver must be a concrete human approver marker")
    checkpoint_commit = checkpoint_commit.strip()
    if not checkpoint_commit:
        raise ValueError("checkpoint_commit must be non-empty")
    validation_receipt = validation_receipt.strip()
    if not validation_receipt:
        raise ValueError("validation_receipt must be non-empty")
    validation_receipt_path = _resolve_under_root(validation_receipt)
    validation_receipt = _display_path(validation_receipt_path)

    candidate_path = _candidate_path(candidate_id, candidate_dir=candidate_dir)
    if not candidate_path.exists():
        raise FileNotFoundError(f"candidate packet not found: {_display_path(candidate_path)}")

    candidate = _load_yaml(candidate_path)
    packet_identity = candidate.get("packet_identity", {})
    if not isinstance(packet_identity, dict):
        raise ValueError(f"{_display_path(candidate_path)} packet_identity must be a mapping")

    if packet_identity.get("packet_status") != "candidate":
        raise ValueError(f"{_display_path(candidate_path)} packet_status must be candidate before acceptance")
    if packet_identity.get("review_level") != 3:
        raise ValueError(f"{_display_path(candidate_path)} requires review_level 3 for accepted transition")
    if packet_identity.get("target_claim_level") != "verified":
        raise ValueError(f"{_display_path(candidate_path)} must target verified claim level")

    approval = candidate.get("approval", {})
    if not isinstance(approval, dict):
        raise ValueError(f"{_display_path(candidate_path)} approval must be a mapping")
    if approval.get("approval_record") != "pending" or approval.get("approver") != "pending":
        raise ValueError(
            f"{_display_path(candidate_path)} approval must remain pending before accepted transition"
        )

    accepted = copy.deepcopy(candidate)
    accepted.setdefault("packet_identity", {})["packet_status"] = "accepted"

    accepted.setdefault("approval", {})["approval_record"] = "approved"
    accepted["approval"]["approver"] = approver_value

    accepted["acceptance_gate"] = {
        "previous_packet_status": "candidate",
        "checkpoint_commit": checkpoint_commit,
        "validation_receipt": validation_receipt,
        "level3_checkpoint": bool(level3_checkpoint),
        "direct_promotion": bool(direct_promotion),
    }

    return accepted


def write_accepted_packet(packet: dict[str, Any], accepted_out: Path) -> None:
    accepted_out.parent.mkdir(parents=True, exist_ok=True)
    accepted_out.write_text(_as_yaml_dump(packet), encoding="utf-8")


def write_all_accepted(
    *,
    approver: str,
    checkpoint_commit: str,
    validation_receipt: str,
    accepted_dir: Path = ACCEPTED_DIR,
    candidate_dir: Path = CANDIDATE_DIR,
    prune_stale: bool = False,
) -> int:
    stale = stale_accepted_artifacts(candidate_dir=candidate_dir, accepted_dir=accepted_dir)
    if stale and not prune_stale:
        stale_paths = ", ".join(_display_path(path) for path in stale)
        raise ValueError(f"stale accepted packet artifact(s) found: {stale_paths}")
    for stale_path in stale:
        stale_path.unlink()

    candidate_ids = list_candidate_ids(candidate_dir)
    accepted_dir.mkdir(parents=True, exist_ok=True)
    for candidate_id in candidate_ids:
        candidate_path = _candidate_path(candidate_id, candidate_dir=candidate_dir)
        accepted = build_accepted_packet(
            candidate_id=_candidate_base(candidate_path),
            approver=approver,
            checkpoint_commit=checkpoint_commit,
            validation_receipt=validation_receipt,
            candidate_dir=candidate_dir,
        )
        write_accepted_packet(accepted, accepted_out=_accepted_path_for_candidate(candidate_path, accepted_dir))
    return len(candidate_ids)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", default="hid_get_report")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--approver", default="")
    parser.add_argument("--checkpoint-commit", default="")
    parser.add_argument("--validation-receipt", default="")
    parser.add_argument("--out")
    parser.add_argument("--out-dir", default="docs/evidence/accepted")
    parser.add_argument("--candidate-dir", default="docs/evidence/candidates")
    parser.add_argument("--prune-stale", action="store_true")
    parser.add_argument("--write", action="store_true", help="Write accepted packet files")
    args = parser.parse_args()

    try:
        accepted_dir = _resolve_under_root(args.out_dir)
        candidate_dir = _resolve_under_root(args.candidate_dir)

        if args.all:
            count = write_all_accepted(
                approver=args.approver,
                checkpoint_commit=args.checkpoint_commit,
                validation_receipt=args.validation_receipt,
                accepted_dir=accepted_dir,
                candidate_dir=candidate_dir,
                prune_stale=args.prune_stale,
            )
            print(
                "Generated accepted packet batch: "
                f"{count} packet(s), accepted_created=true"
            )
            return 0

        if args.write:
            if not args.out:
                accepted_path = _accepted_path_for_candidate(
                    _candidate_path(args.candidate, candidate_dir=candidate_dir),
                    accepted_dir=accepted_dir,
                )
            else:
                accepted_path = _resolve_under_root(args.out)

            packet = build_accepted_packet(
                candidate_id=args.candidate,
                approver=args.approver,
                checkpoint_commit=args.checkpoint_commit,
                validation_receipt=args.validation_receipt,
                candidate_dir=candidate_dir,
            )
            write_accepted_packet(packet, accepted_out=accepted_path)
            print(
                "Generated accepted packet: "
                f"{_display_path(accepted_path)} | packet_status=accepted"
            )
            return 0

        packet = build_accepted_packet(
            candidate_id=args.candidate,
            approver=args.approver,
            checkpoint_commit=args.checkpoint_commit,
            validation_receipt=args.validation_receipt,
            candidate_dir=candidate_dir,
        )
        print(_as_yaml_dump(packet), end="")
        return 0
    except (FileNotFoundError, ValueError, TypeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
