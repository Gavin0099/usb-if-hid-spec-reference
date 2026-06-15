# Response Envelope Contract

Repo-local adoption: reporting convention only.

Source baseline: `ai-governance-framework`
`governance/RESPONSE_ENVELOPE_CONTRACT.md` at commit
`3221da66f30dc13c2a310d1e96084cd5e8741540`.

## Purpose

This contract defines a compact structure for reporting completed work in this
HID reference repo.

The goal is to keep scope, evidence, claim ceiling, and risk separate enough for
review.

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

## Claim Ceiling Preservation

Do not merge unverified implications into `done`.

If a capability was not validated, proven, or authorized in the current scope:

- state the positive boundary under `claim_ceiling`
- list the non-asserted items under `not_claimed`
- disclose remaining evidence gaps under `risk`

## Non-goals

This contract does not add:

- runtime enforcement
- automatic semantic verification
- CI gates
- HID source validation
- firmware behavior validation
