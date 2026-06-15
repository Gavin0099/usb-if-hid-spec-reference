# HID Class Requests

## Page Purpose

本頁提供 USB HID class-specific requests 的初始 reference scaffold。
目前只整理 request name、`bRequest` value、direction 與 interface recipient
邊界，方便 firmware repo 查找 request identity。

## Governed Matrix

Machine-readable source:

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

- `GET_REPORT`：host 從 device 讀取 HID report。
- `SET_REPORT`：host 將 HID report 傳送給 device。

本 repo 目前不解釋 report payload 格式、report ID routing、或 firmware
handler correctness。

### Idle requests

- `GET_IDLE`：讀取目前 idle rate。
- `SET_IDLE`：設定 idle rate。

本 repo 目前不宣告 idle timing behavior、interrupt IN scheduling、或 host stack
行為。

### Protocol requests

- `GET_PROTOCOL`：讀取目前 protocol selection。
- `SET_PROTOCOL`：切換 boot protocol 或 report protocol。

本 repo 目前不宣告 keyboard/mouse boot behavior 已驗證，也不宣告 product-specific
protocol policy。

## Source Boundary

Source reference:

- HID Specification 1.11, section 7.2
- `https://www.usb.org/sites/default/files/documents/hid1_11.pdf`

目前這只是 source anchor 與 scaffold，不是 evidence packet，也不是 verified
promotion。

## Non-claims

- 本頁不宣告 HID request behavior fully verified。
- 本頁不宣告 firmware request handler correctness。
- 本頁不宣告 OS HID driver behavior。
- 本頁不宣告 report payload semantics。
- 本頁不宣告任何 entry 已完成 evidence-backed verified promotion。
