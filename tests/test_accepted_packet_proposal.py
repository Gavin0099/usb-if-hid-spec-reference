import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.generate_accepted_packet_proposal import build_proposal, render_markdown, write_all_proposals


ROOT = Path(__file__).resolve().parents[1]


class AcceptedPacketProposalTests(unittest.TestCase):
    def test_get_report_proposal_is_proposal_only(self) -> None:
        proposal = build_proposal("hid_get_report")
        self.assertEqual(proposal["authority_ceiling"], "accepted_packet_proposal_only")
        self.assertEqual(proposal["proposal_status"], "proposal_only")
        self.assertEqual(proposal["candidate"], "docs/evidence/candidates/hid_get_report_candidate.yaml")
        self.assertEqual(proposal["future_accepted_packet"], "docs/evidence/accepted/hid_get_report_accepted.yaml")
        self.assertIs(proposal["production_accepted_packet_created"], False)
        self.assertIs(proposal["verified_uplift"], False)
        self.assertEqual(proposal["governed_entry"]["entry_id"], "hid_get_report")
        self.assertIn("no_production_accepted_packet", proposal["claim_ceiling"])
        self.assertIn("no_verified_uplift", proposal["claim_ceiling"])

    def test_get_report_proposal_has_required_acceptance_gate(self) -> None:
        proposal = build_proposal("hid_get_report")
        gate = proposal["required_level3_acceptance_gate"]
        self.assertEqual(gate["previous_packet_status"], "candidate")
        self.assertEqual(gate["checkpoint_commit"], "TBD_LEVEL3_ACCEPTED_PACKET_COMMIT")
        self.assertEqual(gate["validation_receipt"], "TBD_LEVEL3_VALIDATION_RECEIPT")
        self.assertIs(gate["level3_checkpoint"], True)
        self.assertIs(gate["direct_promotion"], False)
        self.assertTrue(any("validate_evidence_packet_schema.py" in item for item in proposal["required_validators"]))

    def test_markdown_preserves_proposal_claim_ceiling(self) -> None:
        markdown = render_markdown(build_proposal("hid_get_report"))
        self.assertIn("> Status: proposal only", markdown)
        self.assertIn("- Production accepted packet created: no", markdown)
        self.assertIn("- Verified uplift: no", markdown)
        self.assertIn("no accepted evidence packet exists from this proposal", markdown)

    def test_cli_writes_proposal_without_creating_accepted_packet(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as tempdir:
            temp = Path(tempdir)
            markdown_out = temp / "proposal.md"
            json_out = temp / "proposal.json"
            accepted_dir = ROOT / "docs" / "evidence" / "accepted"
            before = sorted(accepted_dir.glob("*.yaml")) if accepted_dir.exists() else []
            result = subprocess.run(
                [
                    sys.executable,
                    "-X",
                    "utf8",
                    "scripts/generate_accepted_packet_proposal.py",
                    "--candidate",
                    "hid_get_report",
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
            after = sorted(accepted_dir.glob("*.yaml")) if accepted_dir.exists() else []
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(before, after)
            self.assertTrue(markdown_out.exists())
            self.assertTrue(json_out.exists())
            data = json.loads(json_out.read_text(encoding="utf-8"))
            self.assertEqual(data["proposal_status"], "proposal_only")
            self.assertFalse(data["production_accepted_packet_created"])

    def test_cli_rejects_output_path_outside_repo(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            markdown_out = Path(tempdir) / "proposal.md"
            result = subprocess.run(
                [
                    sys.executable,
                    "-X",
                    "utf8",
                    "scripts/generate_accepted_packet_proposal.py",
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

    def test_write_all_proposals_creates_batch_without_accepted_packets(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as tempdir:
            temp = Path(tempdir)
            markdown_dir = temp / "docs_proposals"
            json_dir = temp / "json_proposals"
            accepted_dir = ROOT / "docs" / "evidence" / "accepted"
            before = sorted(accepted_dir.glob("*.yaml")) if accepted_dir.exists() else []
            count = write_all_proposals(markdown_dir=markdown_dir, json_dir=json_dir)
            after = sorted(accepted_dir.glob("*.yaml")) if accepted_dir.exists() else []
            self.assertEqual(count, 19)
            self.assertEqual(len(list(markdown_dir.glob("*_accepted_proposal.md"))), 19)
            self.assertEqual(len(list(json_dir.glob("*_accepted_proposal.json"))), 19)
            self.assertEqual(before, after)
            sample = json.loads((json_dir / "hid_set_report_accepted_proposal.json").read_text(encoding="utf-8"))
            self.assertEqual(sample["proposal_status"], "proposal_only")
            self.assertEqual(sample["candidate"], "docs/evidence/candidates/hid_set_report_candidate.yaml")
            self.assertFalse(sample["production_accepted_packet_created"])
            self.assertFalse(sample["verified_uplift"])

    def test_write_all_proposals_fails_on_stale_artifact(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as tempdir:
            temp = Path(tempdir)
            markdown_dir = temp / "docs_proposals"
            json_dir = temp / "json_proposals"
            markdown_dir.mkdir()
            stale = markdown_dir / "stale_accepted_proposal.md"
            stale.write_text("# stale\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "stale accepted-packet proposal artifact"):
                write_all_proposals(markdown_dir=markdown_dir, json_dir=json_dir)
            self.assertTrue(stale.exists())

    def test_write_all_proposals_prunes_stale_artifact_when_requested(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as tempdir:
            temp = Path(tempdir)
            markdown_dir = temp / "docs_proposals"
            json_dir = temp / "json_proposals"
            json_dir.mkdir()
            stale = json_dir / "stale_accepted_proposal.json"
            stale.write_text("{}\n", encoding="utf-8")
            count = write_all_proposals(markdown_dir=markdown_dir, json_dir=json_dir, prune_stale=True)
            self.assertEqual(count, 19)
            self.assertFalse(stale.exists())
            self.assertEqual(len(list(json_dir.glob("*_accepted_proposal.json"))), 19)

    def test_cli_all_rejects_output_directory_outside_repo(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            result = subprocess.run(
                [
                    sys.executable,
                    "-X",
                    "utf8",
                    "scripts/generate_accepted_packet_proposal.py",
                    "--all",
                    "--markdown-dir",
                    str(Path(tempdir) / "docs_proposals"),
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("output path must stay under repository root", result.stderr)


if __name__ == "__main__":
    unittest.main()
