# Agent Runtime Profile Boundary

Repo-local adoption: boundary record only.

Source baseline: `ai-governance-framework` observed upstream `main` short
commit `65b3388`.

## Purpose

The upstream framework now includes reviewer-facing agent runtime governance
profile materials for describing memory, context files, skills, plugins, tool
execution, gateways, schedulers, subagents, and rollback surfaces.

This HID reference repo records that surface as known upstream governance
context, but does not adopt the runtime profile schema or validator as a repo
gate.

## Adopted Here

- The claim ceiling vocabulary is adopted as review language.
- Runtime-surface claims must be downgraded unless supported by a concrete
  load-bearing boundary and validation evidence.
- Response envelopes should disclose runtime enforcement, semantic correctness,
  evidence truthfulness, and authority correctness as non-claims unless they
  were separately validated.

## Not Adopted Here

- Runtime profile YAML schema
- Runtime profile validator
- Hermes integration
- OS sandbox, RBAC, or containment claims
- Runtime hook enforcement
- Authority correctness validation
- Semantic evidence validation

## HID Repo Claim Ceiling

This repo may use runtime-profile language only to discuss agent/reporting
governance boundaries.

It must not be used to assert:

- HID semantic correctness
- firmware behavior correctness
- host operating-system input-stack behavior
- runtime containment
- tool execution safety

## Safe Wording

- reviewer-facing profile
- structural boundary record
- reporting convention
- in-process heuristic
- not runtime enforcement
- not semantic validation

## Unsafe Wording Without Separate Evidence

- runtime enforced
- sandboxed
- contained
- authority confirmed
- evidence validated
- behaviorally safe
- semantically verified
