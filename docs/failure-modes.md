# Failure modes

## Hard reject becomes a small penalty
An ineligible opportunity remains highly ranked because enough positive points outweigh the penalty. Response: hard gates run before scoring and return immediately.

## Duplicate opportunity appears twice
Tracking parameters or title formatting make the same source look new. Response: remove only known tracking query parameters, drop fragments, normalize the title, and use the resulting pair as a caller-side duplicate key.

## Distinct query-backed opportunities collapse together
A canonicalizer strips an identity-bearing query such as `?id=42` and accidentally treats it as the same source as `?id=43`. Response: preserve non-tracking query parameters and canonicalize their ordering.

## Heuristic weights look empirically authoritative
Specific values such as 22, 16, and 12 are mistaken for measured conversion effects. Response: document them as explicit default policy constants and keep provenance visible; do not claim calibration without evidence.

## Score is mistaken for close probability
A deterministic attention score gets read as “80% likely to buy.” Response: never label it as probability or model confidence.

## Stale opportunity remains attractive
Old evidence is strong but no longer actionable. Response: freshness participates in scoring and expiry can hard-reject.

## High score triggers automatic outreach
The system bypasses review. Response: proof plans end with human review before contact.

## Weak evidence gets a polished pitch
There is little proof value. Response: research/deprioritize rather than manufacture confidence.
