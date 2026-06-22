import unittest

from scripts.validate_verification_status import expected_counts, validate


class VerificationStatusCountsTests(unittest.TestCase):
    def test_visible_counts_match_request_matrix(self) -> None:
        self.assertEqual(validate(), [])
        counts = expected_counts()
        self.assertEqual(counts["tracked"], 19)
        self.assertEqual(counts["verified"], 0)
        self.assertEqual(counts["reviewed"], 19)
        self.assertEqual(counts["inferred"], 0)
        self.assertEqual(counts["missing"], 0)
        self.assertEqual(counts["evidence_packets"], 0)
        self.assertEqual(counts["area_expected"]["HID descriptors"]["tracked"], 7)
        self.assertEqual(counts["area_expected"]["HID descriptors"]["reviewed"], 7)
        self.assertEqual(counts["area_expected"]["HID descriptors"]["verified"], 0)
        self.assertEqual(counts["area_expected"]["HID descriptors"]["inferred"], 0)
        self.assertEqual(counts["area_expected"]["HID descriptors"]["missing"], 0)
        self.assertEqual(counts["area_expected"]["HID report descriptors"]["tracked"], 6)
        self.assertEqual(counts["area_expected"]["HID report descriptors"]["reviewed"], 6)
        self.assertEqual(counts["area_expected"]["HID report descriptors"]["verified"], 0)
        self.assertEqual(counts["area_expected"]["HID report descriptors"]["inferred"], 0)
        self.assertEqual(counts["area_expected"]["HID report descriptors"]["missing"], 0)
        self.assertEqual(counts["area_expected"]["HID class requests"]["tracked"], 6)
        self.assertEqual(counts["area_expected"]["HID class requests"]["reviewed"], 6)
        self.assertEqual(counts["area_expected"]["HID class requests"]["verified"], 0)
        self.assertEqual(counts["area_expected"]["HID class requests"]["inferred"], 0)
        self.assertEqual(counts["area_expected"]["HID class requests"]["missing"], 0)


if __name__ == "__main__":
    unittest.main()
