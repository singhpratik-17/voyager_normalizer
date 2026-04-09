import unittest
from normalizer import VoyagerNormalizer

class TestVoyager(unittest.TestCase):
    def setUp(self):
        self.nr = VoyagerNormalizer()

    def test_whitespace_and_nulls(self):
        raw = {"public_identifier": "  alice  ", "summary": None}
        res = self.nr.normalize(raw)
        self.assertEqual(res["public_identifier"], "alice")
        self.assertEqual(res["summary"], "")

    def test_current_role_selection(self):
        raw = {
            "positions": [
                {"title": "CEO", "company_name": "A", "date_range": {"end": None}},
                {"title": "Intern", "company_name": "B", "date_range": {"end": {"year": 2022}}}
            ]
        }
        res = self.nr.normalize(raw)
        self.assertEqual(res["current_role_title"], "CEO")

if __name__ == "__main__":
    unittest.main()