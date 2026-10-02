# Opportunity Intelligence Core

Deterministic triage for public opportunities: reject ineligible work before scoring, apply a transparent heuristic policy, and stop higher-priority cases at human review before any contact.

**Hard rejects do not get consolation points.**

This public sample comes from my private acquisition tooling. It makes the triage policy inspectable; I can adapt the rubric and build the surrounding discovery, review, and application workflows. Account access, contact data, submissions, messaging, and payment behavior stay outside this sample.

## Eligibility: reject before spending effort on a score

Dangerous or regulated scope, expiry, remote ineligibility, or geography ineligibility triggers rejection. `assess()` returns before calling `score()`.

```mermaid
flowchart LR
    O["<b>assess opportunity</b>"] --> G{"Hard reject?"}
    G -- Yes --> R["<b>Reject</b><br/>Score 0, scoring bypassed"]
    G -- No --> S["<b>Heuristic score</b><br/>Named reasons"]
    classDef input fill:#e8e6df,stroke:#55534a,color:#20201d,stroke-width:2px;
    classDef pass fill:#d2e5d8,stroke:#38734d,color:#183923,stroke-width:2px;
    classDef stop fill:#f4dadd,stroke:#b14253,color:#611c29,stroke-width:2px;
    class O,G,S input;
    class R stop;
```

Identity cleanup is optional caller-side work: `assess()` does not call `canonical_url()` or `duplicate_key()`.

## Priority: prepare evidence, then stop for review

Only `prepare_proof` and `verify_then_prepare` produce a proof plan. Its final step is `human_review_before_contact`; the module performs no contact. Lower bands return no proof plan.

```mermaid
flowchart LR
    S["<b>Heuristic score</b>"] --> B{"Proof band?"}
    B -- Yes --> P["<b>Small proof plan</b>"]
    P --> H["<b>Human review</b><br/>Before contact"]
    B -- No --> X["<b>Research / deprioritize</b><br/>No proof plan"]
    classDef input fill:#e8e6df,stroke:#55534a,color:#20201d,stroke-width:2px;
    classDef pass fill:#d2e5d8,stroke:#38734d,color:#183923,stroke-width:2px;
    classDef stop fill:#f4dadd,stroke:#b14253,color:#611c29,stroke-width:2px;
    class S,B,X input;
    class P pass;
    class H stop;
```

## How the flow works

1. **Optional identity cleanup.** `canonical_url()` removes known tracking parameters and URL fragments while preserving other query parameters that can identify a distinct opportunity. `duplicate_key()` combines that URL with a normalized title.
2. **Hard gates first.** Dangerous or regulated scope, expiry, remote ineligibility, or geography ineligibility returns `decision="reject"` immediately.
3. **Heuristic policy scoring.** Eligible rows receive named positive contributions and penalties from `scoring.py`; every contribution is returned in `reasons`.
4. **Decision band.** The score controls triage priority, not predicted outcomes.
5. **Higher-priority proof planning.** Only `prepare_proof` and `verify_then_prepare` create a small reversible proof plan, which ends at `human_review_before_contact`.

The URL canonicalizer is deliberately conservative: known tracking noise is removed, identity-bearing query parameters are retained, and repeated-key value order is preserved while keys are canonicalized.

## What the score means

The exact `22/16/12/...` values are **explicit default policy weights used for prioritization**. They are not learned parameters, probabilities, confidence scores, or calibrated estimates of conversion likelihood.

The public repository contains no dataset, calibration report, controlled experiment, or outcome history that empirically derives those exact values. A higher score means only “inspect this first under the current rubric.”

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
| [`src/opportunity_intelligence/normalization.py`](src/opportunity_intelligence/normalization.py) | conservative URL canonicalization and deterministic duplicate identity |
| [`src/opportunity_intelligence/gates.py`](src/opportunity_intelligence/gates.py) | hard rejection conditions |
| [`src/opportunity_intelligence/scoring.py`](src/opportunity_intelligence/scoring.py) | visible additive heuristic and decision bands |
| [`src/opportunity_intelligence/planning.py`](src/opportunity_intelligence/planning.py) | small proof plan ending in human review |
| [`src/opportunity_intelligence/core.py`](src/opportunity_intelligence/core.py) | hard gates return before scoring |
| [`tests/`](tests/) | strong opportunity, hard reject, query-safe duplicate identity, bands, planning |

Verification commands and what they prove: [`docs/verification.md`](docs/verification.md).

## What the score cannot tell you

The repository proves deterministic triage behavior only. It does not claim predictive accuracy, production conversion performance, or automatic outreach.

See [`PROVENANCE.md`](PROVENANCE.md) for the scoring and extraction history.
