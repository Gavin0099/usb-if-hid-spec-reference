import unittest

from scripts.validate_hid_class_request_matrix import EXPECTED_REQUESTS, validate


class HidClassRequestMatrixTests(unittest.TestCase):
    def test_request_matrix_contains_expected_hid_requests(self) -> None:
        self.assertEqual(validate(), [])
        self.assertEqual(
            set(EXPECTED_REQUESTS),
            {"GET_REPORT", "SET_REPORT", "GET_IDLE", "SET_IDLE", "GET_PROTOCOL", "SET_PROTOCOL"},
        )


if __name__ == "__main__":
    unittest.main()
