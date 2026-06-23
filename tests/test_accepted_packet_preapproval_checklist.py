import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.generate_accepted_packet_preapproval_checklist import (
    build_checklist,
    list_candidate_ids,
    render_markdown,
    stale_preapproval_reports,
)


ROOT = Path(__file__).resolve().parents[1]


class AcceptedPacketPreapprovalChecklistTests(unittest.TestCase):
    def test_get_report_checklist_reports_gaps_without_acceptance(self) -> None:
        checklist = build_checklist(candidate_id="hid_get_report")
        self.assertEqual(checklist["authority_ceiling"], "accepted_preapproval_gap_report_only")
        self.assertEqual(checklist["candidate"], "docs/evidence/candidates/hid_get_report_candidate.yaml")
        self.assertEqual(checklist["future_accepted_packet"], "docs/evidence/accepted/hid_get_report_accepted.yaml")
        self.assertIn("no_production_accepted_packet", checklist["claim_ceiling"])
        self.assertIn("no_verified_uplift", checklist["claim_ceiling"])
        self.assertTrue(any("acceptance_gate.checkpoint_commit" in gap for gap in checklist["gaps"]))
        self.assertTrue(any("human approver" in gap for gap in checklist["gaps"]))

    def test_markdown_preserves_gap_report_claim_ceiling(self) -> None:
        markdown = render_markdown(build_checklist(candidate_id="hid_get_report"))
        self.assertIn("> Status: gap report only", markdown)
        self.assertIn("- Production accepted packet created: no", markdown)
        self.assertIn("- Verified uplift: no", markdown)
        self.assertIn("no accepted evidence packet exists from this report", markdown)

    def test_cli_out_writes_report_without_creating_accepted_packet(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as tempdir:
            out = Path(tempdir) / "hid_get_report_preapproval_checklist.md"
            accepted_dir = ROOT / "docs" / "evidence" / "accepted"
            before = sorted(accepted_dir.glob("*.yaml")) if accepted_dir.exists() else []
            result = subprocess.run(
                [
                    sys.executable,
                    "-X",
                    "utf8",
                    "scripts/generate_accepted_packet_preapproval_checklist.py",
                    "--candidate",
                    "hid_get_report",
                    "--out",
                    str(out.relative_to(ROOT)),
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            after = sorted(accepted_dir.glob("*.yaml")) if accepted_dir.exists() else []
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(out.exists())
            self.assertEqual(before, after)
            self.assertIn("gap report only", out.read_text(encoding="utf-8"))

    def test_candidate_id_listing_covers_all_candidate_packets(self) -> None:
        candidate_ids = list_candidate_ids()
        self.assertEqual(len(candidate_ids), 19)
        self.assertIn("hid_get_report", candidate_ids)
        self.assertIn("hid_set_protocol", candidate_ids)
        self.assertIn("report_descriptor_reserved_item_type", candidate_ids)

    def test_cli_all_writes_all_reports_without_creating_accepted_packets(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as tempdir:
            out_dir = Path(tempdir) / "preapproval"
            accepted_dir = ROOT / "docs" / "evidence" / "accepted"
            before = sorted(accepted_dir.glob("*.yaml")) if accepted_dir.exists() else []
            result = subprocess.run(
                [
                    sys.executable,
                    "-X",
                    "utf8",
                    "scripts/generate_accepted_packet_preapproval_checklist.py",
                    "--all",
                    "--out-dir",
                    str(out_dir.relative_to(ROOT)),
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            after = sorted(accepted_dir.glob("*.yaml")) if accepted_dir.exists() else []
            reports = sorted(out_dir.glob("*_preapproval_checklist.md"))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(len(reports), 19)
            self.assertEqual(before, after)
            self.assertIn("Generated 19 pre-approval checklist report", result.stdout)
            self.assertTrue((out_dir / "hid_set_protocol_preapproval_checklist.md").exists())

    def test_cli_rejects_output_path_outside_repo(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            out = Path(tempdir) / "outside_preapproval_checklist.md"
            result = subprocess.run(
                [
                    sys.executable,
                    "-X",
                    "utf8",
                    "scripts/generate_accepted_packet_preapproval_checklist.py",
                    "--candidate",
                    "hid_get_report",
                    "--out",
                    str(out),
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("output path must stay under repository root", result.stderr)
            self.assertFalse(out.exists())

    def test_cli_all_rejects_stale_preapproval_report_without_prune(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as tempdir:
            out_dir = Path(tempdir) / "preapproval"
            out_dir.mkdir()
            stale = out_dir / "stale_entry_preapproval_checklist.md"
            stale.write_text("stale\n", encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    "-X",
                    "utf8",
                    "scripts/generate_accepted_packet_preapproval_checklist.py",
                    "--all",
                    "--out-dir",
                    str(out_dir.relative_to(ROOT)),
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("stale pre-approval report", result.stderr)
            self.assertTrue(stale.exists())

    def test_cli_all_prunes_stale_preapproval_report_when_requested(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as tempdir:
            out_dir = Path(tempdir) / "preapproval"
            out_dir.mkdir()
            stale = out_dir / "stale_entry_preapproval_checklist.md"
            stale.write_text("stale\n", encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    "-X",
                    "utf8",
                    "scripts/generate_accepted_packet_preapproval_checklist.py",
                    "--all",
                    "--prune-stale",
                    "--out-dir",
                    str(out_dir.relative_to(ROOT)),
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            reports = sorted(out_dir.glob("*_preapproval_checklist.md"))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(stale.exists())
            self.assertEqual(len(reports), 19)

    def test_current_preapproval_surface_has_no_stale_reports(self) -> None:
        self.assertEqual(stale_preapproval_reports(), [])

    def test_fixture_candidate_missing_validation_shows_gap(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            candidate_dir = root / "docs" / "evidence" / "candidates"
            accepted_dir = root / "docs" / "evidence" / "accepted"
            schema_dir = root / "contract"
            candidate_dir.mkdir(parents=True)
            accepted_dir.mkdir(parents=True)
            schema_dir.mkdir()
            shutil.copy(
                ROOT / "docs" / "evidence" / "candidates" / "hid_get_report_candidate.yaml",
                candidate_dir / "hid_get_report_candidate.yaml",
            )
            shutil.copy(ROOT / "contract" / "evidence_packet_schema.yaml", schema_dir / "evidence_packet_schema.yaml")
            candidate = candidate_dir / "hid_get_report_candidate.yaml"
            candidate.write_text(
                candidate.read_text(encoding="utf-8").replace(
                    "  unit_tests: python -m unittest discover -s tests\n",
                    "",
                ),
                encoding="utf-8",
            )
            checklist = build_checklist(
                candidate_id="hid_get_report",
                candidate_dir=candidate_dir,
                accepted_dir=accepted_dir,
                schema_path=schema_dir / "evidence_packet_schema.yaml",
            )
            self.assertTrue(any("validation command missing: unit_tests" == gap for gap in checklist["gaps"]))


if __name__ == "__main__":
    unittest.main()
