# HID Descriptor Fields

## 頁面用途

這個頁面提供 USB HID 1.11 Section 6.2.1 的 descriptor 欄位身份級別 scaffold。

## 治理矩陣

機器可讀資料來源：

- `data/hid_descriptor_fields_matrix.yaml`

## 欄位摘要

| 欄位 | 意義 | Claim level |
|---|---|---:|
| `bLength` | Descriptor 的總長度（位元組數）。 | scaffold |
| `bDescriptorType` | Descriptor 類型識別碼。 | scaffold |
| `bcdHID` | HID 規格版本（BCD 編碼）身份欄位。 | scaffold |
| `bCountryCode` | 硬體 country code 欄位。 | scaffold |
| `bNumDescriptors` | subordinate descriptor 的項目數。 | scaffold |
| `bDescriptorType_subordinate` | 每個 subordinate descriptor 的 type 欄位。 | scaffold |
| `wDescriptorLength` | 每個 subordinate descriptor 的長度欄位。 | scaffold |

## 範圍與界線

本頁面僅保留欄位身份描述，不描述 parser 行為。

- 不宣告 parser 正確性。
- 不宣告 firmware request parser/行為。
- 不宣告 Host stack 行為。
- 不宣告 report descriptor semantics。

## 欄位關聯說明

- `bNumDescriptors` 是 subordinate descriptor 項目數。
- 每一個 subordinate descriptor 由一組 `bDescriptorType_subordinate` + `wDescriptorLength` 共同描述。
- `wDescriptorLength` 僅保留為身份欄位長度意涵，不做執行時語意推論。

## 來源參考

- HID Specification 1.11, Section 6.2.1
- `https://www.usb.org/sites/default/files/documents/hid1_11.pdf`

欄位仍為 scaffold-only，不代表已完成 verified promotion。

## Non-claims

- 本頁不宣告 parser 正確性。
- 本頁不宣告 firmware descriptor parsing 行為。
- 本頁不宣告 report descriptor semantics。
- 本頁不宣告任何 evidence-backed verified promotion。
