# Usage Page Identity Matrix Proposal

> Status: proposal only
> Authority ceiling: usage_tables_matrix_schema_proposal_only

This proposal defines the first candidate Usage Tables matrix shape without
creating the production matrix.

## Matrix Candidate

- matrix_id: `usage_page_identity_matrix`
- future path: `data/hid_usage_page_identity_matrix.yaml`
- proposed initial status: `scaffold`
- source_id: `hid_usage_tables`
- source authority required state before this proposal: `not_imported`

## Proposed Fields

- `entry_id`
- `usage_page_id`
- `usage_page_name`
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
- reject duplicate `usage_page_id`
- reject production matrix entries before source authority import

## Negative Fixtures

- wrong `source_id`
- `claim_level: verified`
- missing `source_section`
- duplicate `usage_page_id`
- matrix present while source authority remains `not_imported`

## Non-Claims

- no Usage Tables source authority import in this proposal
- no Usage Tables matrix exists in this proposal
- no Usage Tables entries are tracked in this proposal
- no Usage Tables coverage claim in this proposal
- no verified uplift in this proposal
- no report payload semantics in this proposal
