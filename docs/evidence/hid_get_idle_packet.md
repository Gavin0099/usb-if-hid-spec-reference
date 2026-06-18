# HID Evidence Packet (Shell): GET_IDLE

> Purpose: scaffold-reviewed draft support artifact for `GET_IDLE` in HID class
> requests.
> Scope: `scaffold_identity_reference_only`
> Status: reviewed_draft_shell
> Authority: HID 1.11, Section 7.2

## Request Identity

- Name: `GET_IDLE`
- Matrix ID: `hid_class_request_matrix`
- Matrix entry: `hid_get_idle`
- bRequest: `0x02`

## Setup Frame (Field Meaning)

- `bmRequestType`: `0xA1` (device-to-host, class, interface)
- `bRequest`: `0x02`
- `wValue`
  - High byte: `ReportID`
  - Low byte: reserved
- `wIndex`: interface target
- `wLength`: returned idle value payload length

## Claim Ceiling

- This artifact is scaffold-level review draft only.
- No verified claim is made here.
- No firmware/driver/parser/OS-behavior correctness claims.

## Source Anchor

- HID Specification 1.11: `https://www.usb.org/sites/default/files/documents/hid1_11.pdf`
- Section: 7.2

## Residual Risk

- Field interpretation must remain scoped to identity-level reference and not expand to
  runtime behavior.

