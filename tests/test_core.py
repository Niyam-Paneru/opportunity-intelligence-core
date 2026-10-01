import unittest

from opportunity_intelligence.core import Opportunity, assess, canonical_url, duplicate_key


class OpportunityIntelligenceTests(unittest.TestCase):
    def test_canonical_url_drops_query_fragment_and_trailing_slash(self):
        self.assertEqual(
            canonical_url("HTTPS://Example.COM/request/1/?utm=x#top"),
            "https://example.com/request/1",
        )

    def test_duplicate_key_normalizes_title(self):
        a = Opportunity("Need   API-Fix!", "https://example.test/a")
        b = Opportunity("need api fix", "https://example.test/a/")
        self.assertEqual(duplicate_key(a), duplicate_key(b))

    def test_dangerous_scope_is_hard_reject(self):
        a = Opportunity("x", "https://example.test/a", regulated_or_dangerous=True)
        self.assertEqual(assess(a).decision, "reject")

    def test_expired_is_hard_reject(self):
        a = Opportunity("x", "https://example.test/a", expired=True)
        self.assertEqual(assess(a).decision, "reject")

    def test_geography_is_hard_gate(self):
        a = Opportunity("x", "https://example.test/a", geography_eligible=False)
        self.assertEqual(assess(a).decision, "reject")

    def test_strong_evidence_scores_high(self):
        a = Opportunity(
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
        result = assess(a)
        self.assertEqual(result.score, 100)
        self.assertEqual(result.decision, "prepare_proof")

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
        self.assertEqual(assess(base).score - assess(duplicate).score, 20)

    def test_high_competition_penalty(self):
        a = Opportunity(
            "Webhook fix",
            "https://example.test/a",
            explicit_paid_intent=True,
            technical_fit=True,
            high_competition=True,
        )
        self.assertIn("-10:high_competition", assess(a).reasons)

    def test_mid_score_requires_verification(self):
        a = Opportunity(
            "Webhook fix",
            "https://example.test/a",
            explicit_paid_intent=True,
            technical_fit=True,
            proof_possible=True,
            fresh=True,
        )
        self.assertEqual(assess(a).decision, "verify_then_prepare")

    def test_proof_plan_requires_human_review(self):
        a = Opportunity(
            "Webhook fix",
            "https://example.test/a",
            explicit_paid_intent=True,
            budget_known=True,
            technical_fit=True,
            proof_possible=True,
            fresh=True,
            urgent=True,
        )
        self.assertEqual(assess(a).proof_plan[-1], "human_review_before_contact")


if __name__ == "__main__":
    unittest.main()
