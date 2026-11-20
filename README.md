# Opportunity Intelligence Core

You can spend an entire afternoon color-coding job leads. By dinner, the spreadsheet looks ready for a promotion. Nobody has applied anywhere.

I wrote this Python opportunity-triage core because sorting work isn't the same as doing work. It **filters, scores, and explains** leads, then suggests the next small proof to prepare. No mysterious “the AI says this one's 92/100, trust me.”

First come hard eligibility checks. Then eligible candidates get scored against explicit reasons and placed in a review band.

| Score | What the code suggests |
| --- | --- |
| 75–100 | Prepare a small proof |
| 55–74 | Verify missing evidence, then prepare |
| 35–54 | Research further |
| 0–34 | Deprioritize |
| Hard reject | Stop before scoring |

**Human review comes before contact.** The code prepares a proof plan; it doesn't apply, email anyone, or magically produce a paycheck.

## 83 points. Not 83% hired. Sorry.

The weights (22, 16, 12, etc.) are hand-chosen **policy constants**, not probabilities learned from job outcomes. An 83 means “this rubric prioritizes it.” It does **not** mean an 83% chance of getting hired.

The rubric has geography and remote-status eligibility gates. Whether those are sensible for a particular search is a separate policy decision, not evidence that cross-border work is impossible.

URL normalization merges tracking-only variations while keeping identity-bearing parameters distinct. Otherwise the same lead can show up repeatedly and distort the shortlist.

Open [eligibility](src/opportunity_intelligence/gates.py), [scoring](src/opportunity_intelligence/scoring.py), [planning](src/opportunity_intelligence/planning.py), [normalization](src/opportunity_intelligence/normalization.py), and [tests](tests/).

This is a **deterministic triage core**, not a validated hiring predictor or an autonomous job applicant. No recruiter messages, accounts, real submissions, or payments are included. [Verification](docs/verification.md) · [provenance](PROVENANCE.md).

After getting a high score, the next step is reading the job. It would be nice if the spreadsheet could collect the paycheck too, but that's outside the current API.
