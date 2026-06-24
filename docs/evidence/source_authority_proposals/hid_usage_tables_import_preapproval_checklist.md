# HID Usage Tables Source Authority Pre-Approval Checklist

> Status: source authority proposal gap report only
> Authority ceiling: source_authority_preapproval_gap_report_only

- Source candidate: `hid_usage_tables`
- Current source authority status: `not_imported`
- Production source authority change created: no
- Usage Tables governed entries created: no
- Verified uplift: no

## Ready Checks

- preflight artifact exists: `docs/hid_usage_tables_import_preflight.md`
- source candidate is already registered as secondary not-imported authority
- proposal keeps Level 3 approval as TBD
- proposal keeps direct_import: false
- proposal preserves no-source-authority-import claim ceiling
- proposal preserves no Usage Tables coverage claim ceiling
- proposal does not create candidate matrices
- proposal does not create evidence packets
- proposal does not change current 19-entry governed subset

## Gaps Before Source Authority Import

- Level 3 approval must be recorded.
- Human approver must be recorded.
- Source version/publication identity must be selected.
- Imported Usage Tables scope must be selected.
- Excluded Usage Tables scope must be selected.
- `data/source_authority.yaml` must be updated in the approved import slice.
- `evidence/source_registry.yaml` must be updated in the approved import slice.
- Candidate matrices must be introduced in separate slices after source import.
- Validation receipt index must pass after any approved source import.

## Claim Ceiling

- source_authority_preapproval_gap_report_only
- no_source_authority_import
- no_usage_tables_coverage
- no_verified_uplift

## Not Claimed

- HID Usage Tables are not imported.
- Usage Tables entries are not tracked, reviewed, or verified.
- Report payload semantics are not covered.
- Firmware behavior correctness is not claimed.
- OS input stack behavior is not claimed.
- Parser/runtime behavior is not claimed.
- Product-specific HID behavior is not claimed.
