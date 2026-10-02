# Verification

These commands verify the deterministic public triage slice. They do not establish predictive accuracy or client-acquisition performance.

## Behavior and syntax

Linux/macOS/CI:

```bash
python -m compileall -q src
PYTHONPATH=src python -m unittest discover -s tests
```

Windows PowerShell:

```powershell
python -m compileall -q src
$env:PYTHONPATH = "src"
python -m unittest discover -s tests
```

The behavior tests cover:

- hard rejection before scoring;
- a direct regression check that hard-rejected rows never call `score()`;
- strong eligible opportunities ending at `human_review_before_contact`;
- tracking-only URL variants collapsing to one duplicate identity;
- identity-bearing query parameters remaining distinct;
- non-tracking query-order canonicalization.

## CI boundary

[`.circleci/config.yml`](../.circleci/config.yml) runs source compilation, the unittest suite, and public-proof file checks.

A CI configuration is not evidence that a particular remote commit passed. Inspect the current PR/commit checks before making that claim.
