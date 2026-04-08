import unittest
from normalizer import VoyagerNormalizer

class TestNormalizer(unittest.TestCase):
    def test_id_extraction(self):
        data = {"profile": {"entityUrn": "urn:li:fs_profile:JOHNDOE123"}}
        result = VoyagerNormalizer().normalize(data)
        self.assertEqual(result["id"], "JOHNDOE123")

if __name__ == "__main__":
    unittest.main()