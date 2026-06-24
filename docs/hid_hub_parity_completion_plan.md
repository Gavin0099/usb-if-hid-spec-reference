# HID to HUB-Parity Completion Plan

This plan defines how `usb-if-hid-spec-reference` should move toward the
governance and reference-surface maturity of `usb-if-hub-spec-reference`.

The goal is not to copy HUB semantics into HID. The goal is to reach comparable
repo completeness: source authority breadth, governed matrix coverage, evidence
packet coverage, validation receipts, consumer integration gates, and visible
reference navigation.

## Current Baseline

Current HID governed subset:

- 3 governed matrices.
- 19 tracked entries.
- 19 verified identity-level entries.
- 19 accepted evidence packets.
- HID 1.11 source authority currently imported for:
  - Section 7.2 Class-Specific Requests.
  - Section 6.2.1 HID Descriptor.
  - Section 6.2.2 Report Descriptor item type identities.

Current HUB maturity reference:

- 15 governed matrices.
- 204 tracked entries.
- 153 verified entries.
- 153 entry verification packets.
- USB 2.0 freeze surface plus USB 3.x partial verified expansion.
- Broad validator, receipt, wiki/spec, consumer contract, and fingerprint drift
  surfaces.

## Gap Summary

HID is complete only for its currently imported governed subset. It is not yet
complete as a HID reference repository.

Major gaps relative to HUB maturity:

- Source authority breadth: HID Usage Tables are registered only as secondary
  not-imported authority.
- Report descriptor semantics: Main, Global, and Local item semantics are not
  imported beyond identity-level item type shells.
- Report payload semantics: no governed report payload matrix exists.
- Descriptor expansion: only HID descriptor fields are covered, not subordinate
  descriptor relationship semantics.
- Protocol/idle behavior: class request identities are verified, but behavior,
  timing, host, and firmware semantics are not claimed.
- Validation receipts: HID has a small receipt surface compared with HUB's
  broad per-validator receipt archive.
- Wiki/spec breadth: HID has compact zh/en pages, not HUB-style topic maps.
- Consumer gates: HID has manifest/fingerprint smoke gates, but no maturity
  dashboard equivalent to HUB's broader completion guards.

## Completion Phases

### Phase 1: Baseline Claim Reconciliation

Purpose: make public docs match the actual machine-readable state.

Actions:

- Update README, claim boundary, source authority docs, and manifest wording so
  they state `19 tracked / 19 verified` for the current imported subset.
- Preserve the claim ceiling: verified means source-traceable identity-level
  evidence with accepted packets, not firmware, OS, parser, or full HID
  semantic correctness.
- Add a parity plan entry point from README and roadmap.

Gate:

- Existing validators pass.
- No matrix status movement.
- No new source authority import.

### Phase 2: HUB-Style Receipt Surface

Purpose: make validation evidence durable and inspectable.

Status: in progress. `HID-LRA-84` adds the first durable validation receipt
index and per-command receipt archive for the current HID gate suite.
`HID-LRA-85` adds a receipt freshness/staleness validator so missing, failed,
mismatched, or stale receipt files fail the gate.

Actions:

- Add committed validation receipts for the current validators.
- Add a summary receipt index for source authority, matrices, evidence packets,
  manifest, fingerprint, memory, and tests.
- Add stale receipt detection where practical.

Gate:

- Receipts are generated from existing validators.
- Receipts do not imply new semantic coverage.

### Phase 3: HID Usage Tables Import Preflight

Purpose: prepare secondary authority expansion without silently importing it.

Status: in progress. `HID-LRA-86` adds the preflight/eligibility artifact for
HID Usage Tables import without importing the source or creating Usage Tables
governed entries.
`HID-LRA-87` adds a source-authority import proposal/checklist and proposal
validator while keeping HID Usage Tables not imported.

Actions:

- Define source authority extension criteria for HID Usage Tables.
- Add a usage-table import eligibility document.
- Define candidate governed matrices before importing data.

Possible matrices:

- Usage page identity matrix.
- Usage ID identity matrix for selected pages.
- Usage type matrix.
- Collection/usage linkage matrix.

Gate:

- Human Level 3 approval before any new source authority import.
- No Usage Tables citation until `data/source_authority.yaml` is updated.

### Phase 4: Report Descriptor Semantic Surface

Purpose: expand Section 6.2.2 beyond item type identity shells.

Possible matrices:

- Main item tag matrix.
- Global item tag matrix.
- Local item tag matrix.
- Short item size/type/tag encoding matrix.
- Long item prefix and payload boundary matrix.
- Collection item boundary matrix.

Gate:

- Entries start as scaffold or reviewed.
- Verified promotion requires accepted evidence packets.
- No parser/runtime behavior claim.

### Phase 5: Report Payload and Report ID Surface

Purpose: define governed boundaries for reports without claiming product
behavior.

Possible matrices:

- Report type identity matrix.
- Report ID boundary matrix.
- Input/Output/Feature report linkage matrix.
- Unit/logical/physical min-max identity matrix.

Gate:

- No product-specific report layout truth.
- No firmware handler correctness.
- No OS input stack claim.

### Phase 6: Protocol and Idle Semantics Expansion

Purpose: extend class request identity into governed protocol/idle semantics
where source-grounded.

Possible matrices:

- Boot/report protocol mode identity matrix.
- Idle rate request field matrix.
- Request recipient/interface linkage matrix.

Gate:

- No host scheduling behavior.
- No firmware implementation behavior.
- No timing correctness beyond source-stated identity fields.

### Phase 7: Consumer Integration and Drift Maturity

Purpose: reach HUB-style CI usability.

Actions:

- Add a HID completion-surface validator.
- Add a reference surface statistics validator.
- Add a receipt archive for all validators.
- Add drift checks for all governed matrices.
- Add consumer smoke fixtures for manifest pass, fingerprint pass, and drift
  fail attribution.

Gate:

- Consumer gates are advisory reference gates only.
- They do not establish project-specific truth.

### Phase 8: Spec/Wiki Navigation Expansion

Purpose: make the reference surface navigable like HUB.

Actions:

- Add topic-level zh/en pages for imported HID areas.
- Add page frontmatter and source coverage validators if adopted.
- Add cross-reference checks between pages and governed matrices.

Gate:

- Pages mirror governed matrix state.
- Pages cannot become source of truth over YAML/evidence surfaces.

## Target Maturity Definition

HID reaches HUB-parity maturity when:

- All imported HID source areas have governed matrices.
- Each matrix has a validator and negative fixtures.
- Each verified entry has an accepted evidence packet.
- Verification status, manifest, README, claim boundary, and source authority
  docs agree.
- Validation receipts are committed for the primary gate suite.
- Fingerprint drift detection covers every governed table.
- Consumer integration smoke tests cover pass and fail attribution.
- Non-claims remain explicit for firmware, OS, parser/runtime, and
  product-specific behavior.

## Claim Ceiling

This plan may claim only planning and execution governance.

It does not claim:

- Full HID spec coverage today.
- HID Usage Tables coverage today.
- Report descriptor semantic completeness today.
- Report payload semantic completeness.
- Firmware behavior correctness.
- Host OS input stack behavior.
- Parser/runtime behavior.
- Product-specific HID behavior.
