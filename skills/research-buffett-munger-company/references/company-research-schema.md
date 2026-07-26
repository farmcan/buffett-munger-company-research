# Company research schema and QA contract

Use this reference for full company work, production artifacts, batch design, or artifact review.
The reason each v2 dimension exists, its method attribution boundary and its
pipeline stage are defined in `methodology-implementation-crosswalk.json`.

## Contents

1. Evidence model
2. Combined artifact contract
3. Split production artifacts
4. Calculation contract
5. Gate contract
6. Batch contract
7. Review and failure states

## 1. Evidence model

Keep five layers distinct:

| Layer | Meaning | Example |
| --- | --- | --- |
| `facts` | Directly disclosed or deterministically calculated | reported revenue, formula-derived PE |
| `reported_claims` | Management, analyst or third-party assertion | “five core competitive advantages” |
| `interpretations` | Seed judgment from cited facts | moat is provisional |
| `assumptions` | Scenario input | 3% revenue growth, 9% discount rate |
| `source_gaps` | Missing, conflicting or non-comparable evidence | maintenance capex not disclosed |

Every company-evidence source record must contain:

```json
{
  "id": "stable-local-id",
  "tier": "A",
  "source_type": "exchange_filing",
  "title": "Filing title",
  "url": "https://...",
  "published_at_status": "known",
  "published_at": "YYYY-MM-DD",
  "accessed_at": "YYYY-MM-DD",
  "period": "FY2025",
  "audit_status": "audited",
  "scope": "consolidated_group",
  "covers": ["financial statements"],
  "content_sha256": "64 lowercase hexadecimal characters"
}
```

Use source tier `A` for exchange/regulator/company primary records, `B` for reliable transcripts or official summaries, `C` for defined market/consensus data, `D` for reputable secondary reporting, and `L` for leads only.

URLs use HTTPS and every consumed snapshot or response has a content SHA-256.
`published_at_status` is `known`, `not_disclosed` or `not_applicable`. A known
date must be an ISO date; either unavailable state uses `published_at: null` and
requires `date_reason` rather than an invented date. `audit_status` is
`audited`, `unaudited`, `not_applicable` or `unknown`; unknown requires
`audit_reason`. Published and accessed dates cannot exceed
`as_of.research_date`, and publication cannot follow access.

`as_of.price_source_ref` resolves to the same company source catalog and its
`covers` must include `price`. The price date cannot exceed the research date.
`generated_at` includes a timezone and cannot predate the research date.

`methodology_refs` is a separate, non-empty list. Every row requires a stable
`id`, title, HTTPS source URL and a short `use` statement explaining which
method rule it supports. The ID, title and URL must exactly match the executable
catalog in `scripts/company_research_validation.py`; the source-ledger
validator proves that catalog is identical to the 17 audited entries in
`methodology-source-ledger.json`. Every company artifact requires at least one
tier-A/A- source. Tier-B transcript chains may supplement but cannot be the only
method authority. Unknown links, copied-page URLs, title drift and GitHub
engineering references are validation failures.

Do not infer that every required operating check was stated by Buffett or
Munger. The crosswalk classifies each dimension as `primary_method`, `mixed` or
`seed_operating_control`. Customer, supplier, detailed revenue-quality,
accounting/audit, and tax/legal controls can be mandatory for production while
remaining explicitly Seed-authored evidence controls.

## 2. Combined artifact contract

The current combined contract is
`seed.stock-fundamentals-valuation.v2`. Version 2 makes the complete company
research matrix machine-checkable; a v1 artifact that omits customers,
suppliers, industry-chain position or another required dimension must not be
promoted by the production pipeline.

A provisional combined artifact must contain:

```text
schema_version
artifact_type
artifact_role
status
generated_at
security
as_of
methodology_refs
source_refs
source_boundaries
ownership_structure
financial_history
segment_data
research_dimensions
earnings_quality_bridge
owner_earnings
capital_allocation
balance_sheet_quality
pe_matrix
forward_scenarios
intrinsic_value_scenarios
moat_evidence
red_team
gates
historical_valuation
price_move_attribution
source_gaps
invalidation_tests
review
disclaimer
```

`research_dimensions` must contain exactly these 25 ordered rows:

