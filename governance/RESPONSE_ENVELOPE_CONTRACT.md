# Response Envelope Contract

Repo-local adoption: reporting convention only.

Source baseline: `ai-governance-framework`
`governance/RESPONSE_ENVELOPE_CONTRACT.md` at observed upstream `main`
short commit `737fcd4`.

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

## Result-First Final Report Format

Final reports should be result-first, not process-first.

Content language should match the session language. Fixed vocabulary tokens
remain in English where they are used as validation status labels: `PASS`,
`FAIL`, `NOT RUN`, `NOT CLAIMED`, and `NOT PRESENT`.

Recommended Chinese session format:

```text
1. 結果：完成 / 未完成
2. 能力提升：
3. 變更檔案：
4. 驗證：
   - structural:    PASS — <指令> | FAIL — <指令> | NOT RUN
   - build:         PASS — <指令> | FAIL — <指令> | NOT RUN
   - semantic:      NOT CLAIMED | PASS — 人工審查：[審查者/日期]
   - behavioral:    NOT PRESENT | 已驗證 — [如何]
   - ext evidence:  NOT PRESENT | [來源與範圍]
5. 風險：
   - scope drift:        none | [說明]
   - claim inflation:    none | [說明]
   - evidence maturity:  [一行說明]
6. 附帶清理：   none | file=[路徑] reason=[原因] semantic_change=no
7. Governance surface 變更：none / 列舉
8. 剩餘阻擋：
9. 本次無法宣告：
   - [列出未驗證、未確認、未證明的項目；不得省略]
```

Recommended English session format:

```text
1. Result: Done / Not done
2. Capability increased:
3. Changed files:
4. Validation:
   - structural:    PASS — <command> | FAIL — <command> | NOT RUN
   - build:         PASS — <command> | FAIL — <command> | NOT RUN
   - semantic:      NOT CLAIMED | PASS — human review: [reviewer/date]
   - behavioral:    NOT PRESENT | verified — [how]
   - ext evidence:  NOT PRESENT | [source and scope]
5. Risk:
   - scope drift:        none | [description]
   - claim inflation:    none | [description]
   - evidence maturity:  [one line]
6. Incidental cleanup:   none | file=[path] reason=[why] semantic_change=no
7. Governance surface change: none / list
8. Remaining blocker:
9. Cannot claim this session:
   - [list what was not validated, verified, or proven; never omit]
```

## Golden Examples

Schema-only change:

```text
1. Result: Done
2. Capability increased: section_refs schema extended
3. Changed files: wiki/port-status.md
4. Validation:
   - structural:    PASS — grep section_refs wiki/port-status.md
   - build:         NOT RUN — markdown-only change
   - semantic:      NOT CLAIMED
   - behavioral:    NOT PRESENT
   - ext evidence:  NOT PRESENT
5. Risk:
   - scope drift:        none
   - claim inflation:    none
   - evidence maturity:  structural layer only; no semantic verification
6. Incidental cleanup:   none
7. Governance surface change: none
8. Remaining blocker:     none
9. Cannot claim this session:
   - semantic correctness of section references
   - PDF-level content verification
```

Partial validation:

```text
1. Result: Not done — build failed
2. Capability increased: none
3. Changed files: wiki/port-status.md (uncommitted)
4. Validation:
   - structural:    PASS — validate_wiki_frontmatter (exit 0)
   - build:         FAIL — npm run build (exit 1)
   - semantic:      NOT CLAIMED
   - behavioral:    NOT PRESENT
   - ext evidence:  NOT PRESENT
5. Risk:
   - scope drift:        none
   - claim inflation:    none — task not complete
   - evidence maturity:  build failure; no completion evidence
6. Incidental cleanup:   none
7. Governance surface change: none
8. Remaining blocker:     build error must be resolved before commit
9. Cannot claim this session:
   - task complete
   - validation above build layer
```
