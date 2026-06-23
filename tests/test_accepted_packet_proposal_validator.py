import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.validate_accepted_packet_proposals import validate


ROOT = Path(__file__).resolve().parents[1]


class AcceptedPacketProposalValidatorTests(unittest.TestCase):
    def _fixture_root(self) -> tempfile.TemporaryDirectory[str]:
        fixture = tempfile.TemporaryDirectory()
        root = Path(fixture.name)
        proposal_dir = root / "evidence" / "accepted_proposals"
        proposal_dir.mkdir(parents=True)
        (root / "docs" / "evidence" / "candidates").mkdir(parents=True)
        (root / "docs" / "evidence" / "preapproval").mkdir(parents=True)
        shutil.copy(
            ROOT / "evidence" / "accepted_proposals" / "hid_get_report_accepted_proposal.json",
            proposal_dir / "hid_get_report_accepted_proposal.json",
        )
        shutil.copy(
            ROOT / "docs" / "evidence" / "candidates" / "hid_get_report_candidate.yaml",
            root / "docs" / "evidence" / "candidates" / "hid_get_report_candidate.yaml",
        )
        shutil.copy(
            ROOT / "docs" / "evidence" / "preapproval" / "hid_get_report_preapproval_checklist.md",
            root / "docs" / "evidence" / "preapproval" / "hid_get_report_preapproval_checklist.md",
        )
        return fixture

    def _proposal_path(self, root: Path) -> Path:
        return root / "evidence" / "accepted_proposals" / "hid_get_report_accepted_proposal.json"

    def _edit_proposal(self, root: Path, key_path: tuple[str, ...], value) -> None:
        path = self._proposal_path(root)
        data = json.loads(path.read_text(encoding="utf-8"))
        target = data
        for key in key_path[:-1]:
            target = target[key]
        target[key_path[-1]] = value
        path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")

    def test_current_proposals_are_valid(self) -> None:
        errors, receipt = validate()
        self.assertEqual(errors, [])
        self.assertEqual(receipt["result"], "PASS")
        self.assertEqual(receipt["checked_proposal_count"], 1)
        self.assertIn("evidence/accepted_proposals/hid_get_report_accepted_proposal.json", receipt["checked_proposals"])

    def test_proposal_with_accepted_status_fails(self) -> None:
        with self._fixture_root() as fixture:
            root = Path(fixture)
            self._edit_proposal(root, ("proposal_status",), "accepted")
            errors, receipt = validate(proposal_dir=root / "evidence" / "accepted_proposals", root=root)
            self.assertEqual(receipt["result"], "FAIL")
            self.assertTrue(any("proposal_status" in error for error in errors))

    def test_proposal_with_accepted_packet_created_fails(self) -> None:
        with self._fixture_root() as fixture:
            root = Path(fixture)
            self._edit_proposal(root, ("production_accepted_packet_created",), True)
            errors, receipt = validate(proposal_dir=root / "evidence" / "accepted_proposals", root=root)
            self.assertEqual(receipt["result"], "FAIL")
            self.assertTrue(any("production_accepted_packet_created" in error for error in errors))

    def test_proposal_with_verified_uplift_fails(self) -> None:
        with self._fixture_root() as fixture:
            root = Path(fixture)
            self._edit_proposal(root, ("verified_uplift",), True)
            errors, receipt = validate(proposal_dir=root / "evidence" / "accepted_proposals", root=root)
            self.assertEqual(receipt["result"], "FAIL")
            self.assertTrue(any("verified_uplift" in error for error in errors))

    def test_proposal_future_accepted_path_exists_fails(self) -> None:
        with self._fixture_root() as fixture:
            root = Path(fixture)
            accepted = root / "docs" / "evidence" / "accepted" / "hid_get_report_accepted.yaml"
            accepted.parent.mkdir(parents=True)
            accepted.write_text("packet_identity:\n  packet_status: accepted\n", encoding="utf-8")
            errors, receipt = validate(proposal_dir=root / "evidence" / "accepted_proposals", root=root)
            self.assertEqual(receipt["result"], "FAIL")
            self.assertTrue(any("future accepted packet path must not exist" in error for error in errors))

    def test_proposal_gate_checkpoint_must_remain_placeholder(self) -> None:
        with self._fixture_root() as fixture:
            root = Path(fixture)
            self._edit_proposal(root, ("required_level3_acceptance_gate", "checkpoint_commit"), "abc1234")
            errors, receipt = validate(proposal_dir=root / "evidence" / "accepted_proposals", root=root)
            self.assertEqual(receipt["result"], "FAIL")
            self.assertTrue(any("checkpoint_commit must remain a TBD placeholder" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
