# Consumer Integration Contract

> **Status**: Active
> **Established**: 2026-06-18
> **Claim ceiling**: scaffold_identity_reference_only

## Entry Point

The canonical entry point for consuming repo integration is:

```text
exports/hid_governed_surface_manifest.yaml
```

This manifest is the governed truth index for this repository's current HID
reference scaffold. It covers:

- HID 1.11 class request scaffold entries: 6
- HID 1.11 descriptor field reviewed identity entries: 7
- HID 1.11 report descriptor item reviewed identity entries: 6
- Total tracked entries: 19
- Total scaffold entries: 0
- Reviewed entries: 19
- Verified entries: 0
- Evidence packets: 0

Consuming repos should not read individual YAML matrices directly as their
primary contract. The manifest is the stable consumer-facing index; individual
tables are its implementation.

## Two-Step Integration Check

Before using any governed surface output, a consuming repo CI should run both
checks in sequence:

### Step 1 - Manifest Structural Integrity

```powershell
python scripts\validate_hid_governed_surface_manifest.py
```

Expected output:

```text
PASS: hid_governed_surface_manifest validation
  manifest_id: hid_governed_surface_manifest
  governed_tables: 3 (hid11=3)
  hid11: state=scaffold tracked=19 scaffold=0 verified=0 reviewed=19
```

### Step 2 - Table Content Drift Detection

```powershell
python scripts\probe_table_fingerprint.py --mode check `
  --manifest exports\hid_governed_surface_manifest.yaml `
  --baseline-in evidence\table_fingerprint_baseline.jsonl
```

Expected output:

```text
Table fingerprint check PASSED: 3 table(s), 0 drift
```

Both checks must pass before treating the scaffold surface as stable.

## Allowed Usage

| Use | Description |
|---|---|
| Table drift detection | Detect whether governed HID YAML matrices changed since the last known-good baseline |
| Request identity scaffold lookup | Look up HID class request name, bRequest, direction, request type, and recipient |
| Descriptor field identity scaffold lookup | Look up HID descriptor field names listed in the scaffold matrix |
| Report descriptor item identity scaffold lookup | Look up Section 6.2.2 report descriptor item shells listed in the scaffold matrix |
| Claim boundary lookup | Read `scaffold_scope`, `verified_scope`, and manifest `claim_ceiling` before using an entry |

## Forbidden Usage

| Forbidden Use | Why |
|---|---|
| Firmware compliance truth | Scaffold entries do not prove firmware implements HID correctly |
| HID semantic completeness | The current surface is not a complete HID 1.11 interpretation |
| Report payload semantics | Report data meaning and HID Usage Tables are not imported |
| Report descriptor parser behavior | Descriptor field identity does not prove parser behavior |
| Boot protocol runtime behavior | Boot/report protocol runtime behavior is not verified |
| Idle handling correctness | Idle request identity does not prove firmware idle-rate handling |
| OS input stack behavior | Host operating-system behavior is excluded unless separately sourced |
| Overriding consuming repo facts | Confirmed project facts win over this reference |

## Failure Interpretation

### Failure mode 1: Manifest validator FAIL

```text
FAIL: hid_governed_surface_manifest validation
  R8: hid11 tracked sum mismatch: ...
```

Meaning: the export contract is broken. A governed matrix count, path, state, or
required field changed without updating the manifest.

Required action: do not use the governed surface output. Review the matrix diff
and update the manifest only if the change is authorized.

### Failure mode 2: Fingerprint drift FAIL

```text
Table fingerprint check DRIFT_DETECTED: 1 drift, 0 error(s)
  [drift] hid_class_request_matrix: sha256:abc... -> sha256:def...
```

Meaning: a governed table changed since the recorded baseline. This does not
prove the change is wrong; it proves review is required.

Required action: review the table diff. If authorized, regenerate the baseline:

```powershell
python scripts\probe_table_fingerprint.py --mode baseline `
  --manifest exports\hid_governed_surface_manifest.yaml `
  --baseline-out evidence\table_fingerprint_baseline.jsonl

python scripts\probe_table_fingerprint.py --mode compact `
  --baseline-in evidence\table_fingerprint_baseline.jsonl `
  --baseline-out evidence\table_fingerprint_baseline.jsonl
```

## Governance Layer Model

| Layer | Status | Description |
|---|---|---|
| L1 - script exists | Active | Validator scripts present in `scripts/` |
| L2 - contract declared | Active | This document and `exports/hid_governed_surface_manifest.yaml` |
| L3 - CI runs | Advisory | Validators can run in consuming repo CI |
| L4 - framework invokes | Not claimed | AI governance runtime invocation is not required |
| L5 - consumer enforces | Consumer-owned | Blocking enforcement belongs to consuming repos |

## What This Contract Does Not Establish

- Any HID entry is verified.
- HID semantic coverage is complete.
- HID Usage Tables are imported.
- Report descriptor semantics are verified.
- Firmware behavior or compliance is established.
- Host OS input-stack behavior is established.
- USB-IF certification evidence exists.
