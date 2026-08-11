#!/usr/bin/env python3
"""Build the public YOFC 06869.HK research pack.

The package follows the public Meitu-style company-research contract: two
reader doors, 25 dimensions, 50 indicator families, nine evidence gates,
three earnings/cash/capital bridges, an event monitor and a source ledger.
Unknowns stay unknown and sensitivity cases are not forecasts.
"""

from __future__ import annotations

import csv
import hashlib
import json
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RESEARCH_DATE = "2026-08-11"
PRICE_DATE = "2026-08-10"
GENERATED_AT = "2026-08-11T11:30:00+08:00"
H_PRICE = 124.60
A_PRICE = 343.09
FX_HKD_CNY = 0.86536
TOTAL_SHARES = 827_905_108
H_SHARES = 421_566_794
A_SHARES = 406_338_314
A_TREASURY_SHARES = 6_000_000
EFFECTIVE_SHARES = TOTAL_SHARES - A_TREASURY_SHARES


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


SOURCE_ROWS = [
    {
        "id": "S1", "tier": "A", "source_type": "exchange_filing",
        "title": "YOFC Annual Report 2025", "url": "https://www.hkexnews.hk/listedco/listconews/sehk/2026/0327/2026032703338_c.pdf",
        "published_at_status": "known", "published_at": "2026-03-27", "accessed_at": RESEARCH_DATE,
        "period": "FY2023-FY2025", "audit_status": "audited", "scope": "consolidated group",
        "covers": ["five-year bridge", "segments", "cash flow", "capital expenditure", "risk factors"],
        "content_sha256": "58888b55e4ada8f8b985e9377e83d5c71c31907c9acf873f10b1b1281c7f8d48",
    },
    {
        "id": "S2", "tier": "A", "source_type": "exchange_filing",
        "title": "YOFC Annual Report 2023", "url": "https://www1.hkexnews.hk/listedco/listconews/sehk/2024/0426/2024042600583.pdf",
        "published_at_status": "known", "published_at": "2024-04-26", "accessed_at": RESEARCH_DATE,
        "period": "FY2019-FY2023", "audit_status": "audited", "scope": "consolidated group",
        "covers": ["five-year summary", "FY2023 statements", "capital expenditure", "industry discussion"],
        "content_sha256": "226877c4f197b3886861ded0fb853982515bc168e421bff7ea2b1fc0a52567a1",
    },
    {
        "id": "S3", "tier": "A", "source_type": "exchange_filing",
        "title": "YOFC Annual Report 2022", "url": "https://www1.hkexnews.hk/listedco/listconews/sehk/2023/0427/2023042702169.pdf",
        "published_at_status": "known", "published_at": "2023-04-27", "accessed_at": RESEARCH_DATE,
        "period": "FY2018-FY2022", "audit_status": "audited", "scope": "consolidated group",
        "covers": ["FY2021-FY2022 statements", "cash flow", "capital expenditure", "working-capital cycles"],
        "content_sha256": "41af943325eef323b50f1ffc6be8b190524de213cb728de73b033f9db873242c",
    },
    {
        "id": "S4", "tier": "A", "source_type": "exchange_filing",
        "title": "YOFC 2026 First Quarterly Report", "url": "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0429/2026042904820.pdf",
        "published_at_status": "known", "published_at": "2026-04-29", "accessed_at": RESEARCH_DATE,
        "period": "2026Q1", "audit_status": "unaudited", "scope": "consolidated group",
        "covers": ["quarterly income", "gross margin", "cash flow", "working capital", "balance sheet"],
        "content_sha256": "534e15456c3d5d527226f0c2f6afdc6bc9316251d68385770b9562940ff872f2",
    },
    {
        "id": "S5", "tier": "A", "source_type": "exchange_filing",
        "title": "YOFC Positive Profit Alert for 2026H1", "url": "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0714/2026071401066.pdf",
        "published_at_status": "known", "published_at": "2026-07-14", "accessed_at": RESEARCH_DATE,
        "period": "2026H1 preliminary", "audit_status": "unaudited", "scope": "consolidated group",
        "covers": ["profit range", "adjusted profit range", "management explanation", "risk warning"],
        "content_sha256": "8c85cb9d45697998d085d2ec7b73aae97656b02cf3bb33d391540cc5b1582054",
    },
    {
        "id": "S6", "tier": "A", "source_type": "exchange_filing",
        "title": "Completion of Placing of 70 million New H Shares", "url": "https://www1.hkexnews.hk/listedco/listconews/sehk/2025/1217/2025121700608.pdf",
        "published_at_status": "known", "published_at": "2025-12-17", "accessed_at": RESEARCH_DATE,
        "period": "2025-12", "audit_status": "not_applicable", "scope": "H-share capital and proceeds",
        "covers": ["share issuance", "placing price", "net proceeds", "use of proceeds"],
        "content_sha256": "deed795150d8f7b341756f7933e0b348c59c6e6f536f4b00ccebd91f0464309d",
    },
    {
        "id": "S7", "tier": "A", "source_type": "exchange_filing",
        "title": "YOFC July 2026 Monthly Return", "url": "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0805/2026080500442.pdf",
        "published_at_status": "known", "published_at": "2026-08-05", "accessed_at": RESEARCH_DATE,
        "period": "2026-07", "audit_status": "not_applicable", "scope": "A/H issued and treasury shares",
        "covers": ["H shares", "A shares", "treasury shares", "public float"],
        "content_sha256": "5c5feabeb449a6fe1eb9ab2b0d9195c7a92fd8fbd1b38dde2f55516a77b96f42",
    },
    {
        "id": "S8", "tier": "A", "source_type": "exchange_market_infrastructure",
        "title": "SSE Southbound Eligible Securities Query", "url": "https://www.sse.com.cn/services/hkexsc/disclo/eligible/",
        "published_at_status": "not_disclosed", "published_at": None, "date_reason": "Point-in-time official query page.", "accessed_at": RESEARCH_DATE,
        "period": "2026-08-11 query", "audit_status": "not_applicable", "scope": "Shanghai Southbound eligibility",
        "covers": ["Stock Connect eligibility", "official query boundary"],
        "content_sha256": "21bd6fd37c2a53a163919047b7e4c11e476213e59da66d14c466551197d8ba40",
    },
    {
        "id": "S9", "tier": "A", "source_type": "exchange_market_infrastructure",
        "title": "SZSE Southbound Eligible Securities Query", "url": "https://www.szse.cn/szhk/hkbussiness/underlylist/",
        "published_at_status": "not_disclosed", "published_at": None, "date_reason": "Point-in-time official query page.", "accessed_at": RESEARCH_DATE,
        "period": "2026-08-11 query", "audit_status": "not_applicable", "scope": "Shenzhen Southbound eligibility",
        "covers": ["Stock Connect eligibility", "official query boundary"],
        "content_sha256": "14217e51de2161ddb0e3ff469a588f816bfd8b72f8580a219da255aa288b3961",
    },
    {
        "id": "S10", "tier": "C", "source_type": "defined_market_data_api",
        "title": "Tencent 06869.HK Daily Prices", "url": "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=hk06869,day,2026-05-01,2026-08-11,200,qfq",
        "published_at_status": "not_disclosed", "published_at": None, "date_reason": "Machine endpoint has no separate publication timestamp.", "accessed_at": RESEARCH_DATE,
        "period": "through 2026-08-11 intraday; valuation frozen at 2026-08-10 close", "audit_status": "not_applicable", "scope": "H-share price and volume",
        "covers": ["price", "price history", "drawdown", "rebound", "volume"],
        "content_sha256": "70530b6d714c171b07a047b9dbe37681746e5c805923162e7a9ca612eeb8e362",
    },
    {
        "id": "S11", "tier": "C", "source_type": "defined_market_data_api",
        "title": "Tencent 601869.SH Daily Prices", "url": "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=sh601869,day,2026-05-01,2026-08-11,200,qfq",
        "published_at_status": "not_disclosed", "published_at": None, "date_reason": "Machine endpoint has no separate publication timestamp.", "accessed_at": RESEARCH_DATE,
        "period": "through 2026-08-10 close", "audit_status": "not_applicable", "scope": "A-share price and volume",
        "covers": ["A-share price history", "A/H valuation bridge", "cross-listing momentum"],
        "content_sha256": "1c4d80e13d4bb5f86ab71e8007323c05c0960ea1cd147d64a62234d6190e62ec",
    },
    {
        "id": "S12", "tier": "A", "source_type": "official_fx_query",
        "title": "SAFE RMB Central Parity Query", "url": "https://www.safe.gov.cn/AppStructured/hlw/RMBQuery.do",
        "published_at_status": "known", "published_at": PRICE_DATE, "accessed_at": RESEARCH_DATE,
        "period": PRICE_DATE, "audit_status": "not_applicable", "scope": "100 HKD = CNY86.536 central parity",
        "covers": ["HKD/CNY", "A/H bridge", "valuation currency conversion"],
        "content_sha256": "d01391bd193c9b34f78339eba926af361e08c9c456ad8ec0f672018300e7af18",
    },
    {
        "id": "S13", "tier": "A", "source_type": "industry_primary_source",
        "title": "Corning Q2 2026 Results and Optical Communications Demand", "url": "https://investor.corning.com/news-and-events/news/news-details/2026/Cornings-Strong-Second-Quarter-2026-Financial-Results1-Demonstrate-Progress-on-Recently-Upgraded-Springboard-Plan/default.aspx",
        "published_at_status": "known", "published_at": "2026-07-28", "accessed_at": RESEARCH_DATE,
        "period": "2026Q2", "audit_status": "unaudited", "scope": "Corning optical communications segment; adjacent global demand signal",
        "covers": ["optical communications growth", "enterprise network demand", "future capacity expansion"],
        "content_sha256": "28f354fe180288e8d34234f31960ce0c45ecb2d24d559912eca441e5bf0b1d79",
    },
    {
        "id": "S14", "tier": "A", "source_type": "competitor_exchange_filing",
        "title": "Dahan Cable Optical Fibre and Preform Capacity Project", "url": "https://disc.static.szse.cn/download/disc/disk03/finalpage/2026-06-26/c0eea83a-c03e-407f-ad8b-926cd6fe760f.PDF",
        "published_at_status": "known", "published_at": "2026-06-26", "accessed_at": RESEARCH_DATE,
        "period": "2026 expansion plan", "audit_status": "not_applicable", "scope": "announced domestic optical-fibre capacity",
        "covers": ["capacity plan", "project cost", "phasing", "uncertainty warning"],
        "content_sha256": "dee7f6b4cde8310038baeb3828c903c5a06e3f80b4a7c71cd290a787cdaf0d59",
    },
    {
        "id": "S15", "tier": "A", "source_type": "issuer_product_release",
        "title": "YOFC HollowBand Hollow-Core Fibre Launch", "url": "https://en.yofc.com/view/3543.html",
        "published_at_status": "known", "published_at": "2026-03-06", "accessed_at": RESEARCH_DATE,
        "period": "2026 product and pilot progress", "audit_status": "not_applicable", "scope": "issuer technology claims",
        "covers": ["hollow-core performance", "integrated manufacturing", "pilot projects", "commercialisation boundary"],
        "content_sha256": "89602cccf221b530a573909a193cfd89604f113444719e47f384c9c6e15dd434",
    },
    {
        "id": "S16", "tier": "A", "source_type": "exchange_filing",
        "title": "Acquisition of 25% of YOFC Shanghai", "url": "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0730/2026073002049.pdf",
        "published_at_status": "known", "published_at": "2026-07-30", "accessed_at": RESEARCH_DATE,
        "period": "2026-07", "audit_status": "not_applicable", "scope": "EUR12m acquisition and consolidation change",
        "covers": ["transaction", "consolidation scope", "target financials", "industry-cycle risk"],
        "content_sha256": "e5439945699208065c7f829ca277cc2c770353de9ca9cc5792cfb951d4e7c22e",
    },
    {
        "id": "S17", "tier": "A", "source_type": "peer_investor_relations",
        "title": "Lumentum FY2026 Results Date", "url": "https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Announces-Reporting-Date-for-Fourth-Quarter-and-Fiscal-Year-2026-Results/default.aspx",
        "published_at_status": "known", "published_at": "2026-07-29", "accessed_at": RESEARCH_DATE,
        "period": "2026-08-11 event", "audit_status": "not_applicable", "scope": "adjacent optical-component event",
        "covers": ["earnings date", "overnight sector signal"],
        "content_sha256": "7e76d9c7ad19dc928dfee5a0e4c5eafdf472c5a8c8b214b00d2ba87f987b3ff8",
    },
    {
        "id": "S18", "tier": "A", "source_type": "peer_investor_relations",
        "title": "Coherent FY2026 Results Date", "url": "https://www.coherent.com/news/press-releases/fy2026-fourth-quarter-fy2026-conference-call-announced",
        "published_at_status": "known", "published_at": "2026-07-23", "accessed_at": RESEARCH_DATE,
        "period": "2026-08-12 event", "audit_status": "not_applicable", "scope": "adjacent optical-component event",
        "covers": ["earnings date", "overnight sector signal"],
        "content_sha256": "c21d9abd343c9fabcb268acc51fa3520177f4092ec4eef16a0ea839cffe57002",
    },
    {
        "id": "S19", "tier": "C", "source_type": "defined_market_data_api",
        "title": "Tencent CIG 06166.HK Daily Prices", "url": "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=hk06166,day,2026-07-24,2026-08-11,40,qfq",
        "published_at_status": "not_disclosed", "published_at": None, "date_reason": "Machine endpoint has no separate publication timestamp.", "accessed_at": RESEARCH_DATE,
        "period": "2026-07-24 to 2026-08-11", "audit_status": "not_applicable", "scope": "adjacent Hong Kong optical theme tape",
        "covers": ["sector comparison", "relative rebound"],
        "content_sha256": "e1b57029a4298509c245ea54d139b915f459b3d352e555a1e3b553ae1d3bced5",
    },
    {
        "id": "S20", "tier": "C", "source_type": "defined_market_data_api",
        "title": "Tencent HSCEI Daily Prices", "url": "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=hkHSCEI,day,2026-07-24,2026-08-11,40,qfq",
        "published_at_status": "not_disclosed", "published_at": None, "date_reason": "Machine endpoint has no separate publication timestamp.", "accessed_at": RESEARCH_DATE,
        "period": "2026-07-24 to 2026-08-11", "audit_status": "not_applicable", "scope": "broad Hong Kong market benchmark",
        "covers": ["market comparison", "idiosyncratic attribution"],
        "content_sha256": "1ee2f8b971bf3bcaa25ca7a7f46e925d846f2811fc00b8d7da1a9581e4c6af49",
    },
]


