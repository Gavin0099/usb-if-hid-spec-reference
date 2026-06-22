# HID Descriptor Fields

## Page Purpose

Provide an identity-level scaffold for USB HID 1.11 Section 6.2.1 descriptor fields.

## Governed Matrix

Machine-readable source:

- `data/hid_descriptor_fields_matrix.yaml`

## Field Summary

| Field | Meaning | Claim level |
|---|---|---:|
| `bLength` | HID descriptor total-length identity field. | reviewed |
| `bDescriptorType` | HID descriptor type-code identity field. | reviewed |
| `bcdHID` | HID class specification release identity field. | reviewed |
| `bCountryCode` | Hardware country-code identity field. | reviewed |
| `bNumDescriptors` | Subordinate descriptor entry-count identity field. | reviewed |
| `bDescriptorType_subordinate` | Descriptor type identity field for each subordinate descriptor entry. | reviewed |
| `wDescriptorLength` | Descriptor length identity field for each subordinate descriptor entry. | reviewed |

## Scope and Boundary

This page records identity-level field intent only.

- It does not claim parser behavior.
- It does not claim firmware descriptor parsing behavior.
- It does not claim host stack semantics.
- It does not claim report descriptor semantics.
- It does not claim runtime transport, framing, or timing semantics.

## Identity Conventions

- Scope is field-name identity and type intent only.
- Numeric semantics are intentionally limited to reviewed identity wording.
- This page and matrix are not a behavioral spec.

## Reviewed Identity Notes

- `bLength`, `bDescriptorType`, `bcdHID`, `bCountryCode`, and
  `bNumDescriptors` are recorded as HID descriptor identity fields only.
- `bDescriptorType_subordinate` and `wDescriptorLength` are recorded as the
  identity fields for subordinate descriptor entries.
- The reviewed state means repo-local wording review only; it does not verify
  parser behavior or runtime descriptor handling.

## Relationship Notes

- `bNumDescriptors` is the entry count for subordinate descriptor elements.
- Each subordinate descriptor element is described by a pair: `bDescriptorType_subordinate` and `wDescriptorLength`.
- `wDescriptorLength` remains identity-level and does not imply runtime parsing behavior.

## Source Reference

- HID Specification 1.11, Section 6.2.1
- `https://www.usb.org/sites/default/files/documents/hid1_11.pdf`

The fields remain identity-level reviewed entries and are not evidence-backed
verified entries.

## Non-claims

- This page does not claim parser correctness.
- This page does not claim firmware descriptor parsing behavior.
- This page does not claim report descriptor semantics.
- This page does not claim any evidence-backed verified promotion.
