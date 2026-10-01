from __future__ import annotations

from dataclasses import dataclass
import re
from urllib.parse import urlsplit, urlunsplit


@dataclass(frozen=True)
class Opportunity:
    title: str
    source_url: str
    explicit_paid_intent: bool = False
    budget_known: bool = False
    buyer_trust: bool = False
    technical_fit: bool = False
    outcome_fit: bool = False
    proof_possible: bool = False
    fresh: bool = False
    urgent: bool = False
    remote_eligible: bool = True
    geography_eligible: bool = True
    regulated_or_dangerous: bool = False
    expired: bool = False
    duplicate_risk: bool = False
    high_competition: bool = False


@dataclass(frozen=True)
class Assessment:
    score: int
    decision: str
    reasons: tuple[str, ...]
    proof_plan: tuple[str, ...]


def canonical_url(url: str) -> str:
    parts = urlsplit(url.strip())
    host = parts.netloc.lower()
    path = re.sub(r"/+$", "", parts.path or "/")
    return urlunsplit((parts.scheme.lower(), host, path, "", ""))


def duplicate_key(opportunity: Opportunity) -> tuple[str, str]:
    normalized_title = " ".join(
        re.findall(r"[a-z0-9]+", opportunity.title.lower())
    )
    return canonical_url(opportunity.source_url), normalized_title


def assess(opportunity: Opportunity) -> Assessment:
    hard_reasons = []
    if opportunity.regulated_or_dangerous:
        hard_reasons.append("regulated_or_dangerous_scope")
    if opportunity.expired:
        hard_reasons.append("expired")
    if not opportunity.remote_eligible:
        hard_reasons.append("not_remote_eligible")
    if not opportunity.geography_eligible:
        hard_reasons.append("geography_ineligible")

    if hard_reasons:
        return Assessment(
            score=0,
            decision="reject",
            reasons=tuple(hard_reasons),
            proof_plan=(),
        )

    score = 0
    reasons: list[str] = []

    components = [
        ("explicit_paid_intent", opportunity.explicit_paid_intent, 22),
        ("budget_known", opportunity.budget_known, 10),
        ("buyer_trust", opportunity.buyer_trust, 10),
        ("technical_fit", opportunity.technical_fit, 16),
        ("outcome_fit", opportunity.outcome_fit, 12),
        ("proof_possible", opportunity.proof_possible, 12),
        ("fresh", opportunity.fresh, 10),
        ("urgent", opportunity.urgent, 8),
    ]

    for name, present, points in components:
        if present:
            score += points
            reasons.append(f"+{points}:{name}")

    if opportunity.high_competition:
        score -= 10
        reasons.append("-10:high_competition")

    if opportunity.duplicate_risk:
        score -= 20
        reasons.append("-20:duplicate_risk")

    score = max(0, min(100, score))

    if score >= 75:
        decision = "prepare_proof"
    elif score >= 55:
        decision = "verify_then_prepare"
    elif score >= 35:
        decision = "research"
    else:
        decision = "deprioritize"

    proof_plan = ()
    if decision in {"prepare_proof", "verify_then_prepare"}:
        steps = ["restate_problem_from_source", "produce_small_reversible_proof"]
        if opportunity.proof_possible:
            steps.append("capture_before_after_evidence")
        steps.append("human_review_before_contact")
        proof_plan = tuple(steps)

    return Assessment(
        score=score,
        decision=decision,
        reasons=tuple(reasons),
        proof_plan=proof_plan,
    )