```text
security_and_legal_subject
control_and_beneficial_ownership
business_model
revenue_structure
industry_chain_position
product_and_unit_economics
customers
suppliers
competition_structure
durable_moat
revenue_quality
earnings_quality
cash_conversion
working_capital
capital_intensity
returns_on_capital
balance_sheet_survival
capital_allocation
management
governance_and_related_parties
accounting_and_audit
tax_and_legal
per_share_economics
valuation
disconfirming_evidence
```

Every row contains:

```json
{
  "dimension": "customers",
  "status": "unknown",
  "summary": "Customer roles are separated, but retention evidence is missing.",
  "indicators": [
    {
      "id": "customer_channel_end_user_and_payer_separation",
      "status": "observed",
      "summary": "Direct customer, channel, end user and payer are separated.",
      "source_refs": ["annual-report-2025"],
      "source_gaps": []
    },
    {
      "id": "concentration_retention_receivables_inventory_and_external_evidence",
      "status": "not_disclosed",
      "summary": "Independent retention evidence is not disclosed.",
      "source_refs": [],
      "source_gaps": ["No customer-side retention source was available."]
    }
  ],
  "source_refs": ["annual-report-2025"],
  "positive_evidence": ["The filing separates channel and end-user roles."],
  "counter_evidence": [],
  "source_gaps": ["No customer-side retention source was available."]
}
```

Allowed statuses are `applicable`, `not_applicable`, `unknown` and
`conflicting`. An applicable row requires at least one indicator, primary or
otherwise explicitly tiered source, and positive evidence. An unknown or
conflicting row requires a source gap. A not-applicable row requires
`not_applicable_reason`; zero is not a substitute. The validator rejects a
missing, duplicate or reordered dimension so a polished narrative cannot hide
an unresearched operating area.

The 25 rows also contain exactly 50 ordered, stable indicator families: two for
each dimension. Their IDs are defined by
`RESEARCH_DIMENSION_INDICATOR_IDS` and mirrored as
`required_indicator_ids` in `methodology-implementation-crosswalk.json`.
Generic placeholders and one-indicator summaries are invalid. Every indicator
contains `id`, `status`, `summary`, `source_refs` and `source_gaps`, with one of
these statuses:

- `observed`: direct source references are required;
- `not_disclosed`: an explicit source gap is required;
- `conflicting`: both source references and an explicit conflict gap are
  required;
- `not_applicable`: a reason is required.

Indicator source references must be included in the parent dimension's
`source_refs` and must resolve to the company-evidence source catalog.
`methodology_refs` explain why a question exists; they cannot substitute for
company evidence. A required `not_disclosed` indicator makes the dimension
`unknown`; a conflicting indicator makes it `conflicting`. A whole
`not_applicable` dimension requires every indicator to be not applicable.
These states then propagate to mapped gates. This contract proves that each
core check family was addressed; it does not permit a generic sentence to
claim all customer, supplier, revenue, governance or valuation work was done.

Required security identity:

```text
security_id, company_name, ticker, exchange, listing_type,
currency, fiscal_year_end, reporting_standard
```

At least three annual periods and the latest material interim should be present when disclosed. Nulls are acceptable; invented values are not.

## 3. Split production artifacts

The production pipeline should split the combined research state so independent stages can be retried:

