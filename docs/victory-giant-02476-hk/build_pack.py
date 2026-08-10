#!/usr/bin/env python3
# ruff: noqa
"""Build the public V2 research artifact for Victory Giant Technology.

The builder intentionally preserves unresolved evidence as ``unknown`` and
does not promote creator claims or customer-specific rumours into facts.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RESEARCH_DATE = "2026-08-10"
GENERATED_AT = "2026-08-10T22:00:00+08:00"
FX_HKD_CNY = 0.8594
EFFECTIVE_SHARES = 982_567_370


SOURCE_ROWS = [
    {
        "id": "S1",
        "tier": "A",
        "source_type": "exchange_filing",
        "title": "Hong Kong prospectus dated 2026-04-13",
        "url": "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0413/2026041300006_c.pdf",
        "published_at_status": "known",
        "published_at": "2026-04-13",
        "accessed_at": RESEARCH_DATE,
        "period": "FY2023-FY2025 and IPO",
        "audit_status": "audited",
        "scope": "consolidated group and H-share offer",
        "covers": ["business", "financial statements", "customers", "capital expenditure", "share offer"],
        "content_sha256": "6c85ba76cf9db4d0f6b84ebb0d43a29a5ea0a47543f915895675e201630a6a04",
    },
    {
        "id": "S2",
        "tier": "A",
        "source_type": "exchange_filing",
        "title": "HKEX May 2026 monthly return",
        "url": "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0603/2026060300800.pdf",
        "published_at_status": "known",
        "published_at": "2026-06-03",
        "accessed_at": RESEARCH_DATE,
        "period": "2026-05",
        "audit_status": "not_applicable",
        "scope": "A-share and H-share capital",
        "covers": ["share count", "treasury shares", "listing status"],
        "content_sha256": "970ba9fa008fd3f972aa880cc872f2f55f5bda94f2e320b365ccf0f3364de053",
    },
    {
        "id": "S3",
        "tier": "A",
        "source_type": "exchange_filing",
        "title": "Full exercise of over-allotment option",
        "url": "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0422/2026042201506.pdf",
        "published_at_status": "known",
        "published_at": "2026-04-22",
        "accessed_at": RESEARCH_DATE,
        "period": "2026 IPO",
        "audit_status": "not_applicable",
        "scope": "H-share offer",
        "covers": ["offer price", "H-share issuance", "dilution"],
        "content_sha256": "dd073733d8418971a2e14db6953001c64a9f2b20646ec052e4955e91354a9c5b",
    },
    {
        "id": "S4",
        "tier": "A",
        "source_type": "exchange_filing",
        "title": "2026 first-quarter report",
        "url": "https://disc.static.szse.cn/download/disc/disk03/finalpage/2026-04-29/74f20b93-58e2-4e54-b46c-11ccaf116614.PDF",
        "published_at_status": "known",
        "published_at": "2026-04-29",
        "accessed_at": RESEARCH_DATE,
        "period": "2026Q1",
        "audit_status": "unaudited",
        "scope": "consolidated group",
        "covers": ["quarterly financial statements", "cash flow", "working capital", "debt"],
        "content_sha256": "2e62b69ae068184bfd3d4230cc554d198216ff0ff0ff5cd9244ed481645be67d",
    },
    {
        "id": "S5",
        "tier": "A",
        "source_type": "issuer_investor_relations_record",
        "title": "2026-03-18 investor-relations record",
        "url": "https://static.cninfo.com.cn/finalpage/2026-03-18/1225017058.PDF",
        "published_at_status": "known",
        "published_at": "2026-03-18",
        "accessed_at": RESEARCH_DATE,
        "period": "2026-03",
        "audit_status": "not_applicable",
        "scope": "management statements",
        "covers": ["aggregate orders", "production", "delivery", "rumour response"],
        "content_sha256": "0d43fd1af728a85c72f1748cd262c55f29f294064cee9544bc0a41b517c00f63",
    },
    {
        "id": "S6",
        "tier": "B",
        "source_type": "issuer_disclosure_mirror",
        "title": "2026-07-08 Thailand capacity investor-relations record",
        "url": "https://vip.stock.finance.sina.com.cn/corp/view/vCB_AllBulletinDetail.php?CompanyCode=80323384&gather=1&id=12435369",
        "published_at_status": "known",
        "published_at": "2026-07-08",
        "accessed_at": RESEARCH_DATE,
        "period": "2026-07",
        "audit_status": "not_applicable",
        "scope": "management statements mirrored from issuer disclosure",
        "covers": ["Thailand capacity", "qualification", "validation boards", "construction"],
        "content_sha256": "6e151daf0e24bac8b6a89e8fceb090ace6c338d56e268a9e684971a6248a02af",
    },
    {
        "id": "S7",
        "tier": "B",
        "source_type": "issuer_disclosure_mirror",
        "title": "2026-07-13 clarification of market rumours",
        "url": "https://money.finance.sina.com.cn/corp/view/vCB_AllBulletinDetail.php?id=12443634&stockid=300476",
        "published_at_status": "known",
        "published_at": "2026-07-13",
        "accessed_at": RESEARCH_DATE,
        "period": "2026-07",
        "audit_status": "not_applicable",
        "scope": "management clarification mirrored from issuer disclosure",
        "covers": ["aggregate backlog", "normal shipment", "long-term demand", "rumour denial"],
        "content_sha256": "fe793757144cce06053f6d8e1daa80268c1c37ddfe6995be176f5444eb60de8d",
    },
    {
        "id": "S8",
        "tier": "A",
        "source_type": "industry_primary_source",
        "title": "NVIDIA Rubin platform AI supercomputer announcement",
        "url": "https://nvidianews.nvidia.com/news/rubin-platform-ai-supercomputer",
        "published_at_status": "known",
        "published_at": "2026-05-31",
        "accessed_at": RESEARCH_DATE,
        "period": "2026 platform roadmap",
        "audit_status": "not_applicable",
        "scope": "NVIDIA platform only; no supplier attribution",
        "covers": ["Rubin platform timing", "industry demand boundary"],
        "content_sha256": "d089dc415ca575cc51d32238d32273aa7f6fca0b758b2b9424df68ec3f019e80",
    },
    {
        "id": "S9",
        "tier": "A",
        "source_type": "exchange_market_infrastructure",
        "title": "HKEX Stock Connect Southbound shareholding query",
        "url": "https://www3.hkexnews.hk/sdw/search/mutualmarket.aspx?t=hk",
        "published_at_status": "not_disclosed",
        "published_at": None,
        "date_reason": "Point-in-time query page; the report records the 2026-08-08 observation date.",
        "accessed_at": RESEARCH_DATE,
        "period": "2026-08-08",
        "audit_status": "not_applicable",
        "scope": "Southbound disclosed holdings",
        "covers": ["Southbound holding", "H-share ownership signal"],
        "content_sha256": "084cd869cbafb525eafd9c8f2e06038d1d315d5f5d71a5b11c4346e64a6e8977",
    },
    {
        "id": "S10",
        "tier": "C",
        "source_type": "defined_market_data_api",
        "title": "Tencent H-share quote and daily prices",
        "url": "https://web.ifzq.gtimg.cn/appstock/app/kline/kline?param=hk02476,day,,,140",
        "published_at_status": "not_disclosed",
        "published_at": None,
        "date_reason": "Machine endpoint does not publish a separate release date.",
        "accessed_at": RESEARCH_DATE,
        "period": "through 2026-08-10 close",
        "audit_status": "not_applicable",
        "scope": "02476.HK secondary-market prices",
        "covers": ["price", "H-share price history", "volume"],
        "content_sha256": "4c983af54c6b9d955b6d6ec477a4924b77722b566d79ca0e8e3cee3086de3182",
    },
    {
        "id": "S11",
        "tier": "C",
        "source_type": "defined_market_data_api",
        "title": "Tencent A-share quote and daily prices",
        "url": "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=sz300476,day,,,140,",
        "published_at_status": "not_disclosed",
        "published_at": None,
        "date_reason": "Machine endpoint does not publish a separate release date.",
        "accessed_at": RESEARCH_DATE,
        "period": "through 2026-08-10 close",
        "audit_status": "not_applicable",
        "scope": "300476.SZ secondary-market prices",
        "covers": ["A-share price history", "volume", "cross-listing price"],
        "content_sha256": "9cb2cf370c944cf8b81648adf7751c687ec42a590a8a0ead1f4e9441cff6a598",
    },
    {
        "id": "S12",
        "tier": "C",
        "source_type": "defined_market_data_api",
        "title": "Tencent HKD/CNY quote",
        "url": "https://qt.gtimg.cn/q=whHKDCNY",
        "published_at_status": "not_disclosed",
        "published_at": None,
        "date_reason": "Machine endpoint does not publish a separate release date.",
        "accessed_at": RESEARCH_DATE,
        "period": "2026-08-10 snapshot",
        "audit_status": "not_applicable",
        "scope": "HKD/CNY conversion",
        "covers": ["foreign exchange", "A/H valuation bridge"],
        "content_sha256": "c9a7b610953110403157ae25d553b701d9f23b1ae019104de73ea80be565492c",
    },
    {
        "id": "S14",
        "tier": "B",
        "source_type": "asr_secondary_private_snapshot",
        "title": "Qian Doctor 2026-08-09 livestream ASR snapshot",
        "url": "https://b23.tv/KYODk1x",
        "published_at_status": "known",
        "published_at": "2026-08-09",
        "accessed_at": RESEARCH_DATE,
        "period": "2026-08-09 livestream",
        "audit_status": "not_applicable",
        "scope": "Creator statements only; full transcript retained privately and not published",
        "covers": ["creator statements", "rumour taxonomy", "ASR evidence boundary"],
        "content_sha256": "56ab5868950edc347fb05ce7ce4732eec410da80652ddfc4e2d3b7e076dc2732",
    },
    {
        "id": "S16",
        "tier": "B",
        "source_type": "regulatory_filing_mirror",
        "title": "Victory Giant 2025 audited annual report",
        "url": "https://vip.stock.finance.sina.com.cn/corp/view/vCB_AllBulletinDetail.php?CompanyCode=80323384&gather=1&id=11993270",
        "published_at_status": "known",
        "published_at": "2026-03-13",
        "accessed_at": RESEARCH_DATE,
        "period": "FY2025",
        "audit_status": "audited",
        "scope": "consolidated group; regulatory filing mirror",
        "covers": ["audited revenue", "profit", "cash flow", "working capital", "borrowings"],
        "content_sha256": "7a061e30a7fd1fe365124e20aa2c39526e376d83378059601759ced8c40e9849",
    },
    {
        "id": "S17",
        "tier": "A",
        "source_type": "exchange_filing",
        "title": "2026-08-07 abnormal trading announcement",
        "url": "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0807/2026080701319_c.pdf",
        "published_at_status": "known",
        "published_at": "2026-08-07",
        "accessed_at": RESEARCH_DATE,
        "period": "2026-08-07",
        "audit_status": "not_applicable",
        "scope": "issuer announcement",
        "covers": ["aggregate backlog", "long-term demand", "material-information boundary", "interim-report schedule"],
        "content_sha256": "b4240ba3a5b2800eba23a0dd531a6896613e0ca6bd9a3184da7e05f26091a819",
    },
    {
        "id": "S19",
        "tier": "A",
        "source_type": "exchange_filing",
        "title": "2026-06-29 EGM poll results",
        "url": "https://www.hkexnews.hk/listedco/listconews/sehk/2026/0629/2026062902405.pdf",
        "published_at_status": "known",
        "published_at": "2026-06-29",
        "accessed_at": RESEARCH_DATE,
        "period": "2026-06-29",
        "audit_status": "not_applicable",
        "scope": "A-share and H-share voting capital",
        "covers": ["gross shares", "treasury shares", "effective voting shares"],
        "content_sha256": "ee165a1e1c09ca79a7664e971d263a3ca776f3e28288193402cfabe6d8f044d7",
    },
]


INDICATORS = {
    "security_and_legal_subject": (
        "exact_security_issuer_share_class_and_rights",
        "dated_price_share_count_currency_and_listing_status",
    ),
    "control_and_beneficial_ownership": (
        "controller_voting_pledges_and_cross_holdings",
        "value_transfers_nci_and_related_party_exposure",
    ),
    "business_model": (
        "payer_value_proposition_revenue_and_cash_mechanism",
        "capital_needs_and_business_failure_variables",
    ),
    "revenue_structure": (
        "segment_product_and_geography_reconciliation",
        "volume_price_mix_acquisition_and_scope_bridge",
    ),
    "industry_chain_position": (
        "upstream_process_customer_payer_and_substitute_map",
        "profit_pool_and_inventory_credit_technology_risk",
    ),
    "product_and_unit_economics": (
        "price_volume_mix_and_incremental_economics",
        "industry_denominator_scope_and_comparability",
    ),
    "customers": (
        "customer_channel_end_user_and_payer_separation",
        "concentration_retention_receivables_inventory_and_external_evidence",
    ),
    "suppliers": (
        "critical_inputs_concentration_related_parties_and_substitution",
        "terms_prepayments_availability_and_cost_pass_through",
    ),
    "competition_structure": (
        "entry_exit_capacity_price_and_substitution",
        "competitor_customer_and_regulator_corroboration",
    ),
    "durable_moat": (
        "mechanism_economic_result_durability_and_direction",
        "strongest_falsifying_evidence",
    ),
    "revenue_quality": (
        "revenue_receivables_contract_assets_returns_and_cash",
        "acquisition_period_end_channel_and_recognition_distortion",
    ),
    "earnings_quality": (
        "reported_to_normalized_parent_earnings_bridge",
        "tax_attribution_scope_and_adjustment_disagreement",
    ),
    "cash_conversion": (
        "profit_operating_cash_and_distributable_cash_bridge",
        "factoring_payment_restricted_cash_and_sector_scope",
    ),
    "working_capital": (
        "receivables_inventory_payables_prepayments_and_contract_balances",
        "sustainable_financing_vs_temporary_cash_release",
    ),
    "capital_intensity": (
        "maintenance_vs_growth_investment_range",
        "capex_capacity_utilization_and_competitive_requirements",
    ),
    "returns_on_capital": (
        "multiperiod_roe_roic_and_incremental_returns",
        "leverage_buyback_cycle_and_accounting_decomposition",
    ),
    "balance_sheet_survival": (
        "debt_liquidity_covenants_guarantees_pledges_and_off_balance",
        "adverse_scenario_financing_need",
    ),
    "capital_allocation": (
        "reinvestment_ma_dividend_buyback_issuance_debt_and_cash_ledger",
        "diluted_per_share_outcomes_and_opportunity_cost",
    ),
    "management": (
        "dated_commitments_vs_outcomes",
        "incentives_compensation_succession_insider_actions_and_candor",
    ),
    "governance_and_related_parties": (
        "related_sales_purchases_loans_guarantees_and_asset_transfers",
        "pricing_minority_fairness_oversight_and_dissent",
    ),
    "accounting_and_audit": (
        "audit_kam_standard_policy_and_restatement",
        "statement_reproduction_and_conflict_preservation",
    ),
    "tax_and_legal": (
        "effective_deferred_and_uncertain_tax",
        "litigation_penalties_compliance_and_tail_exposure",
    ),
    "per_share_economics": (
        "basic_diluted_and_fully_diluted_share_reconciliation",
        "per_share_growth_distribution_issuance_and_repurchase_outcomes",
    ),
    "valuation": (
        "currency_consistent_value_range_assumptions_and_dates",
        "reverse_expectations_sensitivities_and_cross_check",
    ),
    "disconfirming_evidence": (
        "independent_strongest_counter_thesis",
        "observable_invalidation_next_evidence_and_review_date",
    ),
}


DIMENSION_INPUTS = {
    "security_and_legal_subject": {
        "status": "applicable",
        "summary": "02476.HK and 300476.SZ are separate H- and A-share trading lines of the same legal issuer; the report values each line at its own dated price.",
        "sources": ["S2", "S3", "S10", "S11", "S19"],
        "indicator_statuses": ["observed", "observed"],
        "indicator_summaries": ["Issuer, two share classes and their rights are identified from exchange filings.", "Price, currency, gross shares and treasury shares are bound to 2026-08-10 and dated filings."],
        "positive": ["The H-share line has 110,227,500 issued shares after over-allotment; effective group shares exclude 217,443 treasury A shares."],
    },
    "control_and_beneficial_ownership": {
        "status": "unknown",
        "summary": "The prospectus describes the controller and offer structure, but this package has not completed a current pledge, cross-holding, NCI and related-value-transfer graph.",
        "sources": ["S1"],
        "indicator_statuses": ["observed", "not_disclosed"],
        "indicator_summaries": ["Controller information is available in the prospectus.", "A current, reconciled value-transfer and NCI map is not in this package."],
        "gaps": ["Current controller pledges, cross-holdings, NCI and related-value-transfer testing require a dedicated governance pass."],
    },
    "business_model": {
        "status": "applicable",
        "summary": "Customers pay for increasingly complex PCB products; value capture depends on product mix, qualification, yield, utilisation, delivery and cash collection.",
        "sources": ["S1", "S5", "S6", "S7"],
        "indicator_statuses": ["observed", "observed"],
        "indicator_summaries": ["The customer-to-cash mechanism is described from PCB sales through shipment and collection.", "Capital needs and failure variables include qualification, yield, utilisation, customer allocation and heavy expansion."],
        "positive": ["FY2025 higher-end product mix coincided with a material revenue, margin and profit step-up."],
        "counter": ["A large capacity cycle can destroy economics if qualification or utilisation lags."],
    },
    "revenue_structure": {
        "status": "unknown",
        "summary": "Product families and customer concentration are visible, but a full product/site/geography and volume-price-mix bridge is not available for the current run-rate.",
        "sources": ["S1", "S4"],
        "indicator_statuses": ["observed", "not_disclosed"],
        "indicator_summaries": ["The prospectus provides product and geography disclosures for the historical period.", "Current volume, price, mix, site and scope effects are not fully reconciled."],
        "gaps": ["2026 product/site revenue, volume, price and gross-margin bridge is pending the interim report."],
    },
    "industry_chain_position": {
        "status": "applicable",
        "summary": "Victory Giant sits between laminate/equipment inputs and AI-system customers; profit depends on converting complexity into certified high-yield board production.",
        "sources": ["S1", "S6", "S8"],
        "indicator_statuses": ["observed", "observed"],
        "indicator_summaries": ["Inputs, PCB processes, direct customers, end demand and platform substitution are mapped.", "Customer allocation, inventory, credit, technology shifts and capacity absorption determine who retains the profit pool."],
        "positive": ["High-density and high-layer-count products can increase PCB value per AI system."],
        "counter": ["NVIDIA platform demand does not identify Victory Giant as a supplier or guarantee retained margin."],
    },
    "product_and_unit_economics": {
        "status": "unknown",
        "summary": "Historical ASP and product-mix evidence is positive, but current site-level yield, utilisation, contribution margin and comparable denominators are missing.",
        "sources": ["S1", "S6"],
        "indicator_statuses": ["observed", "not_disclosed"],
        "indicator_summaries": ["Historical HDI ASP and mix movement are disclosed.", "Current yield, utilisation and contribution economics by product/site are not disclosed."],
        "gaps": ["Site-level yield, utilisation, ASP and contribution-margin evidence is required."],
    },
    "customers": {
        "status": "unknown",
        "summary": "The largest customer reached 29.7% and the top five 51.0% in FY2025; independent customer-side retention and programme evidence remains unavailable.",
        "sources": ["S1", "S7", "S17"],
        "indicator_statuses": ["observed", "not_disclosed"],
        "indicator_summaries": ["Direct customer and end-platform roles are separated where disclosed.", "Concentration is disclosed, but customer-side retention, allocation and inventory corroboration is incomplete."],
        "gaps": ["Named customer confirmation, retention, programme allocation and channel/inventory corroboration are missing."],
    },
    "suppliers": {
        "status": "unknown",
        "summary": "The report identifies laminate, equipment and material availability as economic variables, but it lacks a complete supplier concentration and pass-through schedule.",
        "sources": ["S1"],
        "indicator_statuses": ["not_disclosed", "not_disclosed"],
        "indicator_summaries": ["Critical-input concentration, related suppliers and substitution time are not fully reconciled.", "Procurement terms, prepayments and realised cost pass-through are not fully disclosed."],
        "gaps": ["Supplier concentration, prepayments, substitution time and realised input-cost pass-through need primary evidence."],
    },
    "competition_structure": {
        "status": "unknown",
        "summary": "Qualification and manufacturing ramp are barriers, but competitor capacity, pricing, customer allocation and substitution are not reconciled on a comparable basis.",
        "sources": ["S1", "S6", "S8"],
        "indicator_statuses": ["observed", "not_disclosed"],
        "indicator_summaries": ["Entry, qualification, capacity and substitution mechanisms are described.", "Comparable competitor, customer and regulator corroboration remains incomplete."],
        "gaps": ["A same-scope peer capacity, yield, price and customer-allocation comparison is missing."],
    },
    "durable_moat": {
        "status": "applicable",
        "summary": "Technology, customer qualification and manufacturing ramp form a moat candidate, but fast platform cycles and multi-sourcing prevent a ten-year durability conclusion.",
        "sources": ["S1", "S6", "S7", "S8"],
        "indicator_statuses": ["observed", "observed"],
        "indicator_summaries": ["The candidate mechanism and its current economic result are explicit; durability remains provisional.", "Platform change, customer concentration, competitor ramp and margin normalisation are preserved as falsifiers."],
        "positive": ["The FY2025 mix and margin step-up is consistent with real manufacturing value capture."],
        "counter": ["No customer-specific Rubin order is verified, and platform transitions can reallocate programmes quickly."],
    },
    "revenue_quality": {
        "status": "unknown",
        "summary": "FY2025 and 2026Q1 operating cash support real collection, but contract-asset, returns, channel and period-end recognition tests are incomplete.",
        "sources": ["S1", "S4", "S16"],
        "indicator_statuses": ["observed", "not_disclosed"],
        "indicator_summaries": ["Revenue, receivables and operating cash are compared across available periods.", "Period-end, returns, channel and acquisition distortions are not fully tested."],
        "gaps": ["Detailed contract-asset, returns, channel inventory and quarter-end recognition data is missing."],
    },
    "earnings_quality": {
        "status": "unknown",
        "summary": "Reported parent profit is available, but a complete reported-to-normalised bridge with tax and adjustment disagreements has not been built.",
        "sources": ["S1", "S4", "S16"],
        "indicator_statuses": ["not_disclosed", "not_disclosed"],
        "indicator_summaries": ["The package does not yet reconcile every non-operating item to normalised parent earnings.", "Tax attribution, scope and adjustment disagreements require a note-level bridge."],
        "gaps": ["A note-level reported-to-normalised parent-earnings bridge is pending."],
    },
    "cash_conversion": {
        "status": "unknown",
        "summary": "Operating cash exceeded parent profit in FY2025 and remained strong in 2026Q1, but distributable cash, restricted cash and financing distortions are unresolved.",
        "sources": ["S4", "S16"],
        "indicator_statuses": ["observed", "not_disclosed"],
        "indicator_summaries": ["Profit and operating cash are reconciled for the available periods.", "Factoring, delayed payments, restricted cash and post-IPO distributable cash are not fully reconciled."],
        "gaps": ["Restricted cash, factoring and post-IPO distributable-cash evidence is required."],
    },
    "working_capital": {
        "status": "unknown",
        "summary": "Receivables, inventory and construction-in-progress are tracked, but the sustainable working-capital requirement versus temporary cash release is unresolved.",
        "sources": ["S4", "S16"],
        "indicator_statuses": ["observed", "not_disclosed"],
        "indicator_summaries": ["Receivables and inventory movements are visible; Q1 inventory rose 23.5% from year-end.", "Sustainable operating financing versus temporary cash release is not established."],
        "gaps": ["A full receivables/inventory/payables/prepayments/contract-balance turnover bridge is pending."],
    },
    "capital_intensity": {
        "status": "unknown",
        "summary": "FY2025 fixed-asset cash outflow exceeded operating cash, but maintenance and growth investment cannot yet be separated.",
        "sources": ["S1", "S4", "S6", "S16"],
        "indicator_statuses": ["not_disclosed", "observed"],
        "indicator_summaries": ["A defensible maintenance-capex range is not disclosed.", "Capex, construction progress, qualification and future utilisation requirements are tracked."],
        "gaps": ["Maintenance versus growth capex and mature-site replacement requirements are not disclosed."],
    },
    "returns_on_capital": {
        "status": "unknown",
        "summary": "Profit growth is clear, but multi-period ROIC and incremental returns after the current expansion have not been reproduced.",
        "sources": ["S1", "S4", "S16"],
        "indicator_statuses": ["not_disclosed", "not_disclosed"],
        "indicator_summaries": ["A same-scope multi-period ROIC and incremental-return series is not in the package.", "Leverage, IPO issuance, cycle and accounting effects are not fully decomposed from returns."],
        "gaps": ["ROIC, incremental ROIC, reinvestment rate and leverage decomposition remain open."],
    },
    "balance_sheet_survival": {
        "status": "unknown",
        "summary": "The H-share IPO added substantial gross cash, but the first post-IPO cash/debt/capex bridge and a covenant-level stress test await the interim report.",
        "sources": ["S1", "S3", "S4", "S16"],
        "indicator_statuses": ["not_disclosed", "not_disclosed"],
        "indicator_summaries": ["Debt balances are visible, but maturity, covenants, guarantees, pledges and restricted liquidity are not fully tested.", "Financing needs under an adverse ramp and margin scenario are not quantified after the IPO."],
        "gaps": ["Post-IPO net cash, debt maturity, covenants, guarantees and adverse-scenario funding needs are unresolved."],
    },
    "capital_allocation": {
        "status": "unknown",
        "summary": "Management has chosen an unusually large reinvestment and equity-financing cycle; per-share returns from that capital are not yet observable.",
        "sources": ["S1", "S3", "S4", "S6"],
        "indicator_statuses": ["observed", "not_disclosed"],
        "indicator_summaries": ["Reinvestment, debt and H-share issuance are recorded.", "Diluted per-share outcomes and opportunity cost cannot be judged before utilisation and cash returns emerge."],
        "gaps": ["Post-IPO capital deployment and incremental per-share owner earnings are pending."],
    },
    "management": {
        "status": "unknown",
        "summary": "Management statements on orders and capacity are dated and testable, but a long commitment-outcome, compensation and succession ledger is incomplete.",
        "sources": ["S5", "S6", "S7", "S17"],
        "indicator_statuses": ["observed", "not_disclosed"],
        "indicator_summaries": ["Dated order, shipment and capacity statements are preserved for later outcome testing.", "Compensation, succession, insider actions and candour are not fully reconciled."],
        "gaps": ["A multi-year commitment-outcome, compensation, succession and insider-action review is missing."],
    },
    "governance_and_related_parties": {
        "status": "unknown",
        "summary": "This report records the public elevator-video controversy as an overhang, but it does not complete the required related-party and minority-fairness audit.",
        "sources": ["S1"],
        "indicator_statuses": ["not_disclosed", "not_disclosed"],
        "indicator_summaries": ["Related sales, purchases, loans, guarantees and asset transfers are not fully reconciled.", "Pricing basis, minority fairness, oversight and dissent require a dedicated governance review."],
        "gaps": ["Related-party transactions, guarantees, minority treatment and board oversight need a note-level pass."],
    },
    "accounting_and_audit": {
        "status": "applicable",
        "summary": "FY2023-FY2025 financial history is anchored to audited disclosures and 2026Q1 is explicitly unaudited; calculated facts retain formulas and period boundaries.",
        "sources": ["S1", "S4", "S16"],
        "indicator_statuses": ["observed", "observed"],
        "indicator_summaries": ["Audit status, reporting standard and period boundaries are explicit.", "Revenue, profit, cash flow, shares and TTM profit are reproduced from cited statements or formulas."],
        "positive": ["The package separates audited annual figures from the unaudited quarter and does not call fixed-asset outflow maintenance capex."],
    },
    "tax_and_legal": {
        "status": "unknown",
        "summary": "No critical tax or legal event was promoted from secondary reporting, but effective tax, uncertain positions and tail liabilities are not fully audited here.",
        "sources": ["S1"],
        "indicator_statuses": ["not_disclosed", "not_disclosed"],
        "indicator_summaries": ["Effective, deferred and uncertain tax positions are not fully reconciled.", "Litigation, penalties, data, environmental and compliance tail exposures need a dedicated pass."],
        "gaps": ["Tax-rate bridge and complete litigation/compliance tail-risk schedule are missing."],
    },
    "per_share_economics": {
        "status": "applicable",
        "summary": "Gross A/H shares, treasury shares, effective shares, IPO dilution and separate listing-line market values are explicitly bridged.",
        "sources": ["S2", "S3", "S9", "S10", "S11", "S12", "S19"],
        "indicator_statuses": ["observed", "observed"],
        "indicator_summaries": ["Basic, effective and listing-line share counts are reconciled; no free conversion between A and H is assumed.", "Issuance, treasury shares, Southbound holdings and per-share valuation effects are recorded."],
        "positive": ["The analysis avoids multiplying the H price by total group shares and avoids treating the A line as a peer."],
    },
    "valuation": {
        "status": "applicable",
        "summary": "At the 2026-08-10 close, mechanical TTM P/E is about 46.0x for H and 60.0x for A; valuation remains range-only because owner earnings is unavailable.",
        "sources": ["S2", "S4", "S10", "S11", "S12", "S16", "S19"],
        "indicator_statuses": ["observed", "observed"],
        "indicator_summaries": ["Currency, price, date, EPS period and share denominator are consistent for the H-line PE matrix.", "Reverse earnings requirements and bear/base/upside sensitivities expose what current prices require."],
        "positive": ["H shares have a relative valuation discount to A shares."],
        "counter": ["Neither listing has a demonstrated owner-earnings margin of safety at the frozen prices."],
    },
    "disconfirming_evidence": {
        "status": "applicable",
        "summary": "The strongest bear case is a peak-mix profit step-up coinciding with heavy expansion, customer concentration and an event-driven valuation rerating.",
        "sources": ["S1", "S4", "S6", "S7", "S17"],
        "indicator_statuses": ["observed", "observed"],
        "indicator_summaries": ["The independent counter-thesis covers order attribution, margin normalisation, utilisation, concentration and valuation.", "Observable invalidation tests are tied to the 2026 interim report, later ramp data and the cornerstone unlock window."],
        "positive": ["Counter-evidence and next validation dates are explicit rather than hidden behind a score."],
        "counter": ["Several tests cannot resolve until post-research-date filings become available."],
    },
}


def indicator_row(indicator_id: str, status: str, summary: str, sources: list[str], gap: str | None):
    refs = sources if status in {"observed", "conflicting"} else []
    gaps = [gap] if gap and status in {"not_disclosed", "conflicting"} else []
    row = {
        "id": indicator_id,
        "status": status,
        "summary": summary,
        "source_refs": refs,
        "source_gaps": gaps,
    }
    return row


def build_dimensions():
    rows = []
    for dimension, indicator_ids in INDICATORS.items():
        item = DIMENSION_INPUTS[dimension]
        gap = (item.get("gaps") or [None])[0]
        rows.append(
            {
                "dimension": dimension,
                "status": item["status"],
                "summary": item["summary"],
                "indicators": [
                    indicator_row(indicator_ids[0], item["indicator_statuses"][0], item["indicator_summaries"][0], item["sources"], gap),
                    indicator_row(indicator_ids[1], item["indicator_statuses"][1], item["indicator_summaries"][1], item["sources"], gap),
                ],
                "source_refs": item["sources"],
                "positive_evidence": item.get("positive", []),
                "counter_evidence": item.get("counter", []),
                "source_gaps": item.get("gaps", []),
            }
        )
    return rows


def hkd_eps(net_profit_rmb: float) -> float:
    return net_profit_rmb / EFFECTIVE_SHARES / FX_HKD_CNY


def build_artifact():
    fy_eps_hkd = hkd_eps(4_311_988_274.40)
    ttm_eps_hkd = hkd_eps(4_679_768_481.39)
    scenarios = []
    for name, profit in (("bear", 5_000_000_000), ("base", 6_500_000_000), ("upside", 8_000_000_000)):
        eps = hkd_eps(profit)
        scenarios.append(
            {
                "scenario": name,
                "status": "calculated_pe",
                "forecast_eps": eps,
                "implied_pe_at_current_price": 255.2 / eps,
                "assumption": f"FY2026 parent profit sensitivity RMB{profit / 1e9:.1f}bn; not a forecast.",
                "source_refs": ["S1", "S4", "S10", "S12", "S16"],
            }
        )

    return {
        "schema_version": "seed.stock-fundamentals-valuation.v2",
        "artifact_type": "stock_fundamentals_valuation",
        "artifact_role": "public_research_support",
        "status": "needs_human_review",
        "generated_at": GENERATED_AT,
        "security": {
            "security_id": "HKEX:02476",
            "company_name": "Victory Giant Technology (HuiZhou) Co., Ltd.",
            "company_name_zh": "胜宏科技（惠州）股份有限公司",
            "ticker": "02476",
            "exchange": "HKEX",
            "listing_type": "H_share_cross_listed_with_SZSE_A_share",
            "currency": "HKD",
            "fiscal_year_end": "12-31",
            "reporting_standard": "PRC Accounting Standards for Business Enterprises",
            "cross_listing": "SZSE:300476",
        },
        "as_of": {
            "research_date": RESEARCH_DATE,
            "price_date": RESEARCH_DATE,
            "price": 255.2,
            "price_source_ref": "S10",
            "timezone": "Asia/Shanghai",
        },
        "methodology_refs": [
            {
                "id": "berkshire_owner_manual",
                "title": "Berkshire Hathaway Owner's Manual",
                "url": "https://www.berkshirehathaway.com/ownman.pdf",
                "use": "Owner orientation, per-share value and survival boundary.",
            },
            {
                "id": "berkshire_1986_letter",
                "title": "1986 Chairman's Letter",
                "url": "https://www.berkshirehathaway.com/letters/1986.html",
                "use": "Owner-earnings concept and maintenance-capex uncertainty.",
            },
            {
                "id": "berkshire_2007_letter",
                "title": "2007 Chairman's Letter",
                "url": "https://www.berkshirehathaway.com/letters/2007ltr.pdf",
                "use": "Durable moat and capital-intensity tests.",
            },
            {
                "id": "berkshire_2018_letter",
                "title": "2018 Chairman's Letter",
                "url": "https://www.berkshirehathaway.com/letters/2018ltr.pdf",
                "use": "Business-value versus market-timing and per-share capital allocation.",
            },
        ],
        "source_refs": SOURCE_ROWS,
        "source_boundaries": {
            "facts": "Exchange filings, audited statements and deterministic calculations.",
            "reported_claims": "Management aggregate-order language and creator statements remain attributed claims.",
            "interpretations": "Moat, timing and valuation readings are Seed research judgments.",
            "assumptions": "FY2026 profit cases are sensitivities without probabilities.",
            "source_gaps": "Customer-specific Rubin order, owner earnings and post-IPO net cash remain unresolved.",
            "publication": "The complete ASR transcript is retained privately; the public package contains only short attributed excerpts and a checksum-bound source record.",
        },
        "ownership_structure": {
            "gross_total_shares": 982_784_813,
            "h_shares": 110_227_500,
            "gross_a_shares": 872_557_313,
            "treasury_a_shares": 217_443,
            "effective_total_shares": EFFECTIVE_SHARES,
            "source_refs": ["S2", "S3", "S19"],
            "boundary": "A and H are separately priced trading lines; no free fungibility or arbitrage is assumed.",
        },
        "financial_history": {
            "currency": "CNY",
            "scope": "consolidated group",
            "periods": [
                {"period": "FY2023", "revenue_bn": 7.931, "gross_margin_pct": 20.7, "parent_profit_bn": 0.671, "operating_cash_flow_bn": 1.280, "fixed_asset_cash_outflow_bn": 0.270, "source_refs": ["S1"]},
                {"period": "FY2024", "revenue_bn": 10.731, "gross_margin_pct": 22.7, "parent_profit_bn": 1.154, "operating_cash_flow_bn": 1.358, "fixed_asset_cash_outflow_bn": 0.834, "source_refs": ["S1", "S16"]},
                {"period": "FY2025", "revenue_bn": 19.292, "gross_margin_pct": 35.2, "parent_profit_bn": 4.312, "operating_cash_flow_bn": 4.603, "fixed_asset_cash_outflow_bn": 6.617, "source_refs": ["S1", "S16"]},
                {"period": "2026Q1", "revenue_bn": 5.519, "gross_margin_pct": 34.5, "parent_profit_bn": 1.288, "operating_cash_flow_bn": 2.117, "fixed_asset_cash_outflow_bn": None, "source_refs": ["S4"]},
            ],
        },
        "segment_data": {
            "industry_branch": "manufacturing_electronics_pcb",
            "value_chain": "materials and equipment -> PCB process and qualification -> direct customer -> AI server/system demand",
            "known_concentration": {"fy2025_largest_customer_pct": 29.7, "fy2025_top_five_pct": 51.0},
            "limitations": ["Current product/site revenue and gross-margin bridge is not disclosed.", "Named Rubin customer attribution is not verified."],
            "source_refs": ["S1", "S6", "S7", "S8"],
        },
        "research_dimensions": build_dimensions(),
        "earnings_quality_bridge": {
            "status": "partial",
            "reported_parent_profit_fy2025_cny_bn": 4.312,
            "ttm_parent_profit_through_2026q1_cny_bn": 4.680,
            "normalised_parent_profit": None,
            "reason": "Note-level non-operating, tax and adjustment bridge is incomplete.",
            "source_refs": ["S1", "S4", "S16"],
        },
        "owner_earnings": {
            "currency": "HKD",
            "status": "unavailable",
            "range": [],
            "reason": "Maintenance capex, required working capital and post-IPO net cash cannot yet be separated reliably.",
            "limitations": ["FY2025 fixed-asset cash outflow includes major growth investment.", "2026 interim post-IPO cash and debt bridge is not yet available at the research date."],
            "source_refs": ["S1", "S4", "S16"],
        },
        "capital_allocation": {
            "status": "large_reinvestment_cycle_needs_outcome_evidence",
            "actions": ["High-end PCB expansion", "Thailand capacity build-out", "H-share equity financing"],
            "per_share_outcome": "not_yet_observable",
            "source_refs": ["S1", "S3", "S4", "S6"],
        },
        "balance_sheet_quality": {
            "status": "post_ipo_bridge_pending",
            "q1_2026_short_term_borrowings_cny_bn": 3.047,
            "q1_2026_long_term_borrowings_cny_bn": 4.823,
            "gross_h_share_offer_proceeds_hkd_bn": 23.135,
            "limitations": ["Gross proceeds are not post-IPO net cash.", "Debt maturities, covenants and restricted cash need the interim filing."],
            "source_refs": ["S3", "S4"],
        },
        "pe_matrix": [
            {
                "label": "reported_fy",
                "status": "calculated",
                "price": 255.2,
                "currency": "HKD",
                "price_as_of": RESEARCH_DATE,
                "eps": fy_eps_hkd,
                "eps_period": "FY2025",
                "eps_type": "reported_parent_profit_on_effective_group_shares_translated_to_HKD",
                "formula": "HKD255.2 / (CNY4.311988bn / 982.567370m / 0.8594)",
                "pe": 255.2 / fy_eps_hkd,
                "earnings_yield": fy_eps_hkd / 255.2,
                "source_refs": ["S2", "S10", "S12", "S16", "S19"],
                "confidence": "medium",
                "limitations": ["Trailing reported profit is not owner earnings."],
            },
            {
                "label": "reported_ttm",
                "status": "calculated",
                "price": 255.2,
                "currency": "HKD",
                "price_as_of": RESEARCH_DATE,
                "eps": ttm_eps_hkd,
                "eps_period": "TTM through 2026Q1",
                "eps_type": "reported_parent_profit_on_effective_group_shares_translated_to_HKD",
                "formula": "HKD255.2 / ((FY2025 + 2026Q1 - 2025Q1) / 982.567370m / 0.8594)",
                "pe": 255.2 / ttm_eps_hkd,
                "earnings_yield": ttm_eps_hkd / 255.2,
                "source_refs": ["S2", "S4", "S10", "S12", "S16", "S19"],
                "confidence": "medium",
                "limitations": ["TTM combines audited annual and unaudited quarterly inputs."],
            },
            {
                "label": "normalised_owner_earnings",
                "status": "unavailable",
                "price": 255.2,
                "currency": "HKD",
                "price_as_of": RESEARCH_DATE,
                "eps": None,
                "eps_period": "normalised",
                "eps_type": "owner_earnings_per_share",
                "pe": None,
                "source_refs": ["S1", "S4", "S16"],
                "confidence": "low",
                "limitations": ["Maintenance capex and required working capital are unresolved."],
                "reason": "No decision-grade owner-earnings denominator is available.",
            },
        ],
        "forward_scenarios": {
            "currency": "HKD",
            "price_anchor": 255.2,
            "price_as_of": RESEARCH_DATE,
            "scenarios": scenarios,
            "boundary": "Sensitivity labels, not probabilities or forecasts.",
        },
        "intrinsic_value_scenarios": {
            "currency": "HKD",
            "scenarios": [
                {"scenario": "bear", "status": "unavailable", "intrinsic_value_per_share": None, "discount_rate_pct": None, "terminal_growth_pct": None, "reason": "Owner earnings and post-IPO net cash are unavailable."},
                {"scenario": "base", "status": "unavailable", "intrinsic_value_per_share": None, "discount_rate_pct": None, "terminal_growth_pct": None, "reason": "Owner earnings and post-IPO net cash are unavailable."},
                {"scenario": "upside", "status": "unavailable", "intrinsic_value_per_share": None, "discount_rate_pct": None, "terminal_growth_pct": None, "reason": "Owner earnings and post-IPO net cash are unavailable."},
            ],
            "boundary": "No DCF value is manufactured from reported profit or unsupported maintenance-capex assumptions.",
        },
        "moat_evidence": {
            "positive_evidence": ["Higher-end product mix coincided with a large margin and profit step-up.", "Qualification, yield and manufacturing ramp create non-trivial execution barriers."],
            "counter_evidence": ["Customer concentration increased sharply.", "Platform transitions, multi-sourcing and competitor expansion can reallocate economics."],
            "missing_tests": ["Site-level yield and utilisation.", "Customer-side allocation evidence.", "Cross-cycle incremental ROIC."],
            "source_refs": ["S1", "S6", "S7", "S8"],
        },
        "red_team": [
            {"claim": "Specific Rubin order is narrative rather than disclosed fact.", "test": "Named customer/product shipment or auditable order value.", "status": "unresolved", "source_refs": ["S5", "S6", "S7", "S8", "S14"]},
            {"claim": "FY2025 margin may represent peak mix rather than durable economics.", "test": "Interim site/product bridge, margin and cash conversion.", "status": "pending", "source_refs": ["S1", "S4", "S16"]},
            {"claim": "Expansion may outrun demand and depress owner cash.", "test": "Utilisation, shipment, revenue and cash ramp relative to construction spend.", "status": "pending", "source_refs": ["S4", "S6", "S16"]},
            {"claim": "Recent rerating may be event anticipation rather than new fundamental evidence.", "test": "Interim report adds quantifiable margin, cash and order evidence.", "status": "pending", "source_refs": ["S10", "S11", "S17"]},
        ],
        "gates": [
            {"gate": "identity_and_source_integrity", "result": "provisional", "reason": "Security and share lines resolve, but governance and related-value-transfer work is incomplete.", "blocking_gaps": ["Current controller and related-party map."], "source_refs": ["S1", "S2", "S3", "S19"]},
            {"gate": "circle_of_competence", "result": "provisional", "reason": "PCB value creation is understandable, while customer, supplier and site-unit economics remain incomplete.", "blocking_gaps": ["Customer-side and supplier-side corroboration."], "source_refs": ["S1", "S6"]},
            {"gate": "business_economics", "result": "mixed", "reason": "Revenue, margin, profit and cash improved, but product/site economics, ROIC and working-capital durability remain unresolved.", "source_refs": ["S1", "S4", "S16"]},
            {"gate": "durable_moat", "result": "provisional", "reason": "Technology, qualification and manufacturing ramp are moat candidates, not yet a cross-cycle proof.", "source_refs": ["S1", "S6", "S8"]},
            {"gate": "management_and_capital_allocation", "result": "provisional", "reason": "A large reinvestment and issuance cycle is observable, but per-share outcomes and full governance review are pending.", "source_refs": ["S1", "S3", "S6"]},
            {"gate": "owner_earnings", "result": "range_only", "reason": "Reported cash is strong, but maintenance capex, required working capital and post-IPO distributable cash cannot be separated.", "source_refs": ["S1", "S4", "S16"]},
            {"gate": "survival_and_balance_sheet", "result": "provisional", "reason": "IPO proceeds improve gross liquidity, but post-IPO net cash, covenants and adverse-scenario funding remain unknown.", "source_refs": ["S3", "S4"]},
            {"gate": "intrinsic_value_and_margin_of_safety", "result": "inconclusive", "reason": "Trailing and forward PE sensitivities are reproducible; owner-earnings value and safety margin are not.", "source_refs": ["S10", "S12", "S16"]},
            {"gate": "decision_and_disconfirming_evidence", "result": "inconclusive", "reason": "The package supports monitoring and falsification, not a decision-ready conclusion; named human review is also absent.", "blocking_gaps": ["Interim report", "Owner-earnings bridge", "Named human review"], "source_refs": ["S17"]},
        ],
        "historical_valuation": {
            "status": "insufficient_point_in_time_history",
            "current_h_ttm_pe": 255.2 / ttm_eps_hkd,
            "current_a_ttm_pe": 60.0,
            "reason": "No no-look-ahead historical PE series was built; distance from the historical price high is not a valuation percentile.",
            "source_refs": ["S10", "S11", "S12"],
        },
        "price_move_attribution": {
            "status": "multi_factor_not_single_cause",
            "window": "2026-08-03 to 2026-08-10",
            "h_share_change_pct": 38.7,
            "a_share_change_pct": 51.1,
            "interpretation": "Aggregate order language, AI-PCB narrative and event anticipation are plausible contributors; price action does not verify a customer-specific order.",
            "source_refs": ["S7", "S10", "S11", "S14", "S17"],
        },
        "source_gaps": [
            "No customer-specific Rubin purchase order, price, volume or shipment disclosure.",
            "No post-IPO net-cash, debt and capex bridge before the interim report.",
            "No site-level yield, utilisation, revenue and margin bridge for the Thailand ramp.",
            "No decision-grade maintenance-capex owner-earnings bridge.",
            "No complete controller, related-party, tax/legal and supplier audit in this package.",
            "No named human review.",
        ],
        "invalidation_tests": [
            {"test": "Order-to-cash chain", "invalidated_if": "Order language stays qualitative while margin, cash conversion and inventory deteriorate across reporting periods.", "next_evidence": "2026 interim report", "review_date": "2026-08-28"},
            {"test": "Capacity economics", "invalidated_if": "Construction and depreciation rise without matching utilisation, shipment and revenue.", "next_evidence": "Thailand and Huizhou ramp disclosures", "review_date": "2026-12-31"},
            {"test": "Customer concentration", "invalidated_if": "Top-customer dependence rises while pricing or programme allocation weakens.", "next_evidence": "H1/FY2026 concentration", "review_date": "2026-08-28"},
            {"test": "Valuation support", "invalidated_if": "Normalised owner earnings do not approach the level required by the frozen price sensitivity.", "next_evidence": "Interim earnings and cash bridge", "review_date": "2026-08-28"},
        ],
        "review": {
            "human_review_required": True,
            "human_review_status": "pending",
            "production_reviewed": False,
            "machine_validation": "pending_rebuild",
            "publication_boundary_reviewed": True,
            "unresolved_critical_gaps": ["customer-specific order", "owner earnings", "post-IPO net cash", "named human review"],
        },
        "disclaimer": "Independent public-source research support, not investment advice. It is not affiliated with Berkshire Hathaway, Warren Buffett or Charlie Munger. No buy/sell instruction, target price or return guarantee is provided.",
    }


def main():
    artifact = build_artifact()
    (ROOT / "combined-artifact.v2.json").write_text(
        json.dumps(artifact, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    public_ledger = {
        "schema_version": "seed.public-company-source-ledger.v2",
        "as_of": RESEARCH_DATE,
        "publication_boundary": "No raw PDFs, API responses or full ASR transcript are included in the public package.",
        "sources": SOURCE_ROWS,
    }
    (ROOT / "source-ledger.json").write_text(
        json.dumps(public_ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
