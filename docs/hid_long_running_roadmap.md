# HID Long-Running Roadmap

## Phase Summary

### HID-LRA-1: Long-Running Agent Contract

- status: Active
- objective: define a repeatable execution contract and queue controls for docs-only
  long-running agent work.
- outputs: `governance/hid_long_running_agent_contract.md`,
  `governance/hid_work_queue.yaml`.
- verification: no content-surface uplift.

### HID-LRA-2: Work Queue Expansion

- status: Completed
- objective: define governance-ready queue and per-task boundaries for initial
  HID class request drafts.
- output: `governance/hid_work_queue.yaml`.

### HID-LRA-3: HID-REQ-1 Slice

- status: Completed (reviewed)
- objective: GET_REPORT reviewed draft under Section 7.2 with human approval.
- gate: no scaffold status promotion without approval.
- latest checkpoint commit: 939a61b
- latest checkpoint status: approved by user; scaffold->reviewed transition completed.

### HID-LRA-4: HID-REQ-2 Slice

- status: Completed (reviewed)
- objective: SET_REPORT reviewed draft under Section 7.2 with quick human checkpoint.
- gate: reviewed-draft preparation only.
- latest checkpoint commit: 3d158d1
- latest checkpoint status: approved by user; scaffold->reviewed transition completed.

### HID-LRA-5: HID-REQ-3 Slice

- status: Completed (reviewed)
- objective: GET_IDLE reviewed draft under Section 7.2 with quick human checkpoint.
- gate: reviewed-draft preparation only.
- latest checkpoint commit: f114274
- latest checkpoint status: approved by user; scaffold->reviewed transition completed.

### HID-LRA-6: HID-REQ-4 Slice

- status: Completed (reviewed)
- objective: SET_IDLE reviewed draft under Section 7.2 with quick human checkpoint.
- gate: reviewed-draft preparation only.
- latest checkpoint commit: 2425f09
- latest checkpoint status: approved by user; scaffold->reviewed transition completed.

### HID-LRA-7: HID-REQ-5 Slice

- status: Completed (reviewed)
- objective: GET_PROTOCOL reviewed draft under Section 7.2 with quick human checkpoint.
- gate: reviewed-draft preparation only.
- latest checkpoint commit: c3939e8
- latest checkpoint status: approved by user; scaffold->reviewed transition completed.

### HID-LRA-8: HID-REQ-6 Slice

- status: Completed (reviewed)
- objective: SET_PROTOCOL reviewed draft under Section 7.2 with quick human checkpoint.
- gate: reviewed-draft preparation only.
- latest checkpoint commit: 0b9eec2
- latest checkpoint status: approved by user; scaffold->reviewed transition completed.
### HID-LRA-9: HID-DESC-1 Slice

- status: Completed
- objective: HID Descriptor field wording alignment pass under Section 6.2.1 with scaffold identity constraints.
- gate: reviewed-draft preparation only.
- latest checkpoint commit: this checkpoint
- latest checkpoint status: approved by user; keep counts unchanged.

### HID-LRA-10: Consumer Integration & Validation Surface

- status: Completed
- objective: Add repo-local evidence/consumer-integration contract + validator plumbing for the governed HID reference surface.
- verification: no review-count uplift; contract and fixture surface stabilized.

### HID-LRA-11: Source Authority Extension Preflight

- status: Completed
- objective: define next source-authority expansion scope and preflight constraints before importing additional HID governance surface.
- latest checkpoint: e0d42f1
- gate: source authority registration and LRA kickoff bookkeeping only (no count movement).

### HID-LRA-12: Source Authority Extension Import Eligibility

- status: Completed
- objective: define the explicit criteria to move `6.2.2` to current imported usage and launch governed import implementation work.
- dependencies: user-approved `HID-EXT-1` preflight and follow-up claim-ceiling update.
- latest checkpoint: 0c175d9
- gate: no scope-semantic imports until explicit scope and review checkpoint are set.
- artifact: `docs/hid_6_2_2_import_eligibility.md`

### HID-LRA-13: Checkpoint Memory Visibility

- status: Completed
- objective: add repo-local warning-only tooling that detects unbound daily
  memory entries and emits checkpoint memory records.
- gate: governance visibility only; no HID semantic or runtime-enforcement claim.

### HID-LRA-14: 6.2.2 Import-Prep Shell

- status: Completed
- objective: add report descriptor item import-prep matrix, validator, tests, and
  zh/en spec pages without moving `6.2.2` to current imported usage.
- latest checkpoint: 0c175d9
- gate: import-prep only; no parser/report descriptor semantic claim.

