# AGENTS.md - USB-IF HID Spec Reference

<!-- governance:memory_authority -->
memory_root: memory/
external_memory_allowed: false
operational_records_must_stay_under_memory_root: true

## Purpose

This repository is a read-only HID spec reference layer.

Its permitted role is to clarify USB HID class specification semantics for
consuming firmware repositories.

It does not govern firmware behavior directly. It does not override confirmed
project facts.

## Usage Boundary

This repository may be used to:

- Clarify HID descriptor, report descriptor, report, protocol, idle, and class
  request semantics
- Provide standard-side input for project-specific review
- Support claim boundary and evidence tracking for HID reference content

This repository must not be used to:

- Replace confirmed project facts with generic HID interpretation
- Override firmware architecture decisions in consuming repos
- Serve as source of truth for project-specific HID behavior
- Define operating-system input stack behavior unless explicitly grounded in a
  cited HID source

## Standard Conflict Resolution

When a consuming repo detects a conflict between this spec reference and a
confirmed project fact, the consuming repo owns the escalation and resolution.

This repo only provides the standard-side reference input.

## Governance Calibration

<!-- governance:key=critical_path -->
The most dangerous path in this repo is misuse: HID reference content must not
silently replace confirmed firmware behavior or product-specific input policy.

<!-- governance:key=l2_escalation -->
Escalate in the consuming repo when:

- A firmware behavior change is proposed based solely on this reference
- HID descriptor/report interpretation conflicts with confirmed project facts
- A new HID interpretation affects device enumeration, report parsing, boot
  protocol, idle handling, or host-visible behavior

<!-- governance:key=forbidden_shortcuts -->
Forbidden in this repo:

- Adding project-specific implementation guidance
- Marking a HID interpretation as required without source-section traceability
- Treating reviewed reference content as verified implementation truth

## Document Relationship

- `specs/index.md` - zh-TW HID reference entry
- `specs/en/index.md` - English HID reference entry
- `specs/hid_scope.md` - initial HID reference scope and boundaries
- `specs/en/hid_scope.md` - English scope counterpart
- `specs/verification_status.md` - zh-TW verification status
- `specs/en/verification_status.md` - English verification status

## Commit Checkpoint

When reporting a completed work chunk, include:

- `Commit Checkpoint: <short hash or NO_COMMIT>`
- `Scope: <files or area covered>`
- `Validation: <checks run or NONE>`
- `Risk: <open risk or NONE>`