INDICATORS = {
    "security_and_legal_subject": ("exact_security_issuer_share_class_and_rights", "dated_price_share_count_currency_and_listing_status"),
    "control_and_beneficial_ownership": ("controller_voting_pledges_and_cross_holdings", "value_transfers_nci_and_related_party_exposure"),
    "business_model": ("payer_value_proposition_revenue_and_cash_mechanism", "capital_needs_and_business_failure_variables"),
    "revenue_structure": ("segment_product_and_geography_reconciliation", "volume_price_mix_acquisition_and_scope_bridge"),
    "industry_chain_position": ("upstream_process_customer_payer_and_substitute_map", "profit_pool_and_inventory_credit_technology_risk"),
    "product_and_unit_economics": ("price_volume_mix_and_incremental_economics", "industry_denominator_scope_and_comparability"),
    "customers": ("customer_channel_end_user_and_payer_separation", "concentration_retention_receivables_inventory_and_external_evidence"),
    "suppliers": ("critical_inputs_concentration_related_parties_and_substitution", "terms_prepayments_availability_and_cost_pass_through"),
    "competition_structure": ("entry_exit_capacity_price_and_substitution", "competitor_customer_and_regulator_corroboration"),
    "durable_moat": ("mechanism_economic_result_durability_and_direction", "strongest_falsifying_evidence"),
    "revenue_quality": ("revenue_receivables_contract_assets_returns_and_cash", "acquisition_period_end_channel_and_recognition_distortion"),
    "earnings_quality": ("reported_to_normalized_parent_earnings_bridge", "tax_attribution_scope_and_adjustment_disagreement"),
    "cash_conversion": ("profit_operating_cash_and_distributable_cash_bridge", "factoring_payment_restricted_cash_and_sector_scope"),
    "working_capital": ("receivables_inventory_payables_prepayments_and_contract_balances", "sustainable_financing_vs_temporary_cash_release"),
    "capital_intensity": ("maintenance_vs_growth_investment_range", "capex_capacity_utilization_and_competitive_requirements"),
    "returns_on_capital": ("multiperiod_roe_roic_and_incremental_returns", "leverage_buyback_cycle_and_accounting_decomposition"),
    "balance_sheet_survival": ("debt_liquidity_covenants_guarantees_pledges_and_off_balance", "adverse_scenario_financing_need"),
    "capital_allocation": ("reinvestment_ma_dividend_buyback_issuance_debt_and_cash_ledger", "diluted_per_share_outcomes_and_opportunity_cost"),
    "management": ("dated_commitments_vs_outcomes", "incentives_compensation_succession_insider_actions_and_candor"),
    "governance_and_related_parties": ("related_sales_purchases_loans_guarantees_and_asset_transfers", "pricing_minority_fairness_oversight_and_dissent"),
    "accounting_and_audit": ("audit_kam_standard_policy_and_restatement", "statement_reproduction_and_conflict_preservation"),
    "tax_and_legal": ("effective_deferred_and_uncertain_tax", "litigation_penalties_compliance_and_tail_exposure"),
    "per_share_economics": ("basic_diluted_and_fully_diluted_share_reconciliation", "per_share_growth_distribution_issuance_and_repurchase_outcomes"),
    "valuation": ("currency_consistent_value_range_assumptions_and_dates", "reverse_expectations_sensitivities_and_cross_check"),
    "disconfirming_evidence": ("independent_strongest_counter_thesis", "observable_invalidation_next_evidence_and_review_date"),
}


DIMENSIONS = {
    "security_and_legal_subject": ("applicable", "06869.HK 与 601869.SH 是同一发行人的 H/A 两类股份；分别定价、不可假定自由互换。", ["S7", "S10", "S11", "S12"], ("observed", "observed")),
    "control_and_beneficial_ownership": ("unknown", "主要股东可见，但质押、交叉持股、少数股东价值转移图未完成。", ["S4", "S7"], ("observed", "not_disclosed")),
    "business_model": ("applicable", "从预制棒到光纤、光缆和光互联组件一体化；现金取决于需求、ASP、产品组合、良率、回款与资本开支。", ["S1", "S4", "S5"], ("observed", "observed")),
    "revenue_structure": ("unknown", "2025 光传输 58.6%、光互联 22.1%，海外收入约 42.3%；2026H1 细分桥待正式中报。", ["S1", "S5"], ("observed", "not_disclosed")),
    "industry_chain_position": ("applicable", "位于石英/套管/设备之后、运营商与数据中心连接之前；AI 是增量，不是全部收入。", ["S1", "S13", "S15"], ("observed", "observed")),
    "product_and_unit_economics": ("unknown", "毛利率跃迁已观察，但光纤销量、ASP、有效产能、良率和单位贡献未完整披露。", ["S1", "S4", "S5"], ("observed", "not_disclosed")),
    "customers": ("unknown", "运营商仍是基础客户，算力数据中心客户扩张由公司归因确认；客户集中、留存与终端库存未完整披露。", ["S1", "S5"], ("observed", "not_disclosed")),
    "suppliers": ("unknown", "一体化降低部分上游依赖，但原料、能源、设备瓶颈、关联采购与成本传导表未完成。", ["S1"], ("not_disclosed", "not_disclosed")),
    "competition_structure": ("applicable", "普通单模光纤历史上价格周期明显，AI 新型光纤改善需求；国内外扩产会重新分配利润池。", ["S1", "S13", "S14"], ("observed", "observed")),
    "durable_moat": ("applicable", "预制棒工艺、一体化制造、全球基地与空芯光纤是护城河候选；跨周期 ROIC 与份额保持仍未证明。", ["S1", "S15"], ("observed", "observed")),
    "revenue_quality": ("unknown", "2025 和 2026Q1 经营现金流支持收入真实性，但海外工程、回款和期末确认仍需跟踪。", ["S1", "S4"], ("observed", "not_disclosed")),
    "earnings_quality": ("applicable", "2025 扣非利润仅 RMB5.16 亿；2026Q1 扣非利润 RMB4.61 亿，H1 扣非预告 RMB20—26 亿，质量明显改善但未审计。", ["S1", "S4", "S5"], ("observed", "observed")),
    "cash_conversion": ("unknown", "2025 CFO RMB36.53 亿，减全部长期资产购置现金后代理值 RMB22.31 亿；不等同 owner earnings。", ["S1"], ("observed", "not_disclosed")),
    "working_capital": ("unknown", "2026Q1 应收较年末微降、存货升 11.1%；是否对应备货还是消化放缓尚不能确认。", ["S4"], ("observed", "not_disclosed")),
    "capital_intensity": ("unknown", "2025 长期资产购置现金 RMB14.22 亿；维护与增长投入不可拆分，海外扩产会提高未来资本需求。", ["S1", "S6"], ("not_disclosed", "observed")),
    "returns_on_capital": ("unknown", "2025 加权 ROE 6.92%，2026Q1 单季 3.53%；周期、杠杆、配股与新增产能的增量 ROIC 未拆。", ["S1", "S4", "S6"], ("observed", "not_disclosed")),
    "balance_sheet_survival": ("unknown", "2026Q1 现金 RMB55.25 亿、债务代理约 RMB87.05 亿；配股改善流动性，但仍不是净现金公司。", ["S4", "S6"], ("observed", "not_disclosed")),
    "capital_allocation": ("unknown", "70m H 股配售、海外扩产、员工持股和上海子公司收购均已记录；每股回报尚待结果。", ["S1", "S6", "S16"], ("observed", "not_disclosed")),
    "management": ("unknown", "对 H1 增长原因的表述可在正式中报验证；长期承诺—结果、薪酬、接班与内部人行动账本未完成。", ["S5"], ("observed", "not_disclosed")),
    "governance_and_related_parties": ("unknown", "A/H 股权与收购事项可见，但关联交易、定价、公平性和监督机制的注释级复核未完成。", ["S1", "S16"], ("observed", "not_disclosed")),
    "accounting_and_audit": ("applicable", "2021—2025 来自审计年报；2026Q1 与 H1 预告明确标为未审计，未混同。", ["S1", "S2", "S3", "S4", "S5"], ("observed", "observed")),
    "tax_and_legal": ("unknown", "有效税率波动和海外法域扩大已识别，完整递延税、诉讼、制裁、合规尾部风险表未完成。", ["S1"], ("observed", "not_disclosed")),
    "per_share_economics": ("applicable", "总股本 827.905m，H 股 421.567m，A 股 406.338m，其中库存 A 股 6m；配股摊薄已入分母。", ["S6", "S7"], ("observed", "observed")),
    "valuation": ("applicable", "按 H 股 8 月 10 日收盘与官方汇率，FY2025 P/E 约 109.7×、Q1 TTM 约 77.1×；H1 年化敏感性约 14.9—18.6×。", ["S1", "S4", "S5", "S7", "S10", "S12"], ("observed", "observed")),
    "disconfirming_evidence": ("applicable", "最强反方是利润率处于周期峰值、供给扩张和 AI 收入纯度被高估；验证点已绑定正式中报和扩产兑现。", ["S5", "S13", "S14"], ("observed", "observed")),
}


