---
name: research-buffett-munger-company
description: Research one listed company or a frozen stock universe with a source-backed Buffett–Munger decision workflow. Use for value-investing due diligence, circle-of-competence tests, business economics, durable moat, management and capital allocation, owner earnings, balance-sheet survival, intrinsic-value scenarios, margin of safety, red-team review, or auditable A-share, Hong Kong Stock Connect, US, and other listed-company research. Produces evidence-linked conditional conclusions, never buy/sell instructions.
---

# Research a company with the Buffett–Munger workflow

Use Buffett and Munger as a decision architecture, not as a quotation style, personality
simulation, fixed score, or trading signal. Separate disclosed facts, reported claims,
calculations, interpretations, assumptions, and unresolved gaps.

Always state that the result is research support, not investment advice. This is an independent,
unofficial workflow and is not affiliated with Berkshire Hathaway, Warren Buffett, Charlie
Munger, their estates, or the cited publishers.

## Read before working

- Read `references/methodology.md` to distinguish attributable principles from this project's
  operating controls.
- Read and execute `references/company-research-master-checklist.md` for every full company
  review.
- Read `references/company-research-schema.md` before writing or validating a combined artifact.
- Read `references/methodology-source-ledger.json` when citing the method or auditing source and
  rights boundaries.
- Read `references/methodology-implementation-crosswalk.json` before changing dimensions,
  indicators, stages, or gates.
- Read `references/hk-stock-connect-research-rollout.md` before designing a Hong Kong Stock
  Connect batch.
- Read `references/public-report-template-contract.md` before building a public HTML report.
  Keep the publication shell and reader spine fixed; express industry differences through KPI,
  accounting, cash-bridge, and valuation slots instead of inventing another theme or status
  vocabulary.

## Choose the workflow

### One company

1. Freeze the security identity, research date, price date, reporting standard, and source set.
2. Run all nine gates in order.
3. Complete the 25 ordered research dimensions and 50 ordered indicator families.
4. Build owner-earnings, earnings-quality, forward, and intrinsic-value scenarios.
5. Run an independent red-team pass.
6. Validate the artifact.
7. Require a named human review before publication or use in a real decision process.

### A market universe

1. Freeze an official, dated security universe.
2. Resolve securities to legal issuers and deduplicate share classes.
3. Run a deterministic U0 identity and U1 evidence/readiness screen across the full universe.
4. Deep-research only survivors, uncertainty samples, sector-control samples, and random rejects.
5. Preserve every exclusion reason and allow re-entry when new filings arrive.

Never call a broad screen “company research.” Do not rank the deep-research queue by recent price
movement or model preference.

## Nine gates

Execute these in order. A later gate cannot repair missing primary evidence in an earlier gate.

1. **Identity and sources** — resolve security, issuer, exchange, currency, fiscal year, listing
   type, control structure, reporting period, and price timestamp.
2. **Circle of competence** — explain how the business earns money, key customers and suppliers,
   unit economics, capital needs, and accounting complications.
3. **Business economics** — compare at least 3–5 periods plus the latest interim where available:
   revenue, margins, parent earnings, ROE/ROIC, cash flow, capex, leverage, and segment drivers.
4. **Durable moat** — test willingness to pay, switching cost, network effect, cost advantage,
   efficient scale, licenses, and process or asset advantages. High margins and rankings are clues,
   not proof.
5. **Management and capital allocation** — test candor, incentives, related parties, dilution,
   dividends, buybacks, M&A, reinvestment, and per-share value creation.
6. **Owner earnings** — begin with parent-attributable earnings, add defensible non-cash charges,
   and subtract maintenance reinvestment and required working capital. Use a range when maintenance
   capex is not disclosed.
7. **Survival and balance sheet** — test debt maturity, off-balance-sheet exposure, regulated or
   customer liabilities, cyclicality, and tail-risk survival.
8. **Intrinsic value and margin of safety** — use transparent scenarios, reverse expectations, and
   at least one cross-check. Bind every multiple to a price date and EPS definition.
9. **Decision boundary and disconfirmation** — return gate statuses, strongest opposing evidence,
   invalidation tests, source gaps, and the next filing or event to examine.

Allowed gate results are:

```text
pass
pass_with_scope
mixed_positive
mixed
provisional
range_only
inconclusive
research_ready
research_ready_not_decision_ready
fail
outside_circle
blocked
```

Explain every result. Do not collapse the gates into a weighted score.

- An `unknown` or `conflicting` dimension prohibits a positive result on every mapped gate.
- A `fail`, `outside_circle`, or `blocked` gate propagates forward.
- Readiness results are valid only for the final gate.
- The final gate cannot be positive while any dimension is unresolved.

## Source protocol

Use this order:

1. Exchange, regulator, issuer filings, official statistics, and court or regulatory records.
2. Audited statements, earnings materials, and official meeting records.
3. Licensed market or consensus data with exact definitions.
4. Reputable reporting and industry research.
5. Social posts only as leads.

