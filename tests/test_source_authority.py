import unittest

from scripts.validate_source_authority import DEFAULT_AUTHORITY, load_yaml, validate


class SourceAuthorityTests(unittest.TestCase):
    def test_source_authority_is_locked_to_hid_1_11(self) -> None:
        self.assertEqual(validate(), [])

    def test_hid_descriptor_scaffolded_import(self) -> None:
        data = load_yaml(DEFAULT_AUTHORITY)
        hid_1_11 = data["primary_sources"][0]
        current_sections = {
            entry["section"]
            for entry in hid_1_11["current_imported_usage"]
        }
        future_usage = hid_1_11["future_authorized_usage"]
        self.assertIn("6.2.1", current_sections)
        self.assertGreaterEqual(len(future_usage), 1)
        future_sections = {entry["section"] for entry in future_usage}
        self.assertIn("6.2.2", future_sections)
        self.assertTrue(
            any(
                entry.get("status") == "scaffolded_preflight"
                for entry in future_usage
            )
        )


if __name__ == "__main__":
    unittest.main()