| Artifact | Producer | Consumer | Required contents |
| --- | --- | --- | --- |
| `filing-source-manifest` | official exchange/disclosure index providers | downloader, fact-pack builder, U1 scheduler | official index response checksum, query window, pagination completeness, document ID/title/date/URL, full-vs-summary priority, listing/disclosure relationship, content retrieval boundary |
| `filing-document-manifest` | official PDF downloader + page extractor | fact-pack builder and source-integrity QA | every delivery attempt, final official provider/URL, PDF content type/magic/size/SHA-256, content-addressed path, page text path/checksum/coverage, extraction errors |
| `filing-fact-pack` | deterministic evidence parser/reconciler | independent QA and later industry parser | report periods; strict statement rows; unit/currency/period/value-column/scope; exact-reproduction, single-primary and explicit-restatement fact tiers; restatement chain; statement/note links; audit/standard, business, share/dilution evidence; equation checks; conflicts and source gaps |
| `filing-fact-pack-review` | independent deterministic reviewer | human reviewer and U1 scheduler | local PDF/text checksum verification, tier-aware fact reproduction, conflict and accounting-equation checks, audit/standard/note/share/issuer gates, three-period route-specific core coverage, blockers and human-review eligibility; machine review never sets U2 ready |
| `filing-fact-pack-approval` | identified human reviewer through `record-company-fact-pack-approval` | batch scheduler and U2 admission gate | immutable decision, rationale, required confirmations, reviewed fact-pack/review paths and SHA-256; applies only to U2 company research, not valuation or trading |
| `company-filing-ocr-sidecar` | optional OCR provider plus external manifest | page evidence extractor | exact PDF SHA-256, low-text page number/text hash/confidence, provider/model/usage/cost; never overwrites sufficient native text and never auto-promotes facts |
| `company-industry-fact-sidecar` | deterministic industry provider or identified human reviewer | fact-pack reviewer | security/as-of/industry route/subtype, typed category/metric/fact type/period/value/unit/scope, stable annual document-set hash, selected official document SHA-256/page/evidence ref/source text, review status, provider/model/usage/cost; complete three-period core rows from a supported financial, property, cyclical, gas-utility or hospital route may suppress conflicting generic normalized candidates while retaining those rows for audit/recall, but model-only candidates never satisfy the industry gate |
| `company-industry-coverage-plan` | deterministic frozen-batch planner | parser/provider calibration and human planning | batch/market artifact paths and SHA-256, config/input hash, market/route/official-industry counts, calibrated samples, reproducible candidates, issuer/industry/source/human-review gaps, next specialized route, provider/model/usage/cost; candidates are engineering samples, never rankings or investment selections |
| `source-manifest` | filing/market providers | all later stages | source URL, checksum, period, tier, scope, fetched time |
| `fact-pack` | deterministic parser/reviewer | screen and research | identity, statements, segments, ownership, events |
| `value-quality-screen` | deterministic rules | batch scheduler | result per rule, exclusion reason, re-entry trigger |
| `company-research` | research agent | red team and report | gates 1–7, claims, evidence, gaps |
| `red-team` | independent prompt/stage | valuation/review | counter-thesis, fraud/governance/cycle risks, tests |
| `valuation` | deterministic calculator + assumptions | review/report | PE matrix, owner earnings, scenarios, sensitivity |
| `review` | QA/human | publication and batch ledger | validation, critical gaps, reviewer, status |

Do not let an LLM overwrite parsed filing facts. Derived artifacts should cite stable fact IDs.

The deterministic promotion pipeline routes each v2 dimension exactly once:
identity, revenue, industry chain, customer/supplier, accounting and other
reproducible operating rows go to `fact-pack`; business model, competition,
moat, returns, capital allocation, management and governance go to
`company-research`; `disconfirming_evidence` goes to `red-team`; and
`valuation` goes to `valuation`. Pipeline tests must prove that the union of
the four stage outputs is the complete 25-row contract without duplication.

An official filing-index hit is not a parsed fact. Before download, every document must use:

```text
content_retrieval_status = index_only_not_downloaded
content_sha256 = null
fact_pack_status = pending_deterministic_extraction
```

Keep full reports and summaries as separate document IDs. A summary is `secondary_summary`; it must not replace a full report. Mark an incomplete page set `truncated`. HKEX title-search selectors are not legal issuer IDs, and codes co-listed on the same announcement prove only a disclosure association until legal-entity evidence is added. An exact statutory identifier in a selected primary filing may resolve the company-level issuer only when the same filing explicitly binds the issuer to the relevant listing or A/H relationship; ticker and fuzzy-name matching never satisfy this gate.

For SSE, a CNINFO legal-disclosure PDF may be recorded as an official content-delivery fallback only after matching exact security, document type, report period and full/summary status. Record both the failed SSE attempt and successful fallback. Filter reports merely disclosed by the listed company for a subsidiary or related entity.

A numeric observation may enter the fact layer only from a strict primary-statement row with parsed table, unit, currency, period, rightmost value-column and consolidation scope. Preserve one of these reconciliation tiers:

