import unittest

from scripts.validate_verification_status import expected_counts, validate


class VerificationStatusCountsTests(unittest.TestCase):
    def test_visible_counts_match_request_matrix(self) -> None:
        self.assertEqual(validate(), [])
        self.assertEqual(
            expected_counts(),
            {
                "tracked": 6,
                "verified": 0,
                "reviewed": 0,
                "inferred": 0,
                "missing": 0,
                "evidence_packets": 0,
            },
        )


if __name__ == "__main__":
    unittest.main()
