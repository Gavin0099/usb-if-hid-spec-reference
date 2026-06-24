# HID Usage Tables Import Preflight

## Purpose

This artifact defines the minimum preflight criteria before `HID Usage Tables`
can move from secondary not-imported authority toward any governed HID reference
surface in this repository.

Status: preflight only. This document does not import HID Usage Tables, cite HID
Usage Tables as authority, create Usage Tables matrices, or promote any HID
entry.

## Current Authority State

`data/source_authority.yaml` currently lists HID Usage Tables as a secondary
source with `status: not_imported`.

Until a separate Level 3 source-authority transition updates
`data/source_authority.yaml`, agents must not:

- cite HID Usage Tables as source authority;
- add Usage Tables sections to current imported usage;
- create verified Usage Tables entries;
- infer report payload, parser, firmware, OS, or product-specific behavior from
  Usage Tables naming.

## Candidate Governed Surfaces

If a future Level 3 source-authority transition approves HID Usage Tables import,
candidate surfaces should be introduced in small, separately validated slices.

Initial candidates:

- usage page identity matrix;
- usage ID identity matrix for explicitly scoped usage pages;
- usage type identity matrix;
- usage page to usage ID linkage matrix;
- report descriptor usage item linkage boundary matrix.

Each candidate matrix must begin at `scaffold` or `reviewed`, not `verified`,
unless accepted evidence packets and Level 3 verification gates already exist
for the exact entries.

## Entry Criteria

HID Usage Tables work may proceed past preflight only when all of the following
are true:

1. A Level 3 approval explicitly authorizes updating `data/source_authority.yaml`.
2. The source authority update defines:
   - exact source ID;
   - version or publication identity;
   - imported scope;
   - excluded scope;
   - claim ceiling;
   - allowed current usage.
3. `docs/source_authority.md`, `docs/claim_boundary.md`, and
   `docs/hid_hub_parity_completion_plan.md` are updated in the same checkpoint.
4. Candidate governed matrices are named before content import starts.
5. Each candidate matrix has:
   - schema expectations;
   - validator plan;
   - negative fixture plan;
   - evidence packet plan;
   - fingerprint plan;
   - visible zh/en documentation plan.
6. Existing HID validators still pass with no count drift in the current 19-entry
   governed subset.
7. The checkpoint reports:
   - commit;
   - changed files;
   - validation;
   - stats before/after;
   - can claim;
   - cannot claim;
   - residual risk.

## Hard No-Go Clauses

- No firmware behavior correctness claims.
- No OS HID input stack behavior claims.
- No parser/runtime behavior claims.
- No product-specific HID behavior claims.
- No report payload semantics claims.
- No Usage Tables coverage claim before source authority import.
- No direct `reviewed` to `verified` promotion without accepted evidence packets.
- No broad import of all Usage Tables pages in one checkpoint.

## Required First Implementation Slice

The first implementation slice after approval should be source-authority import
only. It should not add Usage Tables data entries.

That slice should:

- update `data/source_authority.yaml`;
- update source registry and claim boundary docs;
- add queue and roadmap entries for the first candidate matrix;
- run the full validation receipt index gate;
- keep tracked HID governed entries at 19 until the first matrix is separately
  introduced.

## Claim Ceiling

This preflight may claim only that HID Usage Tables import criteria exist.

It does not claim:

- HID Usage Tables are imported;
- Usage Tables entries are tracked;
- Usage Tables entries are reviewed or verified;
- report descriptor semantics are complete;
- report payload semantics are covered;
- parser/runtime behavior is covered;
- firmware behavior correctness;
- OS input stack behavior;
- product-specific HID behavior.
