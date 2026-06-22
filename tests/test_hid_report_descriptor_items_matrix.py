import unittest

from scripts.validate_hid_report_descriptor_items_matrix import EXPECTED_ITEMS, validate


class HidReportDescriptorItemsMatrixTests(unittest.TestCase):
    def test_report_descriptor_items_matrix_is_reviewed_identity_only(self) -> None:
        self.assertEqual(validate(), [])
        self.assertEqual(EXPECTED_ITEMS, {
            "short_item_prefix",
            "long_item_prefix",
            "main_item_type",
            "global_item_type",
            "local_item_type",
            "reserved_item_type",
        })


if __name__ == "__main__":
    unittest.main()
