import unittest

from scripts.validate_evidence_packet_schema import validate


class EvidencePacketSchemaTests(unittest.TestCase):
    def test_verified_preflight_schema_is_valid(self) -> None:
        errors, receipt = validate()
        self.assertEqual(errors, [])
        self.assertEqual(receipt["result"], "PASS")
        self.assertEqual(receipt["authority_ceiling"], "verified_preflight_contract_only")
        self.assertEqual(receipt["verified_gate"]["review_level"], 3)
        self.assertEqual(receipt["verified_gate"]["required_packet_status"], "accepted")
        self.assertGreaterEqual(len(receipt["checked_shell_packets"]), 6)
        self.assertIn("hid_1_11:7.2", receipt["checked_source_authority_bindings"])
        self.assertEqual(len(receipt["checked_candidate_packets"]), 6)
        for candidate in (
            "docs/evidence/candidates/hid_get_report_candidate.yaml",
            "docs/evidence/candidates/hid_set_report_candidate.yaml",
            "docs/evidence/candidates/hid_get_idle_candidate.yaml",
            "docs/evidence/candidates/hid_set_idle_candidate.yaml",
            "docs/evidence/candidates/hid_get_protocol_candidate.yaml",
            "docs/evidence/candidates/hid_set_protocol_candidate.yaml",
        ):
            self.assertIn(candidate, receipt["checked_candidate_packets"])


if __name__ == "__main__":
    unittest.main()
