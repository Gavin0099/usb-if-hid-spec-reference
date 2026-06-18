# HID Evidence Packet (Shell): GET_REPORT

> Purpose: scaffold-reviewed draft support artifact for `GET_REPORT` in HID class
> requests.
> Scope: `scaffold_identity_reference_only`
> Status: reviewed_draft_shell
> Authority: HID 1.11, Section 7.2

## Request Identity

- Name: `GET_REPORT`
- Matrix ID: `hid_class_request_matrix`
- Matrix entry: `hid_get_report`
- bRequest: `0x01`

## Setup Frame (Field Meaning)

- `bmRequestType`: `0xA1` (device-to-host, class, interface)
- `bRequest`: `0x01`
- `wValue`
  - High byte: `ReportType`
  - Low byte: `ReportID`
- `wIndex`: interface target
- `wLength`: response payload length

## Claim Ceiling

- This artifact is scaffold-level review only.
- No verified claim is made here.
- No firmware/driver/parser/OS-behavior correctness claims.

## Source Anchor

- HID Specification 1.11: `https://www.usb.org/sites/default/files/documents/hid1_11.pdf`
- Section: 7.2

## Residual Risk

- Field interpretation must remain scoped to identity-level reference and not expand to
  runtime behavior.

