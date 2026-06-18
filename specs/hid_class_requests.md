# HID Class Requests

## Page Purpose

本頁提供 USB HID class-specific requests 的初始 reference scaffold。
目前涵蓋 request name、`bRequest`、方向與介面 recipient 邊界。

## Governed Matrix

機制來源：

- `data/hid_class_request_matrix.yaml`

## Request Summary

| Request | `bRequest` | Direction | Recipient | Claim level |
|---|---:|---|---|---|
| `GET_REPORT` | `0x01` | Device to host | Interface | scaffold |
| `SET_REPORT` | `0x09` | Host to device | Interface | scaffold |
| `GET_IDLE` | `0x02` | Device to host | Interface | scaffold |
| `SET_IDLE` | `0x0A` | Host to device | Interface | scaffold |
| `GET_PROTOCOL` | `0x03` | Device to host | Interface | scaffold |
| `SET_PROTOCOL` | `0x0B` | Host to device | Interface | scaffold |

## Request Families

### Report requests

- `GET_REPORT`：host 向 device 讀取 HID report。
- `SET_REPORT`：host 向 device 傳送 HID report。

此 repo 目前不描述 report payload 格式、report ID 路由、或 firmware handler
correctness。

### GET_REPORT reviewed 草稿

- 請求：`GET_REPORT`（`hid_get_report`）
- `bmRequestType`: `0xA1`
  - 方向：Device-to-host
  - Type：class
  - Recipient：interface
- `bRequest`: `0x01`
- `wValue`
  - 高位元組（`ReportType`）：選擇 input/output/feature 型別
  - 低位元組（`ReportID`）：指定 report ID
- `wIndex`
  - 對應目前介面的 request context
- `wLength`
  - 回應 payload 預期位元組長度

來源：

- HID Specification 1.11, section 7.2
- `https://www.usb.org/sites/default/files/documents/hid1_11.pdf`

此 reviewed 草稿僅記錄欄位身份與 scaffold 級意涵，未提升本 repo 的
verified/reviewed 狀態。

### SET_REPORT reviewed 草稿

- 請求：`SET_REPORT`（`hid_set_report`）
- `bmRequestType`: `0x21`
  - 方向：Host-to-device
  - Type：class
  - Recipient：interface
- `bRequest`: `0x09`
- `wValue`
  - 高位元組（`ReportType`）：指定 input/output/feature report type
  - 低位元組（`ReportID`）：指定 report ID
- `wIndex`
  - 對應目前介面的 request context
- `wLength`
  - 指定要傳送的 report payload 預期位元組長度

來源：

- HID Specification 1.11, section 7.2
- `https://www.usb.org/sites/default/files/documents/hid1_11.pdf`

此 reviewed 草稿僅記錄欄位身份與 scaffold 級意涵，未提升本 repo 的
verified/reviewed 狀態。

### GET_IDLE reviewed 草稿

- 請求：`GET_IDLE`（`hid_get_idle`）
- `bmRequestType`: `0xA1`
  - 方向：Device-to-host
  - Type：class
  - Recipient：interface
- `bRequest`: `0x02`
- `wValue`
  - 高位元組（`ReportID`）：report selector
  - 低位元組（`0`）：本請求中作為保留欄位
- `wIndex`
  - 對應目前介面的 request context
- `wLength`
  - 回傳 idle value payload 的位元組數

來源：

- HID Specification 1.11, section 7.2
- `https://www.usb.org/sites/default/files/documents/hid1_11.pdf`

此 reviewed 草稿僅記錄欄位身份與 scaffold 級意涵，未提升本 repo 的
verified/reviewed 狀態。

### SET_IDLE reviewed 草稿

- 請求：`SET_IDLE`（`hid_set_idle`）
- `bmRequestType`: `0x21`
  - 方向：Host-to-device
  - Type：class
  - Recipient：interface
- `bRequest`: `0x0A`
- `wValue`
  - 高位元組（`ReportID`）：report selector
  - 低位元組（`Duration`）：duration selector
- `wIndex`
  - 對應目前介面的 request context
- `wLength`
  - 常見情況為 0

來源：

- HID Specification 1.11, section 7.2
- `https://www.usb.org/sites/default/files/documents/hid1_11.pdf`

此 reviewed 草稿僅記錄欄位身份與 scaffold 級意涵，未提升本 repo 的
verified/reviewed 狀態。

### Protocol requests

- `GET_PROTOCOL`：讀取目前 protocol 選擇。
- `SET_PROTOCOL`：設定 boot protocol 或 report protocol。

目前不描述 keyboard/mouse boot 行為是否驗證，亦不宣告產品專屬 protocol 政策。

### GET_PROTOCOL reviewed 草稿

- 請求：`GET_PROTOCOL`（`hid_get_protocol`）
- `bmRequestType`: `0xA1`
  - 方向：Device-to-host
  - Type：class
  - Recipient：interface
- `bRequest`: `0x03`
- `wValue`
  - 此請求下保留或為 0 的欄位意涵
- `wIndex`
  - 對應目前介面的 request context
- `wLength`
  - 回傳 protocol value payload 的位元組數

來源：

- HID Specification 1.11, section 7.2
- `https://www.usb.org/sites/default/files/documents/hid1_11.pdf`

此 reviewed 草稿僅記錄欄位身份與 scaffold 級意涵，未提升本 repo 的
verified/reviewed 狀態。

### SET_PROTOCOL reviewed 草稿

- 請求：`SET_PROTOCOL`（`hid_set_protocol`）
- `bmRequestType`: `0x21`
  - 方向：Host-to-device
  - Type：class
  - Recipient：interface
- `bRequest`: `0x0B`
- `wValue`
  - 低位元組：protocol select 訊號（身份層意涵）
  - 高位元組：保留
- `wIndex`
  - 對應目前介面的 request context
- `wLength`
  - 通常為 0

來源：

- HID Specification 1.11, section 7.2
- `https://www.usb.org/sites/default/files/documents/hid1_11.pdf`

此 reviewed 草稿僅記錄欄位身份與 scaffold 級意涵，未提升本 repo 的
verified/reviewed 狀態。

## Source Boundary

來源參考：

- HID Specification 1.11, section 7.2
- `https://www.usb.org/sites/default/files/documents/hid1_11.pdf`

此頁是 source anchor 與 scaffold，非 evidence packet，也不是 verified promotion。

## Non-claims

- 本頁不宣告 HID request 行為 fully verified。
- 本頁不宣告 firmware request handler correctness。
- 本頁不宣告 OS HID driver 行為。
- 本頁不宣告 report payload semantics。
- 本頁不宣告任何 entry 已完成 evidence-backed verified promotion。
