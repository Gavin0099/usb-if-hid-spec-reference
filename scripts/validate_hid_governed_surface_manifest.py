#!/usr/bin/env python3
"""Validate the HID governed surface manifest.

Authority ceiling: manifest_structural_integrity_only.
Does not re-validate matrix semantics; use per-matrix validators for that.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "exports" / "hid_governed_surface_manifest.yaml"

VALID_SPEC_FAMILIES = {"hid11"}
VALID_STATES = {"scaffold"}


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return data


def main() -> int:
    if not MANIFEST_PATH.exists():
        print(f"FAIL: manifest not found: {MANIFEST_PATH}")
        return 1

    doc = _load_yaml(MANIFEST_PATH)
    errors: list[str] = []

    if doc.get("manifest_id") != "hid_governed_surface_manifest":
        errors.append("R1: manifest_id must be hid_governed_surface_manifest")

    entries = doc.get("governed_tables") or []
    if not isinstance(entries, list) or not entries:
        errors.append("R2: governed_tables list missing or empty")
        entries = []

    seen_ids: set[str] = set()
    family_tracked: dict[str, int] = {}
    family_scaffold: dict[str, int] = {}
    family_verified: dict[str, int] = {}
    family_reviewed: dict[str, int] = {}

    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"R3: entry[{index}] is not a dict")
            continue

        entry_id = str(entry.get("id", f"<entry[{index}]>"))
        if entry_id in seen_ids:
            errors.append(f"R7: duplicate entry id {entry_id!r}")
        seen_ids.add(entry_id)

        for field in ("id", "spec_family", "path", "validator", "state", "tracked", "scaffold", "verified", "reviewed"):
            if field not in entry:
                errors.append(f"R3: entry {entry_id!r} missing required field {field!r}")

        raw_path = entry.get("path", "")
        table_path = ROOT / str(raw_path)
        if raw_path and not table_path.exists():
            errors.append(f"R4: entry {entry_id!r} path does not exist: {table_path}")

        raw_validator = entry.get("validator", "")
        validator_path = ROOT / str(raw_validator)
        if raw_validator and not validator_path.exists():
            errors.append(f"R4: entry {entry_id!r} validator does not exist: {validator_path}")

        spec_family = entry.get("spec_family", "")
        if spec_family not in VALID_SPEC_FAMILIES:
            errors.append(f"R5: entry {entry_id!r} spec_family {spec_family!r} not in {VALID_SPEC_FAMILIES}")

        state = entry.get("state", "")
        if state not in VALID_STATES:
            errors.append(f"R6: entry {entry_id!r} state {state!r} not in {VALID_STATES}")

        if spec_family in VALID_SPEC_FAMILIES:
            family_tracked[spec_family] = family_tracked.get(spec_family, 0) + int(entry.get("tracked", 0))
            family_scaffold[spec_family] = family_scaffold.get(spec_family, 0) + int(entry.get("scaffold", 0))
            family_verified[spec_family] = family_verified.get(spec_family, 0) + int(entry.get("verified", 0))
            family_reviewed[spec_family] = family_reviewed.get(spec_family, 0) + int(entry.get("reviewed", 0))

    authority = doc.get("authority_surface") or {}
    if not isinstance(authority, dict):
        errors.append("R8: authority_surface must be a mapping")
        authority = {}

    for spec_family in VALID_SPEC_FAMILIES:
        surface = authority.get(spec_family) or {}
        if not isinstance(surface, dict):
            errors.append(f"R8: authority_surface.{spec_family} must be a mapping")
            continue
        checks = {
            "tracked": family_tracked.get(spec_family, 0),
            "scaffold": family_scaffold.get(spec_family, 0),
            "verified": family_verified.get(spec_family, 0),
            "reviewed": family_reviewed.get(spec_family, 0),
        }
        for field, actual in checks.items():
            expected = surface.get(field)
            if expected is not None and int(expected) != actual:
                errors.append(
                    f"R8: {spec_family} {field} sum mismatch: "
                    f"authority_surface.{field}={expected}, governed_tables sum={actual}"
                )

    if errors:
        print("FAIL: hid_governed_surface_manifest validation")
        for error in errors:
            print(f"  {error}")
        return 1

    hid11_tables = [entry for entry in entries if isinstance(entry, dict) and entry.get("spec_family") == "hid11"]
    print("PASS: hid_governed_surface_manifest validation")
    print(f"  manifest_id: {doc.get('manifest_id')}")
    print(f"  governed_tables: {len(entries)} (hid11={len(hid11_tables)})")
    surface = authority.get("hid11") or {}
    print(
        "  hid11: "
        f"state={surface.get('state')} "
        f"tracked={surface.get('tracked')} "
        f"scaffold={surface.get('scaffold')} "
        f"verified={surface.get('verified')} "
        f"reviewed={surface.get('reviewed')}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
