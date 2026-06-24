# Usage Type Identity Matrix Proposal

> Status: proposal only
> Authority ceiling: usage_tables_matrix_schema_proposal_only

This proposal defines a candidate Usage type identity matrix while keeping Usage
Tables unimported and without producing a production matrix.

## Matrix Candidate

- matrix_id: `usage_type_identity_matrix`
- future path: `data/hid_usage_type_identity_matrix.yaml`
- proposed initial status: `scaffold`
- source_id: `hid_usage_tables`
- source authority required state before this proposal: `not_imported`

## Proposed Fields

- `entry_id`
- `usage_type_id`
- `usage_type_name`
- `source_id`
- `source_section`
- `status`
- `claim_level`
- `notes`

## Validator Plan

- reject `source_id` other than `hid_usage_tables`
- reject initial `status` above `scaffold`
- reject `claim_level: verified`
- reject missing `source_section`
- reject `future_matrix_path` mismatch
- reject production matrix entries before source authority import

## Negative Fixtures

- wrong `source_id`
- `claim_level: verified`
- missing `source_section`
- matrix ID/path mismatch
- production matrix exists while source authority remains `not_imported`

## Non-Claims

- no Usage Tables source authority import in this proposal
- no Usage Tables matrix exists in this proposal
- no Usage Tables entries are tracked in this proposal
- no Usage Tables coverage claim in this proposal
- no verified uplift in this proposal
- no report payload semantics in this proposal
