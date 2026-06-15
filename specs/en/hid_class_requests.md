# HID Class Requests

## Page Purpose

This page provides the initial reference scaffold for USB HID class-specific
requests. It currently covers request name, `bRequest` value, direction, and
interface-recipient boundary only.

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

- `GET_REPORT`: host reads a HID report from the device.
- `SET_REPORT`: host sends a HID report to the device.

This repo does not currently describe report payload format, report ID routing,
or firmware handler correctness.

### Idle requests

- `GET_IDLE`: reads the current idle rate.
- `SET_IDLE`: sets the idle rate.

This repo does not currently claim idle timing behavior, interrupt IN scheduling,
or host stack behavior.

### Protocol requests

- `GET_PROTOCOL`: reads the active protocol selection.
- `SET_PROTOCOL`: selects boot protocol or report protocol.

This repo does not currently claim keyboard/mouse boot behavior is verified, and
it does not claim product-specific protocol policy.

## Source Boundary

Source reference:

- HID Specification 1.11, section 7.2
- `https://www.usb.org/sites/default/files/documents/hid1_11.pdf`

This is a source anchor and scaffold only. It is not an evidence packet and not a
verified promotion.

## Non-claims

- This page does not claim HID request behavior is fully verified.
- This page does not claim firmware request handler correctness.
- This page does not claim OS HID driver behavior.
- This page does not claim report payload semantics.
- This page does not claim any entry has evidence-backed verified promotion.
