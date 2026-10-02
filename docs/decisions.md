# Decisions

## Hard rejection is separate from scoring

Some conditions should not be “minus 30 points.” `assess()` evaluates hard gates first and returns `reject` immediately when any are present. The scoring function is bypassed.

## Duplicate identity is explicit and conservative

`duplicate_key()` canonicalizes the source URL and normalizes the title so callers can suppress repeated identities before assessment. Canonicalization removes known tracking parameters and fragments, but preserves other query parameters because they may identify different opportunities. The public core exposes the identity rule; it does not include the private discovery/storage layer that applies it across a lead set.

## Scores are additive and inspectable

Every point has a named source in `reasons`. The current weights are explicit default heuristic constants for prioritization. They are not learned parameters and no public calibration evidence justifies reading them as probabilities or confidence.

## Decision bands are policy, not prediction

`75+` prepares proof, `55–74` verifies then prepares, `35–54` researches, and lower scores are deprioritized. These thresholds encode triage policy under the current rubric; they are not validated outcome cutoffs.

## Proof before contact

Higher-priority opportunities get a small reversible proof plan. The final step remains `human_review_before_contact`; this repository contains no outreach or sending behavior.
