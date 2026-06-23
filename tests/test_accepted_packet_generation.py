import subprocess
import sys
import tempfile
from pathlib import Path

import unittest

from scripts.generate_accepted_packet import build_accepted_packet, write_all_accepted


ROOT = Path(__file__).resolve().parents[1]


class AcceptedPacketGenerationTests(unittest.TestCase):
    def test_build_accepted_packet_promotes_status_and_gate(self) -> None:
        accepted = build_accepted_packet(
            candidate_id="hid_get_report",
            approver="human:level3-reviewer",
            checkpoint_commit="7f5a12c",
            validation_receipt="evidence/validation_receipt_hid_get_report_accepted.json",
        )
        self.assertEqual(accepted["packet_identity"]["packet_status"], "accepted")
        self.assertEqual(accepted["approval"]["approval_record"], "approved")
        self.assertEqual(accepted["approval"]["approver"], "human:level3-reviewer")
        gate = accepted["acceptance_gate"]
        self.assertEqual(gate["previous_packet_status"], "candidate")
        self.assertEqual(gate["checkpoint_commit"], "7f5a12c")
        self.assertEqual(gate["validation_receipt"], "evidence/validation_receipt_hid_get_report_accepted.json")
        self.assertTrue(gate["level3_checkpoint"])
        self.assertFalse(gate["direct_promotion"])

    def test_build_accepted_packet_rejects_missing_approver(self) -> None:
        with self.assertRaisesRegex(ValueError, "approver"):
            build_accepted_packet(
                candidate_id="hid_get_report",
                approver="pending",
                checkpoint_commit="7f5a12c",
                validation_receipt="evidence/validation_receipt_hid_get_report_accepted.json",
            )

    def test_cli_dry_run_outputs_candidate_transition(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "-X",
                "utf8",
                "scripts/generate_accepted_packet.py",
                "--candidate",
                "hid_get_report",
                "--approver",
                "human:level3-reviewer",
                "--checkpoint-commit",
                "7f5a12c",
                "--validation-receipt",
                "evidence/validation_receipt_hid_get_report_accepted.json",
                "--candidate-dir",
                "docs/evidence/candidates",
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("acceptance_gate:", result.stdout)
        self.assertIn("packet_status: accepted", result.stdout)

    def test_cli_rejects_missing_level3_context(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "-X",
                "utf8",
                "scripts/generate_accepted_packet.py",
                "--candidate",
                "hid_get_report",
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ERROR:", result.stderr)

    def test_write_all_to_temp_dir_fails_on_stale_without_prune(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as tempdir:
            temp = Path(tempdir)
            stale = temp / "stale_accepted.yaml"
            stale.parent.mkdir(parents=True, exist_ok=True)
            stale.write_text("packet_identity: {}\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "stale accepted packet artifact"):
                write_all_accepted(
                    approver="human:level3-reviewer",
                    checkpoint_commit="7f5a12c",
                    validation_receipt="evidence/validation_receipt_all_accepted.json",
                    accepted_dir=temp,
                )

    def test_cli_all_can_write_to_temp_dir(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as tempdir:
            temp = Path(tempdir)
            count = write_all_accepted(
                approver="human:level3-reviewer",
                checkpoint_commit="7f5a12c",
                validation_receipt="evidence/validation_receipt_all_accepted.json",
                accepted_dir=temp,
                candidate_dir=ROOT / "docs" / "evidence" / "candidates",
                prune_stale=True,
            )
            self.assertEqual(count, 19)
            self.assertEqual(len(list(temp.glob("*_accepted.yaml"))), 19)

    def test_cli_rejects_output_outside_repo(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            result = subprocess.run(
                [
                    sys.executable,
                    "-X",
                    "utf8",
                    "scripts/generate_accepted_packet.py",
                    "--candidate",
                    "hid_get_report",
                    "--approver",
                    "human:level3-reviewer",
                    "--checkpoint-commit",
                    "7f5a12c",
                    "--validation-receipt",
                    "evidence/validation_receipt_hid_get_report_accepted.json",
                    "--write",
                    "--out",
                    str(Path(tempdir) / "outside_accepted.yaml"),
                    "--candidate-dir",
                    "docs/evidence/candidates",
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
