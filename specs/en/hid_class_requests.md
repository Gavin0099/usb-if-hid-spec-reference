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

### GET_REPORT reviewed draft

#### Setup fields (identity-level only)

- Request: `GET_REPORT` (`hid_get_report`)
- `bmRequestType`: `0xA1`
  - Direction: device-to-host
  - Type: class
  - Recipient: interface
- `bRequest`: `0x01`
- `wValue`
  - High byte (`ReportType`): scope selector byte (input/output/feature request class in HID identity context)
  - Low byte (`ReportID`): report identifier selector
- `wIndex`
  - Interface number context for the request
- `wLength`
  - Number of bytes carried in the report payload response (identity-level scope only)

Source anchor:

- HID Specification 1.11, section 7.2
- `https://www.usb.org/sites/default/files/documents/hid1_11.pdf`

This reviewed draft is limited to field identity and scaffold-level meaning from the
imported source. It does not advance this repo’s verification state.

### SET_REPORT reviewed draft

#### Setup fields (identity-level only)

- Request: `SET_REPORT` (`hid_set_report`)
- `bmRequestType`: `0x21`
  - Direction: host-to-device
  - Type: class
  - Recipient: interface
- `bRequest`: `0x09`
- `wValue`
  - High byte (`ReportType`): indicates input/output/feature report type selector
  - Low byte (`ReportID`): report identifier selector
- `wIndex`
  - Interface context for the request target
- `wLength`
  - Number of bytes in the outgoing report payload (identity-level scope only)

Source anchor:

- HID Specification 1.11, section 7.2
- `https://www.usb.org/sites/default/files/documents/hid1_11.pdf`

This reviewed draft is limited to field identity and scaffold-level meaning from the
imported source. It does not advance this repo’s verification state.

### Idle requests

- `GET_IDLE`: reads the current idle rate.
- `SET_IDLE`: sets the idle rate.

This repo does not currently claim idle timing behavior, interrupt IN scheduling,
or host stack behavior.

### GET_IDLE reviewed draft

#### Setup fields (identity-level only)

- Request: `GET_IDLE` (`hid_get_idle`)
- `bmRequestType`: `0xA1`
  - Direction: device-to-host
  - Type: class
  - Recipient: interface
- `bRequest`: `0x02`
- `wValue`
  - High byte (`ReportID`): report selector
  - Low byte (`0`): reserved in this request identity context
- `wIndex`
  - Interface context for the request target
- `wLength`
  - Payload bytes expected in the returned idle value (`1` in this request identity context)

Source anchor:

- HID Specification 1.11, section 7.2
- `https://www.usb.org/sites/default/files/documents/hid1_11.pdf`

This reviewed draft is limited to field identity and scaffold-level meaning from the
imported source. It does not advance this repo’s verification state.

### SET_IDLE reviewed draft

#### Setup fields (identity-level only)

- Request: `SET_IDLE` (`hid_set_idle`)
- `bmRequestType`: `0x21`
  - Direction: host-to-device
  - Type: class
  - Recipient: interface
- `bRequest`: `0x0A`
- `wValue`
  - High byte (`ReportID`): report selector
  - Low byte (`Duration`): duration selector
- `wIndex`
  - Interface context for the request target
- `wLength`
  - Usually zero for this request payload (`0` in this request identity context)

Source anchor:

- HID Specification 1.11, section 7.2
- `https://www.usb.org/sites/default/files/documents/hid1_11.pdf`

This reviewed draft is limited to field identity and scaffold-level meaning from the
imported source. It does not advance this repo’s verification state.

### Protocol requests

- `GET_PROTOCOL`: reads the active protocol selection.
- `SET_PROTOCOL`: selects boot protocol or report protocol.

This repo does not currently claim keyboard/mouse boot behavior is verified, and
it does not claim product-specific protocol policy.

### GET_PROTOCOL reviewed draft

#### Setup fields (identity-level only)

- Request: `GET_PROTOCOL` (`hid_get_protocol`)
- `bmRequestType`: `0xA1`
  - Direction: device-to-host
  - Type: class
  - Recipient: interface
- `bRequest`: `0x03`
- `wValue`
  - Reserved (should be set to `0` for request identity in this scaffold)
- `wIndex`
  - Interface context for the request target
- `wLength`
  - Payload bytes expected in the response (`1` in this request identity context)

Source anchor:

- HID Specification 1.11, section 7.2
- `https://www.usb.org/sites/default/files/documents/hid1_11.pdf`

This reviewed draft is limited to field identity and scaffold-level meaning from the
imported source. It does not advance this repo’s verification state.

### SET_PROTOCOL reviewed draft

#### Setup fields (identity-level only)

- Request: `SET_PROTOCOL` (`hid_set_protocol`)
- `bmRequestType`: `0x21`
  - Direction: host-to-device
  - Type: class
  - Recipient: interface
- `bRequest`: `0x0B`
- `wValue`
  - High byte: reserved in this request identity context
  - Low byte: selected protocol value (`0` = Boot Protocol, `1` = Report Protocol)
- `wIndex`
  - Interface context for the request target
- `wLength`
  - Usually zero for this request payload

Source anchor:

- HID Specification 1.11, section 7.2
- `https://www.usb.org/sites/default/files/documents/hid1_11.pdf`

This reviewed draft is limited to field identity and scaffold-level meaning from the
imported source. It does not advance this repo’s verification state.

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
