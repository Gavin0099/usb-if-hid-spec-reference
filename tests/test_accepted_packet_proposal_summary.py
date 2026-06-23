import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.generate_accepted_packet_proposal_summary import build_summary, render_markdown


ROOT = Path(__file__).resolve().parents[1]


class AcceptedPacketProposalSummaryTests(unittest.TestCase):
    def test_summary_reports_current_proposal_surface(self) -> None:
        summary = build_summary()
        self.assertEqual(summary["authority_ceiling"], "accepted_packet_proposal_summary_only")
        self.assertEqual(summary["candidate_count"], 19)
        self.assertEqual(summary["proposal_markdown_count"], 19)
        self.assertEqual(summary["proposal_json_count"], 19)
        self.assertEqual(summary["validator_checked_proposal_count"], 19)
        self.assertEqual(summary["production_accepted_packet_count"], 0)
        self.assertEqual(summary["verified_entry_count"], 0)
        self.assertIn("no_production_accepted_packet", summary["claim_ceiling"])
        self.assertTrue(any(entry["entry_id"] == "hid_get_report" for entry in summary["entries"]))

    def test_markdown_preserves_claim_ceiling_totals(self) -> None:
        markdown = render_markdown(build_summary())
        self.assertIn("> Status: proposal summary only", markdown)
        self.assertIn("- proposal JSON artifacts: 19", markdown)
        self.assertIn("- production accepted packets: 0", markdown)
        self.assertIn("- verified entries: 0", markdown)
        self.assertIn("no accepted evidence packet exists from this summary", markdown)

    def test_cli_writes_summary_under_repo_root(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as tempdir:
            temp = Path(tempdir)
            markdown_out = temp / "proposal_summary.md"
            json_out = temp / "proposal_summary.json"
            result = subprocess.run(
                [
                    sys.executable,
                    "-X",
                    "utf8",
                    "scripts/generate_accepted_packet_proposal_summary.py",
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
            self.assertEqual(data["proposal_json_count"], 19)
            self.assertEqual(data["production_accepted_packet_count"], 0)

    def test_cli_rejects_output_path_outside_repo(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            markdown_out = Path(tempdir) / "proposal_summary.md"
            result = subprocess.run(
                [
                    sys.executable,
                    "-X",
                    "utf8",
                    "scripts/generate_accepted_packet_proposal_summary.py",
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
