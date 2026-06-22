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

## Current Shell Packet Boundary

Existing files under `docs/evidence/` are shell artifacts. They are useful for
review navigation and claim-boundary planning, but they do not satisfy the
verified gate.

## Non-Claims

This schema does not claim:

- any HID entry is verified
- any evidence packet has been accepted
- any firmware behavior is correct
- any OS input stack behavior is covered
- any parser or runtime behavior is verified
