import unittest

from scripts.validate_hid_descriptor_fields_matrix import EXPECTED_FIELDS, validate


class HidDescriptorFieldsMatrixTests(unittest.TestCase):
    def test_descriptor_fields_matrix_contains_only_expected_reviewed_fields(self) -> None:
        self.assertEqual(validate(), [])
        self.assertEqual(EXPECTED_FIELDS, {
            "bLength",
            "bDescriptorType",
            "bcdHID",
            "bCountryCode",
            "bNumDescriptors",
            "bDescriptorType_subordinate",
            "wDescriptorLength",
        })


if __name__ == "__main__":
    unittest.main()
