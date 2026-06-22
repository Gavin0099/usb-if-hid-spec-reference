# HID Descriptor Fields

## 頁面目的

本頁為 USB HID 1.11 Section 6.2.1 descriptor fields 提供 identity-level
reviewed wording。

## Governed Matrix

機器可讀來源：

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

本頁只記錄 HID descriptor field identity。

- 不宣告 parser behavior。
- 不宣告 firmware descriptor parsing behavior。
- 不宣告 host stack semantics。
- 不宣告 report descriptor semantics。
- 不宣告 runtime transport、framing 或 timing semantics。

## Reviewed Identity Notes

- `bLength`, `bDescriptorType`, `bcdHID`, `bCountryCode` 與
  `bNumDescriptors` 只記錄 HID descriptor identity field。
- `bDescriptorType_subordinate` 與 `wDescriptorLength` 只記錄 subordinate
  descriptor entry 的 identity field。
- reviewed 狀態只代表 repo-local wording review，不代表 parser behavior 或
  runtime descriptor handling 已驗證。

## Relationship Notes

- `bNumDescriptors` 是 subordinate descriptor element 的 entry count identity。
- 每一個 subordinate descriptor element 由 `bDescriptorType_subordinate` 與
  `wDescriptorLength` 這組 identity fields 描述。
- `wDescriptorLength` 保持 identity-level，不表示 runtime parsing behavior。

## Source Reference

- HID Specification 1.11, Section 6.2.1
- `https://www.usb.org/sites/default/files/documents/hid1_11.pdf`

## Non-claims

- 本頁不宣告 parser correctness。
- 本頁不宣告 firmware descriptor parsing behavior。
- 本頁不宣告 report descriptor semantics。
- 本頁不宣告任何 evidence-backed verified promotion。
