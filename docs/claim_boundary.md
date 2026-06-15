# Claim Boundary

This repo is a USB HID spec reference layer.

## Current Claim Ceiling

At the current stage, the repo may claim:

- HID reference repo scaffold exists.
- Repo-local governance boundary exists.
- HID class request identity scaffold exists.
- Visible zh/en reference pages describe scaffold status.

The repo must not claim:

- HID spec coverage is complete.
- HID request behavior is fully verified.
- HID firmware handler correctness is verified.
- OS HID input stack behavior is covered.
- Any HID entry has evidence-backed verified promotion.

## Claim Level Meanings

| Claim level | Meaning |
|---|---|
| `scaffold` | Entry exists as a reference placeholder with basic identity fields. |
| `review_required` | Entry has enough structure for review but has not been accepted. |
| `reviewed` | Entry has passed repo-local review but is not evidence-backed verified. |
| `verified` | Entry has source-traceable evidence and an accepted evidence packet. |

## Firmware Boundary

Consuming firmware repos may use this repo as standard-side reference input.
They must not treat this repo as project-specific implementation truth.
