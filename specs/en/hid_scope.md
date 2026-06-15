# HID Scope

## Page Purpose

This page defines the HID reference surface allowed in this repo. It keeps HID
content separate from the Hub reference repo and prevents consuming repos from
treating reference text as firmware implementation truth.

## In Scope

| Area | Status | Notes |
|---|---|---|
| HID descriptors | scaffolded | Descriptor field identity scaffold is active |
| HID report descriptors | planned | Item/tag/value reference boundary only |
| HID class requests | scaffolded | Request identity, direction, and recipient boundary only |
| Report / boot / idle semantics | planned | Standard-side semantic reference only |
| Evidence packets | planned | No packets exist yet |

## Out of Scope

| Area | Reason |
|---|---|
| Hub class behavior | Covered by `usb-if-hub-spec-reference` |
| Firmware implementation truth | Owned by consuming firmware repos |
| Product-specific input policy | Project-specific behavior, not generic HID reference |
| OS input stack behavior | Host/platform-specific unless explicitly sourced |

## Initial Import Rule

HID content should be introduced in small, auditable phases:

1. Define governed tables.
2. Add zh/en readable reference pages.
3. Add evidence packet schema and validator.
4. Promote entries only after source traceability exists.

## Non-claims

- This page does not claim complete HID semantic coverage.
- This page does not claim any verified HID entry.
- This page does not define firmware implementation requirements.
