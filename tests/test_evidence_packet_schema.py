import unittest
import shutil
import tempfile
from pathlib import Path

from scripts.validate_evidence_packet_schema import validate


ROOT = Path(__file__).resolve().parents[1]


class EvidencePacketSchemaTests(unittest.TestCase):
    def test_verified_preflight_schema_is_valid(self) -> None:
        errors, receipt = validate()
        self.assertEqual(errors, [])
        self.assertEqual(receipt["result"], "PASS")
        self.assertEqual(receipt["authority_ceiling"], "verified_preflight_contract_only")
        self.assertEqual(receipt["verified_gate"]["review_level"], 3)
        self.assertEqual(receipt["verified_gate"]["required_packet_status"], "accepted")
        self.assertEqual(receipt["verified_gate"]["acceptance_workflow"]["required_previous_status"], "candidate")
        self.assertEqual(receipt["verified_gate"]["acceptance_workflow"]["required_approval_record"], "approved")
        self.assertIs(receipt["verified_gate"]["acceptance_workflow"]["required_validation_receipt"], True)
        self.assertGreaterEqual(len(receipt["checked_shell_packets"]), 6)
        self.assertIn("hid_1_11:7.2", receipt["checked_source_authority_bindings"])
        self.assertEqual(
            receipt["checked_matrix_source_refs"]["hid_class_request_matrix"],
            ["hid_1_11:7.2"],
        )
        self.assertEqual(len(receipt["checked_candidate_packets"]), 19)
        for candidate in (
            "docs/evidence/candidates/hid_get_report_candidate.yaml",
            "docs/evidence/candidates/hid_set_report_candidate.yaml",
            "docs/evidence/candidates/hid_get_idle_candidate.yaml",
            "docs/evidence/candidates/hid_set_idle_candidate.yaml",
            "docs/evidence/candidates/hid_get_protocol_candidate.yaml",
            "docs/evidence/candidates/hid_set_protocol_candidate.yaml",
            "docs/evidence/candidates/hid_bLength_candidate.yaml",
            "docs/evidence/candidates/hid_bDescriptorType_candidate.yaml",
            "docs/evidence/candidates/hid_bcdHID_candidate.yaml",
            "docs/evidence/candidates/hid_bCountryCode_candidate.yaml",
            "docs/evidence/candidates/hid_bNumDescriptors_candidate.yaml",
            "docs/evidence/candidates/hid_bDescriptorType_subordinate_candidate.yaml",
            "docs/evidence/candidates/hid_wDescriptorLength_candidate.yaml",
            "docs/evidence/candidates/report_descriptor_short_item_prefix_candidate.yaml",
            "docs/evidence/candidates/report_descriptor_long_item_prefix_candidate.yaml",
            "docs/evidence/candidates/report_descriptor_main_item_type_candidate.yaml",
            "docs/evidence/candidates/report_descriptor_global_item_type_candidate.yaml",
            "docs/evidence/candidates/report_descriptor_local_item_type_candidate.yaml",
            "docs/evidence/candidates/report_descriptor_reserved_item_type_candidate.yaml",
        ):
            self.assertIn(candidate, receipt["checked_candidate_packets"])

    def _fixture_root(self) -> tempfile.TemporaryDirectory[str]:
        fixture = tempfile.TemporaryDirectory()
        root = Path(fixture.name)
        (root / "contract").mkdir()
        (root / "data").mkdir()
        (root / "docs" / "evidence" / "candidates").mkdir(parents=True)
        shutil.copy(ROOT / "contract" / "evidence_packet_schema.yaml", root / "contract" / "evidence_packet_schema.yaml")
        shutil.copy(ROOT / "data" / "source_authority.yaml", root / "data" / "source_authority.yaml")
        shutil.copy(ROOT / "data" / "hid_class_request_matrix.yaml", root / "data" / "hid_class_request_matrix.yaml")
        shutil.copy(
            ROOT / "docs" / "evidence" / "candidates" / "hid_get_report_candidate.yaml",
            root / "docs" / "evidence" / "candidates" / "hid_get_report_candidate.yaml",
        )
        return fixture

    def _validate_fixture(self, root: Path):
        return validate(
            schema_path=root / "contract" / "evidence_packet_schema.yaml",
            source_authority_path=root / "data" / "source_authority.yaml",
            evidence_dir=root / "docs" / "evidence",
            candidate_dir=root / "docs" / "evidence" / "candidates",
            matrix_paths={
                "hid_class_request_matrix": root / "data" / "hid_class_request_matrix.yaml",
            },
        )

    def test_candidate_with_unknown_source_id_fails(self) -> None:
        with self._fixture_root() as fixture:
            candidate = Path(fixture) / "docs" / "evidence" / "candidates" / "hid_get_report_candidate.yaml"
            candidate.write_text(
                candidate.read_text(encoding="utf-8").replace("source_id: hid_1_11", "source_id: hid_fake_1_11"),
                encoding="utf-8",
            )
            errors, receipt = self._validate_fixture(Path(fixture))
            self.assertEqual(receipt["result"], "FAIL")
            self.assertTrue(any("current imported source authority" in error for error in errors))

    def test_candidate_with_wrong_source_section_fails(self) -> None:
        with self._fixture_root() as fixture:
            candidate = Path(fixture) / "docs" / "evidence" / "candidates" / "hid_get_report_candidate.yaml"
            candidate.write_text(
                candidate.read_text(encoding="utf-8").replace('source_section: "7.2"', 'source_section: "6.2.1"'),
                encoding="utf-8",
            )
            errors, receipt = self._validate_fixture(Path(fixture))
            self.assertEqual(receipt["result"], "FAIL")
            self.assertTrue(any("hid_class_request_matrix.source_refs" in error for error in errors))

    def test_candidate_conflicting_matrix_source_ref_fails(self) -> None:
        with self._fixture_root() as fixture:
            matrix = Path(fixture) / "data" / "hid_class_request_matrix.yaml"
            matrix.write_text(
                matrix.read_text(encoding="utf-8").replace('section: "7.2"', 'section: "6.2.1"', 1),
                encoding="utf-8",
            )
            errors, receipt = self._validate_fixture(Path(fixture))
            self.assertEqual(receipt["result"], "FAIL")
            self.assertTrue(any("hid_class_request_matrix.source_refs" in error for error in errors))

    def test_candidate_with_accepted_status_fails(self) -> None:
        with self._fixture_root() as fixture:
            candidate = Path(fixture) / "docs" / "evidence" / "candidates" / "hid_get_report_candidate.yaml"
            candidate.write_text(
                candidate.read_text(encoding="utf-8").replace("packet_status: candidate", "packet_status: accepted"),
                encoding="utf-8",
            )
            errors, receipt = self._validate_fixture(Path(fixture))
            self.assertEqual(receipt["result"], "FAIL")
            self.assertTrue(any("packet_identity.packet_status must be candidate" in error for error in errors))

    def test_candidate_with_non_pending_approval_fails(self) -> None:
        with self._fixture_root() as fixture:
            candidate = Path(fixture) / "docs" / "evidence" / "candidates" / "hid_get_report_candidate.yaml"
            candidate.write_text(
                candidate.read_text(encoding="utf-8").replace("approval_record: pending", "approval_record: approved"),
                encoding="utf-8",
            )
            errors, receipt = self._validate_fixture(Path(fixture))
            self.assertEqual(receipt["result"], "FAIL")
            self.assertTrue(any("approval_record must remain pending" in error for error in errors))

    def test_candidate_with_verified_current_claim_level_fails(self) -> None:
        with self._fixture_root() as fixture:
            candidate = Path(fixture) / "docs" / "evidence" / "candidates" / "hid_get_report_candidate.yaml"
            candidate.write_text(
                candidate.read_text(encoding="utf-8").replace("current_claim_level: reviewed", "current_claim_level: verified"),
                encoding="utf-8",
            )
            errors, receipt = self._validate_fixture(Path(fixture))
            self.assertEqual(receipt["result"], "FAIL")
            self.assertTrue(any("current_claim_level does not match governed entry" in error for error in errors))

    def test_schema_missing_acceptance_workflow_fails(self) -> None:
        with self._fixture_root() as fixture:
            schema = Path(fixture) / "contract" / "evidence_packet_schema.yaml"
            schema.write_text(
                schema.read_text(encoding="utf-8").replace(
                    "  acceptance_workflow:\n"
                    "    required_previous_status: candidate\n"
                    "    required_approval_record: approved\n"
                    "    required_approver: human\n"
                    "    required_checkpoint_commit: true\n"
                    "    required_validation_receipt: true\n"
                    "    required_level3_checkpoint: true\n"
                    "    forbidden_direct_promotion: true\n",
                    "",
                ),
                encoding="utf-8",
            )
            errors, receipt = self._validate_fixture(Path(fixture))
            self.assertEqual(receipt["result"], "FAIL")
            self.assertTrue(any("acceptance_workflow" in error for error in errors))

    def test_schema_with_weak_acceptance_workflow_fails(self) -> None:
        with self._fixture_root() as fixture:
            schema = Path(fixture) / "contract" / "evidence_packet_schema.yaml"
            schema.write_text(
                schema.read_text(encoding="utf-8").replace("required_validation_receipt: true", "required_validation_receipt: false"),
                encoding="utf-8",
            )
            errors, receipt = self._validate_fixture(Path(fixture))
            self.assertEqual(receipt["result"], "FAIL")
            self.assertTrue(any("required_validation_receipt" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
