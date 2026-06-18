import unittest

from scripts.validate_source_registry import validate


class SourceRegistryTests(unittest.TestCase):
    def test_source_registry_matches_source_authority(self) -> None:
        errors, receipt = validate()
        self.assertEqual(errors, [])
        self.assertEqual(receipt["result"], "PASS")
        self.assertIn("hid_1_11", receipt["registry_ids"])
        self.assertIn("hid_usage_tables", receipt["registry_ids"])


if __name__ == "__main__":
    unittest.main()
