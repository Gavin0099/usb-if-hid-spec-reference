# Governance Authority Table

> machine-readable: true
> version: 1.0.0
> updated: 2026-06-15

## Authority Levels

- `canonical`: highest repo-local authority. It defines the controlling rule
  when other surfaces conflict.
- `reference`: supporting authority. It informs agent or reviewer decisions but
  cannot override canonical documents.
- `derived`: generated, adapted, summarized, or cached material derived from
  canonical or reference sources. It cannot create new authority by itself.

## Audience Types

- `agent-runtime`: may be loaded automatically at session start or runtime
  initialization.
- `agent-on-demand`: may be loaded when a task requires the relevant context.
- `human-only`: intended for reviewers or operators. Agents must not treat these
  documents as runtime-loaded policy unless explicitly asked to review them.

## Default Load Modes

- `always`: load at session start or runtime initialization.
- `on-demand`: load only when the current task needs that context.
- `incremental`: load selectively when a specific memory or record is relevant.
- `never`: do not load automatically; human-review surface only.

---

## Authority Table

| document | audience | authority | can_override | overridden_by | default_load |
|----------|----------|-----------|--------------|---------------|--------------|
| `AGENTS.md` (workspace) | agent-runtime | canonical | false | ~ | always |
| `README.md` | agent-on-demand | reference | false | AGENTS.md | on-demand |
| `specs/hid_scope.md` | agent-on-demand | reference | false | AGENTS.md | on-demand |
| `specs/en/hid_scope.md` | agent-on-demand | reference | false | AGENTS.md | on-demand |
| `specs/hid_class_requests.md` | agent-on-demand | reference | false | AGENTS.md | on-demand |
| `specs/en/hid_class_requests.md` | agent-on-demand | reference | false | AGENTS.md | on-demand |
| `specs/hid_descriptor_fields.md` | agent-on-demand | reference | false | AGENTS.md | on-demand |
| `specs/en/hid_descriptor_fields.md` | agent-on-demand | reference | false | AGENTS.md | on-demand |
| `specs/verification_status.md` | agent-on-demand | reference | false | AGENTS.md | on-demand |
| `specs/en/verification_status.md` | agent-on-demand | reference | false | AGENTS.md | on-demand |
| `data/hid_class_request_matrix.yaml` | agent-on-demand | reference | false | AGENTS.md | on-demand |
| `data/hid_descriptor_fields_matrix.yaml` | agent-on-demand | reference | false | AGENTS.md | on-demand |
| `data/source_authority.yaml` | agent-on-demand | canonical | false | AGENTS.md | on-demand |
| `contract/*.yaml` | agent-on-demand | reference | false | data/source_authority.yaml | on-demand |
| `exports/hid_governed_surface_manifest.yaml` | agent-on-demand | reference | false | data/source_authority.yaml | on-demand |
| `evidence/source_registry.yaml` | agent-on-demand | reference | false | data/source_authority.yaml | on-demand |
| `evidence/table_fingerprint_baseline.jsonl` | agent-on-demand | derived | false | exports/hid_governed_surface_manifest.yaml | on-demand |
| `docs/claim_boundary.md` | agent-on-demand | reference | false | AGENTS.md | on-demand |
| `docs/source_authority.md` | agent-on-demand | reference | false | data/source_authority.yaml | on-demand |
| `docs/CONSUMER_INTEGRATION_CONTRACT.md` | agent-on-demand | reference | false | AGENTS.md | on-demand |
| `docs/agent_execution_model.md` | agent-on-demand | reference | false | AGENTS.md | on-demand |
| `docs/hid_long_running_roadmap.md` | agent-on-demand | reference | false | AGENTS.md | on-demand |
| `governance/AUTHORITY.md` | agent-on-demand | canonical | false | AGENTS.md | on-demand |
| `governance/REVIEW_CRITERIA.md` | human-only | reference | false | AGENTS.md | never |
| `governance/hid_long_running_agent_contract.md` | human-only | canonical | false | AGENTS.md | never |
| `governance/hid_work_queue.yaml` | agent-on-demand | reference | false | AGENTS.md | on-demand |
| `governance/RESPONSE_ENVELOPE_CONTRACT.md` | agent-on-demand | reference | false | AGENTS.md | on-demand |
| `governance/MEMORY_AUTHORITY_CONTRACT.md` | agent-on-demand | reference | false | AGENTS.md | on-demand |
| `governance/AGENT_RUNTIME_PROFILE_BOUNDARY.md` | agent-on-demand | reference | false | AGENTS.md | on-demand |
| `governance/framework.lock.json` | agent-on-demand | derived | false | AUTHORITY.md | on-demand |
| `memory/YYYY-MM-DD.md` | agent-on-demand | derived | false | AGENTS.md | incremental |

---

## Conflict Resolution Rules

Authority precedence:

```text
canonical > reference > derived
```

Rules:

1. `canonical` wins over `reference`.
2. `canonical` wins over `derived`.
3. `reference` wins over `derived`.
4. Workspace instructions such as `AGENTS.md` must not be overridden by imported
   framework material.
5. `agent-on-demand` surfaces may provide task context, but they must not replace
   always-loaded canonical runtime rules.
6. `derived` material is cache or adaptation only. It must be traced back to its
   governing source before being treated as authority.

---

## Import Boundary

This repo adopts only repo-local governance surfaces from
`ai-governance-framework`.

Not imported:

- fleet governance scope
- external repo onboarding authority
- runtime gate policy
- governance drift workflows
- framework producer tooling
- runtime profile validator
- agent runtime profile schema
- trust boundary taxonomy as enforcement
- CodeBurn observation as gate input
- framework memory workflow implementation
- framework mutation catalog as enforcement

These surfaces may exist in the framework producer repo, but their presence
there does not make them authority in this HID reference repo.

---

## Latest Framework Refresh Notes

Observed upstream framework baseline `737fcd4` adds framework-side memory
workflow and mutation-catalog surfaces, plus expanded result-first response
reporting guidance.

Repo-local adoption in this HID reference repo is limited to reporting
convention refresh in `governance/RESPONSE_ENVELOPE_CONTRACT.md` and the
framework lock baseline update. It does not import framework producer tooling,
runtime gate policy, memory workflow implementation, mutation enforcement, or
any new HID source authority.
