# HID Report Descriptor Items

## Page Purpose

Prepare an import-prep identity shell for USB HID 1.11 Section 6.2.2 report
descriptor item structure.

This page is not a current imported source surface. It exists to make the next
source-authority import checkpoint reviewable before `6.2.2` is moved into
`current_imported_usage`.

## Import-Prep Matrix

Machine-readable source:

- `data/hid_report_descriptor_items_matrix.yaml`

## Item Shell Summary

| Item shell | Role | Claim level | Evidence status |
|---|---|---:|---|
| `short_item_prefix` | Short item prefix identity shell. | scaffold | not_imported |
| `long_item_prefix` | Long item prefix identity shell. | scaffold | not_imported |
| `main_item_type` | Main item type identity shell. | scaffold | not_imported |
| `global_item_type` | Global item type identity shell. | scaffold | not_imported |
| `local_item_type` | Local item type identity shell. | scaffold | not_imported |
| `reserved_item_type` | Reserved item type identity shell. | scaffold | not_imported |

## Scope and Boundary

This page records report descriptor item identity shells only.

- It does not claim parser behavior.
- It does not claim report payload semantics.
- It does not claim firmware report descriptor parsing behavior.
- It does not claim host stack behavior.
- It does not move `6.2.2` into current imported usage.

## Source Reference

- HID Specification 1.11, Section 6.2.2
- `https://www.usb.org/sites/default/files/documents/hid1_11.pdf`

## Non-claims

- This page does not claim HID report descriptor semantic completeness.
- This page does not claim any evidence-backed verified promotion.
- This page does not claim implementation, runtime, or parser correctness.