```text
exact_reproduction_pass
  = same amount reproduced from distinct primary-report locations

single_primary_statement_pass_needs_human_review
  = one exact current-period primary-statement row

single_explicit_restatement_pass_needs_human_review
  = a later filing explicitly restates the comparative and supersedes the
    earlier amount through an append-only restatement chain
```

Two different amounts for the same fact/period/currency remain a blocking conflict unless the later filing explicitly marks the comparative as restated. Every tier still requires independent checksum/reproduction QA, statement equations where applicable, audit and accounting-standard evidence, notes traceability, current share-capital/dilution evidence, legal issuer/listing identity, route-specific facts and the immutable human approval. Segment/ownership/control data, OCR fallback and specialized banking, insurance, property, cyclical, utility and healthcare providers remain separate gates where applicable. A completed pipeline may be reused only after every recorded downstream artifact checksum matches; pre-write sidecar validation must run against the in-memory replacement document manifest so a failed run cannot leave a mixed artifact set. The current deterministic schemas are `seed.company-filing-document-manifest.v22`, `seed.company-filing-fact-pack.v30`, `seed.company-fact-pack-pipeline.v30`, `seed.company-filing-fact-pack-review.v16`, `seed.company-industry-fact-sidecar.v2` and `seed.company-industry-coverage-plan.v1`.

### Industry provider profile

Supported subtypes must satisfy their own evidence profile; one subtype never proves coverage of the whole broad route. The current profiles are:

| Subtype | Required industry evidence |
| --- | --- |
| `commercial_bank` | capital adequacy, asset quality/coverage and net-interest-margin facts with exact bank/group scope |
| `diversified_insurance_group` | group solvency, life/health NBV, P&C combined ratio and banking-segment quality/margin with legal-entity scope preserved |
| `residential_property_developer` | sales, sold-but-not-completed obligations, construction/planned GFA, interest-bearing debt and net gearing |
| `integrated_coal_producer` | production, sales volume, realized price, unit production cost and mine-development/mining capex using the latest explicitly restated scope |
| `gas_network_and_sales_utility` | three periods of throughput/service volume, tariff or unit economics, capital intensity/debt service and counterparty/procurement concentration, plus latest network/capacity/concession footprint |
| `general_hospital_operator` | three periods of patient-service volume, medical revenue/mix, separately scoped hospital-unit revenue/profit and fixed-assets-plus-construction-in-progress intensity, plus audited three-period core statements |

For `gas_network_and_sales_utility`, exact native-text subtype markers and a utilities route are both required. Keep production distinct from sales volume; keep customer, supplier and related-party concentration distinct; keep approximate network/storage/design capacity explicitly approximate. Gross margin does not establish an allowed regulatory return, tariff mechanism or spread. Physical footprint alone does not establish an exclusive concession, durable moat or economic value.

For `general_hospital_operator`, exact native-text subtype markers and a healthcare route are both required. Preserve reported patient-volume units and separately identify each hospital unit and any scope change. Patient volume does not establish clinical quality or pricing power, medical revenue share does not establish payer mix, and fixed-asset intensity does not establish asset value or a moat. DRG case mix, bed occupancy, reimbursement, clinician retention and clinical outcomes stay as U2 source gaps unless separately evidenced.

## 4. Calculation contract

### Earnings bridge

```text
reported parent net income
- material non-operating gains
+ defensible one-off losses
= adjusted earnings candidate
```

Store amount, pre/post-tax scope, source, rationale and disagreement for every adjustment.

### Owner earnings

```text
parent-attributable earnings
+ attributable non-cash charges
- maintenance capex
- required incremental working capital
= owner earnings
```

When attributable D&A, maintenance capex or required working capital is missing,
return a range and state the scope mismatch. Never relabel `CFO-capex` as owner
earnings without proving comparability. The `owner_earnings` block stores an
explicit `currency` matching `security.currency` and one of these states:

- `calculated`: store at least two finite, low-to-high range values and each
  formula. Values are signed. A negative range is an economic result, not a
  schema error, and must never be coerced to zero or a positive proxy.
- `unavailable`: store an empty `range`, a non-empty `reason` and the unresolved
  limitations. Do not manufacture a range from EBITDA, reported profit or an
  unsupported maintenance-capex assumption.

