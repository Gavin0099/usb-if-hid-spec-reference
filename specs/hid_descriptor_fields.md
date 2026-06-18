# HID 描述符欄位

## 頁面目的

建立 USB HID 1.11 §6.2.1 的 descriptor 欄位識別 scaffold，提供欄位名稱、作用與 scope 邊界，作為 descriptor 入門的 reference anchor。

## Governed Matrix

機器可讀來源：

- `data/hid_descriptor_fields_matrix.yaml`

## 欄位摘要

| 欄位 | 說明 | Claim level |
|---|---|---:|
| `bLength` | descriptor 的總長度（位元組）。 | scaffold |
| `bDescriptorType` | descriptor 類型識別碼。 | scaffold |
| `bcdHID` | HID 規範版本欄位。 | scaffold |
| `bCountryCode` | 設備語系/國碼欄位。 | scaffold |
| `bNumDescriptors` | subordinate descriptor 數目欄位。 | scaffold |
| `bDescriptorType_subordinate` | subordinate descriptor 的 type 欄位。 | scaffold |
| `wDescriptorLength` | subordinate descriptor 的長度欄位。 | scaffold |

## 範圍與界線

本頁面只做欄位身份層級 scaffold（欄位名稱與用途邊界），不推導為 parser 行為模型，也不聲明 implementation 行為。

## 欄位關係（描述）

- `bNumDescriptors` 表示 subordinate descriptor 的對應組件數量。
- 每個 subordinate descriptor 的對應欄位是 `bDescriptorType_subordinate` 與 `wDescriptorLength`。
- 目前不將可變長度重複條目展開為完整 parser contract，避免超出 `scaffold` claim。

## Source Reference

來源：

- HID Specification 1.11, section 6.2.1
- `https://www.usb.org/sites/default/files/documents/hid1_11.pdf`

本頁為 scaffold/identity reference，尚未做 verified promotion。

## Non-claims

- 本頁不宣告 parser 正確性、長度邏輯推導或實作行為。
- 本頁不宣告 Report Descriptor 條目 semantics。
- 本頁不宣告任何 HID entry 的 verified promotion。
