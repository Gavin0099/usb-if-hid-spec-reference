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

## Source Authority Rule

Agents must not cite or import additional HID/USB documents as authority until
they are registered in `data/source_authority.yaml`.

Current primary source authority:

- Device Class Definition for Human Interface Devices (HID), Version 1.11
- USB Implementers Forum
- `https://www.usb.org/sites/default/files/documents/hid1_11.pdf`
- Current imported usage: Section 7.2 Class-Specific Requests and Section 6.2.1 HID Descriptor scaffold only

Explicitly excluded unless separately scoped:

- HID over I2C
- OS input stack behavior
- firmware handler correctness
- hub class behavior
- report payload semantics beyond identity-level scaffold

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
- `specs/hid_class_requests.md` - HID class request scaffold summary
- `specs/en/hid_class_requests.md` - English HID class request counterpart
- `specs/hid_descriptor_fields.md` - HID descriptor field scaffold summary
- `specs/en/hid_descriptor_fields.md` - English HID descriptor field counterpart
- `specs/verification_status.md` - zh-TW verification status
- `specs/en/verification_status.md` - English verification status
- `data/hid_class_request_matrix.yaml` - HID class request machine-readable scaffold
- `data/hid_descriptor_fields_matrix.yaml` - HID descriptor field machine-readable scaffold
- `contract/` - repo-local authority, claim, evidence, and version-scope rules
- `exports/hid_governed_surface_manifest.yaml` - consumer-facing HID scaffold manifest
- `evidence/source_registry.yaml` - evidence-facing source registry
- `evidence/table_fingerprint_baseline.jsonl` - governed matrix fingerprint baseline
- `data/source_authority.yaml` - HID source authority registry
- `docs/claim_boundary.md` - current claim ceiling and claim level definitions
- `docs/source_authority.md` - human-readable source authority boundary
- `docs/CONSUMER_INTEGRATION_CONTRACT.md` - consumer integration contract
- `governance/AUTHORITY.md` - repo-local governance authority registry
- `governance/REVIEW_CRITERIA.md` - review/audit guidance
- `governance/RESPONSE_ENVELOPE_CONTRACT.md` - structured closeout/reporting convention
- `governance/MEMORY_AUTHORITY_CONTRACT.md` - repo-local memory authority boundary
- `scripts/validate_memory_records.py` - warning-only repo-local memory record validator
- `scripts/emit_checkpoint_memory_entry.py` - checkpoint-to-memory entry helper
- `governance/AGENT_RUNTIME_PROFILE_BOUNDARY.md` - latest upstream runtime-profile boundary record
- `governance/framework.lock.json` - imported governance framework baseline

## Review Tasks

If the agent is asked to perform `review` or `audit` work:

- The agent must read `governance/REVIEW_CRITERIA.md` before producing review output.
- The agent must not skip that read step.
- The final review output must include a `Review Inputs Checked` block.

## Commit Checkpoint

When reporting a completed work chunk, include:

- `Commit Checkpoint: <short hash or NO_COMMIT>`
- `Scope: <files or area covered>`
- `Validation: <checks run or NONE>`
- `Risk: <open risk or NONE>`
