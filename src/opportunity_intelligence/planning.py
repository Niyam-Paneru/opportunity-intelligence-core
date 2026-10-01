from __future__ import annotations

from .models import Opportunity


def proof_plan_for(opportunity: Opportunity, *, decision: str) -> tuple[str, ...]:
    if decision not in {"prepare_proof", "verify_then_prepare"}:
        return ()

    steps = ["restate_problem_from_source", "produce_small_reversible_proof"]
    if opportunity.proof_possible:
        steps.append("capture_before_after_evidence")
    steps.append("human_review_before_contact")
    return tuple(steps)
