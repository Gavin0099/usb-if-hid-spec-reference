# HID Report Descriptor Items

## 頁面目的

本頁為 USB HID 1.11 Section 6.2.2 report descriptor item structure 建立
identity-level scaffold。

## Governed Matrix

機器可讀來源：

- `data/hid_report_descriptor_items_matrix.yaml`

## Item Shell Summary

| Item shell | Role | Claim level | Evidence status |
|---|---|---:|---|
| `short_item_prefix` | Short item prefix identity shell. | scaffold | not_verified |
| `long_item_prefix` | Long item prefix identity shell. | scaffold | not_verified |
| `main_item_type` | Main item type identity shell. | scaffold | not_verified |
| `global_item_type` | Global item type identity shell. | scaffold | not_verified |
| `local_item_type` | Local item type identity shell. | scaffold | not_verified |
| `reserved_item_type` | Reserved item type identity shell. | scaffold | not_verified |

## Scope and Boundary

本頁只記錄 report descriptor item 的 identity shell。

- 不宣告 parser behavior。
- 不宣告 report payload semantics。
- 不宣告 firmware report descriptor parsing behavior。
- 不宣告 host stack behavior。
- 不宣告超出 identity shell 的 Main / Global / Local item semantics。

## Source Reference

- HID Specification 1.11, Section 6.2.2
- `https://www.usb.org/sites/default/files/documents/hid1_11.pdf`

## Non-claims

- 本頁不宣告 HID report descriptor semantic completeness。
- 本頁不宣告任何 evidence-backed verified promotion。
- 本頁不宣告 implementation、runtime 或 parser correctness。
