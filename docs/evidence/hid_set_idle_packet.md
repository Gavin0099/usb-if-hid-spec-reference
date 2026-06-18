# HID Evidence Packet (Shell): SET_IDLE

> Purpose: scaffold-reviewed draft support artifact for `SET_IDLE` in HID class
> requests.
> Scope: `scaffold_identity_reference_only`
> Status: reviewed_draft_shell
> Authority: HID 1.11, Section 7.2

## Request Identity

- Name: `SET_IDLE`
- Matrix ID: `hid_class_request_matrix`
- Matrix entry: `hid_set_idle`
- bRequest: `0x0A`

## Setup Frame (Field Meaning)

- `bmRequestType`: `0x21` (host-to-device, class, interface)
- `bRequest`: `0x0A`
- `wValue`
  - High byte: `ReportID`
  - Low byte: `Duration`
- `wIndex`: interface target
- `wLength`: outgoing payload length context (typically zero for this request)

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

