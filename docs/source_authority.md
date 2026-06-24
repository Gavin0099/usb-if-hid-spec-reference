# Source Authority

This document fixes the current HID specification authority boundary for this
repo.

Machine-readable source:

- `data/source_authority.yaml`

## Primary Source

| Source | Version | Publisher | Current usage |
|---|---|---|---|
| Device Class Definition for Human Interface Devices (HID) | 1.11 | USB Implementers Forum | Section 7.2 Class-Specific Requests, Section 6.2.1 HID Descriptor, and Section 6.2.2 Report Descriptor item type identities are the current imported governed subset. |

Primary source URL:

- `https://www.usb.org/sites/default/files/documents/hid1_11.pdf`

## Currently Imported Usage

| Section | Topic | Status | Surface |
|---|---|---|---|
| 7.2 | Class-Specific Requests | imported governed subset | `data/hid_class_request_matrix.yaml` |
| 6.2.1 | HID Descriptor | imported governed subset | `data/hid_descriptor_fields_matrix.yaml` |
| 6.2.2 | Report Descriptor item type identities | imported governed subset | `data/hid_report_descriptor_items_matrix.yaml` |

## Future Authorized Usage

No additional future authorized usage is registered yet.

## Not Yet Imported

| Source area | Status |
|---|---|
| Report descriptor Main / Global / Local item semantics | not imported |
| HID Usage Tables | not imported |

## Secondary Sources

| Source | Role | Status |
|---|---|---|
| HID Usage Tables | secondary | not imported |

Secondary sources may not be cited as authority until
`data/source_authority.yaml` is updated and reviewed.

## Explicitly Excluded

| Excluded area | Reason |
|---|---|
| HID over I2C | Not USB HID core reference scope |
| OS input stack behavior | Host OS behavior is outside this reference repo |
| Firmware handler correctness | Implementation behavior belongs to consuming firmware repos |
| Hub class behavior | Belongs to `usb-if-hub-spec-reference` |
| Report payload semantics beyond identity-level scaffold | Requires a separate governed surface and evidence boundary |

## Import Rule

Agents must not cite or import additional HID/USB documents as authority until
they are registered in `data/source_authority.yaml`.

Registering a source does not promote any HID entry to `verified`.

## Non-claims

- This repo does not claim full HID spec coverage.
- This repo does not claim HID Usage Tables coverage.
- This repo does not claim HID descriptor behavior is verified beyond
  identity-level source binding.
- This repo does not claim HID request behavior is verified beyond
  identity-level source binding.
- This repo does not claim report descriptor parser/runtime semantics.
- This repo does not claim firmware implementation correctness.
