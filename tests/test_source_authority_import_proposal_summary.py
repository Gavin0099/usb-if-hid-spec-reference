import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.generate_source_authority_import_proposal_summary import build_summary, render_markdown


ROOT = Path(__file__).resolve().parents[1]


class SourceAuthorityImportProposalSummaryTests(unittest.TestCase):
    def test_summary_reports_current_usage_tables_proposal_surface(self) -> None:
        summary = build_summary()
        self.assertEqual(summary["authority_ceiling"], "source_authority_import_proposal_summary_only")
        self.assertEqual(summary["proposal_count"], 1)
        self.assertEqual(summary["checklist_count"], 1)
        self.assertEqual(summary["execution_plan_count"], 1)
        self.assertEqual(summary["source_identity_packet_count"], 1)
        self.assertEqual(summary["source_authority_status"], "not_imported")
        self.assertEqual(summary["source_registry_section_count"], 0)
        self.assertEqual(summary["production_source_authority_change_count"], 0)
        self.assertEqual(summary["usage_tables_governed_entry_count"], 0)
        self.assertEqual(summary["verified_uplift_count"], 0)
        self.assertTrue(summary["ready_for_level3_import"])
        self.assertEqual(summary["proposals"][0]["source_id"], "hid_usage_tables")

    def test_markdown_preserves_claim_ceiling_totals(self) -> None:
        markdown = render_markdown(build_summary())
        self.assertIn("> Status: proposal summary only", markdown)
        self.assertIn("- source authority status: `not_imported`", markdown)
        self.assertIn("- execution plans: 1", markdown)
        self.assertIn("- source identity packets: 1", markdown)
        self.assertIn("- Usage Tables governed entries: 0", markdown)
        self.assertIn("- verified uplift count: 0", markdown)
        self.assertIn("- HID Usage Tables are not imported", markdown)

    def test_cli_writes_summary_under_repo_root(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as tempdir:
            temp = Path(tempdir)
            markdown_out = temp / "source_summary.md"
            json_out = temp / "source_summary.json"
            result = subprocess.run(
                [
                    sys.executable,
                    "-X",
                    "utf8",
                    "scripts/generate_source_authority_import_proposal_summary.py",
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
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue(markdown_out.exists())
            self.assertTrue(json_out.exists())
            data = json.loads(json_out.read_text(encoding="utf-8"))
            self.assertEqual(data["proposal_count"], 1)
            self.assertEqual(data["source_authority_status"], "not_imported")

    def test_cli_rejects_output_path_outside_repo(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            markdown_out = Path(tempdir) / "source_summary.md"
            result = subprocess.run(
                [
                    sys.executable,
                    "-X",
                    "utf8",
                    "scripts/generate_source_authority_import_proposal_summary.py",
                    "--markdown-out",
                    str(markdown_out),
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("path must stay under repository root", result.stderr)
            self.assertFalse(markdown_out.exists())

    def test_cli_assert_match_passes_on_committed_summary(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "-X",
                "utf8",
                "scripts/generate_source_authority_import_proposal_summary.py",
                "--assert-match",
                "evidence/source_authority_proposals/summary.json",
                "--check-only",
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(
            "PASS source authority import proposal summary matches evidence/source_authority_proposals/summary.json",
            result.stdout,
        )

    def test_cli_assert_match_detects_tampered_summary(self) -> None:
        source = ROOT / "evidence" / "source_authority_proposals" / "summary.json"
        with tempfile.TemporaryDirectory(dir=ROOT) as tempdir:
            temp_summary = Path(tempdir) / "summary.json"
            shutil.copy(source, temp_summary)
            data = json.loads(temp_summary.read_text(encoding="utf-8"))
            data["proposal_count"] = 999
            temp_summary.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    "-X",
                    "utf8",
                    "scripts/generate_source_authority_import_proposal_summary.py",
                    "--assert-match",
                    str(temp_summary.relative_to(ROOT)),
                    "--check-only",
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("summary field mismatch proposal_count", result.stdout + result.stderr)

    def test_cli_assert_match_writes_receipt(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as tempdir:
            receipt = Path(tempdir) / "summary_receipt.json"
            result = subprocess.run(
                [
                    sys.executable,
                    "-X",
                    "utf8",
                    "scripts/generate_source_authority_import_proposal_summary.py",
                    "--assert-match",
                    "evidence/source_authority_proposals/summary.json",
                    "--check-only",
                    "--receipt-out",
                    str(receipt.relative_to(ROOT)),
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(receipt.read_text(encoding="utf-8"))
            self.assertEqual(payload["result"], "PASS")
            self.assertEqual(payload["error_count"], 0)


if __name__ == "__main__":
    unittest.main()
