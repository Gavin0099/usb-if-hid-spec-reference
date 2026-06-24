# HID Usage Tables Source Authority Import Proposal

> Status: proposal only
> Authority ceiling: source_authority_import_proposal_only

- Source candidate: `hid_usage_tables`
- Current source authority status: `not_imported`
- Proposed future action: Level 3 source-authority import decision
- Production source authority change created: no
- Usage Tables governed entries created: no
- Verified uplift: no

## Proposed Source Authority Change

- source_id: `hid_usage_tables`
- current_role: `secondary`
- current_status: `not_imported`
- proposed_next_status: `pending_level3_source_authority_import`
- required_approval: `Level 3 source-authority approval`

## Required Level 3 Gate

- approval_record: `TBD_LEVEL3_APPROVAL`
- approver: `TBD_HUMAN_APPROVER`
- checkpoint_commit: `TBD_LEVEL3_SOURCE_IMPORT_COMMIT`
- validation_receipt: `TBD_LEVEL3_VALIDATION_RECEIPT`
- direct_import: `false`

## Proposed First Implementation Slice After Approval

The first approved implementation slice should update source-authority metadata
only. It should not add Usage Tables governed entries.

Required scope:

- update `data/source_authority.yaml`;
- update `evidence/source_registry.yaml`;
- update `docs/source_authority.md`;
- update `docs/claim_boundary.md`;
- add candidate matrix queue entries;
- run the validation receipt index gate.

## Required Validators

- `python -X utf8 scripts/validate_source_authority.py`
- `python -X utf8 scripts/validate_source_registry.py`
- `python -X utf8 scripts/validate_validation_receipt_index.py`
- `python -X utf8 scripts/generate_validation_receipt_index.py --check-only --assert-match evidence/validation_receipt_index.json`
- `python -B -m unittest discover -s tests`

## Remaining Gaps

- Level 3 approval is not recorded.
- `data/source_authority.yaml` is not updated.
- `evidence/source_registry.yaml` is not updated.
- Usage Tables source version/publication identity is not selected.
- Imported scope is not selected.
- Excluded scope is not selected.
- Candidate Usage Tables matrices are not created.
- Usage Tables evidence packets are not created.
- Usage Tables validation receipts are not created.

## Claim Ceiling

- source_authority_import_proposal_only
- no_source_authority_import
- no_usage_tables_coverage
- no_verified_uplift

## Not Claimed

- HID Usage Tables are not imported.
- Usage Tables entries are not tracked, reviewed, or verified.
- Report payload semantics are not covered.
- Report descriptor semantic completeness is not claimed.
- Firmware behavior correctness is not claimed.
- OS input stack behavior is not claimed.
- Parser/runtime behavior is not claimed.
- Product-specific HID behavior is not claimed.
