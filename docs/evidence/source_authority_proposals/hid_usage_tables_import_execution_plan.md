# HID Usage Tables Source Authority Import Execution Plan

> Status: proposal only
> Authority ceiling: source_authority_import_execution_plan_only

This plan defines the first allowed post-approval source-authority import slice
for HID Usage Tables. It is not the import itself.

## Source

- source_id: `hid_usage_tables`
- current status: `not_imported`
- proposed next transition: Level 3 source-authority import approval

## First Slice Scope

Allowed first-slice files after explicit Level 3 approval:

- `data/source_authority.yaml`
- `evidence/source_registry.yaml`
- `docs/source_authority.md`
- `docs/claim_boundary.md`
- `governance/hid_work_queue.yaml`
- `docs/hid_long_running_roadmap.md`
- `docs/hid_long_running_checkpoint_rollup.md`
- `memory/2026-06-23.md`

Forbidden in the first source-authority import slice:

- Usage Tables governed matrix creation
- Usage Tables governed entries
- report payload semantics
- parser/runtime behavior
- firmware behavior correctness
- OS input stack behavior
- product-specific HID behavior
- verified uplift

## Required Level 3 Inputs

- human approval record
- approver identity
- checkpoint commit
- validation receipt
- selected Usage Tables publication/version identity
- selected imported scope
- selected excluded scope

## Non-Claims

- no direct source authority import in this plan
- no Usage Tables governed entries in this plan
- no Usage Tables coverage claim in this plan
- no verified uplift in this plan
