# HID Accepted Packet Proposal

> Status: proposal only
> Authority ceiling: accepted_packet_proposal_only

- Candidate: `docs/evidence/candidates/hid_get_report_candidate.yaml`
- Pre-approval report: `docs/evidence/preapproval/hid_get_report_preapproval_checklist.md`
- Future accepted packet path: `docs/evidence/accepted/hid_get_report_accepted.yaml`
- Production accepted packet created: no
- Verified uplift: no

## Governed Entry

- matrix: `hid_class_request_matrix`
- entry_id: `hid_get_report`
- current_claim_level: `reviewed`
- current_evidence_status: `not_introduced`

## Required Level 3 Acceptance Gate

- previous_packet_status: `candidate`
- checkpoint_commit: `TBD_LEVEL3_ACCEPTED_PACKET_COMMIT`
- validation_receipt: `TBD_LEVEL3_VALIDATION_RECEIPT`
- level3_checkpoint: `true`
- direct_promotion: `false`

## Required Approval

- approval_record: `approved`
- approver: `TBD_HUMAN_APPROVER`
- requested_approval: `Level 3 approval for accepted packet status only`

## Required Validators

- `python -X utf8 scripts/validate_source_authority.py`
- `python -X utf8 scripts/validate_evidence_packet_schema.py`
- `python -X utf8 scripts/validate_hid_governed_surface_manifest.py`
- `python -X utf8 scripts/validate_hid_class_request_matrix.py`
- `python -X utf8 scripts/validate_hid_descriptor_fields_matrix.py`
- `python -X utf8 scripts/validate_hid_report_descriptor_items_matrix.py`
- `python -X utf8 scripts/validate_verification_status.py`
- `python -X utf8 scripts/probe_table_fingerprint.py --mode check --manifest exports/hid_governed_surface_manifest.yaml --baseline-in evidence/table_fingerprint_baseline.jsonl`
- `python -m unittest discover -s tests`

## Remaining Gaps

- future accepted packet must add acceptance_gate.previous_packet_status
- future accepted packet must add acceptance_gate.checkpoint_commit
- future accepted packet must add acceptance_gate.validation_receipt
- future accepted packet must add acceptance_gate.level3_checkpoint
- future accepted packet must add acceptance_gate.direct_promotion
- human approver must be recorded before acceptance
- approval_record must change to approved only in the accepted packet
- checkpoint_commit must reference the accepted-packet checkpoint commit
- validation_receipt must reference a durable receipt for the accepted-packet checkpoint
- level3_checkpoint must be true only after Level 3 approval
- direct_promotion must be false
- accepted packet file must be reviewed before any later verified promotion slice

## Claim Ceiling

- accepted_packet_proposal_only
- no_production_accepted_packet
- no_verified_uplift

## Not Claimed

- no accepted evidence packet exists from this proposal
- no HID entry is verified by this proposal
- no firmware behavior correctness
- no OS input stack behavior
- no parser runtime behavior
- no product-specific HID behavior