For insurers and regulated financial holding companies, replace the industrial bridge with:

```text
subsidiary statutory earnings
- required increase in regulatory capital
- prudent solvency / capital buffer
- non-distributable reserve and legal-entity restrictions
= potential subsidiary upstream cash

potential subsidiary upstream cash
- parent operating costs, interest and taxes
- required capital injections
= parent-distributable owner cash
```

Store reported earnings, management operating profit, statutory earnings, subsidiary dividends upstreamed, parent free cash and shareholder distributions as separate fields. If statutory earnings or required-capital changes are unavailable, a defensible insurer range may use realized shareholder cash, realized subsidiary upstream dividends and a clearly labeled normalized-profit upper proxy. The upper proxy is not distributable cash.

Additional insurer rules:

- Never use consolidated CFO-minus-capex without a legal-entity reconciliation; bank borrowings, insurer portfolio purchases, repos and reserve flows invalidate the industrial interpretation.
- Do not call insurance contract liabilities free or costless float. Separate life guarantees/participation/lapse/duration economics from P&C underwriting and reserve development.
- Reconcile NBV growth to CSM stock and release; rising new business does not prove the in-force profit stock is growing.
- Compare actual and through-cycle net investment yield with the return assumption used in operating profit or embedded value.
- Build solvency and capital tests at group, life, P&C and bank levels. Consolidated leverage does not replace legal-entity survival.
- Use parent-attributable subsidiary earnings or the value of the parent stake. Do not add 100% of subsidiary earnings and its market value.
- Model potential conversion dilution with the related debt/capital relief, not the share denominator alone.

### PE matrix

The row vocabulary is:

```text
label, status, price, currency, price_as_of, eps, eps_period, eps_type,
formula, pe, earnings_yield, source_refs, confidence, limitations, reason
```

Use FY, TTM, adjusted, forward and normalized rows. Every row uses one explicit
state:

- `calculated`: EPS is positive, PE is numeric and must reproduce
  `price / eps`; `formula` is required.
- `not_meaningful`: EPS is numeric and non-positive, PE is `null`, and `reason`
  explains why a price/earnings multiple has no economic meaning.
- `unavailable`: EPS and PE are both `null`, and `reason` identifies the missing
  or non-comparable input.

Price, currency, price date, EPS period/type and confidence remain explicit in
all three states. Do not turn a loss into a small positive EPS merely to produce
a PE. Historical PE may only use information available at the historical date.

### Forward scenarios

Use `bear/base/upside` as labels, not probabilities. Prefer segment volume × price × margin. If disclosure does not support this, use a simpler driver and record the limitation.
The block uses currency-neutral fields `currency`, `price_anchor` and
`forecast_eps`; do not use market-specific names such as `price_anchor_cny`.
Its currency must match `security.currency`.

Each scenario uses one state:

- `calculated_pe`: positive forecast EPS and a reproduced current-price PE;
- `loss_case`: non-positive forecast EPS, `null` implied PE and a reason;
- `unavailable`: `null` forecast EPS, `null` implied PE and a reason.

The block always retains a positive current-price anchor. A bear case may be a
loss case; scenario symmetry never justifies fabricating positive EPS.

### Intrinsic value

Store starting owner earnings, explicit-period growth/reinvestment, discount rate, terminal growth, terminal-value share, excess-cash policy, share count and per-share result. Require `discount_rate > terminal_growth`.
Store the result as `intrinsic_value_per_share` under a block-level `currency`
matching `security.currency`. Cross-currency SOTP components retain their
original currency, FX source and FX date, but the security-level result must be
translated into the listed security's currency.

Each sensitivity row uses one state:

- `calculated`: positive per-share equity value and valid assumptions;
- `non_positive_equity_value`: zero or negative per-share equity value, valid
  assumptions and an explicit reason;
- `unavailable`: `null` per-share value and a reason. Discount and terminal
  assumptions may both be absent; if supplied, both must be numeric and
  `discount_rate > terminal_growth`.

Zero and negative equity values are legitimate downside outputs. Do not floor
them to a positive amount to preserve a visually attractive range.

Use at least three sensitivities or a reverse-expectations test. A wide range should produce `inconclusive`, not selective anchoring.