FINANCIAL_HISTORY = [
    {"period": "FY2021", "revenue_bn": 9.5361, "gross_profit_bn": 1.8718, "gross_margin_pct": 19.6, "parent_profit_bn": 0.7085, "cfo_bn": 0.5267, "capex_bn": 1.0736, "cash_after_all_capex_bn": -0.5469, "source_refs": ["S3"]},
    {"period": "FY2022", "revenue_bn": 13.8303, "gross_profit_bn": 3.2432, "gross_margin_pct": 23.5, "parent_profit_bn": 1.1670, "cfo_bn": 1.5945, "capex_bn": 2.2282, "cash_after_all_capex_bn": -0.6337, "source_refs": ["S3"]},
    {"period": "FY2023", "revenue_bn": 13.3528, "gross_profit_bn": 3.2720, "gross_margin_pct": 24.5, "parent_profit_bn": 1.2974, "cfo_bn": 1.5144, "capex_bn": 2.2627, "cash_after_all_capex_bn": -0.7483, "source_refs": ["S1", "S2"]},
    {"period": "FY2024", "revenue_bn": 12.1974, "gross_profit_bn": 3.3301, "gross_margin_pct": 27.3, "parent_profit_bn": 0.6759, "cfo_bn": 1.7834, "capex_bn": 1.3858, "cash_after_all_capex_bn": 0.3976, "source_refs": ["S1"]},
    {"period": "FY2025", "revenue_bn": 14.2521, "gross_profit_bn": 4.3803, "gross_margin_pct": 30.7, "parent_profit_bn": 0.8137, "cfo_bn": 3.6529, "capex_bn": 1.4222, "cash_after_all_capex_bn": 2.2306, "source_refs": ["S1"]},
    {"period": "2026Q1", "revenue_bn": 3.6954, "gross_profit_bn": 1.5341, "gross_margin_pct": 41.51, "parent_profit_bn": 0.4951, "cfo_bn": 0.6178, "capex_bn": 0.3359, "cash_after_all_capex_bn": 0.2818, "source_refs": ["S4"]},
]


PRICE_ROWS = [
    ["2026-06-22", 235.6, 286.0, 290.6, 235.0, 48_305_855],
    ["2026-06-23", 290.2, 264.6, 305.0, 260.2, 32_256_541],
    ["2026-06-26", 286.8, 250.6, 286.8, 242.0, 28_472_896],
    ["2026-07-02", 228.4, 198.3, 229.2, 198.0, 40_078_361],
    ["2026-07-14", 142.0, 153.9, 154.1, 134.6, 36_305_166],
    ["2026-07-15", 176.9, 156.4, 188.0, 153.0, 65_793_972],
    ["2026-07-21", 144.8, 142.0, 148.2, 125.3, 61_279_031],
    ["2026-07-30", 100.9, 92.0, 103.9, 91.15, 38_972_784],
    ["2026-08-03", 96.0, 95.7, 98.25, 93.05, 18_295_744],
    ["2026-08-04", 98.5, 105.6, 107.0, 98.5, 33_415_662],
    ["2026-08-05", 100.2, 121.0, 126.7, 99.1, 64_441_246],
    ["2026-08-06", 118.0, 117.3, 124.0, 114.5, 37_495_052],
    ["2026-08-07", 118.2, 124.1, 125.9, 116.8, 35_291_030],
    ["2026-08-10", 128.8, 124.6, 132.7, 119.6, 28_445_826],
    ["2026-08-11_intraday", 122.0, 122.3, 123.5, 118.0, 6_691_996],
]


def indicator_row(indicator_id: str, status: str, refs: list[str], gap: str) -> dict:
    return {
        "id": indicator_id,
        "status": status,
        "summary": "Evidence is recorded in the dimension result." if status == "observed" else gap,
        "source_refs": refs if status in {"observed", "conflicting"} else [],
        "source_gaps": [gap] if status in {"not_disclosed", "conflicting"} else [],
    }


def build_dimensions() -> list[dict]:
    rows = []
    for name, ids in INDICATORS.items():
        status, summary, refs, indicator_statuses = DIMENSIONS[name]
        gap = f"{name} requires additional primary-source evidence."
        rows.append({
            "dimension": name,
            "status": status,
            "summary": summary,
            "indicators": [
                indicator_row(ids[0], indicator_statuses[0], refs, gap),
                indicator_row(ids[1], indicator_statuses[1], refs, gap),
            ],
            "source_refs": refs,
            "positive_evidence": [summary] if status == "applicable" else [],
            "counter_evidence": ["The strongest contrary reading is preserved in the report and red-team review."],
            "source_gaps": [gap] if "not_disclosed" in indicator_statuses or status == "unknown" else [],
        })
    return rows


def hkd_eps(profit_cny: float) -> float:
    return profit_cny / TOTAL_SHARES / FX_HKD_CNY


def evidence_block(status: str, reason: str, refs: list[str], rows: list[dict], gaps: list[str]) -> dict:
    return {"status": status, "reason": reason, "source_refs": refs, "rows": rows, "gaps": gaps}


