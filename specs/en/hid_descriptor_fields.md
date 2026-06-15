# HID Descriptor Fields

## Page Purpose

Provide an identity-level scaffold for USB HID 1.11 §6.2.1 descriptor fields.

## Governed Matrix

Machine-readable source:

- `data/hid_descriptor_fields_matrix.yaml`

## Field Summary

| Field | Meaning | Claim level |
|---|---|---:|
| `bLength` | Total descriptor length in bytes. | scaffold |
| `bDescriptorType` | Descriptor type identifier. | scaffold |
| `bcdHID` | HID specification release version value. | scaffold |
| `bCountryCode` | Hardware country code field. | scaffold |
| `bNumDescriptors` | Number of subordinate descriptor entries. | scaffold |
| `bDescriptorType_subordinate` | Descriptor type in each subordinate descriptor entry. | scaffold |
| `wDescriptorLength` | Descriptor length for each subordinate descriptor entry. | scaffold |

## Scope and Boundary

This page records identity-level field scaffold only.
It does not model parser behavior, implementation details, or variable-length expansion as an authoritative contract.

## Relationship Notes

- `bNumDescriptors` is the count field for subordinate descriptor elements.
- `bDescriptorType_subordinate` and `wDescriptorLength` are the paired fields for each subordinate descriptor entry.
- The variable-length list semantics are deliberately kept as scaffold-level description to avoid overclaiming parser behavior.

## Source Reference

- HID Specification 1.11, section 6.2.1
- `https://www.usb.org/sites/default/files/documents/hid1_11.pdf`

The fields remain scaffold-only and are not evidence-backed verified entries.

## Non-claims

- This page does not claim parser correctness.
- This page does not claim firmware descriptor parsing behavior.
- This page does not claim report descriptor semantics.
- This page does not claim any evidence-backed verified promotion.
