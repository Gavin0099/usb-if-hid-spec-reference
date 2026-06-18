import unittest

from scripts.validate_contract_files import validate


class ContractFilesTests(unittest.TestCase):
    def test_contract_files_are_consistent(self) -> None:
        errors, receipt = validate()
        self.assertEqual(errors, [])
        self.assertEqual(receipt["result"], "PASS")
        self.assertEqual(receipt["manifest_claim_ceiling"], "scaffold_identity_reference_only")


if __name__ == "__main__":
    unittest.main()
