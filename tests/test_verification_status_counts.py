import unittest

from scripts.validate_verification_status import expected_counts, validate


class VerificationStatusCountsTests(unittest.TestCase):
    def test_visible_counts_match_request_matrix(self) -> None:
        self.assertEqual(validate(), [])
        counts = expected_counts()
        self.assertEqual(counts["tracked"], 13)
        self.assertEqual(counts["verified"], 0)
        self.assertEqual(counts["reviewed"], 0)
        self.assertEqual(counts["inferred"], 0)
        self.assertEqual(counts["missing"], 0)
        self.assertEqual(counts["evidence_packets"], 0)
        self.assertEqual(counts["area_tracked"]["HID descriptors"], 7)
        self.assertEqual(counts["area_tracked"]["HID class requests"], 6)


if __name__ == "__main__":
    unittest.main()
