# USB-IF HID Spec Reference

Read-only USB HID specification reference layer for consuming firmware
repositories.

This repository is intentionally separate from
`usb-if-hub-spec-reference`. HID is a USB class reference surface, not a Hub
class sub-surface.

## Current Status

- Canonical visible reference surface: `specs/` and `specs/en/`
- Initial focus: HID class request scaffold
- Tracked entries: 6
- Scaffold entries: 6
- Verified entries: 0
- Reviewed entries: 0
- Inferred entries: 0

## Scope

This repo may cover:

- HID descriptors
- HID report descriptors
- HID report types and item semantics
- HID class requests
- Boot protocol, report protocol, and idle-rate semantics
- Claim boundary and evidence tracking

## Source Authority

Current primary source:

- Device Class Definition for Human Interface Devices (HID), Version 1.11
- Publisher: USB Implementers Forum
- URL: `https://www.usb.org/sites/default/files/documents/hid1_11.pdf`
- Current imported usage: Section 7.2 Class-Specific Requests scaffold only
- Future authorized usage: Section 6.2.1 HID Descriptor is authorized but not imported

Source authority is registered in:

- `data/source_authority.yaml`
- `docs/source_authority.md`

This repo does not cover:

- Hub class behavior
- Firmware implementation truth
- Product-specific HID policy
- OS input stack behavior unless explicitly sourced

## Claim Boundary

Until evidence packets and reviewed/verified governed tables are introduced,
all content in this repo is scaffold or orientation-level reference material
only.

No verified HID entries are claimed yet.

## Reference Entry Points

- `specs/hid_scope.md`
- `specs/hid_class_requests.md`
- `specs/verification_status.md`
- `docs/claim_boundary.md`
- `docs/source_authority.md`
