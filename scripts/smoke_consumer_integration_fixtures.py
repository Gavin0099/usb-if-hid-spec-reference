#!/usr/bin/env python3
"""Smoke test the HID consumer integration contract.

Authority ceiling: consumer_integration_contract_smoke_only.
Does not validate HID semantics or upgrade scaffold claims.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_VALIDATOR = ROOT / "scripts" / "validate_hid_governed_surface_manifest.py"
FINGERPRINT_PROBE = ROOT / "scripts" / "probe_table_fingerprint.py"
REAL_MANIFEST = ROOT / "exports" / "hid_governed_surface_manifest.yaml"
REAL_BASELINE = ROOT / "evidence" / "table_fingerprint_baseline.jsonl"

RECEIPT_DIR = ROOT / "evidence" / "validation_receipts" / "consumer_integration_smoke"
RECEIPT_SUMMARY = ROOT / "evidence" / "validation_receipt_consumer_integration_smoke.json"

DRIFT_TARGET_ID = "hid_class_request_matrix"
CORRUPT_HASH = "sha256:0000000000000000000000000000000000000000000000000000000000000000"


def _run(command: list[str]) -> tuple[int, str, str]:
    result = subprocess.run(command, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


def _make_drifted_baseline(source: Path, target_id: str, corrupt_hash: str) -> Path:
    temp_dir = Path(tempfile.mkdtemp())
    destination = temp_dir / "baseline.jsonl"
    lines: list[str] = []
    for raw in source.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        entry = json.loads(line)
        if entry.get("table_id") == target_id:
            entry["content_hash"] = corrupt_hash
        lines.append(json.dumps(entry, ensure_ascii=True))
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return destination


def case_manifest_integrity_pass() -> dict:
    name = "manifest_integrity_pass"
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    receipt_path = RECEIPT_DIR / f"{name}.json"

    exit_code, stdout, stderr = _run([sys.executable, str(MANIFEST_VALIDATOR)])
    passed = exit_code == 0 and "PASS" in stdout
    result = {
        "name": name,
        "note": "validate_hid_governed_surface_manifest.py against real manifest",
        "expected_exit": 0,
        "actual_exit": exit_code,
        "expected_stdout_contains": "PASS",
        "stdout_contains_pass": "PASS" in stdout,
        "result": "PASS" if passed else "FAIL",
    }
    if not passed:
        result["stdout"] = stdout[:400]
        result["stderr"] = stderr[:200]
    receipt_path.write_text(json.dumps(result, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return result


def case_fingerprint_no_drift() -> dict:
    name = "fingerprint_no_drift"
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    receipt_path = RECEIPT_DIR / f"{name}.json"

    with tempfile.TemporaryDirectory() as temp_dir:
        receipt_out = Path(temp_dir) / "receipt.json"
        exit_code, stdout, stderr = _run([
            sys.executable,
            str(FINGERPRINT_PROBE),
            "--mode",
            "check",
            "--manifest",
            str(REAL_MANIFEST),
            "--baseline-in",
            str(REAL_BASELINE),
            "--receipt-out",
            str(receipt_out),
        ])
        probe_receipt = json.loads(receipt_out.read_text(encoding="utf-8")) if receipt_out.exists() else {}

    tables_checked = probe_receipt.get("tables_checked", -1)
    drift_count = probe_receipt.get("drift_count", -1)
    error_count = probe_receipt.get("error_count", -1)
    passed = exit_code == 0 and tables_checked == 2 and drift_count == 0 and error_count == 0
    result = {
        "name": name,
        "note": "fingerprint check on real manifest and baseline; expect 2 tables, 0 drift",
        "expected_exit": 0,
        "actual_exit": exit_code,
        "expected_tables_checked": 2,
        "actual_tables_checked": tables_checked,
        "expected_drift_count": 0,
        "actual_drift_count": drift_count,
        "expected_error_count": 0,
        "actual_error_count": error_count,
        "result": "PASS" if passed else "FAIL",
    }
    if not passed:
        result["stdout"] = stdout[:400]
        result["stderr"] = stderr[:200]
    receipt_path.write_text(json.dumps(result, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return result


def case_fingerprint_drift_detected() -> dict:
    name = "fingerprint_drift_detected"
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    receipt_path = RECEIPT_DIR / f"{name}.json"

    drifted_baseline = _make_drifted_baseline(REAL_BASELINE, DRIFT_TARGET_ID, CORRUPT_HASH)
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            receipt_out = Path(temp_dir) / "receipt.json"
            exit_code, stdout, stderr = _run([
                sys.executable,
                str(FINGERPRINT_PROBE),
                "--mode",
                "check",
                "--manifest",
                str(REAL_MANIFEST),
                "--baseline-in",
                str(drifted_baseline),
                "--receipt-out",
                str(receipt_out),
            ])
            probe_receipt = json.loads(receipt_out.read_text(encoding="utf-8")) if receipt_out.exists() else {}
    finally:
        try:
            drifted_baseline.unlink()
            drifted_baseline.parent.rmdir()
        except OSError:
            pass

    findings = probe_receipt.get("findings", [])
    drifted_ids = [finding.get("table_id") for finding in findings]
    target_named = DRIFT_TARGET_ID in drifted_ids
    target_in_stdout = DRIFT_TARGET_ID in stdout
    drift_count = probe_receipt.get("drift_count", -1)
    passed = exit_code == 1 and drift_count == 1 and target_named and target_in_stdout
    result = {
        "name": name,
        "note": f"fingerprint check with corrupted hash for {DRIFT_TARGET_ID}",
        "expected_exit": 1,
        "actual_exit": exit_code,
        "expected_drift_count": 1,
        "actual_drift_count": drift_count,
        "expected_drifted_table": DRIFT_TARGET_ID,
        "drifted_table_in_findings": target_named,
        "drifted_table_in_stdout": target_in_stdout,
        "result": "PASS" if passed else "FAIL",
    }
    if not passed:
        result["stdout"] = stdout[:400]
        result["stderr"] = stderr[:200]
        result["drifted_ids_found"] = drifted_ids
    receipt_path.write_text(json.dumps(result, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return result


def main() -> int:
    results = [
        case_manifest_integrity_pass(),
        case_fingerprint_no_drift(),
        case_fingerprint_drift_detected(),
    ]
    failed = [result for result in results if result["result"] == "FAIL"]
    summary = {
        "smoke_runner": "smoke_consumer_integration_fixtures.py",
        "authority_ceiling": "consumer_integration_contract_smoke_only",
        "total_cases": len(results),
        "failed_cases": len(failed),
        "result": "PASS" if not failed else "FAIL",
        "cases": results,
    }
    RECEIPT_SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    for result in results:
        print(f"[{result['result']}] {result['name']} -> {result['note']}")
    if failed:
        print(f"Consumer integration smoke FAILED: {len(failed)}/{len(results)} cases failed")
        return 1
    print(f"Consumer integration smoke PASSED: {len(results)}/{len(results)} cases passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