### HID-LRA-15: 6.2.2 Current Scaffold Import

- status: Completed
- objective: move Section 6.2.2 report descriptor item identity shells from
  future-authorized preflight into current imported scaffold surface.
- latest checkpoint: 92c3296
- gate: Level 3 source-authority transition; no verified or parser semantic
  claim.

### HID-LRA-16: 6.2.2 Reviewed Identity Wording

- status: Completed
- objective: promote the six Section 6.2.2 report descriptor item identity
  shells from scaffold to reviewed wording.
- latest checkpoint: cce6c21
- gate: reviewed identity only; no verified or parser semantic claim.

### HID-LRA-17: 6.2.1 HID Descriptor Field Reviewed Wording

- status: Completed
- objective: promote the seven Section 6.2.1 HID descriptor field identity
  entries from scaffold to reviewed wording.
- latest checkpoint: 21a956f
- gate: reviewed identity only; no verified, parser, or runtime descriptor
  handling claim.

### HID-LRA-18: Verified Evidence Packet Preflight Gate

- status: Completed
- objective: define the schema, validator, and Level 3 approval criteria needed
  before any future reviewed-to-verified promotion.
- latest checkpoint: 0937dc7
- gate: governance preflight only; no verified count movement and no firmware,
  OS input stack, parser/runtime, or product-specific HID behavior claim.

### HID-LRA-19: GET_REPORT Verified Candidate Packet Skeleton

- status: Completed
- objective: add a machine-checkable `HID-REQ-1` GET_REPORT candidate packet
  skeleton for future Level 3 review preparation.
- latest checkpoint: ad0badb
- gate: candidate packet only; no accepted evidence packet and no verified count
  movement.

### HID-LRA-20: Remaining HID Request Candidate Packet Skeletons

- status: Completed
- objective: add machine-checkable candidate packet skeletons for SET_REPORT,
  GET_IDLE, SET_IDLE, GET_PROTOCOL, and SET_PROTOCOL.
- latest checkpoint: d20d87d
- gate: candidate packet only; no accepted evidence packet and no verified count
  movement.

### HID-LRA-21: Candidate Source Authority Binding Validator

- status: Completed
- objective: require candidate packet `source_trace.source_id/source_section` to
  match current imported usage in `data/source_authority.yaml`.
- latest checkpoint: bf16027
- gate: validator hardening only; no source import, no accepted evidence packet,
  and no verified count movement.

### HID-LRA-22: Candidate Matrix Source Ref Binding Validator

- status: Completed
- objective: require candidate packet source trace to match both source authority
  current imported usage and the bound matrix `source_refs`.
- latest checkpoint: 35b16dd
- gate: validator/source-id alignment only; no source import, no accepted
  evidence packet, and no verified count movement.

### HID-LRA-23: Candidate Source Binding Negative Tests

- status: Completed
- objective: add negative fixture tests that prove candidate source binding
  validation fails on wrong source id, wrong source section, or conflicting
  matrix source refs.
- latest checkpoint: 130dcdb
- gate: test coverage only; no source import, no accepted evidence packet, and
  no verified count movement.

### HID-LRA-24: Candidate Accepted-Gate Negative Tests

- status: Completed
- objective: add negative fixture tests proving candidate validation fails on
  accepted packet status, non-pending approval, and verified current claim level.
- latest checkpoint: 184dbab
- gate: test coverage only; no accepted evidence packet and no verified count
  movement.

### HID-LRA-25: HID Descriptor Field Candidate Packet Skeletons

- status: Completed
- objective: add machine-checkable candidate packet skeletons for the seven HID
  descriptor field entries under Section 6.2.1.
- latest checkpoint: 211c438
- gate: candidate packet only; no accepted evidence packet and no verified count
  movement.

### HID-LRA-26: HID Report Descriptor Item Candidate Packet Skeletons

- status: Completed
- objective: add machine-checkable candidate packet skeletons for the six HID
  report descriptor item identity entries under Section 6.2.2.
- latest checkpoint: c2dae74
- gate: candidate packet only; no accepted evidence packet and no verified count
  movement.

### HID-LRA-27: Level 3 Accepted Packet Workflow Contract

- status: Completed
- objective: define and validate the required workflow for future
  candidate-to-accepted evidence packet transitions.
- latest checkpoint: f111729
- gate: workflow contract only; no accepted evidence packet and no verified count
  movement.

### HID-LRA-28: Level 3 Accepted Packet Dry-Run Fixtures

