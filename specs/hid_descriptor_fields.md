# HID Descriptor Fields

## 頁面用途

本頁提供 USB HID 1.11 第 6.2.1 節的 descriptor 欄位身份層（identity）對照。

## 欄位索引

機械可讀對照表：

- `data/hid_descriptor_fields_matrix.yaml`

## 欄位摘要

| 欄位 | 意義 | Claim level |
|---|---|---:|
| `bLength` | descriptor 的總長度。 | scaffold |
| `bDescriptorType` | descriptor 類型識別值。 | scaffold |
| `bcdHID` | HID 規格版本（BCD 編碼）。 | scaffold |
| `bCountryCode` | 硬體國別碼欄位。 | scaffold |
| `bNumDescriptors` | subordinate descriptor 的項目數。 | scaffold |
| `bDescriptorType_subordinate` | 每個 subordinate descriptor 的類型欄位。 | scaffold |
| `wDescriptorLength` | 每個 subordinate descriptor 的長度欄位。 | scaffold |

## Scope and Boundary

本頁僅保留身份層語意：

- 不宣告 parser 行為。
- 不宣告 firmware request parser/descriptor 行為。
- 不宣告 host stack 行為。
- 不宣告 report descriptor semantics。

## 身份約定

- 範圍限定在欄位名稱與型別意圖。
- 數值語意僅保留 scaffold 級別描述，不推論執行流程。
- 本頁與矩陣不代表行為規範文件。

## 關聯備註

- `bNumDescriptors` 是 subordinate descriptor 的項目數量。
- 每一個 subordinate descriptor 由一組 `bDescriptorType_subordinate` + `wDescriptorLength` 一起描述。
- `wDescriptorLength` 仍為身份層定義，不含 runtime 解析正確性。

## 來源

- HID Specification 1.11, Section 6.2.1
- `https://www.usb.org/sites/default/files/documents/hid1_11.pdf`

## 非聲明項

- 本頁不宣告 parser 正確性。
- 本頁不宣告 firmware descriptor parsing 行為。
- 本頁不宣告 report descriptor semantics。
- 本頁不宣告 evidence-backed verified 提升。
