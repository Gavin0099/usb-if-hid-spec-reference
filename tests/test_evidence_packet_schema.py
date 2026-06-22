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
        self.assertIn(
            "docs/evidence/candidates/hid_get_report_candidate.yaml",
            receipt["checked_candidate_packets"],
        )


if __name__ == "__main__":
    unittest.main()
