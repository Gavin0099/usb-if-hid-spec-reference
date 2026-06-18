# Memory Authority Contract

Repo-local adoption: warning/reporting convention only.

Source baseline: `ai-governance-framework` memory authority guidance at
observed upstream `main` short commit `65b3388`.

Baseline version: 1.0.0.

## Purpose

This contract defines when a memory entry may be treated as useful project
record in this HID reference repo.

Presence under `memory/` improves cross-session visibility, but it does not by
itself make a claim authoritative.

Presence in `memory/` is necessary for repo-local operational visibility, but
it is not sufficient for binding authority.

## Canonical Memory Boundary

- Operational records must stay under `memory/`.
- External private memory is not canonical for this repo.
- Non-closeout phases should not write memory records unless explicitly scoped.
- Memory records must not introduce HID semantic claims that are absent from
  governed specs, tables, or evidence.

## Session-Derived Memory

Daily files such as `memory/YYYY-MM-DD.md` should include:

- `session_id`
- changed files or surfaces
- validation performed
- claim ceiling
- commit hash when a commit exists

An uncommitted or unanchored memory entry is a session note, not a binding
authority.

Binding requirement for a session-derived entry:

- `commit hash: <5-40 hex chars>`, or
- `session_id: <explicit session identifier>`

`commit hash: pending` is not binding.

Violation code: `unbound_memory`.

## Structural Long-Term Memory

If `memory/00_long_term.md` exists, each `##`-level section should carry a
`promoted_by:` marker identifying the human reviewer or promotion artifact that
authorized the entry.

Sections without `promoted_by:` are structural notes, not binding governance
authority.

Violation code: `structural_memory_auto_write`.

## Private Memory Boundary

Private tool memory outside this repo is not canonical for this HID reference
repo.

Closeouts or governance artifacts must not cite private tool memory paths as
authority for repo-local HID claims.

Violation code: `private_memory_cited`.

## Missing Canonical Memory

If session-level work is performed and committed, but no corresponding
repo-local daily memory file exists for that date, the session record may be
incomplete.

This is a warning heuristic, not a blocking gate in this repo.

Violation code: `missing_canonical_memory`.

## Violation Semantics

| Code | Severity | Blocks | Meaning |
|---|---|---|---|
| `unbound_memory` | warning | no | Daily entry lacks commit hash and session ID |
| `structural_memory_auto_write` | info | no | Long-term section lacks promotion marker |
| `private_memory_cited` | warning | no | External private memory cited as authority |
| `missing_canonical_memory` | warning | no | Commit exists without corresponding daily memory record |

## Non-claims

This contract does not add:

- memory write enforcement
- session-end hooks
- CI gates
- automatic freshness checks
- HID verification authority
