# Design overview

This repository is a deterministic triage layer for public opportunities, not a predictive sales model.

The intended control flow is:

1. canonicalize the source URL and derive a duplicate identity;
2. let the caller suppress repeated identities;
3. run hard eligibility gates;
4. if any hard gate fails, return `reject` immediately and **skip scoring**;
5. otherwise apply the additive heuristic and map it to an explicit decision band;
6. only the two higher-priority bands create a small reversible proof plan;
7. every proof plan ends at human review before contact.

The score answers one narrow question: **where should attention go first under the current rubric?** It does not answer “how likely is this opportunity to close?”

See `PROVENANCE.md` for why the current numeric weights must be treated as configurable heuristics rather than empirically calibrated likelihoods.
