import tempfile
import unittest
from pathlib import Path

from scripts.validate_memory_records import validate


class MemoryRecordsTests(unittest.TestCase):
    def test_current_memory_records_are_warning_only(self) -> None:
        warnings, receipt = validate()
        self.assertEqual(receipt["validator"], "validate_memory_records.py")
        self.assertIn(receipt["result"], {"PASS", "PASS_WITH_WARNINGS"})
        if warnings:
            self.assertGreaterEqual(receipt["warning_count"], 1)

    def test_no_commit_memory_entry_warns(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "2026-06-18.md").write_text(
                "# 2026-06-18\n\n"
                "## Example\n\n"
                "session_id: example\n\n"
                "commit_hash: NO_COMMIT\n",
                encoding="utf-8",
            )

            warnings, receipt = validate(root)

        self.assertEqual(receipt["result"], "PASS_WITH_WARNINGS")
        self.assertTrue(any("NO_COMMIT" in warning for warning in warnings))
        self.assertIn("memory_unbound_commit", {finding["code"] for finding in receipt["findings"]})

    def test_bound_memory_entry_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "2026-06-18.md").write_text(
                "# 2026-06-18\n\n"
                "## Example\n\n"
                "session_id: example\n\n"
                "commit_hash: abc1234\n",
                encoding="utf-8",
            )

            warnings, receipt = validate(root)

        self.assertEqual(warnings, [])
        self.assertEqual(receipt["result"], "PASS")
        self.assertEqual(receipt["bound_commits"], ["abc1234"])


if __name__ == "__main__":
    unittest.main()
