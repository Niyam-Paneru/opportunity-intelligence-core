from __future__ import annotations

from dataclasses import dataclass


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