def build_artifact() -> dict:
    fy_profit = 813_737_266
    ttm_profit = fy_profit + 495_131_710 - 151_696_565
    forward_cases = [("bear", 3_400_000_000), ("base", 4_800_000_000), ("upside", 6_000_000_000)]
    scenarios = []
    for name, profit in forward_cases:
        eps = hkd_eps(profit)
        scenarios.append({
            "scenario": name, "status": "calculated_pe", "forecast_eps": eps,
            "implied_pe_at_current_price": H_PRICE / eps,
            "assumption": f"FY2026 parent-profit sensitivity CNY{profit / 1e9:.1f}bn; not a forecast.",
            "source_refs": ["S5", "S7", "S10", "S12"],
        })
    gates = [
        {"gate": "identity_and_source_integrity", "result": "provisional", "reason": "Issuer, A/H classes, shares, price, currency and Stock Connect status are resolved; full ownership graph is incomplete.", "source_refs": ["S7", "S8", "S9", "S10", "S12"]},
        {"gate": "circle_of_competence", "result": "provisional", "reason": "Demand-to-cash chain is understandable, but product-level ASP, effective capacity and customer mix are not fully disclosed.", "source_refs": ["S1", "S5"]},
        {"gate": "business_economics", "result": "mixed", "reason": "Q1/H1 margins and profit confirm an inflection; cycle duration and segment purity remain unresolved.", "source_refs": ["S4", "S5"]},
        {"gate": "durable_moat", "result": "provisional", "reason": "Integration, process capability and global footprint are moat candidates, not a cross-cycle proof.", "source_refs": ["S1", "S15"]},
        {"gate": "management_and_capital_allocation", "result": "provisional", "reason": "Placement, overseas expansion and acquisition are visible; diluted per-share outcomes are not.", "source_refs": ["S6", "S16"]},
        {"gate": "owner_earnings", "result": "range_only", "reason": "Cash proxy is reproducible, but maintenance capex and required working capital cannot be separated.", "source_refs": ["S1", "S4"]},
        {"gate": "survival_and_balance_sheet", "result": "provisional", "reason": "Liquidity is material and near-term survival is not the core issue; net-debt, overseas expansion and covenant details still need monitoring.", "source_refs": ["S4", "S6"]},
        {"gate": "intrinsic_value_and_margin_of_safety", "result": "inconclusive", "reason": "P/E sensitivities are reproducible, but owner-earnings value and safety margin are unavailable.", "source_refs": ["S5", "S10", "S12"]},
        {"gate": "decision_and_disconfirming_evidence", "result": "inconclusive", "reason": "The pack supports monitoring and falsification; formal H1, owner earnings and named human review remain open.", "source_refs": ["S5", "S14"]},
    ]
    valuation_blocks = {
        "pe_denominator_matrix": evidence_block("partial", "Reported and sensitivity denominators are dated; adjusted and normalized denominators remain open.", ["S1", "S4", "S5", "S10", "S12"], [
            {"label": "reported_fy", "profit_cny_bn": 0.814, "pe": H_PRICE / hkd_eps(fy_profit)},
            {"label": "reported_ttm", "profit_cny_bn": ttm_profit / 1e9, "pe": H_PRICE / hkd_eps(ttm_profit)},
            {"label": "adjusted", "profit_cny_bn": None},
            {"label": "forward_fy1", "profit_cny_bn": 4.8, "pe": H_PRICE / hkd_eps(4.8e9)},
            {"label": "normalized_midcycle", "profit_cny_bn": None},
        ], ["Formal H1 segment and cash bridge", "Normalized mid-cycle profit"]),
        "forward_driver_ledger": evidence_block("partial", "Demand, customer mix, supply and margin drivers are explicit but not all quantified.", ["S5", "S13", "S14"], [{"driver": "AI/data-center fibre demand", "direction": "positive"}, {"driver": "industry capacity additions", "direction": "negative_lagged"}], ["YOFC order volume and ASP"]),
        "segment_forecast_model": evidence_block("unavailable", "H1 segment revenue and margin are not yet published.", ["S5"], [], ["Formal 2026H1 segment note"]),
        "substitution_map": evidence_block("partial", "Solid-core, hollow-core, modules and copper/optical interconnect roles are mapped qualitatively.", ["S1", "S15"], [{"technology": "hollow-core", "status": "optionality_not_material_revenue_proof"}], ["Commercial volumes and margins"]),
        "industry_capacity_cycle": evidence_block("partial", "Demand confirmation and announced capacity are both present; timing and effective output are uncertain.", ["S13", "S14"], [{"side": "demand", "signal": "global AI connectivity growth"}, {"side": "supply", "signal": "new preform/fibre projects"}], ["Effective capacity and ramp dates"]),
        "peer_comparables": evidence_block("partial", "Hengtong, ZTT, Prysmian and Corning are diversified or cross-market; no decision-grade three-peer median is used.", ["S13"], [{"peer": "Corning", "qualification": "adjacent"}, {"peer": "Prysmian", "qualification": "adjacent"}], ["Three same-scope, same-date peers"]),
        "historical_point_in_time": evidence_block("partial", "Price drawdown is dated, but no no-look-ahead historical P/E series is claimed.", ["S10"], [{"date": "2026-06-22", "close": 286.0}, {"date": "2026-07-30", "close": 92.0}, {"date": PRICE_DATE, "close": H_PRICE}], ["Point-in-time EPS history"]),
        "low_pe_diagnosis": evidence_block("partial", "The apparent forward low P/E is caused by annualizing an exceptional H1 profit alert, not by a settled normalized denominator.", ["S5", "S10", "S12"], [{"diagnosis": "duration_of_peak_profit_uncertain"}], ["Formal H1 and H2 order/cash evidence"]),
        "price_owner_earnings_matrix": evidence_block("unavailable", "Owner earnings is unavailable, so no price-to-owner-earnings claim is made.", ["S1", "S4"], [], ["Maintenance capex", "Required working capital"]),
        "investment_return_ledger": evidence_block("partial", "Overseas expansion, placement and acquisition are recorded; incremental return has not matured.", ["S6", "S16"], [{"action": "H-share placing", "amount_hkd_bn": 2.229}, {"action": "YOFC Shanghai 25%", "amount_eur_m": 12}], ["Post-deployment cash returns"]),
        "price_multiple_attribution": evidence_block("partial", "Move reflects fundamental confirmation, supply fear and crowded AI rerating rather than one event.", ["S5", "S10", "S14", "S19", "S20"], [{"factor": "profit alert", "direction": "fundamental_positive"}, {"factor": "capacity expansion", "direction": "valuation_negative"}], ["Investor-flow and borrow data"]),
    }
    return {
        "schema_version": "seed.stock-fundamentals-valuation.v2",
        "artifact_type": "stock_fundamentals_valuation", "artifact_role": "public_research_support",
        "status": "needs_human_review", "generated_at": GENERATED_AT,
        "security": {"security_id": "HKEX:06869", "company_name": "Yangtze Optical Fibre and Cable Joint Stock Limited Company", "company_name_zh": "长飞光纤光缆股份有限公司", "ticker": "06869", "exchange": "HKEX", "listing_type": "H_share_cross_listed_with_SSE_A_share", "currency": "HKD", "fiscal_year_end": "12-31", "reporting_standard": "PRC Accounting Standards for Business Enterprises", "cross_listing": "SSE:601869", "stock_connect": "eligible_via_shanghai_and_shenzhen_southbound_as_checked_2026_08_11"},
        "as_of": {"research_date": RESEARCH_DATE, "price_date": PRICE_DATE, "price": H_PRICE, "price_source_ref": "S10", "timezone": "Asia/Shanghai", "intraday_note": "2026-08-11 quote is partial; all valuation uses the last complete 2026-08-10 close."},
        "methodology_refs": [
            {"id": "berkshire_owner_manual", "title": "Berkshire Hathaway Owner's Manual", "url": "https://www.berkshirehathaway.com/ownman.pdf", "use": "Owner orientation, per-share value and survival boundary."},
            {"id": "berkshire_1986_letter", "title": "1986 Chairman's Letter", "url": "https://www.berkshirehathaway.com/letters/1986.html", "use": "Owner-earnings concept and maintenance-capex uncertainty."},
            {"id": "berkshire_2007_letter", "title": "2007 Chairman's Letter", "url": "https://www.berkshirehathaway.com/letters/2007ltr.pdf", "use": "Durable moat and capital-intensity tests."},
            {"id": "berkshire_2018_letter", "title": "2018 Chairman's Letter", "url": "https://www.berkshirehathaway.com/letters/2018ltr.pdf", "use": "Business-value versus market-timing and per-share capital allocation."},
        ],
        "source_refs": SOURCE_ROWS,
        "source_boundaries": {"facts": "Exchange filings, official issuer/peer releases and deterministic calculations.", "reported_claims": "Company profit-alert explanations and product claims remain attributed.", "interpretations": "Industry classification, cycle position and risk/reward are research judgments.", "assumptions": "FY2026 profit cases are sensitivities without probabilities.", "source_gaps": "Formal H1 segment/cash data, effective capacity, ASP and owner earnings are unresolved.", "publication": "No private portfolio, raw media or transcript is included."},
        "ownership_structure": {"gross_total_shares": TOTAL_SHARES, "h_shares": H_SHARES, "gross_a_shares": A_SHARES, "treasury_a_shares": A_TREASURY_SHARES, "effective_total_shares": EFFECTIVE_SHARES, "source_refs": ["S6", "S7"], "boundary": "A and H are separately priced share classes; the H line is valued with its own price and currency."},
        "financial_history": {"currency": "CNY", "scope": "consolidated group", "periods": FINANCIAL_HISTORY},
        "segment_data": {"industry_branch": "optical_fibre_preform_fibre_cable_and_optical_connectivity_manufacturing", "value_chain": "raw silica and equipment -> preform -> fibre -> cable/connectivity -> operators and data centres -> end-network traffic", "fy2025_mix": {"optical_transmission_pct": 58.56, "optical_interconnect_pct": 22.06, "overseas_revenue_pct": 42.34}, "limitations": ["No formal 2026H1 segment table yet.", "AI/data-centre revenue purity is not disclosed."], "source_refs": ["S1", "S5"]},
        "research_dimensions": build_dimensions(),
        "earnings_quality_bridge": {"status": "partial_but_improving", "reported_parent_profit_fy2025_cny_bn": 0.814, "adjusted_parent_profit_fy2025_cny_bn": 0.516, "q1_2026_parent_profit_cny_bn": 0.495, "q1_2026_adjusted_parent_profit_cny_bn": 0.461, "h1_2026_parent_profit_alert_cny_bn": [2.4, 3.0], "h1_2026_adjusted_profit_alert_cny_bn": [2.0, 2.6], "source_refs": ["S1", "S4", "S5"]},
        "owner_earnings": {"currency": "HKD", "status": "unavailable", "range": [], "reason": "Maintenance capex and required working capital cannot be separated from growth investment and cycle cash release.", "limitations": ["CFO minus all capex is only a conservative cash proxy.", "H1 profit alert contains no cash-flow or segment note."], "source_refs": ["S1", "S4"]},
        "capital_allocation": {"status": "large_reinvestment_and_consolidation_cycle", "actions": ["70m H-share placing", "overseas capacity expansion", "2025 employee stock ownership plan", "YOFC Shanghai 25% acquisition"], "per_share_outcome": "not_yet_observable", "source_refs": ["S1", "S6", "S16"]},
        "balance_sheet_quality": {"status": "adequate_liquidity_with_net_debt_proxy", "q1_2026_cash_cny_bn": 5.525, "q1_2026_interest_debt_proxy_cny_bn": 8.705, "q1_2026_net_debt_proxy_cny_bn": 3.180, "limitations": ["Proxy excludes detailed lease and long-term-payable classification.", "Trading financial assets are not treated as cash."], "source_refs": ["S4"]},
        "pe_matrix": [
            {"label": "reported_fy", "status": "calculated", "price": H_PRICE, "currency": "HKD", "price_as_of": PRICE_DATE, "eps": hkd_eps(fy_profit), "eps_period": "FY2025", "eps_type": "reported_parent_profit_on_current_group_shares_translated_to_HKD", "formula": "HKD124.60 / (CNY0.813737bn / 827.905108m / 0.86536)", "pe": H_PRICE / hkd_eps(fy_profit), "earnings_yield": hkd_eps(fy_profit) / H_PRICE, "source_refs": ["S1", "S7", "S10", "S12"], "confidence": "high", "limitations": ["Current shares are used against historical profit; trailing profit is not owner earnings."]},
            {"label": "reported_ttm", "status": "calculated", "price": H_PRICE, "currency": "HKD", "price_as_of": PRICE_DATE, "eps": hkd_eps(ttm_profit), "eps_period": "TTM through 2026Q1", "eps_type": "reported_parent_profit_on_current_group_shares_translated_to_HKD", "formula": "HKD124.60 / ((FY2025 + 2026Q1 - 2025Q1) / 827.905108m / 0.86536)", "pe": H_PRICE / hkd_eps(ttm_profit), "earnings_yield": hkd_eps(ttm_profit) / H_PRICE, "source_refs": ["S1", "S4", "S7", "S10", "S12"], "confidence": "high", "limitations": ["TTM stops at Q1 and therefore excludes the preliminary Q2 step-up."]},
            {"label": "normalised_owner_earnings", "status": "unavailable", "price": H_PRICE, "currency": "HKD", "price_as_of": PRICE_DATE, "eps": None, "eps_period": "normalised_midcycle", "eps_type": "owner_earnings_per_share", "pe": None, "source_refs": ["S1", "S4"], "confidence": "low", "limitations": ["Maintenance capex and required working capital are unresolved."], "reason": "No decision-grade owner-earnings denominator is available."},
        ],
        "forward_scenarios": {"currency": "HKD", "price_anchor": H_PRICE, "price_as_of": PRICE_DATE, "scenarios": scenarios, "boundary": "Sensitivity cases, not forecasts or probabilities."},
        "intrinsic_value_scenarios": {"currency": "HKD", "scenarios": [{"scenario": name, "status": "unavailable", "intrinsic_value_per_share": None, "discount_rate_pct": None, "terminal_growth_pct": None, "reason": "Owner earnings and normalized cycle economics are unavailable."} for name in ("bear", "base", "upside")], "boundary": "No DCF is manufactured from a preliminary profit alert."},
        "moat_evidence": {"positive_evidence": ["Preform-to-cable integration and global production footprint.", "Hollow-core product and pilot progress.", "Q1/H1 mix and margin step-up."], "counter_evidence": ["Ordinary fibre remains cyclical.", "New capacity can compress ASP.", "AI revenue purity and cross-cycle ROIC are not disclosed."], "missing_tests": ["Effective capacity and yield.", "Order/ASP bridge.", "Cross-cycle incremental ROIC."], "source_refs": ["S1", "S5", "S14", "S15"]},
        "red_team": [
            {"claim": "H1 earnings may be a peak-spread event rather than durable owner economics.", "test": "Formal segment gross margin, H2 ASP and cash conversion.", "status": "pending", "source_refs": ["S5", "S14"]},
            {"claim": "AI data-centre exposure may be smaller than the share-price narrative implies.", "test": "Revenue, customer and product mix disclosed for computing/data-centre business.", "status": "unresolved", "source_refs": ["S1", "S5"]},
            {"claim": "Announced industry expansion can restore oversupply.", "test": "Effective capacity, commissioning, utilisation and price response over 12—24 months.", "status": "pending", "source_refs": ["S13", "S14"]},
            {"claim": "The rebound may be positioning and event anticipation rather than new evidence.", "test": "Formal H1 adds cash, segment and order facts beyond the July alert.", "status": "pending", "source_refs": ["S5", "S10", "S19", "S20"]},
        ],
        "gates": gates,
        "valuation_evidence": {"status": "partial", "subgates": [
            {"gate": "denominator_recency_and_pe_matrix", "result": "pass_with_scope", "reason": "FY and Q1 TTM are dated; forward cases are sensitivities."},
            {"gate": "demand_orders_guidance_and_capacity", "result": "pass_with_scope", "reason": "Issuer and global demand signals exist; YOFC orders and ASP are not quantified."},
            {"gate": "segment_forecast_reconciliation", "result": "blocked", "reason": "Formal H1 segment data is unavailable."},
            {"gate": "substitution_and_capacity_cycle", "result": "pass_with_scope", "reason": "Technology and expansion are mapped qualitatively."},
            {"gate": "peer_and_point_in_time_history", "result": "blocked", "reason": "No three-peer same-scope median or no-look-ahead PE history."},
            {"gate": "owner_earnings_and_investment_double_count", "result": "blocked", "reason": "Maintenance capex is unresolved."},
            {"gate": "valuation_conclusion_separation", "result": "pass", "reason": "Facts, sensitivities and judgment are kept separate."},
        ], **valuation_blocks},
        "historical_valuation": {"status": "insufficient_point_in_time_history", "current_h_fy2025_pe": H_PRICE / hkd_eps(fy_profit), "current_h_q1_ttm_pe": H_PRICE / hkd_eps(ttm_profit), "reason": "Distance from the price high is not a historical valuation percentile.", "source_refs": ["S10", "S12"]},
        "price_move_attribution": {"status": "multi_factor_not_single_cause", "window": "2026-06-22 to 2026-08-10", "high_to_trough_pct": -67.83, "trough_to_price_date_pct": 35.43, "five_session_rebound_pct": 30.20, "interpretation": "Fundamental confirmation, capacity-cycle fear, crowded AI rerating and technical supply zones all matter.", "source_refs": ["S5", "S10", "S14", "S19", "S20"]},
        "risk_reward_assessment": {"status": "verification_watchlist", "long_term": "The H price is not cheap on reported FY/TTM earnings; it becomes mid-teens only if the H1 run rate persists.", "near_term": "Rebound reward to the first supply zone is smaller than downside back to the recent base, so short-window asymmetry is not clearly favorable.", "risk_zones_hkd": [92, 96], "first_supply_zone_hkd": [140, 154], "boundary": "Technical reference zones are not intrinsic values or action instructions."},
        "source_gaps": ["Formal 2026H1 statements and segments.", "Order, volume, ASP and effective-capacity bridge.", "Maintenance capex and required working capital.", "Three same-scope peers and no-look-ahead valuation history.", "Named human review."],
        "invalidation_tests": [
            {"test": "Profit-duration", "invalidated_if": "Formal H1 or H2 shows gross-margin normalization without volume/cash offset.", "next_evidence": "2026 interim results", "review_date": "2026-08-31"},
            {"test": "Capacity-cycle", "invalidated_if": "Announced capacity becomes effective faster than demand and ASP weakens.", "next_evidence": "competitor commissioning and procurement prices", "review_date": "2027-03-31"},
            {"test": "AI purity", "invalidated_if": "Computing/data-centre exposure remains qualitative while ordinary fibre drives most earnings.", "next_evidence": "segment and customer disclosure", "review_date": "2026-08-31"},
            {"test": "Cash conversion", "invalidated_if": "Inventory, receivables and capex absorb the profit step-up.", "next_evidence": "H1 cash flow and working capital", "review_date": "2026-08-31"},
        ],
        "review": {"human_review_required": True, "human_review_status": "pending", "production_reviewed": False, "machine_validation": "pending_rebuild", "publication_boundary_reviewed": True, "unresolved_critical_gaps": ["formal H1", "owner earnings", "effective capacity", "named human review"]},
        "disclaimer": "Independent public-source research support, not investment advice. It is not affiliated with Berkshire Hathaway, Warren Buffett or Charlie Munger. No buy/sell instruction, target price or return guarantee is provided.",
    }


