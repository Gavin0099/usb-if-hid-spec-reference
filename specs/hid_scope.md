# HID Scope

## Page Purpose

本頁定義此 repo 可承載的 HID reference surface，避免 HID 內容被誤放進
Hub reference repo，或被 consuming repo 誤用成 firmware implementation truth。

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

- 本頁不宣告 HID semantic coverage complete。
- 本頁不宣告任何 verified HID entry。
- 本頁不定義 firmware implementation requirements。
