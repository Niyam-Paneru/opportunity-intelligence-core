import unittest
from unittest.mock import patch

from opportunity_intelligence import Opportunity, assess, duplicate_key


class OpportunityPipelineTests(unittest.TestCase):
    def test_strong_eligible_opportunity_ends_at_human_review_not_auto_contact(self):
        opportunity = Opportunity(
            title="Need help fixing webhook failures",
            source_url="https://example.test/request/42?utm=feed",
            explicit_paid_intent=True,
            budget_known=True,
            buyer_trust=True,
            technical_fit=True,
            outcome_fit=True,
            proof_possible=True,
            fresh=True,
            urgent=True,
        )

        result = assess(opportunity)

        self.assertEqual(result.decision, "prepare_proof")
        self.assertEqual(result.proof_plan[-1], "human_review_before_contact")

    def test_hard_rejection_beats_an_otherwise_strong_score(self):
        opportunity = Opportunity(
            title="High-value but ineligible work",
            source_url="https://example.test/request/99",
            explicit_paid_intent=True,
            budget_known=True,
            buyer_trust=True,
            technical_fit=True,
            outcome_fit=True,
            proof_possible=True,
            fresh=True,
            urgent=True,
            expired=True,
        )

        result = assess(opportunity)

        self.assertEqual(result.score, 0)
        self.assertEqual(result.decision, "reject")
        self.assertIn("expired", result.reasons)

    def test_hard_rejection_bypasses_scoring(self):
        opportunity = Opportunity(
            title="Ineligible work",
            source_url="https://example.test/request/100",
            explicit_paid_intent=True,
            technical_fit=True,
            expired=True,
        )

        with patch("opportunity_intelligence.core.score", side_effect=AssertionError("score_called")):
            result = assess(opportunity)

        self.assertEqual(result.decision, "reject")
        self.assertEqual(result.score, 0)

    def test_tracking_noise_does_not_create_a_new_opportunity_identity(self):
        a = Opportunity(
            "Need API fix",
            "https://example.test/request/42?utm_source=one#details",
        )
        b = Opportunity(
            "need   api-fix!",
            "https://example.test/request/42/",
        )

        self.assertEqual(duplicate_key(a), duplicate_key(b))


if __name__ == "__main__":
    unittest.main()
