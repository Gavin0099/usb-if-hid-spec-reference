# HID Report Descriptor Items

## Page Purpose

Provide an identity-level scaffold for USB HID 1.11 Section 6.2.2 report
descriptor item structure.

## Governed Matrix

Machine-readable source:

- `data/hid_report_descriptor_items_matrix.yaml`

## Item Shell Summary

| Item shell | Role | Claim level | Evidence status |
|---|---|---:|---|
| `short_item_prefix` | Short item prefix identity, including item-size/type/tag prefix role only. | reviewed | not_verified |
| `long_item_prefix` | Long item prefix identity for extended item framing only. | reviewed | not_verified |
| `main_item_type` | Main item type identity category only. | reviewed | not_verified |
| `global_item_type` | Global item type identity category only. | reviewed | not_verified |
| `local_item_type` | Local item type identity category only. | reviewed | not_verified |
| `reserved_item_type` | Reserved item type identity category only, with no behavior assigned. | reviewed | not_verified |

## Reviewed Identity Notes

- `short_item_prefix` and `long_item_prefix` are recorded as framing identities,
  not parser behavior.
- `main_item_type`, `global_item_type`, and `local_item_type` are recorded as
  item type categories only.
- `reserved_item_type` is recorded only as an identity category; this repo does
  not assign behavior to reserved item types.

## Scope and Boundary

This page records report descriptor item identity shells only.

- It does not claim parser behavior.
- It does not claim report payload semantics.
- It does not claim firmware report descriptor parsing behavior.
- It does not claim host stack behavior.
- It does not claim Main / Global / Local item semantics beyond identity shell.

## Source Reference

- HID Specification 1.11, Section 6.2.2
- `https://www.usb.org/sites/default/files/documents/hid1_11.pdf`

## Non-claims

- This page does not claim HID report descriptor semantic completeness.
- This page does not claim any evidence-backed verified promotion.
- This page does not claim implementation, runtime, or parser correctness.
