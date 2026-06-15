# Memory Authority Contract

Repo-local adoption: warning/reporting convention only.

Source baseline: `ai-governance-framework` memory authority guidance at commit
`3221da66f30dc13c2a310d1e96084cd5e8741540`.

## Purpose

This contract defines when a memory entry may be treated as useful project
record in this HID reference repo.

Presence under `memory/` improves cross-session visibility, but it does not by
itself make a claim authoritative.

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

## Non-claims

This contract does not add:

- memory write enforcement
- session-end hooks
- CI gates
- automatic freshness checks
- HID verification authority