For every material company fact, store the source reference, period, unit, currency,
publication/access date, legal/accounting scope, covered evidence, and content SHA-256. Preserve
conflicting values and open a reconciliation gap.

For methodology claims:

- Use exact IDs, titles, and URLs from `references/methodology-source-ledger.json`.
- Require at least one tier-A or A- source.
- Treat tier-B transcript chains as supplemental.
- Treat GitHub repositories as engineering references only, never method authority.
- Paraphrase briefly and link; do not reproduce copyrighted source documents.

## Required analysis

At minimum produce:

- a 3–5-period financial trend and latest interim;
- a reported-to-adjusted earnings bridge;
- cash-flow and working-capital diagnostics;
- a low/base/high owner-earnings range;
- a per-listing-line float/supply bridge that separates issued, treasury, non-treasury
  outstanding, regulatory public float, observable tradable-float proxy, and active supply;
- dated float-adjusted market-cap, 20-day ADTV/turnover capacity, and an unlock/conversion/
  award/placement supply calendar with `legal_unlock`, `registration_or_listing`, and
  `actual_disposal` kept distinct;
- FY, TTM, adjusted, forward, and normalized PE states where meaningful;
- bear/base/upside operating and EPS scenarios without fake probabilities;
- intrinsic-value sensitivity with explicit growth, reinvestment, discount, and terminal inputs;
- moat evidence with counter-evidence;
- red-team claims and observable invalidation tests.

Show formulas. Use `null` for unavailable values. Do not substitute EBITDA for owner earnings.
Never label non-treasury outstanding shares as public float. For A/H, ADR, dual-class or other
multi-line securities, compute tradable supply by listing line; a supply event in one line may
affect group dilution or sentiment without directly expanding another line's float. Treat GitHub
repositories as engineering references only; official exchange rules, issuer filings, holder
disclosures and index free-float methodologies control definitions.

Preserve adverse economics:

- negative owner earnings are valid evidence;
- non-positive EPS makes PE `not_meaningful`;
- a forecast loss is `loss_case`, never an implied PE;
- zero or negative equity value is `non_positive_equity_value`, not a positive floor.

Every non-calculated state requires a plain-language reason.

## Industry branches

Select a branch before analyzing economics:

- **Banks:** funding, NIM, asset quality, credit cost, provisions, liquidity, and regulatory
  capital; do not use industrial free cash flow.
- **Insurers:** underwriting, reserves, CSM/NBV, lapse behavior, solvency, investment yield, and
  legal-entity cash upstreaming.
- **Property:** presales, escrow, completion obligations, land bank, gearing, and off-balance-sheet
  vehicles.
- **Commodities:** mid-cycle price and cost, reserve life, sustaining capex, and full-cycle returns.
- **Utilities/infrastructure:** tariff or concession, allowed return, throughput, required capex,
  and refinancing.
- **Manufacturing:** capacity, utilization, yield, ASP, input cost, certification, customer
  concentration, and equipment cycles.
- **Platforms/software:** recurring revenue, retention, acquisition cost, cloud cost, network
  effects, and governance.
- **Pre-profit/biotech:** cash runway, dilution, milestones, exclusivity, and scenario value; PE is
  not meaningful.
- **Holding companies:** legal-entity cash, NCI, double leverage, look-through earnings, and SOTP
  without double counting.

If no reliable branch fits, mark `specialized_provider_required` instead of forcing generic ratios.

## Validate the artifact

From the repository root:

```bash
python skills/research-buffett-munger-company/scripts/validate_company_research.py \
  path/to/company-research.json

python skills/research-buffett-munger-company/scripts/validate_methodology_source_ledger.py \
  skills/research-buffett-munger-company/references/methodology-source-ledger.json

python \
  skills/research-buffett-munger-company/scripts/validate_methodology_implementation_crosswalk.py \
  skills/research-buffett-munger-company/references/methodology-implementation-crosswalk.json

python \
  skills/research-buffett-munger-company/scripts/validate_report_template_parity.py \
  path/to/public-report.html
```

The validators use only the Python standard library.

## Completion rules

Mark an artifact ready for human review only when:

- identity, periods, and price anchors resolve to checksummed sources;
- all 25 ordered dimensions and 50 required indicators are present;
- material calculations reproduce;
- all nine gates have explanations;
- owner earnings and valuation preserve uncertainty;
- moat evidence contains counter-evidence;
- red-team and invalidation tests exist;
- unresolved critical gaps are explicit;
- public HTML exposes all 25 dimensions, 50 indicators and nine gates through the fixed
  `company-research-publication-v1` reader contract;
- no buy/sell, position-size, guaranteed-return, or endorsement language appears.

A failed gate is a valid research outcome. A validator pass is not investment approval.
