from __future__ import annotations

from .gates import hard_rejection_reasons
from .models import Assessment, Opportunity
from .normalization import canonical_url, duplicate_key
from .planning import proof_plan_for
from .scoring import decision_for_score, score


def assess(opportunity: Opportunity) -> Assessment:
    hard_reasons = hard_rejection_reasons(opportunity)
    if hard_reasons:
        return Assessment(score=0, decision="reject", reasons=hard_reasons, proof_plan=())

    value, reasons = score(opportunity)
    decision = decision_for_score(value)
    return Assessment(
        score=value,
        decision=decision,
        reasons=reasons,
        proof_plan=proof_plan_for(opportunity, decision=decision),
    )


__all__ = ["Assessment", "Opportunity", "assess", "canonical_url", "duplicate_key"]
