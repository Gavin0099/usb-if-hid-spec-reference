# HID Evidence Packet (Shell): SET_PROTOCOL

> Purpose: scaffold-reviewed draft support artifact for `SET_PROTOCOL` in HID class
> requests.
> Scope: `scaffold_identity_reference_only`
> Status: reviewed_draft_shell
> Authority: HID 1.11, Section 7.2

## Request Identity

- Name: `SET_PROTOCOL`
- Matrix ID: `hid_class_request_matrix`
- Matrix entry: `hid_set_protocol`
- bRequest: `0x0B`

## Setup Frame (Field Meaning)

- `bmRequestType`: `0x21` (host-to-device, class, interface)
- `bRequest`: `0x0B`
- `wValue`
  - High byte: reserved
  - Low byte: selected protocol value
- `wIndex`: interface target
- `wLength`: typically zero for this request

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

