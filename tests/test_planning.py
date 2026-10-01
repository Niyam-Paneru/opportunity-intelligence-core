import unittest

from opportunity_intelligence.models import Opportunity
from opportunity_intelligence.planning import proof_plan_for


class PlanningTests(unittest.TestCase):
    def test_low_priority_has_no_proof_plan(self):
        opportunity = Opportunity("x", "https://example.test/a")
        self.assertEqual(proof_plan_for(opportunity, decision="research"), ())

    def test_contact_is_after_human_review(self):
        opportunity = Opportunity("x", "https://example.test/a", proof_possible=True)
        plan = proof_plan_for(opportunity, decision="prepare_proof")
        self.assertEqual(plan[-1], "human_review_before_contact")


if __name__ == "__main__":
    unittest.main()
