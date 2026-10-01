# Design overview

This repository is not a “lead score = probability of sale” machine.

It is a deterministic triage layer for public opportunities.

The public slice separates five concerns:

- normalization and deduplication;
- hard rejection gates;
- evidence scoring;
- score-to-decision mapping;
- a small proof plan that still ends in human review.

A score says **where to spend attention**, not “this person will buy.”

The private systems add discovery, evidence collection, operator review, and outcome tracking. Those operational parts stay out of this public proof.
