import unittest

from opportunity_intelligence.gates import hard_rejection_reasons
from opportunity_intelligence.models import Opportunity


class GateTests(unittest.TestCase):
    def test_expired_is_rejected(self):
        reasons = hard_rejection_reasons(Opportunity("x", "https://example.test/a", expired=True))
        self.assertIn("expired", reasons)

    def test_geography_is_rejected(self):
        reasons = hard_rejection_reasons(Opportunity("x", "https://example.test/a", geography_eligible=False))
        self.assertIn("geography_ineligible", reasons)

    def test_clear_opportunity_has_no_hard_reasons(self):
        self.assertEqual(hard_rejection_reasons(Opportunity("x", "https://example.test/a")), ())


if __name__ == "__main__":
    unittest.main()
