# HID Agent Execution Model

## Purpose

This model defines how an AI agent proceeds through long-running HID work while
respecting the repo claim ceiling and forbidden domains.

## Operational Phases

1. Pick the next queue item from `governance/hid_work_queue.yaml`.
2. Verify item status and required approval fields.
3. Run the required validation pass for the slice.
4. Determine review level.
5. For Level 1, apply changes directly and produce one commit checkpoint entry using
   the repository contract format.
6. For Level 2/3, follow gate mode in `governance/hid_review_gate.yaml`.
7. Classify review level and gate outcome.
8. Produce one commit checkpoint entry using the repository contract format.
9. Perform only allowed autonomous work (docs, wording cleanup, consistency checks).
10. Do not change reviewed/verified counts in YAML data tables.

## Review Level Gate

- Level 1 tasks: auto-pass tasks (roadmap, queue state, shell evidence,
  boundary docs) -> checkpoint with `Review level: Level 1` and continue
  automatically when gate passes.
- Level 2 tasks: reviewed-draft preparations (for example HID request entry
  text) -> quick human checkpoint required before moving on.
- Level 3 tasks: reviewed/verified uplift, source import, new matrix,
  descriptor semantic imports -> must stop and await explicit human approval.

## Checkpoint modes (Level 2/3)

For Level 2 and Level 3 work, checkpoint mode is controlled by
`governance/hid_review_gate.yaml`.

### Batch mode (default)

- Use an agent branch under `agent/` (example: `agent/hid-lra-rollup`).
- Record each checkpoint in `docs/hid_long_running_checkpoint_rollup.md`.
- Respect `gate_mode` and `batch_size` in `governance/hid_review_gate.yaml`.
- Pause after each Level 2/3 slice when approval is not yet recorded.
- Respect `batch_size` (default 1 in this branch) only for internal batching,
  and do not auto-advance without explicit approval flags.
- Continue only after user marks approval in `governance/hid_review_gate.yaml`
  (`approved_batch: true` and `approved_through` set).

### PR mode (optional, explicit request only)

- Create a branch in the form `agent/<item-id>-<short-kebab>` before changes.
- Open one PR with body required by
  `governance/hid_long_running_agent_contract.md`.
- Do not start the next queue slice until review approval is recorded.
- PR title should follow:
  `HID-REQ-<N>: <request> reviewed draft preparation` (or equivalent title for
  reviewed/verified uplifts).

## Required Slice Gate

A slice is not complete unless all of the following exist:

- Commit (no `NO_COMMIT`).
- Validation block with required checks passing.
- checkpoint with:
  - `Validation:`
  - `Stats before/after:`
  - `Can claim:`
  - `Cannot claim:`
- Clear review level assignment.

## Human-Approval Gating

- Level 2 and Level 3 tasks require gate-mode-specific checkpoint and human
  approval.
- Any requested status promotion or claim that may alter scope requires human sign-off
  before execution continues.
- If approval is not present, Codex records a stop checkpoint and pauses on the
  current item.

## Safety Invariants

- No source import.
- No firmware behavior claims.
- No OS/input stack claims.
- No parser/driver/runtime assertions.
- No verified claim without explicit evidence packet closure.

## Deliverable Contract

At the end of a run, include:

- `HID-LRA` phase marker (HID-LRA-1, -2, ...)
- queue item id (`HID-REQ-1`, `HID-REQ-2`, ...)
- required checkpoint block from
  `governance/hid_long_running_agent_contract.md`.
