# Provenance

This public triage module was rewritten from deterministic scoring and review boundaries in private acquisition tooling. Private lead/contact data, account access, messaging, proposal submission, and payment behavior are intentionally excluded.

## What the public history supports

The current numeric weights were already present in the earlier monolithic implementation at commit `e8cd82301119a45a370969cca05b4bcf4b9fd2be`. Commit `b012bc11cd740182f613b254cad38a742800b342` later split that logic into `scoring.py` without adding calibration evidence.

The public repository contains no dataset, calibration report, experiment, or outcome history that derives the exact `22/16/12/...` values. Therefore the numbers are documented as **configurable heuristic weights chosen for prioritization**, not empirically calibrated outcome likelihood.

## Preserved behavior

- canonicalization and deterministic duplicate identity;
- hard rejection gates before scoring;
- named additive score contributions;
- explicit score-to-decision bands;
- small reversible proof planning;
- human review before contact.

## Claim boundary

The score ranks attention under a visible rubric. It does not estimate probability of sale, model confidence, predictive accuracy, or client acquisition performance.
