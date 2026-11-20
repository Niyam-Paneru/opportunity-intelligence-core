# Opportunity Intelligence Core

A job spreadsheet can become a work of art. Color-coded priorities, thoughtful notes, beautiful columns — and somehow still no applications.

I built this Python experiment to stop the spreadsheet from winning. It **filters, scores, and explains** opportunities, so there's an actual reason behind the next thing to investigate.

First come hard eligibility checks. Then eligible candidates get scored against explicit reasons and placed in a review band.

| Score | What the code suggests |
| --- | --- |
| 75–100 | Prepare a small proof |
| 55–74 | Verify missing evidence, then prepare |
| 35–54 | Research further |
| 0–34 | Deprioritize |
| Hard reject | Stop before scoring |

**Human review comes before contact.** The code prepares a proof plan; it doesn't apply, email anyone, or magically produce a paycheck.

## An 83 is not an 83% chance of getting hired

The weights (22, 16, 12, etc.) are hand-chosen **policy constants**, not probabilities learned from job outcomes. An 83 means “this rubric prioritizes it.” It does **not** mean an 83% chance of getting hired.

The rubric has geography and remote-status eligibility gates. Whether those are sensible for a particular search is a separate policy decision, not evidence that cross-border work is impossible.

URL normalization merges tracking-only variations while keeping identity-bearing parameters distinct. Otherwise the same lead can show up repeatedly and distort the shortlist.

Open [eligibility](src/opportunity_intelligence/gates.py), [scoring](src/opportunity_intelligence/scoring.py), [planning](src/opportunity_intelligence/planning.py), [normalization](src/opportunity_intelligence/normalization.py), and [tests](tests/).

This is a **deterministic triage core**, not a validated hiring predictor or an autonomous job applicant. No recruiter messages, accounts, real submissions, or payments are included. [Verification](docs/verification.md) · [provenance](PROVENANCE.md).

The next step after a high score is still reading the opportunity. Sadly, the rubric can't do the interview for you.