EVIDENCE_SPECS = [
    ("E1", "five_year_financials", "S1", 8, "2025 revenue, parent profit and operating cash flow are reproduced from the audited annual report.", "FY2023-FY2025", "CNY", "CNY", "consolidated group", "audited", None),
    ("E2", "fy2021_fy2022_history", "S3", 130, "FY2021 and FY2022 revenue and parent profit are reproduced from the consolidated income statement.", "FY2021-FY2022", "CNY", "CNY", "consolidated group", "audited", None),
    ("E3", "cash_capex_bridge", "S1", 86, "FY2025 operating cash flow and long-term asset purchases support the cash proxy.", "FY2025", "CNY", "CNY", "consolidated group", "audited", "CFO - cash paid for long-term assets"),
    ("E4", "q1_financial_inflection", "S4", 2, "Q1 revenue, parent profit, adjusted profit and operating cash flow are unaudited reported figures.", "2026Q1", "CNY", "CNY", "consolidated group", "unaudited", None),
    ("E5", "q1_gross_margin", "S4", 10, "Q1 gross margin is calculated from reported revenue and operating costs.", "2026Q1", "%", "CNY", "consolidated group", "unaudited", "(revenue - operating costs) / revenue"),
    ("E6", "h1_profit_alert", "S5", 1, "H1 parent profit is preliminarily estimated at CNY2.4-3.0bn and adjusted profit at CNY2.0-2.6bn.", "2026H1", "CNY", "CNY", "consolidated group", "unaudited", None),
    ("E7", "h_share_placing", "S6", 2, "70m H shares were placed at HKD32.26 with approximately HKD2.229bn net proceeds.", "2025-12", "shares/HKD", "HKD", "H-share capital", "not_applicable", None),
    ("E8", "current_share_count", "S7", 1, "July monthly return reports 421.567m H shares and 406.338m A shares, including 6m treasury A shares.", "2026-07", "shares", "CNY", "A/H share capital", "not_applicable", None),
    ("E9", "h_price_path", "S10", None, "The H-share close fell from 286.0 to 92.0 and rebounded to 124.6 by the frozen price date.", "2026-06-22 to 2026-08-10", "HKD/share", "HKD", "06869.HK", "not_applicable", "close-to-close percentage change"),
    ("E10", "fx_bridge", "S12", None, "Official central parity for 2026-08-10 is 100 HKD to CNY86.536.", PRICE_DATE, "CNY per 100 HKD", "CNY", "official FX query", "not_applicable", "86.536 / 100"),
    ("E11", "industry_capacity", "S14", 1, "Competitor filing announces phased optical-fibre and preform capacity with explicit execution uncertainty.", "2026 plan", "capacity/project", "CNY", "competitor project", "not_applicable", None),
    ("E12", "hollow_core_optionality", "S15", None, "Issuer reports integrated hollow-core manufacturing and commercial/pilot projects; revenue contribution is not disclosed.", "2026", "technology/project", "N/A", "issuer product release", "not_applicable", None),
    ("E13", "yofc_shanghai_acquisition", "S16", 1, "YOFC agreed to acquire the remaining 25% of YOFC Shanghai for EUR12m.", "2026-07", "EUR", "EUR", "acquisition", "not_applicable", None),
    ("E14", "global_demand_signal", "S13", None, "Corning reports strong optical-communications growth and enterprise-network demand alongside future capacity expansion.", "2026Q2", "USD/percent", "USD", "adjacent global peer", "unaudited", None),
]


