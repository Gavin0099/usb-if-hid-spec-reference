# HID Long-Running Agent Contract (LRA)

> Version: 1.2.0
> Established: 2026-06-18
> Scope: `usb-if-hid-spec-reference` repository
> Claim ceiling: `scaffold_identity_reference_only`

This contract defines how Codex may perform sustained work on this HID reference
repo without broadening scope or accidentally creating verified claims.

## Scope

- Docs-only execution for repo-local governance scaffolding.
- No firmware policy statements.
- No OS/input-stack behavior claims.
- No parser runtime behavior claims.
- No source-authority expansion.
- No verification count changes (`verified`, `reviewed`, `inferred`) unless explicitly
  approved.
- No HID semantic completion beyond imported scope.

## Review Levels

- Level 1 (Auto-pass): roadmap/queue/evidence-shell/navigation/residual claim
  ceiling cleanup tasks. These tasks do not claim HID behavior and do not modify
  review state.
- Level 2 (Quick human checkpoint): reviewed-draft preparation for HID request
  content (for example, GET_REPORT field wording). Human review is required to
  verify:
  1) commit exists,
  2) required validation ran and passed,
  3) reviewed/verified counts unchanged,
  4) no firmware/OS/parser behavior claim was added,
  5) no shell artifact was promoted to verified truth.
- Level 3 (Human approval): reviewed/verified uplift, source imports, new governed
  matrix, HID Descriptor scope import, and Report Descriptor / Usage Table semantic
  additions.

## Allowed Autonomous Work

- specs/docs cleanup and consistency passes.
- scaffold wording normalization (identity-level language only).
- evidence packet shell scaffolding documentation.
- validator receipt documentation updates.
- zh/en page pair consistency checks for already-scaffolded pages.
- residual boundary/reviewability reports.

## Work Requiring Human Approval

Codex must stop and wait for explicit human approval for:

- status transitions from `scaffold` to `reviewed`.
- status transitions from `reviewed` to `verified`.
- adding a new governed matrix.
- changing verification/review counts.
- adding source authority imports.
- any HID report descriptor semantic interpretation.
- any claim that implies firmware correctness, host stack behavior, or parser/runtime behavior.

## Forbidden Claims

While operating under this contract, Codex must not assert:

- firmware implementation correctness.
- OS input-stack semantics.
- product-specific HID policy.
- report descriptor parser behavior.
- HID Usage Table semantic correctness.
- `"verified"` status for any entry unless evidence packets and review gates are
  explicitly satisfied.

## PR-based Checkpoint Gate (Level 2/3)

For Level 2 and Level 3 slices, Codex must follow branch + PR checkpoint flow:

1. Create branch: `agent/<item-id>-<short-description>`
   - Example: `agent/hid-req-5-get-protocol`
2. Do not start the next slice on `main`.
3. Commit checkpoint changes on the branch.
4. Open PR with title:
   - `HID-REQ-<N>: <request> reviewed draft preparation`
5. Stop and wait for approval before starting the next slice.
6. PR body must include:
   - Commit
   - Scope
   - Changed files
   - Validation
   - Stats before/after
   - Review level
   - Can claim
   - Cannot claim
   - Residual risk
   - Requested approval

## Checkpoint Gate

Every slice must satisfy this gate before the next slice starts:

1. Commit created.
2. Required validation ran and passed.
3. For Level 2/3, PR checkpoint exists and references the required fields.
4. Checkpoint block recorded in exact required format.
5. Review level classification appended.
6. Reviewed/verified count changes are explicitly approved by level.

If any point is missing, codex must stop and wait.

Level 1 fast lane exception:

- Level 1 may continue autonomously when validation passes and reviewed/verified
  counts remain unchanged.
- Level 1 does not require PR creation for autonomous continuation.

## Commit Checkpoint Format

Each completed slice under this contract must record a checkpoint in this exact
shape:

```text
Commit Checkpoint:
Commit:
Scope:
Changed files:
Validation:
Stats before/after:
Review level:
Can claim:
Cannot claim:
Residual risk:
Next recommended slice:
```

For this repo baseline, the checkpoint should also restate:

- claim ceiling remains `scaffold_identity_reference_only`.
- no change to tracked/reviewed/verified/inferred counts unless explicitly approved.

## Required Validation Format

Before handing over to the next executor, run the repository validators in the
project standard order and report the observed PASS/FAIL result format:

```powershell
python -X utf8 scripts\validate_source_authority.py
python -X utf8 scripts\validate_hid_class_request_matrix.py
python -X utf8 scripts\validate_verification_status.py
python -m unittest discover -s tests
```

The validator block is required even if no files under validation changed in this
slice; a PASS must be explicitly recorded.

## Long-Running Task Queue Rules

- Only one `in_progress` item may be active in `governance/hid_work_queue.yaml`.
- Human-gated items must have `requires_human_approval: true`.
- Codex may execute only items marked allowed for autonomous work.
- Any item changing status semantics requires approval.
- Queue updates must keep item history append-only and do not alter task IDs.

## Commit / Branch Discipline

- Use short, intentful commit titles with `HID-LRA-<N>` tags.
- Level 1: commit directly.
- Level 2/3: commit on branch `agent/<item-id>-<short-description>`, then PR.
- A commit may include docs-only files plus linked checkpoint artifacts.
- Do not commit if any required validator fails.

## Stop Conditions

- scope ambiguity is detected.
- evidence packet claim is requested without approved source scope.
- a user asks to add behavior-level claims.
- any instruction conflicts with `docs/source_authority.md` or `docs/claim_boundary.md`.