- status: Completed
- objective: add test-only accepted packet dry-run fixtures proving the
  accepted workflow can pass when complete and fail when approval, validation
  receipt, Level 3 checkpoint, or no-direct-promotion controls are missing.
- latest checkpoint: 72ba835
- gate: test coverage only; no production accepted packet and no verified count
  movement.

### HID-LRA-29: Production Accepted Packet Path and Naming Guard

- status: Completed
- objective: harden accepted packet validation so future production accepted
  packets must live under `docs/evidence/accepted/`, use the
  `<candidate-base>_accepted.yaml` filename form, and bind to an existing
  `<candidate-base>_candidate.yaml` packet.
- latest checkpoint: 7da0966
- gate: validator hardening only; no production accepted packet and no verified
  count movement.

### HID-LRA-30: GET_REPORT Accepted Packet Pre-Approval Checklist

- status: Completed
- objective: add a read-only generator for accepted-packet pre-approval
  checklist reports and generate the first GET_REPORT gap report under
  `docs/evidence/preapproval/`.
- latest checkpoint: 52d85ed
- gate: pre-approval gap report only; no production accepted packet and no
  verified count movement.

### HID-LRA-31: Complete Candidate Pre-Approval Checklist Surface

- status: Completed
- objective: extend the pre-approval checklist generator with batch mode and
  generate gap reports for all 19 candidate packets under
  `docs/evidence/preapproval/`.
- latest checkpoint: 4adaeba
- gate: pre-approval gap report only; no production accepted packet and no
  verified count movement.

### HID-LRA-32: Pre-Approval Generator Stale-Report and Path Guard

- status: Completed
- objective: harden the pre-approval checklist generator so output paths stay
  under the repository root and stale reports fail batch generation unless
  explicitly pruned.
- latest checkpoint: ef1865f
- gate: generator hardening only; no production accepted packet and no verified
  count movement.

### HID-LRA-33: Accepted Packet Pre-Approval Readiness Summary

- status: Completed
- objective: add a readiness summary generator and generate Markdown/JSON
  summary artifacts for all 19 pre-approval checklist reports.
- latest checkpoint: 63e1160
- gate: readiness summary only; no production accepted packet and no verified
  count movement.

### HID-LRA-34: GET_REPORT Accepted Packet Proposal Generator

- status: Completed
- objective: add an accepted-packet proposal generator and generate GET_REPORT
  Markdown/JSON proposal artifacts under `accepted_proposals/`.
- latest checkpoint: 9b67f3a
- gate: accepted packet proposal only; no production accepted packet and no
  verified count movement.

### HID-LRA-35: Accepted Packet Proposal Validator

- status: Completed
- objective: add a validator for accepted-packet proposal artifacts covering
  proposal-only status, future accepted path absence, candidate/pre-approval
  bindings, Level 3 placeholders, and claim ceilings.
- latest checkpoint: bc8a365
- gate: proposal validator only; no production accepted packet and no verified
  count movement.

### HID-LRA-36: Accepted Packet Proposal Validator Receipt Path Containment

- status: Completed
- objective: harden `--receipt-out` handling for the accepted-packet proposal
  validator so receipt paths must resolve under the repository root.
- latest checkpoint: 27bda5b
- gate: validator hardening only; no production accepted packet and no verified
  count movement.

### HID-LRA-37: Complete Accepted Packet Proposal Surface

- status: Completed
- objective: extend accepted-packet proposal generation to all 19 candidate
  packets, producing Markdown and JSON proposal artifacts under
  `accepted_proposals/`.
- latest checkpoint: 33915f3
- gate: accepted packet proposal only; no production accepted packet and no
  verified count movement.

### HID-LRA-38: Accepted Packet Proposal Coverage Guard and Summary

- status: Completed
- objective: validate full proposal coverage/alignment for all 19 candidates
  and generate accepted-packet proposal summary Markdown/JSON artifacts.
- latest checkpoint: 1958b2c
- gate: proposal coverage summary only; no production accepted packet and no
  verified count movement.

### HID-LRA-68: Accepted Packet Proposal Summary Drift Gate

- status: Completed
- objective: add summary integrity checks so committed accepted-packet proposal
  summaries are rejected if regenerated output drifts.
- latest checkpoint: 9d606db
- gate: summary drift guard only; no production accepted packet and no verified
  count movement.

### HID-LRA-69: Accepted Packet Production Batch

- status: Completed
- objective: generate production accepted packet artifacts for all 19 identities
  and align proposal/readiness summaries to the post-production accepted surface.
- latest checkpoint: 0903006
- gate: production accepted evidence status only; no verified count movement.
