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


