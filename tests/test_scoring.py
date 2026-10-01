import unittest

from opportunity_intelligence.models import Opportunity
from opportunity_intelligence.scoring import decision_for_score, score


class ScoringTests(unittest.TestCase):
    def test_strong_evidence_can_reach_100(self):
        opportunity = Opportunity(
            "Webhook fix",
            "https://example.test/a",
            explicit_paid_intent=True,
            budget_known=True,
            buyer_trust=True,
            technical_fit=True,
            outcome_fit=True,
            proof_possible=True,
            fresh=True,
            urgent=True,
        )
        value, reasons = score(opportunity)
        self.assertEqual(value, 100)
        self.assertIn("+22:explicit_paid_intent", reasons)

    def test_duplicate_penalty_is_visible(self):
        base = Opportunity(
            "Webhook fix",
            "https://example.test/a",
            explicit_paid_intent=True,
            technical_fit=True,
            proof_possible=True,
            fresh=True,
        )
        duplicate = Opportunity(**{**base.__dict__, "duplicate_risk": True})
        self.assertEqual(score(base)[0] - score(duplicate)[0], 20)

    def test_thresholds_are_explicit(self):
        self.assertEqual(decision_for_score(75), "prepare_proof")
        self.assertEqual(decision_for_score(55), "verify_then_prepare")
        self.assertEqual(decision_for_score(35), "research")
        self.assertEqual(decision_for_score(34), "deprioritize")


if __name__ == "__main__":
    unittest.main()