## 5. Gate contract

The artifact contains exactly these ordered gates:

```text
identity_and_source_integrity
circle_of_competence
business_economics
durable_moat
management_and_capital_allocation
owner_earnings
survival_and_balance_sheet
intrinsic_value_and_margin_of_safety
decision_and_disconfirming_evidence
```

Each gate contains `gate`, `result`, `reason`, and optional `source_refs`, `blocking_gaps` and `next_tests`.

No weighted total score. Do not let an excellent business-economics result cancel a governance or survival failure.

Allowed results are:

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

Gate and dimension states must be coherent:

- An `unknown` or `conflicting` research dimension prevents `pass`,
  `pass_with_scope`, `mixed_positive`, `research_ready` and
  `research_ready_not_decision_ready` on every mapped gate.
- If an earlier gate is `fail`, `outside_circle` or `blocked`, no later gate
  may use one of those positive/readiness results. Later analysis may remain
  `mixed`, `provisional`, `range_only`, `inconclusive`, `fail` or `blocked`.
- `research_ready` and `research_ready_not_decision_ready` may appear only on
  `decision_and_disconfirming_evidence`, and not while any dimension remains
  unknown or conflicting.
- The final decision gate cannot use any positive result while any dimension
  remains unknown or conflicting, even when the dimension's direct gate is
  earlier in the sequence.
- `outside_circle` may appear only on `circle_of_competence`.

The canonical dimension-to-gate map is
`RESEARCH_DIMENSION_GATES` in `scripts/company_research_validation.py`.
`validate_methodology_implementation_crosswalk.py` rejects any documentation
crosswalk that drifts from that executable map.

## 6. Batch contract

Freeze the research universe by `security_master_manifest`, `market`, `as_of`, `source checksum` and inclusion rule.

Broad-screen output must store for every security:

```text
security_id
screen_status
rule_results
exclusion_reasons
source_periods
data_quality
reentry_triggers
scheduled_deep_research
```

Required batch controls:

- idempotent run ID and lock;
- per-company status and retry state;
- provider/model/usage/cost ledger;
- maximum estimated cost gate;
- no cursor advancement on failed source refresh;
- deterministic broad screen before LLM stages;
- sector quotas plus random excluded-name QA samples;
- stale-filing detection;
- separate `pending_sources` and `filing_index_available_fact_pack_pending` queues;
- separate partial-retry, fact-reconciliation and fact-pack human-review queues;
- checksum-bound industry coverage plan before broad parser/provider calibration;
- no U2 scheduling from index metadata alone;
- no cross-listed issuer double counting;
- separate `security_count` and `resolved_company_count`;
- `unknown` rather than false failure when required fields are missing.

Batch completion means every frozen security has a terminal screen state. It does not mean every security received full deep research.

The `company-industry-coverage-plan` must bind the batch screen and every consumed market artifact by SHA-256. It reports separate `security_count`, resolved issuer count, sector-enriched count, deterministic-QA count, provider-sample count and U2-ready count. Selection must be reproducible and exclude explicit ST/delisting records, but it must not imply company quality. Unresolved HK legal issuers and missing official industries remain gaps; do not fuzzy-merge short names or silently purchase a reference-data product.

## 7. Review and failure states

Recommended states:

```text
pending_sources
filing_index_available_fact_pack_pending
filing_evidence_partial_retry_required
filing_evidence_available_reconciliation_pending
filing_fact_pack_available_needs_human_review
source_partial
screened_out
screen_survivor
research_in_progress
research_ready_not_decision_ready
needs_red_team
needs_human_review
production_reviewed
blocked
failed
stale
```

Critical review checks:

- source checksums and dates;
- unit/period/currency consistency;
- ownership and NCI handling;
- formula reproduction;
- finance-company or regulated-industry branch;
- insurer legal-entity capital and parent-cash bridge when applicable;
- maintenance-capex uncertainty;
- historical valuation look-ahead;
- counter-evidence and invalidation tests;
- prohibited advice language;
- reviewer identity, reviewed time and unresolved critical gaps.

Use `production_reviewed` only after human review. A complete machine artifact should remain `needs_human_review` until that event is recorded.
