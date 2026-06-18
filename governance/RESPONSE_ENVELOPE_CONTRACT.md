# Response Envelope Contract

Repo-local adoption: reporting convention only.

Source baseline: `ai-governance-framework`
`governance/RESPONSE_ENVELOPE_CONTRACT.md` at observed upstream `main`
short commit `65b3388`.

Baseline version: v0.1.

## Purpose

This contract defines a compact structure for reporting completed work in this
HID reference repo.

The goal is to keep scope, evidence, claim ceiling, and risk separate enough for
review.

## Authority Boundary

This contract is a reviewer-facing reporting schema. It does not change:

- closeout runtime enforcement
- evidence admissibility rules
- claim ceiling semantics
- risk disclosure semantics
- session-end hook behavior
- gate policy behavior

## Event-Driven Mode Rule

`mode` must describe the workflow event that produced the response. It must not
be treated as an agent-selected style preference.

Every envelope that includes `mode` must also include `mode_source`.

Allowed repo-local mode mappings:

| Event | mode | mode_source |
|---|---|---|
| Completed user-requested work report | `CLOSEOUT` | `user_report` |
| In-progress status update | `PROGRESS` | `intermediate_update` |
| Scoped files staged for commit | `PRE_COMMIT` | `git_staged_diff` |
| Validation command completed | `VALIDATION` | `validation_command` |
| Out-of-scope change detected | `SCOPE_ALERT` | `scope_boundary_check` |

## Minimum Fields

```yaml
mode: CLOSEOUT
mode_source: user_report
task: short bounded task label
task_authority: user_request
scope:
  - exact files or surfaces
done:
  - completed work inside scope
claim_ceiling:
  - explicit upper bound of what is being asserted
not_claimed:
  - claims intentionally not made
evidence_refs:
  - command: command or artifact
    result: PASS | FAIL | NOT RUN | NOT PRESENT | NOT CLAIMED
risk:
  - remaining risk or scope limitation
next_action: one concrete next step or none
```

## task_authority Values

Allowed values:

- `user_request`: explicitly requested or authorized by the user.
- `followup`: directly follows a previously authorized task without expanding
  scope.
- `hook_trigger`: produced by a workflow hook or runtime event.
- `autonomous`: initiated by the agent without direct user authorization.

If `task_authority: autonomous`, the response must include a `risk` entry that
explains why the work did not exceed the current done boundary.

## evidence_refs Rules

Each evidence reference must include:

- `command` or `artifact`
- `result`

Valid `result` values:

- `PASS`
- `FAIL`
- `NOT RUN`
- `NOT PRESENT`
- `NOT CLAIMED`

`PASS` must include a command, artifact, or source that can be independently
checked. Bare `PASS` is not valid.

`evidence_refs` does not upgrade semantic authority. It records what evidence
exists for the stated claim ceiling.

## Claim Ceiling Preservation

Do not merge unverified implications into `done`.

If a capability was not validated, proven, or authorized in the current scope:

- state the positive boundary under `claim_ceiling`
- list the non-asserted items under `not_claimed`
- disclose remaining evidence gaps under `risk`

## Risk Disclosure Preservation

The `risk` field is required because incidental work is otherwise easy to hide
inside narrative prose.

Risk entries should disclose:

- incidental cleanup
- scope drift
- claim inflation
- evidence maturity limits
- autonomous work boundary concerns

Do not replace `risk` with confidence scores, effort estimates, or broad impact
analysis.

## Non-goals

This contract does not add:

- confidence scores
- effort estimates
- generic impact analysis
- runtime enforcement
- automatic semantic verification
- CI gates
- HID source validation
- firmware behavior validation
