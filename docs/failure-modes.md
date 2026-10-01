# Failure modes

## Hard reject becomes a small penalty
An ineligible opportunity remains highly ranked because enough positive points outweigh the penalty. Response: hard gates run before scoring and return immediately.

## Duplicate opportunity appears twice
Tracking parameters or formatting make the same source look new. Response: canonical URL + normalized title form a duplicate key for caller-side deduplication before assessment.

## Heuristic weights look empirically authoritative
Specific values such as 22, 16, and 12 are mistaken for measured conversion effects. Response: document them as configurable prioritization heuristics and keep provenance explicit; do not claim calibration without evidence.

## Score is mistaken for close probability
A deterministic attention score gets read as “80% likely to buy.” Response: never label it as probability or model confidence.

## Stale opportunity remains attractive
Old evidence is strong but no longer actionable. Response: freshness participates in scoring and expiry can hard-reject.

## High score triggers automatic outreach
The system bypasses review. Response: proof plans end with human review before contact.

## Weak evidence gets a polished pitch
There is little proof value. Response: research/deprioritize rather than manufacture confidence.
