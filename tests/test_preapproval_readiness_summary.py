import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.generate_preapproval_readiness_summary import build_summary, render_markdown


ROOT = Path(__file__).resolve().parents[1]


class PreapprovalReadinessSummaryTests(unittest.TestCase):
    def test_summary_counts_match_current_surface(self) -> None:
        summary = build_summary()
        self.assertEqual(summary["authority_ceiling"], "preapproval_readiness_summary_only")
        self.assertEqual(summary["candidate_count"], 19)
        self.assertEqual(summary["preapproval_report_count"], 19)
        self.assertEqual(summary["production_accepted_packet_count"], 19)
        self.assertEqual(summary["verified_entry_count"], 7)
        self.assertEqual(summary["stale_preapproval_report_count"], 0)

    def test_summary_entries_include_required_gap_fields(self) -> None:
        summary = build_summary()
        by_entry = {entry["entry_id"]: entry for entry in summary["entries"]}
        get_report = by_entry["hid_get_report"]
        self.assertEqual(get_report["matrix"], "hid_class_request_matrix")
        self.assertEqual(get_report["ready_check_count"], 16)
        self.assertEqual(get_report["gap_count"], 12)
        self.assertEqual(
            get_report["missing_acceptance_gate_fields"],
            [
                "previous_packet_status",
                "checkpoint_commit",
                "validation_receipt",
                "level3_checkpoint",
                "direct_promotion",
            ],
        )
        self.assertTrue(get_report["requires_human_approval"])
        self.assertTrue(get_report["requires_validation_receipt"])
        self.assertTrue(get_report["accepted_packet_exists"])

    def test_markdown_preserves_summary_claim_ceiling(self) -> None:
        markdown = render_markdown(build_summary())
        self.assertIn("> Status: readiness summary only", markdown)
        self.assertIn("- production accepted packets: 19", markdown)
        self.assertIn("- verified entries: 7", markdown)

    def test_cli_writes_markdown_and_json_inside_repo(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as tempdir:
            temp = Path(tempdir)
            markdown_out = temp / "summary.md"
            json_out = temp / "summary.json"
            result = subprocess.run(
                [
                    sys.executable,
                    "-X",
                    "utf8",
                    "scripts/generate_preapproval_readiness_summary.py",
                    "--markdown-out",
                    str(markdown_out.relative_to(ROOT)),
                    "--json-out",
                    str(json_out.relative_to(ROOT)),
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(markdown_out.exists())
            self.assertTrue(json_out.exists())
            data = json.loads(json_out.read_text(encoding="utf-8"))
            self.assertEqual(data["preapproval_report_count"], 19)
            self.assertEqual(data["production_accepted_packet_count"], 19)

    def test_cli_writes_receipt_inside_repo(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as tempdir:
            temp = Path(tempdir)
            markdown_out = temp / "summary.md"
            json_out = temp / "summary.json"
            receipt_out = temp / "receipt.json"
            result = subprocess.run(
                [
                    sys.executable,
                    "-X",
                    "utf8",
                    "scripts/generate_preapproval_readiness_summary.py",
                    "--markdown-out",
                    str(markdown_out.relative_to(ROOT)),
                    "--json-out",
                    str(json_out.relative_to(ROOT)),
                    "--receipt-out",
                    str(receipt_out.relative_to(ROOT)),
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(receipt_out.exists())
            data = json.loads(receipt_out.read_text(encoding="utf-8"))
            self.assertEqual(data["generator"], "generate_preapproval_readiness_summary.py")
            self.assertEqual(data["candidate_count"], 19)
            self.assertEqual(data["production_accepted_packet_count"], 19)

    def test_cli_rejects_receipt_output_path_outside_repo(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            receipt_out = Path(tempdir) / "receipt.json"
            result = subprocess.run(
                [
                    sys.executable,
                    "-X",
                    "utf8",
                    "scripts/generate_preapproval_readiness_summary.py",
                    "--receipt-out",
                    str(receipt_out),
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("output path must stay under repository root", result.stderr)
            self.assertFalse(receipt_out.exists())

    def test_cli_rejects_output_path_outside_repo(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            markdown_out = Path(tempdir) / "summary.md"
            result = subprocess.run(
                [
                    sys.executable,
                    "-X",
                    "utf8",
                    "scripts/generate_preapproval_readiness_summary.py",
                    "--markdown-out",
                    str(markdown_out),
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("output path must stay under repository root", result.stderr)
            self.assertFalse(markdown_out.exists())


if __name__ == "__main__":
    unittest.main()
