import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_validation_receipt_index import ROOT, validate, _resolve_under_root


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


class ValidationReceiptIndexValidatorTests(unittest.TestCase):
    def _fixture(self) -> tuple[tempfile.TemporaryDirectory[str], Path, Path]:
        temp = tempfile.TemporaryDirectory(prefix="tmp_receipt_index_validator_", dir=ROOT)
        base = Path(temp.name)
        receipt_dir = base / "receipts"
        receipt = {
            "receipt_id": "source_authority",
            "result": "PASS",
            "returncode": 0,
            "claim_ceiling": "source_authority_structural_validation_only",
        }
        receipt_path = receipt_dir / "source_authority.json"
        _write_json(receipt_path, receipt)
        index = {
            "validator": "generate_validation_receipt_index.py",
            "authority_ceiling": "validation_receipt_index_only",
            "result": "PASS",
            "receipt_dir": receipt_dir.relative_to(ROOT).as_posix(),
            "checked_commands": 1,
            "pass_count": 1,
            "fail_count": 0,
            "receipts": [
                {
                    "receipt_id": "source_authority",
                    "result": "PASS",
                    "returncode": 0,
                    "claim_ceiling": "source_authority_structural_validation_only",
                    "receipt_path": receipt_path.relative_to(ROOT).as_posix(),
                    "command": ["python", "-X", "utf8", "scripts/validate_source_authority.py"],
                }
            ],
        }
        index_path = base / "index.json"
        _write_json(index_path, index)
        return temp, index_path, receipt_path

    def test_valid_index_passes(self) -> None:
        temp, index_path, _receipt_path = self._fixture()
        with temp:
            errors, receipt = validate(index_path)
        self.assertEqual(errors, [])
        self.assertEqual(receipt["result"], "PASS")

    def test_missing_receipt_file_fails(self) -> None:
        temp, index_path, receipt_path = self._fixture()
        with temp:
            receipt_path.unlink()
            errors, _receipt = validate(index_path)
        self.assertTrue(any("missing receipt file" in error for error in errors))

    def test_stale_receipt_file_fails(self) -> None:
        temp, index_path, receipt_path = self._fixture()
        with temp:
            _write_json(receipt_path.parent / "stale.json", {"receipt_id": "stale", "result": "PASS", "returncode": 0})
            errors, _receipt = validate(index_path)
        self.assertTrue(any("stale receipt file" in error for error in errors))

    def test_receipt_id_mismatch_fails(self) -> None:
        temp, index_path, receipt_path = self._fixture()
        with temp:
            data = json.loads(receipt_path.read_text(encoding="utf-8"))
            data["receipt_id"] = "wrong"
            _write_json(receipt_path, data)
            errors, _receipt = validate(index_path)
        self.assertTrue(any("does not match index" in error for error in errors))

    def test_failed_receipt_fails(self) -> None:
        temp, index_path, receipt_path = self._fixture()
        with temp:
            data = json.loads(receipt_path.read_text(encoding="utf-8"))
            data["result"] = "FAIL"
            data["returncode"] = 1
            _write_json(receipt_path, data)
            errors, _receipt = validate(index_path)
        self.assertTrue(any("file result is not PASS" in error for error in errors))
        self.assertTrue(any("file returncode is not 0" in error for error in errors))

    def test_resolve_rejects_outside_path(self) -> None:
        outside = ROOT.parent / "outside_validation_receipt_index.json"
        with self.assertRaises(ValueError):
            _resolve_under_root(str(outside), ROOT / "evidence" / "fallback.json")


if __name__ == "__main__":
    unittest.main()
