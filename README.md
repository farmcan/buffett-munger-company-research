# Buffett–Munger Company Research

[中文说明](README.zh-CN.md)

[![CI](https://github.com/farmcan/buffett-munger-company-research/actions/workflows/ci.yml/badge.svg)](https://github.com/farmcan/buffett-munger-company-research/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An independent, source-backed company-research workflow inspired by publicly documented Buffett
and Munger principles.

一套独立、可审计、可执行的巴菲特—芒格式公司研究方法。它不是选股机器人，也不是“大师
语气”的提示词；它把公开原则、现代财报研究和确定性 QA 组合成可复现的研究 contract。

> Unofficial and not affiliated with Berkshire Hathaway, Warren Buffett, Charlie Munger, their
> estates, or any cited publisher. Research support only—not investment advice.

## What is production-grade here?

The repository ships a complete, testable research contract:

- 17 audited methodology sources: 13 tier A, 2 tier A-, and 2 supplemental tier B;
- 21 source-linked method claims;
- 9 ordered research gates;
- 25 ordered company-research dimensions;
- 50 required indicator families;
- exact source provenance, date, checksum, and calculation controls;
- explicit loss-making and pre-profit states;
- gate propagation, red-team, and human-review requirements;
- zero GitHub repositories treated as Buffett/Munger method authority;
- standard-library validators, a synthetic passing artifact, negative tests, and CI.

“Production-grade” means the research process is strict, repeatable, and auditable. It does **not**
mean the repository supplies market data, replaces industry judgment, proves that an input fact is
true, or can approve an investment.

## Core model

```text
official sources
  -> security and legal identity
  -> circle of competence
  -> business economics
  -> durable moat
  -> management and capital allocation
  -> owner earnings
  -> survival and balance sheet
  -> intrinsic-value range
  -> independent red-team
  -> named human review
```

The workflow refuses a universal weighted score. Missing evidence remains missing; it is not
converted into a negative company judgment or filled with model intuition.

## Repository layout

```text
skills/research-buffett-munger-company/
  SKILL.md
  agents/openai.yaml
  references/
    methodology.md
    methodology-source-ledger.json
    methodology-implementation-crosswalk.json
    company-research-master-checklist.md
    company-research-schema.md
    hk-stock-connect-research-rollout.md
  scripts/
    company_research_validation.py
    validate_company_research.py
    validate_methodology_source_ledger.py
    validate_methodology_implementation_crosswalk.py
examples/
  synthetic-company-research.json
tests/
```

## Use as a Codex skill

Install directly from the public GitHub repository with Codex's bundled Skill Installer:

```bash
python3 \
  "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo farmcan/buffett-munger-company-research \
  --path skills/research-buffett-munger-company
```

The install is available to Codex on the next turn. To keep a development checkout instead, clone
and symlink the skill folder:

```bash
git clone https://github.com/farmcan/buffett-munger-company-research.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
ln -s "$PWD/buffett-munger-company-research/skills/research-buffett-munger-company" \
  "${CODEX_HOME:-$HOME/.codex}/skills/research-buffett-munger-company"
```

Then invoke:

```text
Use $research-buffett-munger-company to research <company and security code>.
Freeze the research date, use primary sources, complete all nine gates,
and write a validator-compatible artifact before the conclusion.
```

The Skill format is also usable as a structured prompt-and-reference package in other agent
systems.

## Validate an artifact

Python 3.11+ is sufficient; runtime validators have no third-party dependencies.
The `seed.*` schema identifiers are retained for backward compatibility with the original private
implementation; they do not create a Seed runtime dependency.

```bash
python skills/research-buffett-munger-company/scripts/validate_company_research.py \
  examples/synthetic-company-research.json
```

Expected result:

```json
{
  "valid": true,
  "artifact": "examples/synthetic-company-research.json",
  "errors": [],
  "warnings": [],
  "gate_count": 9,
  "dimension_count": 25,
  "indicator_count": 50,
  "source_count": 2
}
```

Validate the method provenance and crosswalk:

```bash
python skills/research-buffett-munger-company/scripts/validate_methodology_source_ledger.py \
  skills/research-buffett-munger-company/references/methodology-source-ledger.json

python \
  skills/research-buffett-munger-company/scripts/validate_methodology_implementation_crosswalk.py \
  skills/research-buffett-munger-company/references/methodology-implementation-crosswalk.json
```

Run the test suite:

```bash
python -m pip install -e ".[dev]"
pytest
ruff check .
```

## Start a real company review

1. Read the [methodology](skills/research-buffett-munger-company/references/methodology.md).
2. Freeze the exact security, research date, price date, reporting standard, and source set.
3. Execute the [master checklist](skills/research-buffett-munger-company/references/company-research-master-checklist.md).
4. Serialize the result using the [schema contract](skills/research-buffett-munger-company/references/company-research-schema.md).
5. Validate, run an independent red-team, and record a named human review.

Do not replace `example.com` URLs or synthetic facts in the example with guessed real-company
facts. A real artifact must hash the exact documents it used and preserve page- or section-level
evidence outside this top-level contract.

## Method provenance

The methodology is grounded first in official Berkshire materials, including the
[Owner's Manual](https://www.berkshirehathaway.com/ownman.pdf) and official
[shareholder letters](https://www.berkshirehathaway.com/letters/letters.html). Public meeting and
speech records are used with explicit source tiers.

GitHub projects were reviewed for engineering patterns such as portable Skill packaging, provider
separation, checklists, data audits, valuation sensitivity, and red-team workflows. They are not
treated as authority for what Buffett or Munger said, and no third-party code was copied. The
audited snapshots, commits, licenses, adopted patterns, rejected patterns, and rights boundaries
are in
[methodology-source-ledger.json](skills/research-buffett-munger-company/references/methodology-source-ledger.json).

## Hong Kong Stock Connect

The default batch design is issuer-first and official-universe-first. It separates:

- U0 security and issuer identity;
- U1 deterministic evidence/readiness screening;
- U2 full nine-gate company research.

See the
[Hong Kong Stock Connect rollout](skills/research-buffett-munger-company/references/hk-stock-connect-research-rollout.md).
The repository does not bundle a live eligibility list because eligibility changes over time.

## Non-goals

- no stock recommendations or automated trading;
- no Buffett/Munger persona simulation;
- no fixed “Buffett score”;
- no universal ROE, leverage, PE, or margin-of-safety threshold;
- no bundled copyrighted letters, books, transcripts, or market data;
- no claim that validator success proves economic truth;
- no claim of endorsement by any person or organization.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Changes to a method claim require a source-ledger update;
changes to a dimension, indicator, stage, or gate require a crosswalk and validator update.
The evidence-based path from v0.1 to v1.0 is tracked in [ROADMAP.md](ROADMAP.md).

## License and disclaimer

Original code and documentation in this repository are available under the [MIT License](LICENSE).
Third-party source documents and names remain the property of their respective owners and are not
redistributed here. Read [DISCLAIMER.md](DISCLAIMER.md) before use. Cite the project using
[CITATION.cff](CITATION.cff).
