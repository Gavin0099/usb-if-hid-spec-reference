import unittest

from scripts.validate_contract_files import validate


class ContractFilesTests(unittest.TestCase):
    def test_contract_files_are_consistent(self) -> None:
        errors, receipt = validate()
        self.assertEqual(errors, [])
        self.assertEqual(receipt["result"], "PASS")
        self.assertEqual(receipt["manifest_claim_ceiling"], "scaffold_identity_reference_only")
        self.assertEqual(receipt["manifest_claim_counts"]["tracked"], 19)
        self.assertEqual(receipt["manifest_claim_counts"]["scaffold"], 0)
        self.assertEqual(receipt["manifest_claim_counts"]["reviewed"], 6)
        self.assertEqual(receipt["manifest_claim_counts"]["verified"], 13)
        self.assertEqual(
            receipt["evidence_packet_schema"]["authority_ceiling"],
            "verified_preflight_contract_only",
        )
        self.assertEqual(receipt["evidence_packet_schema"]["verified_gate"]["review_level"], 3)
        self.assertEqual(receipt["evidence_packet_schema"]["verified_gate"]["required_packet_status"], "accepted")


if __name__ == "__main__":
    unittest.main()
