# HID 6.2.2 Import Eligibility

## Purpose

This artifact defines the minimum criteria to move `6.2.2` (HID Descriptor Report
Descriptor item types) from `future_authorized_usage` to `current_imported_usage`.

## Scope

`6.2.2` is scoped to report descriptor identity-level item-type scaffolding only:

- item-type identifiers and classes
- setup-level field structure (identities and relationships)
- non-semantic source references and cross-links for future review

It excludes runtime behavior, parser semantics, and firmware/host interpretation.

## Entry criteria

`6.2.2` may move to `current_imported_usage` only when all of the following are
completed in one cohesive slice with checkpoint validation:

1. Repository-local entry surfaces exist:
   - machine-readable surface under `data/`
   - English and zh-TW documentation surfaces under `specs/` and `specs/en/`
2. The matrix/scaffold sets `claim_level` no higher than `reviewed` for any new
   entries.
3. `data/source_authority.yaml` is updated:
   - `future_authorized_usage` entry is removed or relocated to `current_imported_usage`
   - corresponding entry in `not_yet_imported` reflects the new state
4. `docs/source_authority.md` and `docs/claim_boundary.md` are updated for explicit
   ceiling text.
5. Validation passes for at least:
   - `python -X utf8 scripts/validate_source_authority.py`
   - `python -X utf8 scripts/validate_hid_class_request_matrix.py`
   - `python -X utf8 scripts/validate_verification_status.py`
   - `python -m unittest discover -s tests`
6. `HID-EXT-2` `status` can transition from `scaffold` to `reviewed` only with
   recorded human checkpoint approval.

## Hard no-go clauses

- No firmware behavior claims.
- No OS/input stack claims.
- No report parser runtime behavior claims.
- No claim-level uplift to `verified` without evidence packet closure.
