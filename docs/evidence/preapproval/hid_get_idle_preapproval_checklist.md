# HID Accepted Packet Pre-Approval Checklist

> Status: gap report only
> Authority ceiling: accepted_preapproval_gap_report_only

- Candidate: `docs/evidence/candidates/hid_get_idle_candidate.yaml`
- Future accepted packet path: `docs/evidence/accepted/hid_get_idle_accepted.yaml`
- Production accepted packet created: no
- Verified uplift: no

## Governed Entry

- matrix: `hid_class_request_matrix`
- entry_id: `hid_get_idle`
- current_claim_level: `reviewed`
- current_evidence_status: `not_introduced`

## Source Trace

- source_id: `hid_1_11`
- source_section: `7.2`

## Ready Checks

- candidate packet status is candidate
- candidate packet is marked review_level 3
- candidate packet targets verified claim level for future review
- candidate approval is still pending as expected
- validation command present: source_authority_validator
- validation command present: matrix_validator
- validation command present: verification_status_validator
- validation command present: evidence_packet_validator
- validation command present: unit_tests
- non-claim preserved: firmware_implementation_correctness
- non-claim preserved: os_input_stack_behavior
- non-claim preserved: parser_runtime_behavior
- non-claim preserved: product_specific_hid_behavior
- governed matrix binding is present
- source trace binding is present
- future accepted packet directory is docs/evidence/accepted

## Gaps Before Accepted Packet

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

- preapproval_checklist_only
- no_production_accepted_packet
- no_verified_uplift

## Not Claimed

- no accepted evidence packet exists from this report
- no HID entry is verified
- no firmware behavior correctness
- no OS input stack behavior
- no parser runtime behavior
