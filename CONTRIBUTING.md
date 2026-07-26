# Contributing

Contributions should make the workflow more attributable, reproducible, or falsifiable.

## Change rules

- A new or changed Buffett/Munger method claim must update
  `methodology-source-ledger.json` and cite an A/A- source when available.
- A tier-B transcript may supplement, but may not become the sole authority for a core claim.
- A GitHub project may inform engineering structure but may not become method authority.
- A changed dimension, indicator, stage, or gate must update the implementation crosswalk,
  validator, schema documentation, fixture, and tests together.
- A real-company example must have clear redistribution rights. Prefer synthetic fixtures.
- Do not add buy/sell, position-size, guaranteed-return, or endorsement language.
- Do not copy long passages from source documents.

## Local checks

```bash
python -m pip install -e ".[dev]"
pytest
ruff check .

python skills/research-buffett-munger-company/scripts/validate_methodology_source_ledger.py \
  skills/research-buffett-munger-company/references/methodology-source-ledger.json

python \
  skills/research-buffett-munger-company/scripts/validate_methodology_implementation_crosswalk.py \
  skills/research-buffett-munger-company/references/methodology-implementation-crosswalk.json
```

Pull requests should state the evidence or failure mode being addressed and include a negative test
for every new validator rule.
