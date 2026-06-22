# USB-IF HID Spec Reference

Read-only USB HID specification reference layer for consuming firmware
repositories.

This repository is intentionally separate from
`usb-if-hub-spec-reference`. HID is a USB class reference surface, not a Hub
class sub-surface.

## Current Status

- Canonical visible reference surface: `specs/` and `specs/en/`
- Initial focus: HID class request and HID descriptor field scaffold
- AI governance baseline: upstream formal release v1.2.0 plus latest observed
  `main` boundary snapshot (`65b3388`, 2026-06-04)
- Tracked entries: 13
- Scaffold entries: 13
- Verified entries: 0
- Reviewed entries: 0
- Inferred entries: 0

## Scope

This repo may cover:

- HID descriptors
- HID report descriptors
- HID report types and item semantics
- HID class requests
- Boot protocol, report protocol, and idle-rate semantics
- Claim boundary and evidence tracking

Current covered surface:

- HID class requests scaffold (7 entries)
- HID descriptor field scaffold (7 entries)
- No verified or fully interpreted behavior claims

## Source Authority

Current primary source:

- Device Class Definition for Human Interface Devices (HID), Version 1.11
- Publisher: USB Implementers Forum
- URL: `https://www.usb.org/sites/default/files/documents/hid1_11.pdf`
- Current imported usage: Section 7.2 Class-Specific Requests and Section 6.2.1 HID Descriptor are scaffolded

Source authority is registered in:

- `data/source_authority.yaml`
- `docs/source_authority.md`

This repo does not cover:

- Hub class behavior
- Firmware implementation truth
- Product-specific HID policy
- OS input stack behavior unless explicitly sourced

## Claim Boundary

Until evidence packets and reviewed/verified governed tables are introduced,
all content in this repo is scaffold or orientation-level reference material
only.

No verified HID entries are claimed yet.

## Governance Boundary

This repo adopts only repo-local reporting, memory authority, review criteria,
and runtime-profile boundary language from the AI governance framework.

It does not adopt fleet governance, runtime gates, the runtime profile
validator, or CodeBurn observation as enforcement.

## Reference Entry Points

- `specs/hid_scope.md`
- `specs/hid_class_requests.md`
- `specs/hid_descriptor_fields.md`
- `specs/verification_status.md`
- `docs/claim_boundary.md`
- `docs/source_authority.md`
- `docs/agent_execution_model.md`
- `docs/hid_long_running_roadmap.md`
- `docs/CONSUMER_INTEGRATION_CONTRACT.md`
- `exports/hid_governed_surface_manifest.yaml`
- `governance/hid_long_running_agent_contract.md`
- `governance/hid_work_queue.yaml`

## Machine-Readable Surfaces

- `data/`: governed scaffold matrices for HID class requests and HID descriptor
  fields.
- `contract/`: repo-local authority, claim, evidence, and version-scope rules.
- `exports/hid_governed_surface_manifest.yaml`: consumer-facing manifest for
  the current HID scaffold surface.
- `evidence/source_registry.yaml`: evidence-facing mirror of registered and
  excluded HID authority sources.
- `evidence/table_fingerprint_baseline.jsonl`: content-hash baseline for
  governed matrix drift detection.

## Consumer Integration

Consuming repositories can integrate this scaffold surface through a two-step
advisory CI check:

```powershell
python scripts\validate_hid_governed_surface_manifest.py
python scripts\probe_table_fingerprint.py --mode check `
  --manifest exports\hid_governed_surface_manifest.yaml `
  --baseline-in evidence\table_fingerprint_baseline.jsonl
```

Both checks must pass before treating the scaffold surface as stable. Passing
checks do not upgrade any HID entry to verified.

## Validation

Core repo-local checks:

```powershell
python scripts\validate_source_authority.py
python scripts\validate_hid_class_request_matrix.py
python scripts\validate_hid_descriptor_fields_matrix.py
python scripts\validate_verification_status.py
python scripts\validate_source_registry.py `
  --receipt-out evidence\validation_receipt_source_registry.json
python scripts\validate_contract_files.py `
  --receipt-out evidence\validation_receipt_contract_files.json
python scripts\validate_memory_records.py `
  --receipt-out evidence\validation_receipt_memory_records.json
python scripts\validate_hid_governed_surface_manifest.py
python scripts\probe_table_fingerprint.py --mode check `
  --manifest exports\hid_governed_surface_manifest.yaml `
  --baseline-in evidence\table_fingerprint_baseline.jsonl
python scripts\smoke_consumer_integration_fixtures.py
python -m unittest discover -s tests
```
