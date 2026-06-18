# HID Descriptor Fields

## Page Purpose

Provide an identity-level scaffold for USB HID 1.11 Section 6.2.1 descriptor fields.

## Governed Matrix

Machine-readable source:

- `data/hid_descriptor_fields_matrix.yaml`

## Field Summary

| Field | Meaning | Claim level |
|---|---|---:|
| `bLength` | Total descriptor length in bytes. | scaffold |
| `bDescriptorType` | Descriptor type identifier. | scaffold |
| `bcdHID` | HID specification release value (BCD-encoded identity field). | scaffold |
| `bCountryCode` | Hardware country code field. | scaffold |
| `bNumDescriptors` | Number of subordinate descriptor entries. | scaffold |
| `bDescriptorType_subordinate` | Descriptor type for each subordinate descriptor entry. | scaffold |
| `wDescriptorLength` | Descriptor length for each subordinate descriptor entry payload. | scaffold |

## Scope and Boundary

This page records identity-level field intent only.

- It does not claim parser behavior.
- It does not claim firmware descriptor parsing behavior.
- It does not claim host stack semantics.
- It does not claim report descriptor semantics.

## Relationship Notes

- `bNumDescriptors` is the entry count for subordinate descriptor elements.
- Each subordinate descriptor element is described by a pair: `bDescriptorType_subordinate` and `wDescriptorLength`.
- `wDescriptorLength` remains identity-level and does not imply runtime parsing behavior.

## Source Reference

- HID Specification 1.11, Section 6.2.1
- `https://www.usb.org/sites/default/files/documents/hid1_11.pdf`

The fields remain scaffold-only and are not evidence-backed verified entries.

## Non-claims

- This page does not claim parser correctness.
- This page does not claim firmware descriptor parsing behavior.
- This page does not claim report descriptor semantics.
- This page does not claim any evidence-backed verified promotion.
