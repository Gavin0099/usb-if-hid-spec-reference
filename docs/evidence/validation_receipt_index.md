# HID Validation Receipt Index

> Status: validation receipt index only
> Authority ceiling: validation_receipt_index_only

## Summary

- result: PASS
- checked commands: 16
- pass count: 16
- fail count: 0
- receipt directory: `evidence/validation_receipts/hid_current_gate`

## Receipts

| Receipt | Result | Claim ceiling | Path |
|---|---|---|---|
| `source_authority` | PASS | `source_authority_structural_validation_only` | `evidence/validation_receipts/hid_current_gate/source_authority.json` |
| `source_registry` | PASS | `structural_registry_validation_only` | `evidence/validation_receipts/hid_current_gate/source_registry.json` |
| `contract_files` | PASS | `contract_structural_consistency_only` | `evidence/validation_receipts/hid_current_gate/contract_files.json` |
| `hid_class_request_matrix` | PASS | `matrix_identity_validation_only` | `evidence/validation_receipts/hid_current_gate/hid_class_request_matrix.json` |
| `hid_descriptor_fields_matrix` | PASS | `matrix_identity_validation_only` | `evidence/validation_receipts/hid_current_gate/hid_descriptor_fields_matrix.json` |
| `hid_report_descriptor_items_matrix` | PASS | `matrix_identity_validation_only` | `evidence/validation_receipts/hid_current_gate/hid_report_descriptor_items_matrix.json` |
| `verification_status` | PASS | `verification_status_count_consistency_only` | `evidence/validation_receipts/hid_current_gate/verification_status.json` |
| `evidence_packet_schema` | PASS | `verified_preflight_contract_only` | `evidence/validation_receipts/hid_current_gate/evidence_packet_schema.json` |
| `accepted_packet_proposals` | PASS | `accepted_packet_proposal_validation_only` | `evidence/validation_receipts/hid_current_gate/accepted_packet_proposals.json` |
| `accepted_packet_proposal_summary` | PASS | `accepted_packet_proposal_summary_only` | `evidence/validation_receipts/hid_current_gate/accepted_packet_proposal_summary.json` |
| `preapproval_readiness_summary` | PASS | `preapproval_readiness_summary_only` | `evidence/validation_receipts/hid_current_gate/preapproval_readiness_summary.json` |
| `hid_governed_surface_manifest` | PASS | `manifest_structural_integrity_only` | `evidence/validation_receipts/hid_current_gate/hid_governed_surface_manifest.json` |
| `table_fingerprint` | PASS | `table_content_fingerprint_drift_only` | `evidence/validation_receipts/hid_current_gate/table_fingerprint.json` |
| `memory_records` | PASS | `memory_record_structural_visibility_only` | `evidence/validation_receipts/hid_current_gate/memory_records.json` |
| `validation_receipt_index` | PASS | `validation_receipt_index_integrity_only` | `evidence/validation_receipts/hid_current_gate/validation_receipt_index.json` |
| `unit_tests` | PASS | `regression_test_result_only` | `evidence/validation_receipts/hid_current_gate/unit_tests.json` |

## Claim Ceiling

- validation receipt index only
- no new source authority import
- no matrix semantic change
- no verified uplift by receipt index
- no firmware behavior claim

## Not Claimed

- full HID spec coverage
- HID Usage Tables coverage
- report descriptor semantic completeness
- report payload semantics
- firmware behavior correctness
- OS input stack behavior
- parser/runtime behavior
- product-specific HID behavior
