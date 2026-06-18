# HID Descriptor Fields

## 頁面用途

本頁提供 USB HID 1.11 第 6.2.1 節的 descriptor 欄位身份層（scaffold）對照。

## 受治理矩陣管理

機器可讀規格來源：

- `data/hid_descriptor_fields_matrix.yaml`

## 欄位摘要

| 欄位 | 意義 | Claim level |
|---|---|---:|
| `bLength` | Descriptor 全長（位元組）。 | scaffold |
| `bDescriptorType` | Descriptor 型別代碼。 | scaffold |
| `bcdHID` | HID 規格版本識別碼（BCD 編碼）。 | scaffold |
| `bCountryCode` | 硬體所在地區代碼。 | scaffold |
| `bNumDescriptors` | subordinate descriptor 的項目數。 | scaffold |
| `bDescriptorType_subordinate` | 每個 subordinate descriptor 的型別欄位。 | scaffold |
| `wDescriptorLength` | 每個 subordinate descriptor 的長度欄位。 | scaffold |

## Scope and Boundary

本頁內容僅保留身份層級（identity-level）描述，不宣告執行行為。

- 不宣告 parser 行為。
- 不宣告 firmware request parser/descriptor 行為。
- 不宣告 Host stack 行為。
- 不宣告 report descriptor semantics。

## 識別層限制

- 僅記錄欄位名稱與身份層意圖。
- 數值語意限制於 scaffold 級別，不承諾任何執行時語意。
- 此頁與矩陣不作行為層規範文件。

## 關係備註

- `bNumDescriptors` 是 subordinate descriptor 的項目數。
- 每一個 subordinate descriptor 由一組 `bDescriptorType_subordinate` + `wDescriptorLength` 一起描述。
- `wDescriptorLength` 僅保留欄位長度意義，未做傳輸行為對應。

## 來源

- HID Specification 1.11, Section 6.2.1
- `https://www.usb.org/sites/default/files/documents/hid1_11.pdf`

本頁仍為 scaffold-only，且不作任何 verified 升級。

## Non-claims

- 本頁不宣告 parser 正確性。
- 本頁不宣告 firmware descriptor parsing 行為。
- 本頁不宣告 report descriptor semantics。
- 本頁不宣告任何 evidence-backed verified 升級。
