# HID Verified Evidence Packet Schema

This document defines the preflight contract for a future `reviewed` to
`verified` promotion. It does not promote any current HID entry to `verified`.

Machine-readable schema:

- `contract/evidence_packet_schema.yaml`

Validator:

- `scripts/validate_evidence_packet_schema.py`

## Packet Lifecycle

| Status | Meaning | May promote to `verified` |
|---|---|---|
| `shell` | Navigation or draft evidence shell exists. | No |
| `candidate` | Evidence packet is complete enough for Level 3 review. | No |
| `accepted` | Human-approved packet with passing validation. | Yes, in a separate Level 3 promotion slice |
| `rejected` | Packet was reviewed and rejected. | No |

## Required Packet Sections

A future verified evidence packet must include:

- `packet_identity`
- `governed_entry_binding`
- `source_trace`
- `claim_delta`
- `evidence_body`
- `non_claims`
- `validation`
- `approval`
- `residual_risk`

## Verified Gate

Before any governed entry may change to `claim_level: verified`, all of these
conditions must be true:

- The evidence packet status is `accepted`.
- The work is classified as Level 3.
- Human approval is recorded in the packet or checkpoint.
- The source is already registered in `data/source_authority.yaml`.
- The packet binds to one governed matrix entry.
- Required validators pass, including the evidence packet schema validator.
- The packet explicitly preserves non-claims for firmware implementation
  correctness, OS input stack behavior, parser/runtime behavior unless
  separately scoped, and product-specific HID behavior.

## Accepted Packet Workflow

Accepted packets are Level 3 artifacts. A packet may not move from `candidate`
to `accepted` unless all of these are recorded:

- Previous status was `candidate`.
- `approval_record` is `approved`.
- `approver` identifies a human approval record.
- A checkpoint commit exists.
- A validation receipt exists.
- The checkpoint is explicitly marked Level 3.
- The accepted packet still preserves all required non-claims.

This workflow only accepts an evidence packet. A later and separate Level 3
promotion slice is still required before any governed matrix entry can become
`verified`.

## Current Shell Packet Boundary

Existing files under `docs/evidence/` are shell artifacts. They are useful for
review navigation and claim-boundary planning, but they do not satisfy the
verified gate.

## Candidate Packet Location

Candidate packets live under:

- `docs/evidence/candidates/`

Candidate packets are complete enough for Level 3 review preparation, but they
still do not satisfy the verified gate because their approval record remains
pending and their status is not `accepted`.

Each candidate packet must bind `source_trace.source_id` and
`source_trace.source_section` to a current imported usage entry in
`data/source_authority.yaml`. Textual source claims are not sufficient unless the
machine-readable binding is valid.

The same `source_trace` pair must also match the `source_refs` declared by the
candidate packet's bound governed matrix. This prevents candidate packets from
claiming one source while the matrix points at a different source ID or section.

Current candidate packets:

- `docs/evidence/candidates/hid_get_report_candidate.yaml`
- `docs/evidence/candidates/hid_set_report_candidate.yaml`
- `docs/evidence/candidates/hid_get_idle_candidate.yaml`
- `docs/evidence/candidates/hid_set_idle_candidate.yaml`
- `docs/evidence/candidates/hid_get_protocol_candidate.yaml`
- `docs/evidence/candidates/hid_set_protocol_candidate.yaml`
- `docs/evidence/candidates/hid_bLength_candidate.yaml`
- `docs/evidence/candidates/hid_bDescriptorType_candidate.yaml`
- `docs/evidence/candidates/hid_bcdHID_candidate.yaml`
- `docs/evidence/candidates/hid_bCountryCode_candidate.yaml`
- `docs/evidence/candidates/hid_bNumDescriptors_candidate.yaml`
- `docs/evidence/candidates/hid_bDescriptorType_subordinate_candidate.yaml`
- `docs/evidence/candidates/hid_wDescriptorLength_candidate.yaml`
- `docs/evidence/candidates/report_descriptor_short_item_prefix_candidate.yaml`
- `docs/evidence/candidates/report_descriptor_long_item_prefix_candidate.yaml`
- `docs/evidence/candidates/report_descriptor_main_item_type_candidate.yaml`
- `docs/evidence/candidates/report_descriptor_global_item_type_candidate.yaml`
- `docs/evidence/candidates/report_descriptor_local_item_type_candidate.yaml`
- `docs/evidence/candidates/report_descriptor_reserved_item_type_candidate.yaml`

## Non-Claims

This schema does not claim:

- any HID entry is verified
- any evidence packet has been accepted
- any firmware behavior is correct
- any OS input stack behavior is covered
- any parser or runtime behavior is verified
