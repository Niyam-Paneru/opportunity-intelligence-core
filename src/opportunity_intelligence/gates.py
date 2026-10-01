from __future__ import annotations

from .models import Opportunity


def hard_rejection_reasons(opportunity: Opportunity) -> tuple[str, ...]:
    reasons: list[str] = []
    if opportunity.regulated_or_dangerous:
        reasons.append("regulated_or_dangerous_scope")
    if opportunity.expired:
        reasons.append("expired")
    if not opportunity.remote_eligible:
        reasons.append("not_remote_eligible")
    if not opportunity.geography_eligible:
        reasons.append("geography_ineligible")
    return tuple(reasons)
