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

- status: Waiting for human checkpoint review (reviewed-draft closure prepared)
- objective: GET_REPORT reviewed draft under Section 7.2 with human approval.
- gate: no scaffold status promotion without approval.
- latest checkpoint commit: 939a61b
- latest checkpoint status: approved by user; transition held at reviewed-draft shell level.

### HID-LRA-4: HID-REQ-2 Slice

- status: Waiting for human checkpoint review (reviewed-draft closure prepared)
- objective: SET_REPORT reviewed draft under Section 7.2 with quick human checkpoint.
- gate: reviewed-draft preparation only.
- latest checkpoint commit: 3d158d1
- latest checkpoint status: human closure review pending; keep counts unchanged.

### HID-LRA-5: HID-REQ-3 Slice

- status: Waiting for human checkpoint review (reviewed-draft closure prepared)
- objective: GET_IDLE reviewed draft under Section 7.2 with quick human checkpoint.
- gate: reviewed-draft preparation only.
- latest checkpoint commit: f114274
- latest checkpoint status: human closure review pending; keep counts unchanged.

### HID-LRA-6: HID-REQ-4 Slice

- status: Waiting for human checkpoint review (reviewed-draft closure prepared)
- objective: SET_IDLE reviewed draft under Section 7.2 with quick human checkpoint.
- gate: reviewed-draft preparation only.
- latest checkpoint commit: 2425f09
- latest checkpoint status: human closure review pending; keep counts unchanged.

### HID-LRA-7: HID-REQ-5 Slice

- status: Waiting for human checkpoint review (reviewed-draft closure prepared)
- objective: GET_PROTOCOL reviewed draft under Section 7.2 with quick human checkpoint.
- gate: reviewed-draft preparation only.
- latest checkpoint commit: c3939e8
- latest checkpoint status: human closure review pending; keep counts unchanged.

### HID-LRA-8: HID-REQ-6 Slice

- status: Human checkpoint review complete (reviewed-draft shell complete)
- objective: SET_PROTOCOL reviewed draft under Section 7.2 with quick human checkpoint.
- gate: reviewed-draft preparation only.
- latest checkpoint commit: 0b9eec2
- latest checkpoint status: approved by user; keep counts unchanged.
### HID-LRA-9: HID-DESC-1 Slice

- status: In Progress (scope-alignment iteration)
- objective: HID Descriptor field wording alignment pass under Section 6.2.1 with scaffold identity constraints.
- gate: reviewed-draft preparation only.
- latest checkpoint commit: this checkpoint
- latest checkpoint status: reviewed-draft closure in progress; keep counts unchanged.
- pending user checkpoint review.

### HID-LRA-10: Consumer Integration & Validation Surface

- status: Completed
- objective: Add repo-local evidence/consumer-integration contract + validator plumbing for the governed HID reference surface.
- verification: no review-count uplift; contract and fixture surface stabilized.


