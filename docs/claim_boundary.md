# Claim Boundary

This repo is a USB HID spec reference layer.

## Current Claim Ceiling

At the current stage, the repo may claim:

- HID reference repo governed subset exists.
- Repo-local governance boundary exists.
- HID class request identity surface is verified for the current imported
  subset.
- HID descriptor field identity surface is verified for the current imported
  subset.
- HID report descriptor item type identity surface is verified for the current
  imported subset.
- Visible zh/en reference pages describe the current governed subset status.

The repo must not claim:

- HID spec coverage is complete.
- HID request behavior is fully verified beyond identity-level source binding.
- HID report descriptor item semantics are verified or complete.
- HID firmware handler correctness is verified.
- OS HID input stack behavior is covered.
- HID Usage Tables are covered.
- Report payload semantics are covered.
- Parser/runtime behavior is covered.

## Claim Level Meanings

| Claim level | Meaning |
|---|---|
| `scaffold` | Entry exists as a reference placeholder with basic identity fields. |
| `review_required` | Entry has enough structure for review but has not been accepted. |
| `reviewed` | Entry has passed repo-local review but is not evidence-backed verified. |
| `verified` | Entry has source-traceable evidence and an accepted evidence packet. |

## Verified Promotion Gate

A `reviewed` entry may not become `verified` until the evidence packet schema
and Level 3 gate are satisfied. The current imported subset has passed this
gate for identity-level entries only.

Required references:

- `contract/evidence_packet_schema.yaml`
- `docs/evidence_packet_schema.md`
- `scripts/validate_evidence_packet_schema.py`

Candidate or shell artifacts under `docs/evidence/` do not satisfy this gate
unless they are paired with accepted packets and validator-passing governed
matrix status.

## Firmware Boundary

Consuming firmware repos may use this repo as standard-side reference input.
They must not treat this repo as project-specific implementation truth.