def write_csv(name: str, fields: list[str], rows: list[dict]) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    with (DATA / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def fmt_status(value: str) -> str:
    css = "good" if value in {"applicable", "observed", "pass", "pass_with_scope", "mixed_positive"} else "risk" if value in {"fail", "blocked"} else "warn"
    return f'<span class="tag {css}">{escape(value)}</span>'


def render_report(artifact: dict, evidence_index: dict) -> str:
    dimension_rows = []
    for row in artifact["research_dimensions"]:
        ids = "<br>".join(f"<code>{escape(item['id'])}</code> · {fmt_status(item['status'])}" for item in row["indicators"])
        dimension_rows.append(f"<tr><td><b>{escape(row['dimension'])}</b></td><td>{fmt_status(row['status'])}</td><td>{escape(row['summary'])}</td><td>{ids}</td></tr>")
    gate_rows = "".join(f"<tr><td><code>{escape(g['gate'])}</code></td><td>{fmt_status(g['result'])}</td><td>{escape(g['reason'])}</td></tr>" for g in artifact["gates"])
    source_details = []
    for source in SOURCE_ROWS:
        source_details.append(f'<details><summary>{escape(source["id"])} · {escape(source["title"])}</summary><p>{escape(source["scope"])}；期间：{escape(source["period"])}。</p><p><a href="{escape(source["url"])}">打开主源</a> · SHA-256 <code>{source["content_sha256"]}</code></p></details>')
    evidence_details = []
    for anchor in evidence_index["anchors"]:
        evidence_details.append(f'<details data-evidence-id="{anchor["id"]}"><summary>{anchor["id"]} · {escape(anchor["claim_id"])}</summary><p>{escape(anchor["source_text"])}</p><p>来源 {anchor["source_id"]} · 页 {anchor["page"] or "网页/API"} · {escape(anchor["audit_status"])}</p></details>')
    pe_fy = artifact["pe_matrix"][0]["pe"]
    pe_ttm = artifact["pe_matrix"][1]["pe"]
    return REPORT_TEMPLATE.replace("__DIMENSION_ROWS__", "".join(dimension_rows)).replace("__GATE_ROWS__", gate_rows).replace("__SOURCE_DETAILS__", "".join(source_details)).replace("__EVIDENCE_DETAILS__", "".join(evidence_details)).replace("__PE_FY__", f"{pe_fy:.1f}").replace("__PE_TTM__", f"{pe_ttm:.1f}")


REPORT_TEMPLATE = r'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light dark"><meta name="description" content="长飞光纤 06869.HK：行业、供需、五年财务、A/H 估值、事件链、25×50×9 研究审计与当前风险收益。"><title>长飞光纤：利润跃迁之后，市场在押持续时间｜2026-08-11</title><link rel="stylesheet" href="../company-report-theme.css"><style>
:root{--blue:#155b72;--cyan:#2d9bb4;--purple:#67549a;--green:#18734d;--amber:#a56308;--red:#a33d38;--paper:#fff;--line:#d7e1e5;--shadow:0 16px 40px rgba(20,48,60,.08)}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:radial-gradient(circle at 5% 0,#dff2f5,transparent 28rem),#edf3f5;color:#15252d;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;line-height:1.65}.wrap{width:min(1180px,calc(100% - 32px));margin:auto}.hero{padding:62px 0 28px}.eyebrow{font-size:12px;font-weight:900;letter-spacing:.14em;color:var(--blue)}h1{max-width:980px;margin:8px 0 14px;font-size:clamp(38px,6vw,70px);line-height:1.04;letter-spacing:-.045em}.dek{max-width:900px;font-size:clamp(18px,2vw,24px);color:#42545d}.meta{display:flex;flex-wrap:wrap;gap:8px}.pill,.tag{display:inline-block;padding:4px 8px;border-radius:999px;font-size:11px;font-weight:850}.pill{border:1px solid var(--line);background:#fff}.tag.good{color:var(--green);background:#e2f3ea}.tag.warn{color:var(--amber);background:#fff0cf}.tag.risk{color:var(--red);background:#fde8e5}.verdict{display:grid;grid-template-columns:1.5fr .7fr;margin-top:28px;border:1px solid #afd0da;border-radius:20px;overflow:hidden;background:linear-gradient(135deg,#f9feff,#e3f3f7);box-shadow:var(--shadow)}.verdict>div{padding:27px}.verdict .side{border-left:1px solid #c8dfe6}.label{font-size:11px;font-weight:900;color:var(--blue);letter-spacing:.12em}.big{font-size:36px;font-weight:900;color:var(--blue)}nav{position:sticky;top:0;z-index:5;overflow:auto;border-block:1px solid var(--line);background:rgba(237,243,245,.94);backdrop-filter:blur(12px)}nav .wrap{display:flex;gap:4px;padding:7px 0}nav a{flex:none;padding:7px 9px;color:#4b5e67;text-decoration:none;font-size:12px;font-weight:800}main{padding:12px 0 70px}section{scroll-margin-top:64px;margin-top:20px;padding:30px;border:1px solid var(--line);border-radius:20px;background:var(--paper);box-shadow:var(--shadow)}section h2{margin:0 0 7px;font-size:clamp(25px,3vw,37px);line-height:1.2}.section-dek{max-width:940px;margin:0 0 20px;color:#63747c}.grid{display:grid;grid-template-columns:repeat(12,1fr);gap:12px}.card{grid-column:span 3;padding:16px;border:1px solid var(--line);border-radius:14px}.card.wide{grid-column:span 6}.k{font-size:11px;color:#64757e;font-weight:850}.v{font-size:27px;font-weight:900;line-height:1.15}.s{font-size:12px;color:#65767e}.callout{margin:16px 0;padding:16px 18px;border-left:4px solid var(--blue);border-radius:6px 12px 12px 6px;background:#dfeff4}.callout.amber{border-color:var(--amber);background:#fff0cf}.callout.red{border-color:var(--red);background:#fde8e5}.callout.green{border-color:var(--green);background:#e2f3ea}.table-wrap{overflow:auto;border:1px solid var(--line);border-radius:13px}table{width:100%;min-width:760px;border-collapse:collapse;font-size:13px}th,td{padding:10px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}th{background:#f1f5f6;color:#4c5e67;font-size:11px}tr:last-child td{border-bottom:0}.chart{padding:16px;border:1px solid var(--line);border-radius:14px}.chart svg{display:block;width:100%;height:auto}.chart text{font:11px -apple-system,BlinkMacSystemFont,"PingFang SC",sans-serif;fill:#60727b}.axis{stroke:#d7e1e5}.line{fill:none;stroke:var(--blue);stroke-width:4}.line2{fill:none;stroke:var(--purple);stroke-width:4}.timeline{display:grid;grid-template-columns:130px 1fr;gap:8px 16px}.timeline dt{font-weight:900;color:var(--blue)}.timeline dd{margin:0 0 8px}.two{display:grid;grid-template-columns:1fr 1fr;gap:14px}details{margin:8px 0;padding:10px 12px;border:1px solid var(--line);border-radius:10px;background:#fafcfc}summary{cursor:pointer;font-weight:850}code{font-size:11px;overflow-wrap:anywhere}.foot{font-size:12px;color:#66777f}@media(max-width:760px){.verdict,.two{grid-template-columns:1fr}.verdict .side{border-left:0;border-top:1px solid #c8dfe6}.card,.card.wide{grid-column:span 12}section{padding:21px}.timeline{grid-template-columns:1fr}.hero{padding-top:42px}}
</style></head><body data-template="company-research-publication-v1"><!-- template-parity: viewport-qa-required -->
<header class="hero"><div class="wrap"><div class="eyebrow">PUBLIC RESEARCH PACK · 06869.HK / 601869.SH</div><h1>长飞光纤：利润跃迁是真的，难题是它能持续多久</h1><p class="dek">它不是“纯 CPO 股”，而是预制棒—光纤—光缆—光互联的一体化制造商。当前价格同时交易 AI 数据中心需求、光纤周期反转、空芯光纤期权与供给扩张风险。</p><div class="meta"><span class="pill">港股通：沪/深南向均核验命中</span><span class="pill">估值锚：2026-08-10 收盘 HK$124.60</span><span class="pill">状态：needs_human_review</span><span class="pill">证据截至 2026-08-11</span></div><div class="verdict"><div><div class="label">当前风险收益</div><h2>黄色验证区：基本面转强，但反弹后的短窗口赔率并不宽</h2><p>从 HK$286 跌至 HK$92 后反弹到 HK$124.60。到第一供给区 HK$140—154 的空间约 +12%—24%，回到近期基底 HK$92—96 的距离约 -23%—26%。这不是内在价值测算，只说明短线“跌得多”尚未自动形成好赔率。</p></div><div class="side"><div class="label">核心状态</div><div class="big">验证观察</div><p>长期看利润持续性；近期看中报、海外光通信财报与供给扩产。</p></div></div></div></header>
<nav><div class="wrap"><a href="#long-term">长期</a><a href="#event-monitor">近期</a><a href="#industry">行业</a><a href="#financials">财务</a><a href="#market-pricing">估值</a><a href="#research-contract">25×50×9</a><a href="#timeline">事件</a><a href="#sources">证据</a></div></nav>
<main class="wrap">
<section id="status-legend"><h2>0. 状态图例：先分清“有答案”与“没有证据”</h2><p class="section-dek">applicable / unknown 是维度结论；observed / not_disclosed 是指标证据；provisional 是闸门仍需补强；needs_human_review 表示机器校验不等于人工批准。</p><div class="grid"><div class="card"><div class="v">applicable</div><div class="s">证据足以讨论</div></div><div class="card"><div class="v">unknown</div><div class="s">关键事实不足</div></div><div class="card"><div class="v">observed</div><div class="s">主源或可复算事实</div></div><div class="card"><div class="v">not_disclosed</div><div class="s">不能猜测补齐</div></div><div class="card"><div class="v">provisional</div><div class="s">可研究，未决策级</div></div><div class="card"><div class="v">needs_human_review</div><div class="s">待具名复核</div></div></div></section>
<section id="long-term"><h2>1. 长期档案：十年所有者问题</h2><p class="section-dek">第一问不是 AI 热不热，而是完全摊薄后的每股所有者收益能否跨光纤周期增长；第二问才是当前价格有没有安全边际。</p><div class="two"><div class="callout green"><strong>支持：</strong>一体化制造、全球产能、海外收入、光互联组件与空芯光纤，使公司不再只是普通单模光纤价格接受者。</div><div class="callout red"><strong>反证：</strong>历史利润随 ASP 和运营商资本开支波动；AI 收入纯度、有效产能、维护性投入和增量 ROIC 尚未披露。</div></div><p><b>长期结论：</b>经营拐点已进入数据，但“耐久护城河 + 每股 owner earnings + 安全边际”三项还不能同时通过。</p></section>
<section id="summary"><h2>2. 一页结论：风险收益为什么是黄色</h2><div class="grid"><div class="card"><div class="k">行业</div><div class="v">光通信制造</div><div class="s">AI 数据中心是增量主题，不是全部收入</div></div><div class="card"><div class="k">2026Q1 毛利率</div><div class="v">41.5%</div><div class="s">上年同期 27.8%</div></div><div class="card"><div class="k">2026H1 归母预告</div><div class="v">24—30亿</div><div class="s">未审计，正式中报待定</div></div><div class="card"><div class="k">高位回撤 / 低位反弹</div><div class="v">-67.8% / +35.4%</div><div class="s">均为收盘价路径</div></div></div><div class="callout amber"><strong>关键判断：</strong>静态 FY2025 与 Q1 TTM P/E 仍约 __PE_FY__× / __PE_TTM__×；只有把 H1 利润简单年化，才会出现约 14.9—18.6×。因此当前不是“低 PE 已确认”，而是“盈利峰值持续时间”的押注。</div></section>
<section id="event-monitor"><h2>3. 近期事件终端：反弹在交易什么</h2><p class="section-dek">把核心叙事、短线新闻、板块 lead-lag、公司基本面和价格结构分开。</p><div class="table-wrap"><table><thead><tr><th>层</th><th>已观察事实</th><th>当前读法</th><th>下一证据</th></tr></thead><tbody><tr><td>核心叙事</td><td>AI/算力数据中心拉动新型光纤光缆与光互联</td><td>Q1/H1 已出现利润支持</td><td>正式分部收入、订单与 ASP</td></tr><tr><td>供给反方</td><td>国内同行与 Corning 均有扩产安排</td><td>短期供给滞后，长期压缩利润持续性</td><td>投产、良率、利用率</td></tr><tr><td>板块传导</td><td>长飞反弹强于恒生国企指数，也强于部分光模块主题股</td><td>公司/光纤周期因素较多</td><td>海外光通信财报</td></tr><tr><td>价格结构</td><td>高位 HK$286 → 低位 HK$92 → HK$124.60</td><td>强反弹，尚未回到上方密集成交区</td><td>HK$140—154 附近供给反应</td></tr></tbody></table></div></section>
<section id="industry"><h2>4. 属于什么行业：三层标签不能混</h2><div class="table-wrap"><table><thead><tr><th>层级</th><th>正确标签</th><th>错误简化</th><th>影响变量</th></tr></thead><tbody><tr><td>正式行业</td><td>通信设备 / 光纤光缆制造</td><td>纯软件、纯平台</td><td>运营商资本开支、集采、海外基建</td></tr><tr><td>经营行业</td><td>预制棒→光纤→光缆；光互联组件；海外工程与其他</td><td>只看光模块</td><td>ASP、销量、产品组合、良率、回款</td></tr><tr><td>市场主题</td><td>AI 数据中心光连接、光纤紧缺、空芯光纤</td><td>纯 CPO / 与胜宏完全同构</td><td>超大规模客户需求、技术路线、供给扩张</td></tr></tbody></table></div><div class="callout"><strong>与美图、建滔、胜宏的相似处：</strong>都是成熟业务被新叙事重新定价后发生拥挤与估值压缩。<strong>差异：</strong>长飞不是平台资产，也不是母子公司 SOTP；它最核心的是光纤 ASP、有效产能和利润峰值持续时间。</div></section>
<section id="business"><h2>5. 利润传导链：需求不等于利润</h2><div class="chart"><svg viewBox="0 0 980 220" role="img" aria-label="长飞利润传导链"><defs><marker id="a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8z" fill="#60727b"/></marker></defs><g fill="#e3f3f7" stroke="#7db9c8"><rect x="15" y="70" width="135" height="70" rx="12"/><rect x="180" y="70" width="135" height="70" rx="12"/><rect x="345" y="70" width="135" height="70" rx="12"/><rect x="510" y="70" width="135" height="70" rx="12"/><rect x="675" y="70" width="135" height="70" rx="12"/><rect x="840" y="70" width="125" height="70" rx="12"/></g><g stroke="#60727b" marker-end="url(#a)"><line x1="150" y1="105" x2="174" y2="105"/><line x1="315" y1="105" x2="339" y2="105"/><line x1="480" y1="105" x2="504" y2="105"/><line x1="645" y1="105" x2="669" y2="105"/><line x1="810" y1="105" x2="834" y2="105"/></g><g text-anchor="middle"><text x="82" y="100">AI/运营商需求</text><text x="247" y="100">订单与集采</text><text x="412" y="100">有效产能/良率</text><text x="577" y="100">销量 × ASP</text><text x="742" y="100">毛利 - 费用</text><text x="902" y="100">现金与 ROIC</text><text x="82" y="120">外部确认</text><text x="247" y="120">未量化</text><text x="412" y="120">未披露</text><text x="577" y="120">部分可见</text><text x="742" y="120">Q1跃迁</text><text x="902" y="120">待H1验证</text></g></svg></div><p>任何一环缺失，都不能把“行业需求强”直接写成“长飞长期利润确定”。</p></section>
<section id="cycle"><h2>6. 供需周期：短缺与扩产必须同时看</h2><div class="table-wrap"><table><thead><tr><th>证据</th><th>需求侧</th><th>供给侧</th><th>结论边界</th></tr></thead><tbody><tr><td>长飞 H1 预告</td><td>新型光纤光缆需求上升、客户与产品结构优化</td><td>公司未给出有效产能与 ASP</td><td>公司级利润确认，非行业永续证明</td></tr><tr><td>Corning Q2</td><td>光通信与企业网络增长</td><td>同时推进制造扩张</td><td>全球需求确认，也提醒未来供给</td></tr><tr><td>大韩扩产公告</td><td>项目基于市场前景</td><td>60m 芯公里计划、分期实施</td><td>公告产能不等于即时有效产能</td></tr><tr><td>空芯光纤</td><td>低时延/低非线性适配未来连接</td><td>商业规模和利润未披露</td><td>技术期权，不直接计入基准利润</td></tr></tbody></table></div></section>
<section id="financials"><h2>7. 五年财务：收入周期不强，利润率拐点很强</h2><p class="section-dek">单位人民币十亿元；资本开支为购建固定资产、无形资产和其他长期资产支付的现金。</p><div class="table-wrap"><table><thead><tr><th>期间</th><th>收入</th><th>毛利率</th><th>归母利润</th><th>经营现金流</th><th>全部长期资产购置</th><th>CFO-全部投入</th></tr></thead><tbody><tr><td>2021</td><td>9.536</td><td>19.6%</td><td>0.709</td><td>0.527</td><td>1.074</td><td>-0.547</td></tr><tr><td>2022</td><td>13.830</td><td>23.5%</td><td>1.167</td><td>1.595</td><td>2.228</td><td>-0.634</td></tr><tr><td>2023</td><td>13.353</td><td>24.5%</td><td>1.297</td><td>1.514</td><td>2.263</td><td>-0.748</td></tr><tr><td>2024</td><td>12.197</td><td>27.3%</td><td>0.676</td><td>1.783</td><td>1.386</td><td>0.398</td></tr><tr><td>2025</td><td>14.252</td><td>30.7%</td><td>0.814</td><td>3.653</td><td>1.422</td><td>2.231</td></tr><tr><td>2026Q1</td><td>3.695</td><td>41.5%</td><td>0.495</td><td>0.618</td><td>0.336</td><td>0.282</td></tr></tbody></table></div><div class="chart" style="margin-top:16px"><svg viewBox="0 0 900 280" role="img" aria-label="收入和毛利率趋势"><line class="axis" x1="60" y1="225" x2="860" y2="225"/><polyline class="line" points="80,120 230,62 380,70 530,88 680,54 830,36"/><polyline class="line2" points="80,182 230,155 380,145 530,126 680,101 830,44"/><g text-anchor="middle"><text x="80" y="245">2021</text><text x="230" y="245">2022</text><text x="380" y="245">2023</text><text x="530" y="245">2024</text><text x="680" y="245">2025</text><text x="830" y="245">26Q1</text></g><text x="70" y="25">蓝：收入相对规模　紫：毛利率</text></svg></div></section>
<section id="quarter"><h2>8. 最新季度与 H1：利润跃迁来自毛利，而非收入暴增</h2><div class="table-wrap"><table><thead><tr><th>指标</th><th>2025Q1</th><th>2026Q1</th><th>变化</th><th>研究意义</th></tr></thead><tbody><tr><td>收入</td><td>28.94亿</td><td>36.95亿</td><td>+27.7%</td><td>需求改善</td></tr><tr><td>毛利率</td><td>27.8%</td><td>41.5%</td><td>+13.7pct</td><td>产品/供需组合是利润杠杆</td></tr><tr><td>归母利润</td><td>1.52亿</td><td>4.95亿</td><td>+226%</td><td>利润弹性远高于收入</td></tr><tr><td>扣非归母</td><td>0.43亿</td><td>4.61亿</td><td>+966%</td><td>质量比 2025 全年明显改善</td></tr><tr><td>经营现金流</td><td>4.36亿</td><td>6.18亿</td><td>+41.9%</td><td>目前没有明显背离</td></tr><tr><td>存货</td><td>—</td><td>35.04亿</td><td>较年末 +11.1%</td><td>可能是备货，也可能是风险</td></tr></tbody></table></div><div class="callout amber"><strong>H1 预告不能替代中报：</strong>预告只有利润区间和原因，没有分部、现金流、应收、存货、订单、ASP 与有效产能。Q2 推导利润可算，但仍是派生值。</div></section>
<section id="capital"><h2>9. 三座桥：利润、现金、股本分别算</h2><div class="table-wrap"><table><thead><tr><th>桥</th><th>已观察</th><th>不能越界</th><th>状态</th></tr></thead><tbody><tr><td>归母→扣非</td><td>2025 8.14亿→5.16亿；26Q1 4.95亿→4.61亿</td><td>H1 仍为未审计区间</td><td><span class="tag good">改善</span></td></tr><tr><td>利润→CFO→现金代理</td><td>2025 CFO 36.53亿，减全部长期资产购置后 22.31亿</td><td>不能把全部 capex 当维护投入</td><td><span class="tag warn">partial</span></td></tr><tr><td>总股本→每股</td><td>总 827.905m；H 421.567m；A 406.338m；库存 A 6m</td><td>A/H 价格不能互换；配股需摊薄</td><td><span class="tag good">observed</span></td></tr></tbody></table></div><div class="callout red"><strong>Owner earnings 仍是 unavailable。</strong>这不是说现金差，而是维护性 capex、必要营运资本和可分配现金尚不能可靠分拆。</div></section>
<section id="market-pricing"><h2>10. 估值：五个分母给出五个答案</h2><div class="table-wrap"><table><thead><tr><th>盈利分母</th><th>归母利润</th><th>机械 H 股 P/E</th><th>性质</th></tr></thead><tbody><tr><td>FY2025 reported</td><td>8.14亿</td><td>__PE_FY__×</td><td>审计但过时</td></tr><tr><td>Q1 TTM</td><td>11.57亿</td><td>__PE_TTM__×</td><td>不含 Q2 跃迁</td></tr><tr><td>压力敏感性</td><td>34亿</td><td>26.3×</td><td>H1低端 + H2仅10亿</td></tr><tr><td>H1低端年化</td><td>48亿</td><td>18.6×</td><td>敏感性，不是预测</td></tr><tr><td>H1高端年化</td><td>60亿</td><td>14.9×</td><td>把峰值外推风险最高</td></tr><tr><td>正常化 owner earnings</td><td>不可得</td><td>不可得</td><td>缺维护投入和周期利润</td></tr></tbody></table></div><div class="callout amber"><strong>A/H 额外风险：</strong>A 股 CNY343.09；H 股按官方汇率折合约 CNY107.82，A 股溢价约 218%。这不是无风险套利，因为两类股份不可自由互换；但它显示同一发行人的拥挤度和流动性分层极强。</div></section>
<section id="price-action"><h2>11. 从高位暴跌再反弹：到底发生了什么</h2><div class="table-wrap"><table><thead><tr><th>窗口</th><th>价格变化</th><th>事件/解释</th><th>不可写成</th></tr></thead><tbody><tr><td>6/22—6/23</td><td>收盘高 286；盘中 305</td><td>AI 光通信与空芯光纤叙事拥挤</td><td>基本面内在价值</td></tr><tr><td>6/26—7/13</td><td>250.6 → 139.7</td><td>供给扩张、拥挤松动、估值压缩</td><td>单一新闻因果</td></tr><tr><td>7/14—7/15</td><td>利润预告后高开低走</td><td>利好兑现与分歧加大</td><td>业绩不真实</td></tr><tr><td>7/30</td><td>收盘 92</td><td>价格低点；同日披露收购事项</td><td>估值底</td></tr><tr><td>8/3—8/10</td><td>95.7 → 124.6，+30.2%</td><td>超跌、行业催化、事件前再定价</td><td>长期反转已证明</td></tr></tbody></table></div></section>
<section id="scenarios"><h2>12. 当前风险收益：三种可证伪情景</h2><div class="grid"><div class="card wide"><div class="k">压力情景</div><div class="v">H2 利润显著回落</div><div class="s">FY 归母约 34亿，机械 P/E 26.3×；若 ASP 和毛利同步走弱，前高回撤不是安全垫。</div></div><div class="card wide"><div class="k">中性情景</div><div class="v">H1低端大体维持</div><div class="s">FY 归母约 48亿，机械 P/E 18.6×；需要正式现金流与细分支持。</div></div><div class="card wide"><div class="k">上行情景</div><div class="v">高端利润与订单延续</div><div class="s">FY 归母约 60亿，机械 P/E 14.9×；仍要扣除周期峰值和扩产回落风险。</div></div><div class="card wide"><div class="k">近期价格结构</div><div class="v">收益 12%—24% / 风险 23%—26%</div><div class="s">仅以第一供给区和近期基底测量，不代表概率或目标价。</div></div></div><div class="chart" style="margin-top:16px"><svg viewBox="0 0 900 190" role="img" aria-label="风险收益参考区间"><line x1="80" y1="90" x2="820" y2="90" stroke="#d7e1e5" stroke-width="12" stroke-linecap="round"/><line x1="80" y1="90" x2="320" y2="90" stroke="#a33d38" stroke-width="12" stroke-linecap="round"/><line x1="320" y1="90" x2="565" y2="90" stroke="#a56308" stroke-width="12"/><line x1="565" y1="90" x2="820" y2="90" stroke="#18734d" stroke-width="12" stroke-linecap="round"/><g text-anchor="middle"><text x="80" y="65">92</text><text x="320" y="65">124.6</text><text x="565" y="65">140</text><text x="820" y="65">154</text><text x="200" y="125">近期基底风险区</text><text x="442" y="125">当前至第一供给</text><text x="690" y="125">更高供给区</text></g></svg></div></section>
<section id="buffett"><h2>13. 巴菲特—芒格解释：好转的生意，不等于已证明的好价格</h2><div class="table-wrap"><table><thead><tr><th>原则</th><th>支持证据</th><th>反证</th><th>结论</th></tr></thead><tbody><tr><td>企业所有权</td><td>A/H 股本和稀释已桥接</td><td>两条线流动性与价格差异极大</td><td>可理解</td></tr><tr><td>能力圈</td><td>需求—产能—ASP—利润—现金链可描述</td><td>订单、良率、有效产能未量化</td><td>provisional</td></tr><tr><td>护城河</td><td>一体化、工艺、全球基地、空芯技术</td><td>普通光纤价格周期与同行扩产</td><td>候选</td></tr><tr><td>Owner earnings</td><td>2025/26Q1 现金代理改善</td><td>维护投入和必要营运资本不可分</td><td>unavailable</td></tr><tr><td>安全边际</td><td>若 H1 年化维持，H 股倍数下降</td><td>静态倍数很高，正常化利润未知</td><td>inconclusive</td></tr></tbody></table></div></section>
<section id="moat"><h2>14. 护城河与技术期权：空芯光纤不能提前资本化</h2><p>0.04 dB/km、长距离拉制、试点和产业链一体化是技术进展；但没有商业规模、ASP、毛利和客户复购，就不能把它直接加入基准盈利。最可靠的跟踪顺序是：试验 → 商用链路 → 重复订单 → 收入占比 → 毛利 → 资本回报。</p></section>
<section id="red-team"><h2>15. 红队：四条最可能让多头判断出错的路径</h2><div class="table-wrap"><table><thead><tr><th>反方</th><th>为什么危险</th><th>可证伪测试</th></tr></thead><tbody><tr><td>峰值利润外推</td><td>毛利率跃迁远大于收入增速</td><td>H2 ASP、毛利与现金</td></tr><tr><td>AI 纯度高估</td><td>公司仍有大量运营商与传统光传输业务</td><td>算力数据中心分部收入与客户</td></tr><tr><td>扩产恢复过剩</td><td>高毛利会吸引国内外资本开支</td><td>有效产能、利用率和集采价格</td></tr><tr><td>反弹等同反转</td><td>超跌与事件前交易可先于证据</td><td>正式中报是否新增订单与现金事实</td></tr></tbody></table></div></section>
<section id="methodology"><h2>16. 方法论：美图母版在长飞上如何落地</h2><p class="section-dek">同一母版，不同公司换关键经济变量。美图侧重用户、订阅、AI 产品与净现金；长飞侧重需求、集采、有效产能、ASP、毛利、现金和 ROIC。</p><div class="table-wrap"><table><thead><tr><th>层</th><th>本报告做法</th><th>为什么</th></tr></thead><tbody><tr><td>事实层</td><td>年报/Q1/H1预告/股本/价格/汇率逐项冻结</td><td>防止日期与分母错配</td></tr><tr><td>经营层</td><td>行业链、分部、供需、客户、供应商、技术替代</td><td>不把主题当公司利润</td></tr><tr><td>财务层</td><td>五年收入、毛利、归母、CFO、capex</td><td>看跨周期质量</td></tr><tr><td>估值层</td><td>FY、TTM、压力、H1低/高年化、owner earnings</td><td>暴露分母不确定性</td></tr><tr><td>事件层</td><td>高点、暴跌、业绩预告、扩产、同行财报、中报</td><td>分开长期价值与短期催化</td></tr><tr><td>审计层</td><td>25 维度 / 50 指标 / 9 闸门 / 红队 / 失效条件</td><td>保留未知与反证</td></tr></tbody></table></div></section>
<section id="research-contract"><h2>17. 研究契约：25 个维度 × 50 个指标 × 九道闸门</h2><p class="section-dek">每个维度恰有两个指标家族；标识符公开展示，便于机器与人工交叉核对。</p><div class="table-wrap"><table><thead><tr><th>维度</th><th>状态</th><th>结论</th><th>两个指标家族</th></tr></thead><tbody>__DIMENSION_ROWS__</tbody></table></div><h3>九道闸门</h3><div class="table-wrap"><table><thead><tr><th>闸门 ID</th><th>结果</th><th>理由</th></tr></thead><tbody>__GATE_ROWS__</tbody></table></div></section>
<section id="timeline"><h2>18. 事件日历：哪些会改变判断</h2><dl class="timeline"><dt>2025-12-17</dt><dd>70m H 股配售完成，净募资约 HK$2.229bn，主要投向海外业务与营运资金。</dd><dt>2026-03-06</dt><dd>HollowBand 空芯光纤平台发布；技术期权进入商业验证阶段。</dd><dt>2026-04-29</dt><dd>Q1 利润、毛利率与现金流跃迁。</dd><dt>2026-06-22/23</dt><dd>H 股收盘/盘中高点；拥挤度极高。</dd><dt>2026-06-26</dt><dd>同行公布预制棒/光纤扩产计划，供给担忧升温。</dd><dt>2026-07-14</dt><dd>H1 归母利润预告 24—30 亿元。</dd><dt>2026-07-30</dt><dd>H 股收盘低点 92；收购长飞上海余下 25% 权益。</dd><dt>2026-08-11 美股盘后</dt><dd>Lumentum FY2026 业绩，观察光通信需求、缺货、价格和指引。</dd><dt>2026-08-12 美股盘后</dt><dd>Coherent FY2026 业绩，作为相邻光器件链信号。</dd><dt>2026-08 下旬（日期待公告）</dt><dd>长飞正式中报；不要用第三方日历替代官方日期。</dd></dl></section>
<section id="monitor"><h2>19. 下一轮验证清单</h2><div class="table-wrap"><table><thead><tr><th>优先级</th><th>问题</th><th>通过条件</th><th>失效信号</th></tr></thead><tbody><tr><td>P0</td><td>H1 毛利是否可持续</td><td>分部毛利、扣非与现金同步</td><td>仅靠一次性/公允价值或 H2 快速回落</td></tr><tr><td>P0</td><td>利润是否变成现金</td><td>CFO/利润稳定，存货应收可控</td><td>库存、应收和 capex 吞噬利润</td></tr><tr><td>P0</td><td>AI 收入纯度</td><td>算力/数据中心收入、客户或订单量化</td><td>继续只有定性口径</td></tr><tr><td>P1</td><td>供给周期</td><td>需求增速快于有效产能</td><td>集采/现货 ASP 下行</td></tr><tr><td>P1</td><td>空芯商业化</td><td>重复商用订单与利润贡献</td><td>只有纪录与试点</td></tr></tbody></table></div></section>
<section id="sources"><h2>20. 证据与来源</h2><p class="section-dek">先看关键证据锚点，再下钻主源账本。网页和 API 的 checksum 是研究时快照；交易数据属定义明确的二级行情源。</p><div class="two"><div><h3>关键证据</h3>__EVIDENCE_DETAILS__</div><div><h3>来源账本</h3>__SOURCE_DETAILS__</div></div><p class="foot">独立公开来源研究支持，不构成投资建议、目标价或回报保证；与 Berkshire Hathaway、Warren Buffett、Charlie Munger 无关联。artifact_status = needs_human_review，production_reviewed = false。</p></section>
</main></body></html>'''


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    artifact = build_artifact()
    combined_path = ROOT / "combined-artifact.v2.json"
    combined_path.write_text(json.dumps(artifact, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    combined_sha = hashlib.sha256(combined_path.read_bytes()).hexdigest()
    anchors = []
    source_by_id = {row["id"]: row for row in SOURCE_ROWS}
    for evidence_id, claim_id, source_id, page, text, period, unit, currency, scope, audit_status, formula in EVIDENCE_SPECS:
        anchors.append({"id": evidence_id, "claim_id": claim_id, "source_id": source_id, "document_sha256": source_by_id[source_id]["content_sha256"], "page": page, "source_text": text, "period": period, "unit": unit, "currency": currency, "scope": scope, "audit_status": audit_status, "formula": formula, "critical": True})
    evidence_index = {"schema_version": "seed.company-research-evidence-index.v1", "generated_at": GENERATED_AT, "combined_artifact": {"path": "combined-artifact.v2.json", "sha256": combined_sha}, "anchors": anchors}
    (ROOT / "evidence-index.json").write_text(json.dumps(evidence_index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "source-ledger.json").write_text(json.dumps({"schema_version": "seed.public-company-source-ledger.v2", "as_of": RESEARCH_DATE, "publication_boundary": "No raw PDFs, private data, portfolio data or credentials are included.", "sources": SOURCE_ROWS}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "red-team.json").write_text(json.dumps({"schema_version": "1.0", "reviewer_or_agent": "independent-red-team-pass", "reviewed_at": GENERATED_AT, "counter_thesis": "YOFC may be experiencing a peak-margin fibre cycle amplified by AI narrative and scarcity pricing; announced capacity can normalize ASP before new technology becomes material.", "unresolved_issues": ["formal H1 cash and segment data", "effective capacity and ASP", "AI revenue purity", "maintenance capex", "named human review"], "tests": artifact["invalidation_tests"]}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "human-review.json").write_text(json.dumps({"schema_version": "1.0", "reviewer": "pending_assignment", "reviewed_at": "not_yet_reviewed", "decision": "pending", "critical_gaps": ["formal H1", "owner earnings", "effective capacity", "AI revenue purity"], "note": "Machine validation is not human approval."}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "report.html").write_text(render_report(artifact, evidence_index), encoding="utf-8")
    readme = """# 长飞光纤光缆 06869.HK / 601869.SH\n\n公开研究包，沿用美图母版的双入口、25 维度 / 50 指标 / 9 闸门契约，并为光通信制造补入需求—订单—有效产能—ASP—毛利—现金—ROIC 链。\n\n- `report.html`：读者版完整报告\n- `combined-artifact.v2.json`：机器可读研究结论\n- `source-ledger.json` / `evidence-index.json`：来源与证据锚点\n- `red-team.json` / `human-review.json`：反方与审查边界\n- `data/`：五年财务、估值、事件、供需、A/H 和风险收益 CSV\n\n状态：`needs_human_review`；不是投资建议。\n"""
    (ROOT / "README.md").write_text(readme, encoding="utf-8")
    write_csv("financial-history.csv", ["period", "revenue_bn", "gross_profit_bn", "gross_margin_pct", "parent_profit_bn", "cfo_bn", "capex_bn", "cash_after_all_capex_bn"], [{k: v for k, v in row.items() if k != "source_refs"} for row in FINANCIAL_HISTORY])
    write_csv("business-mix-2025.csv", ["segment", "revenue_bn", "yoy_pct", "revenue_share_pct", "gross_margin_pct"], [{"segment": "optical_transmission", "revenue_bn": 8.346, "yoy_pct": 6.09, "revenue_share_pct": 58.56, "gross_margin_pct": 35.90}, {"segment": "optical_interconnect", "revenue_bn": 3.144, "yoy_pct": 48.58, "revenue_share_pct": 22.06, "gross_margin_pct": 39.73}, {"segment": "other", "revenue_bn": 2.496, "yoy_pct": 29.11, "revenue_share_pct": 17.51, "gross_margin_pct": 4.05}])
    write_csv("quarterly-inflection.csv", ["metric", "2025Q1", "2026Q1", "change_pct_or_ppt"], [{"metric": "revenue_bn", "2025Q1": 2.8938, "2026Q1": 3.6954, "change_pct_or_ppt": 27.70}, {"metric": "gross_margin_pct", "2025Q1": 27.84, "2026Q1": 41.51, "change_pct_or_ppt": 13.67}, {"metric": "parent_profit_bn", "2025Q1": 0.1517, "2026Q1": 0.4951, "change_pct_or_ppt": 226.40}, {"metric": "adjusted_parent_profit_bn", "2025Q1": 0.0432, "2026Q1": 0.4612, "change_pct_or_ppt": 966.44}, {"metric": "cfo_bn", "2025Q1": 0.4355, "2026Q1": 0.6178, "change_pct_or_ppt": 41.85}])
    write_csv("owner-earnings-bridge.csv", ["period", "parent_profit_bn", "cfo_bn", "all_long_asset_cash_outflow_bn", "cash_proxy_bn", "owner_earnings_status"], [{"period": row["period"], "parent_profit_bn": row["parent_profit_bn"], "cfo_bn": row["cfo_bn"], "all_long_asset_cash_outflow_bn": row["capex_bn"], "cash_proxy_bn": row["cash_after_all_capex_bn"], "owner_earnings_status": "unavailable"} for row in FINANCIAL_HISTORY])
    write_csv("ah-valuation-bridge.csv", ["line", "price", "currency", "cny_equivalent", "shares", "fungibility", "note"], [{"line": "H", "price": H_PRICE, "currency": "HKD", "cny_equivalent": round(H_PRICE * FX_HKD_CNY, 4), "shares": H_SHARES, "fungibility": "not_freely_fungible", "note": "valuation anchor"}, {"line": "A", "price": A_PRICE, "currency": "CNY", "cny_equivalent": A_PRICE, "shares": A_SHARES, "fungibility": "not_freely_fungible", "note": "218.2% premium to H CNY-equivalent"}])
    write_csv("valuation-scenarios.csv", ["case", "parent_profit_cny_bn", "mechanical_h_pe", "status"], [{"case": "reported_FY2025", "parent_profit_cny_bn": 0.813737, "mechanical_h_pe": round(H_PRICE / hkd_eps(813_737_266), 2), "status": "reported"}, {"case": "Q1_TTM", "parent_profit_cny_bn": 1.157172, "mechanical_h_pe": round(H_PRICE / hkd_eps(1_157_172_411), 2), "status": "reported"}, {"case": "bear_sensitivity", "parent_profit_cny_bn": 3.4, "mechanical_h_pe": round(H_PRICE / hkd_eps(3.4e9), 2), "status": "sensitivity"}, {"case": "H1_low_annualized", "parent_profit_cny_bn": 4.8, "mechanical_h_pe": round(H_PRICE / hkd_eps(4.8e9), 2), "status": "sensitivity"}, {"case": "H1_high_annualized", "parent_profit_cny_bn": 6.0, "mechanical_h_pe": round(H_PRICE / hkd_eps(6.0e9), 2), "status": "sensitivity"}])
    write_csv("industry-capacity-cycle.csv", ["date", "actor", "signal", "demand_or_supply", "evidence_level", "boundary"], [{"date": "2026-07-14", "actor": "YOFC", "signal": "new fibre/cable demand and profitability improved", "demand_or_supply": "demand", "evidence_level": "issuer_profit_alert", "boundary": "no order or ASP"}, {"date": "2026-07-28", "actor": "Corning", "signal": "optical communications and enterprise network growth", "demand_or_supply": "demand_and_future_supply", "evidence_level": "peer_IR", "boundary": "adjacent global peer"}, {"date": "2026-06-26", "actor": "Dahan", "signal": "phased preform and 60m core-km fibre plan", "demand_or_supply": "supply", "evidence_level": "exchange_filing", "boundary": "announced is not effective capacity"}])
    write_csv("event-timeline.csv", ["date", "event", "layer", "source_ref", "research_effect"], [{"date": "2025-12-17", "event": "70m H-share placing completed", "layer": "capital", "source_ref": "S6", "research_effect": "dilution and overseas funding"}, {"date": "2026-03-06", "event": "HollowBand launch", "layer": "technology", "source_ref": "S15", "research_effect": "optionality"}, {"date": "2026-04-29", "event": "Q1 report", "layer": "fundamental", "source_ref": "S4", "research_effect": "margin inflection"}, {"date": "2026-06-26", "event": "competitor capacity plan", "layer": "supply", "source_ref": "S14", "research_effect": "duration risk"}, {"date": "2026-07-14", "event": "H1 profit alert", "layer": "fundamental", "source_ref": "S5", "research_effect": "profit confirmation"}, {"date": "2026-07-30", "event": "YOFC Shanghai acquisition", "layer": "corporate", "source_ref": "S16", "research_effect": "scope change"}, {"date": "2026-08-11", "event": "Lumentum results after US close", "layer": "peer", "source_ref": "S17", "research_effect": "overnight signal"}, {"date": "2026-08-12", "event": "Coherent results after US close", "layer": "peer", "source_ref": "S18", "research_effect": "overnight signal"}, {"date": "TBA late Aug 2026", "event": "YOFC formal H1", "layer": "company", "source_ref": "S5", "research_effect": "critical validation"}])
    write_csv("price-history.csv", ["date", "open", "close", "high", "low", "volume"], [{"date": r[0], "open": r[1], "close": r[2], "high": r[3], "low": r[4], "volume": r[5]} for r in PRICE_ROWS])
    write_csv("risk-reward-scenarios.csv", ["reference", "low", "high", "from_price_low_pct", "from_price_high_pct", "boundary"], [{"reference": "recent_base", "low": 92, "high": 96, "from_price_low_pct": round((92 / H_PRICE - 1) * 100, 2), "from_price_high_pct": round((96 / H_PRICE - 1) * 100, 2), "boundary": "technical reference not intrinsic value"}, {"reference": "first_supply_zone", "low": 140, "high": 154, "from_price_low_pct": round((140 / H_PRICE - 1) * 100, 2), "from_price_high_pct": round((154 / H_PRICE - 1) * 100, 2), "boundary": "technical reference not target price"}])
    write_csv("gate-results.csv", ["gate", "result", "reason"], [{k: row[k] for k in ("gate", "result", "reason")} for row in artifact["gates"]])
    write_csv("research-dimensions.csv", ["dimension", "status", "summary", "indicator_1", "indicator_1_status", "indicator_2", "indicator_2_status"], [{"dimension": row["dimension"], "status": row["status"], "summary": row["summary"], "indicator_1": row["indicators"][0]["id"], "indicator_1_status": row["indicators"][0]["status"], "indicator_2": row["indicators"][1]["id"], "indicator_2_status": row["indicators"][1]["status"]} for row in artifact["research_dimensions"]])


if __name__ == "__main__":
    main()
