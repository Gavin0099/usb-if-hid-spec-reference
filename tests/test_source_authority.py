import unittest

from scripts.validate_source_authority import DEFAULT_AUTHORITY, load_yaml, validate


class SourceAuthorityTests(unittest.TestCase):
    def test_source_authority_is_locked_to_hid_1_11(self) -> None:
        self.assertEqual(validate(), [])

    def test_hid_descriptor_is_authorized_but_not_imported(self) -> None:
        data = load_yaml(DEFAULT_AUTHORITY)
        hid_1_11 = data["primary_sources"][0]
        current_sections = {
            entry["section"]
            for entry in hid_1_11["current_imported_usage"]
        }
        future_usage = hid_1_11["future_authorized_usage"]
        self.assertNotIn("6.2.1", current_sections)
        self.assertEqual(len(future_usage), 1)
        self.assertEqual(future_usage[0]["section"], "6.2.1")
        self.assertEqual(future_usage[0]["topic"], "HID Descriptor")
        self.assertEqual(future_usage[0]["status"], "authorized_not_imported")


if __name__ == "__main__":
    unittest.main()
