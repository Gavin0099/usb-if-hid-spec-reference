import json
import tempfile
import unittest
from pathlib import Path

from scripts import probe_table_fingerprint


class ProbeTableFingerprintTests(unittest.TestCase):
    def test_check_mode_detects_current_baseline_as_clean(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            receipt = Path(temp_dir) / "receipt.json"
            exit_code = probe_table_fingerprint.main_with_args([
                "--mode",
                "check",
                "--manifest",
                str(probe_table_fingerprint.DEFAULT_MANIFEST),
                "--baseline-in",
                str(probe_table_fingerprint.DEFAULT_BASELINE),
                "--receipt-out",
                str(receipt),
            ])
            self.assertEqual(exit_code, 0)
            data = json.loads(receipt.read_text(encoding="utf-8"))
            self.assertEqual(data["result"], "PASS")
            self.assertEqual(data["tables_checked"], 3)


if __name__ == "__main__":
    unittest.main()
