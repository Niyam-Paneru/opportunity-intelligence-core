from __future__ import annotations

from .models import Opportunity


# Configurable prioritization heuristics, not calibrated probabilities or confidence.
# Changing these constants changes triage policy; it does not improve predictive accuracy.
POSITIVE_COMPONENTS = (
    ("explicit_paid_intent", 22),
    ("budget_known", 10),
    ("buyer_trust", 10),
    ("technical_fit", 16),
    ("outcome_fit", 12),
    ("proof_possible", 12),
    ("fresh", 10),
    ("urgent", 8),
)

PENALTIES = (
    ("high_competition", 10),
    ("duplicate_risk", 20),
)


def score(opportunity: Opportunity) -> tuple[int, tuple[str, ...]]:
    value = 0
    reasons: list[str] = []

    for name, points in POSITIVE_COMPONENTS:
        if getattr(opportunity, name):
            value += points
            reasons.append(f"+{points}:{name}")

    for name, points in PENALTIES:
        if getattr(opportunity, name):
            value -= points
            reasons.append(f"-{points}:{name}")

    return max(0, min(100, value)), tuple(reasons)


def decision_for_score(value: int) -> str:
    if value >= 75:
        return "prepare_proof"
    if value >= 55:
        return "verify_then_prepare"
    if value >= 35:
        return "research"
    return "deprioritize"
