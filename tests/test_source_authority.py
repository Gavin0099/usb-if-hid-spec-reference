import unittest

from scripts.validate_source_authority import validate


class SourceAuthorityTests(unittest.TestCase):
    def test_source_authority_is_locked_to_hid_1_11(self) -> None:
        self.assertEqual(validate(), [])


if __name__ == "__main__":
    unittest.main()
