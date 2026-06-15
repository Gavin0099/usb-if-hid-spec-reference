---
audience: human-only
authority: reference
can_override: false
overridden_by: AGENTS.md
default_load: never
---

# REVIEW_CRITERIA.md

Code review and audit protocol for this HID spec reference repo.

Source baseline: `ai-governance-framework` `governance/REVIEW_CRITERIA.md` at
commit `3221da66f30dc13c2a310d1e96084cd5e8741540`.

Repo-local adaptation: this document is review guidance only. It does not add
runtime enforcement, CI gates, or verified HID claims.

## 0. Activation

When `SCOPE = review` or the user asks for a review/audit, this document applies.

The agent should act as a skeptical verifier:

- findings must be tied to evidence
- scope drift must be called out
- reviewed content must not be described as verified
- firmware behavior truth must not be inferred from reference text alone

## 1. Verdict Model

| Verdict | Meaning | Use |
|---|---|---|
| `APPROVED` | Acceptable within stated scope | No blocking correctness or governance issue remains |
| `CHANGES_REQUESTED` | Must be fixed | A concrete blocking issue exists |
| `ESCALATED` | Human decision required | Significant ambiguity remains after review |

## 2. Finding Levels

| Level | Meaning |
|---|---|
| `BLOCKING` | Must be fixed before acceptance |
| `WARNING` | Risk or weak evidence that must be explicit |
| `SUGGESTION` | Non-blocking improvement |

## 3. Mandatory Audit Checklist

Check:

- HID reference boundaries are not expanded into firmware implementation truth.
- Hub class behavior is not introduced into this repo as HID authority.
- New HID claims cite a source section or are clearly marked as planned/reviewed.
- Verified claims have corresponding governed entries and evidence packets.
- zh/en pages stay semantically aligned when both are present.
- Dirty worktree scope is disclosed when relevant.
- Validation claims name the command or artifact that produced the result.

## 4. Review Output

Review output should include:

```markdown
### Review Inputs Checked
- governance/REVIEW_CRITERIA.md
- <additional files read>

### Decision Summary
**Verdict**: APPROVED | CHANGES_REQUESTED | ESCALATED
**Risk Level**: Low | Medium | High

### Technical Findings
1. [BLOCKING|WARNING|SUGGESTION] Title
   - Location: `path:line`
   - Evidence: ...
   - Rule Reference: ...
   - Fix Required / Reasoning: ...
```

If there are no findings, state that explicitly and list remaining validation
gaps.

## 5. Non-claims

This document does not claim:

- any HID entry is verified
- any HID semantic surface is complete
- review guidance is a runtime gate
- consuming firmware behavior can be overridden by this repo
