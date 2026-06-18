import unittest

from scripts.validate_hid_governed_surface_manifest import main as validate_manifest_main


class HidGovernedSurfaceManifestTests(unittest.TestCase):
    def test_manifest_validation_passes(self) -> None:
        self.assertEqual(validate_manifest_main(), 0)


if __name__ == "__main__":
    unittest.main()
