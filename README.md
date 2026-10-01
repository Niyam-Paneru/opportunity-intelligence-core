# Opportunity Intelligence Core

Deterministic triage for public opportunities: normalize identity, reject ineligible work before scoring, apply a transparent additive heuristic, and stop at human review before any contact.

This is the public decision core extracted from private acquisition tooling. It contains no discovery accounts, contact data, proposal submission, messaging, or payment behavior.

![Opportunity triage decision flow](docs/workflow.svg)

## How the flow works

1. **Optional caller-side identity cleanup.** `canonical_url()` removes tracking noise and `duplicate_key()` combines the canonical URL with a normalized title. These helpers are **not called by `assess()`**; callers may use them to suppress repeated identities before assessment.
2. **Run hard gates first.** Dangerous/regulated scope, expiry, remote ineligibility, or geography ineligibility returns `decision="reject"` immediately. `score()` is not called.
3. **Score eligible rows.** `scoring.py` adds named positive evidence and subtracts named penalties. Every contribution is returned in `reasons`.
4. **Map the score to a decision band.** The score controls attention, not predicted outcomes.
5. **Prepare a small proof only for higher-priority bands.** The plan is reversible and ends with `human_review_before_contact`.

## What the score means

The exact `22/16/12/...` values are **explicit default policy weights defined in code for prioritization**. They are not learned parameters, probabilities, confidence scores, or calibrated estimates of conversion likelihood. Changing those constants changes the triage policy; it does not make the score more predictive.

The public repository contains no dataset, calibration report, controlled experiment, or outcome history that empirically derives those exact values. Treat a higher score only as “inspect this first under the current rubric.” See [PROVENANCE.md](PROVENANCE.md) for the code-history evidence behind that claim.

| Score / gate | Decision | Next step |
|---|---|---|
| Any hard reject | `reject` | Stop; scoring is bypassed |
| 75–100 | `prepare_proof` | Build a small reversible proof, then human review |
| 55–74 | `verify_then_prepare` | Verify missing evidence, then prepare proof |
| 35–54 | `research` | Gather evidence; no proof plan |
| 0–34 | `deprioritize` | Spend attention elsewhere |

## Inspect the implementation

| File | What to verify |
|---|---|
| `normalization.py` | canonical URL and deterministic duplicate identity |
| `gates.py` | hard rejection conditions |
| `scoring.py` | visible additive heuristic and decision bands |
| `planning.py` | small proof plan ending in human review |
| `core.py` | hard gates return before scoring |
| `tests/` | strong opportunity, hard reject, duplicate identity, bands, planning |

## Run the proof

```bash
python -m compileall -q src
PYTHONPATH=src python -m unittest discover -s tests
```

The repository proves deterministic triage behavior only. It does **not** claim predictive accuracy, production conversion performance, or automatic outreach.
