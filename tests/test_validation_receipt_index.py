import unittest
from pathlib import Path

from scripts.generate_validation_receipt_index import (
    ROOT,
    build_index,
    render_markdown,
    _resolve_under_root,
)


class ValidationReceiptIndexTests(unittest.TestCase):
    def test_resolve_under_root_rejects_outside_path(self) -> None:
        outside = Path(ROOT).parent / "outside_receipt.json"
        with self.assertRaises(ValueError):
            _resolve_under_root(str(outside), ROOT / "evidence" / "fallback.json")

    def test_build_index_summarizes_pass_and_fail_counts(self) -> None:
        receipts = [
            {
                "receipt_id": "one",
                "result": "PASS",
                "returncode": 0,
                "claim_ceiling": "one_only",
                "receipt_path": "evidence/validation_receipts/hid_current_gate/one.json",
                "command": ["python", "one.py"],
            },
            {
                "receipt_id": "two",
                "result": "FAIL",
                "returncode": 1,
                "claim_ceiling": "two_only",
                "receipt_path": "evidence/validation_receipts/hid_current_gate/two.json",
                "command": ["python", "two.py"],
            },
        ]

        index = build_index(receipts, receipt_dir=ROOT / "evidence" / "validation_receipts" / "hid_current_gate")

        self.assertEqual(index["result"], "FAIL")
        self.assertEqual(index["checked_commands"], 2)
        self.assertEqual(index["pass_count"], 1)
        self.assertEqual(index["fail_count"], 1)
        self.assertIn("no_verified_uplift_by_receipt_index", index["claim_ceiling"])

    def test_render_markdown_lists_receipts_and_non_claims(self) -> None:
        index = {
            "result": "PASS",
            "checked_commands": 1,
            "pass_count": 1,
            "fail_count": 0,
            "receipt_dir": "evidence/validation_receipts/hid_current_gate",
            "receipts": [
                {
                    "receipt_id": "source_authority",
                    "result": "PASS",
                    "claim_ceiling": "source_authority_structural_validation_only",
                    "receipt_path": "evidence/validation_receipts/hid_current_gate/source_authority.json",
                }
            ],
            "not_claimed": ["firmware behavior correctness"],
        }

        markdown = render_markdown(index)

        self.assertIn("| `source_authority` | PASS |", markdown)
        self.assertIn("validation receipt index only", markdown)
        self.assertIn("firmware behavior correctness", markdown)


if __name__ == "__main__":
    unittest.main()
