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
        self.assertEqual(receipt["accepted_packet_location"]["directory"], "docs/evidence/accepted")
        self.assertEqual(receipt["accepted_packet_location"]["filename_pattern"], "<candidate-base>_accepted.yaml")
        self.assertEqual(receipt["accepted_packet_location"]["matching_candidate_pattern"], "<candidate-base>_candidate.yaml")
        self.assertGreaterEqual(len(receipt["checked_shell_packets"]), 6)
        self.assertIn("hid_1_11:7.2", receipt["checked_source_authority_bindings"])
        self.assertEqual(
            receipt["checked_matrix_source_refs"]["hid_class_request_matrix"],
            ["hid_1_11:7.2"],
        )
        self.assertEqual(len(receipt["checked_candidate_packets"]), 19)
        self.assertEqual(receipt["accepted_path_guard"]["required_directory_suffix"], "docs/evidence/accepted")
        self.assertEqual(receipt["accepted_path_guard"]["required_filename_pattern"], r"^[A-Za-z0-9_]+_accepted\.yaml$")
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
            accepted_dir=root / "docs" / "evidence" / "accepted",
            matrix_paths={
                "hid_class_request_matrix": root / "data" / "hid_class_request_matrix.yaml",
            },
        )

    def _write_accepted_fixture(self, root: Path) -> Path:
        accepted_dir = root / "docs" / "evidence" / "accepted"
        accepted_dir.mkdir(parents=True, exist_ok=True)
        candidate = root / "docs" / "evidence" / "candidates" / "hid_get_report_candidate.yaml"
        accepted = accepted_dir / "hid_get_report_accepted.yaml"
        accepted.write_text(
            candidate.read_text(encoding="utf-8")
            .replace("packet_status: candidate", "packet_status: accepted")
            .replace("approval_record: pending", "approval_record: approved")
            .replace("approver: pending", "approver: human:HID-LRA-dry-run")
            + "\nacceptance_gate:\n"
            + "  previous_packet_status: candidate\n"
            + "  checkpoint_commit: dryrun123\n"
            + "  validation_receipt: evidence/dryrun_validation_receipt.json\n"
            + "  level3_checkpoint: true\n"
            + "  direct_promotion: false\n",
            encoding="utf-8",
        )
        return accepted

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
                candidate.read_text(encoding="utf-8").replace("current_claim_level: verified", "current_claim_level: reviewed"),
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

    def test_accepted_dry_run_fixture_passes(self) -> None:
        with self._fixture_root() as fixture:
            self._write_accepted_fixture(Path(fixture))
            errors, receipt = self._validate_fixture(Path(fixture))
            self.assertEqual(errors, [])
            self.assertEqual(receipt["result"], "PASS")
            self.assertEqual(len(receipt["checked_accepted_packets"]), 1)

    def test_accepted_packet_outside_accepted_dir_fails(self) -> None:
        with self._fixture_root() as fixture:
            root = Path(fixture)
            accepted = self._write_accepted_fixture(root)
            misplaced = root / "docs" / "evidence" / "candidates" / accepted.name
            shutil.copy(accepted, misplaced)
            errors, receipt = validate(
                schema_path=root / "contract" / "evidence_packet_schema.yaml",
                source_authority_path=root / "data" / "source_authority.yaml",
                evidence_dir=root / "docs" / "evidence",
                candidate_dir=root / "docs" / "evidence" / "candidates",
                accepted_dir=root / "docs" / "evidence" / "candidates",
                matrix_paths={
                    "hid_class_request_matrix": root / "data" / "hid_class_request_matrix.yaml",
                },
            )
            self.assertEqual(receipt["result"], "FAIL")
            self.assertTrue(any("docs/evidence/accepted" in error for error in errors))

    def test_accepted_packet_without_matching_candidate_name_fails(self) -> None:
        with self._fixture_root() as fixture:
            accepted = self._write_accepted_fixture(Path(fixture))
            unbound = accepted.with_name("hid_unknown_accepted.yaml")
            accepted.rename(unbound)
            errors, receipt = self._validate_fixture(Path(fixture))
            self.assertEqual(receipt["result"], "FAIL")
            self.assertTrue(any("corresponding candidate packet" in error for error in errors))

    def test_accepted_packet_with_invalid_filename_fails(self) -> None:
        with self._fixture_root() as fixture:
            accepted = self._write_accepted_fixture(Path(fixture))
            invalid = accepted.with_name("hid-get-report-accepted.yaml")
            accepted.rename(invalid)
            errors, receipt = self._validate_fixture(Path(fixture))
            self.assertEqual(receipt["result"], "FAIL")
            self.assertTrue(any("filename must match" in error for error in errors))

    def test_accepted_dry_run_missing_approval_fails(self) -> None:
        with self._fixture_root() as fixture:
            accepted = self._write_accepted_fixture(Path(fixture))
            accepted.write_text(
                accepted.read_text(encoding="utf-8").replace("approval_record: approved", "approval_record: pending"),
                encoding="utf-8",
            )
            errors, receipt = self._validate_fixture(Path(fixture))
            self.assertEqual(receipt["result"], "FAIL")
            self.assertTrue(any("approval_record" in error for error in errors))

    def test_accepted_dry_run_missing_validation_receipt_fails(self) -> None:
        with self._fixture_root() as fixture:
            accepted = self._write_accepted_fixture(Path(fixture))
            accepted.write_text(
                accepted.read_text(encoding="utf-8").replace("  validation_receipt: evidence/dryrun_validation_receipt.json\n", ""),
                encoding="utf-8",
            )
            errors, receipt = self._validate_fixture(Path(fixture))
            self.assertEqual(receipt["result"], "FAIL")
            self.assertTrue(any("validation_receipt" in error for error in errors))

    def test_accepted_dry_run_without_level3_checkpoint_fails(self) -> None:
        with self._fixture_root() as fixture:
            accepted = self._write_accepted_fixture(Path(fixture))
            accepted.write_text(
                accepted.read_text(encoding="utf-8").replace("level3_checkpoint: true", "level3_checkpoint: false"),
                encoding="utf-8",
            )
            errors, receipt = self._validate_fixture(Path(fixture))
            self.assertEqual(receipt["result"], "FAIL")
            self.assertTrue(any("level3_checkpoint" in error for error in errors))

    def test_accepted_dry_run_direct_promotion_fails(self) -> None:
        with self._fixture_root() as fixture:
            accepted = self._write_accepted_fixture(Path(fixture))
            accepted.write_text(
                accepted.read_text(encoding="utf-8").replace("direct_promotion: false", "direct_promotion: true"),
                encoding="utf-8",
            )
            errors, receipt = self._validate_fixture(Path(fixture))
            self.assertEqual(receipt["result"], "FAIL")
            self.assertTrue(any("direct_promotion" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
