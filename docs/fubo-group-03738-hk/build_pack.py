#!/usr/bin/env python3
# ruff: noqa
"""Build the public, checksum-bound Vobile Group research package."""

from __future__ import annotations

import csv
import hashlib
import html
import json
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
TMP = Path("/tmp/fubo-research.L9O3PD")
DATA = ROOT / "data"
DATA.mkdir(parents=True, exist_ok=True)


def dump_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict], fields: list[str] | None = None) -> None:
    if fields is None:
        fields = list(dict.fromkeys(key for row in rows for key in row)) if rows else []
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pct(new: float, old: float) -> float:
    return (new / old - 1.0) * 100.0


def source_ref(
    source_id: str,
    tier: str,
    source_type: str,
    title: str,
    url: str,
    period: str,
    audit_status: str,
    scope: str,
    covers: list[str],
    *,
    published_at: str | None,
    digest: str | None = None,
) -> dict:
    row = {
        "id": source_id,
        "tier": tier,
        "source_type": source_type,
        "title": title,
        "url": url,
        "published_at_status": "known" if published_at else "not_disclosed",
        "published_at": published_at,
        "accessed_at": "2026-07-27",
        "period": period,
        "audit_status": audit_status,
        "scope": scope,
        "covers": covers,
    }
    if not published_at:
        row["date_reason"] = "The live primary page or company deck does not disclose a stable publication date."
    if digest:
        row["content_sha256"] = digest
    return row


source_refs = [
    source_ref(
        "F01", "A", "exchange_filing", "Vobile Group Annual Report 2025",
        "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0430/2026043003894.pdf",
        "FY2025", "audited", "consolidated_group",
        ["financial_statements", "revenue", "cash_flow", "share_capital", "governance", "customers"],
        published_at="2026-04-30",
        digest="0f4c34299259887c418fc1599a6df4c2174615296b0013493cd919fd6267c7fa",
    ),
    source_ref(
        "F02", "A", "exchange_filing", "Vobile Group Interim Report 2025",
        "https://www.hkexnews.hk/listedco/listconews/sehk/2025/0930/2025093003000.pdf",
        "2025H1", "unaudited", "consolidated_group",
        ["financial_statements", "revenue", "cash_flow", "operating_kpis"],
        published_at="2025-09-30",
        digest="7493774c0dce9632f8fe8fa9f25fcdc8216a34ea4e1c836ccd3db643af2f1f76",
    ),
    source_ref(
        "F03", "A", "exchange_announcement", "Unaudited Operating Data for Q1 2026",
        "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0519/2026051900384.pdf",
        "2026Q1", "unaudited", "consolidated_group",
        ["revenue_growth", "monthly_recurring_revenue"],
        published_at="2026-05-19",
        digest="48366f874f224a4a0e59e49903250e35cf723118e730059fac2dda9ad10d9a8c",
    ),
    source_ref(
        "F04", "A", "exchange_announcement", "Proposed HK$1.6bn Zero-Coupon Convertible Bonds due 2026",
        "https://www1.hkexnews.hk/listedco/listconews/sehk/2025/0923/2025092300072.pdf",
        "2025-09-23", "not_applicable", "listed_security",
        ["convertible_bond", "dilution", "use_of_proceeds"],
        published_at="2025-09-23",
        digest="30458b857b382f0706dc128f87153c776d7435423300a43cfb8006d06fab41df",
    ),
    source_ref(
        "F05", "A", "monthly_return", "Monthly Return for June 2026",
        "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0707/2026070701937.pdf",
        "2026-06", "not_applicable", "listed_security",
        ["issued_shares", "treasury_shares", "options", "convertible_bond"],
        published_at="2026-07-07",
        digest="6af5a0718526315c90d23ddf8c7ebebc846364d6054ede48c3d3d0d60991352d",
    ),
    source_ref(
        "F06", "B", "company_presentation", "FY2025 Results Presentation",
        "https://vobile.com/storage/upload/260522/6a101d1b03327.pdf",
        "FY2025", "unaudited", "company_defined_operating_kpis",
        ["active_assets", "subscription_mrr", "retention", "products"],
        published_at=None,
        digest="cfc82492af0c0af963342d706df15a7bdde175ec5fefa861b215c482f51d5fb8",
    ),
    source_ref(
        "F07", "B", "management_transcript", "Q1 2026 Earnings Call Transcript",
        "https://vobile.com/storage/upload/260527/6a16cc402ca76.pdf",
        "2026Q1", "unaudited", "management_claims",
        ["active_assets", "ai_assets", "platform_policy", "management_commentary"],
        published_at="2026-05-27",
        digest="bcfc9dfaf406905180d0d21a34a5b75c41e67124902b6a53608f14b00b3856be",
    ),
    source_ref(
        "F08", "A", "audited_annual_report", "Vobile Group Annual Report 2024",
        "https://vobile.com/storage/upload/250430/68123d631b833.pdf",
        "FY2024", "audited", "consolidated_group",
        ["financial_statements", "cash_flow", "revenue"],
        published_at="2025-04-30",
        digest="4130d4d43e367c0bcd601688206fb666653143e78f5d77b6895f5dddab0dd210",
    ),
    source_ref(
        "F09", "A", "audited_annual_report", "Vobile Group Annual Report 2023",
        "https://vobile.com/storage/upload/250430/6812417b860ae.pdf",
        "FY2023", "audited", "consolidated_group",
        ["financial_statements", "cash_flow", "revenue"],
        published_at="2024-04-30",
        digest="3d455c081481bc7743ce602536ca4e684c435fc828bcaa171a0530b02a758561",
    ),
    source_ref(
        "F10", "A", "audited_annual_report", "Vobile Group Annual Report 2022",
        "https://vobile.com/storage/upload/240424/66287e5980439.pdf",
        "FY2022", "audited", "consolidated_group",
        ["financial_statements", "cash_flow", "revenue"],
        published_at="2023-04-28",
        digest="9623e2f9344efb01c6b3e43164c8d71febae7f3c47c2fc635fe2a60362780c7d",
    ),
    source_ref(
        "M01", "C", "market_data", "Yahoo Finance 3738.HK chart API snapshot",
        "https://query1.finance.yahoo.com/v8/finance/chart/3738.HK?range=5y&interval=1d&events=history",
        "2021-07-27 to 2026-07-27", "not_applicable", "listed_security",
        ["price", "volume"],
        published_at="2026-07-27",
        digest="e7873401f2aa541b476b0c318300c295779eb470a23ff6862a2092b788c3d60f",
    ),
    source_ref(
        "M02", "C", "market_data", "Yahoo Finance Hang Seng Index chart API snapshot",
        "https://query1.finance.yahoo.com/v8/finance/chart/%5EHSI?range=5y&interval=1d&events=history",
        "2021-07-27 to 2026-07-27", "not_applicable", "benchmark_index",
        ["benchmark_price"],
        published_at="2026-07-27",
        digest="6440865a7ddc8481d178fbf41867e37f70b1bdca9ba903206b14b324fd3a20a6",
    ),
    source_ref(
        "S01", "A", "regulator_data", "SFC Aggregated Reportable Short Positions 2026-07-17",
        "https://www.sfc.hk/-/media/EN/pdf/spr/2026/07/17/Short_Position_Reporting_Aggregated_Data_Eng_20260717.pdf",
        "2026-07-17", "not_applicable", "reportable_short_positions",
        ["short_position"],
        published_at="2026-07-24",
        digest="06a022febb026e6b3897705239419a11530c3156789513f8dfa5f6901c68b890",
    ),
    source_ref(
        "I01", "B", "platform_primary", "YouTube: New tools to protect creators and artists",
        "https://blog.youtube/news-and-events/responsible-ai-tools/",
        "2024-09-05", "not_applicable", "platform_policy",
        ["platform_substitution", "ai_content_identification"],
        published_at="2024-09-05",
        digest="0e2024dd0574ce51fbf2a386c4a1d58728966ad07bcbe1b05f312500102a5856",
    ),
    source_ref(
        "I02", "B", "platform_primary", "YouTube: Improving AI labels for viewers and creators",
        "https://blog.youtube/news-and-events/improving-ai-labels-viewers-creators/",
        "2026-05-27", "not_applicable", "platform_policy",
        ["automatic_ai_detection", "c2pa_handling"],
        published_at="2026-05-27",
        digest="55e0d1c26cf46dc4fc46bf8d48efcc90c7251a5c9e5be109116e042c2b8bc438",
    ),
    source_ref(
        "I03", "A", "regulator_primary", "U.S. Copyright Office releases Part 2 of AI Report",
        "https://www.copyright.gov/newsnet/2025/1060.html?loclr=licop",
        "2025-01-29", "not_applicable", "regulatory_policy",
        ["ai_output_copyrightability"],
        published_at="2025-01-29",
        digest="b508523831f07b8a37357d062391482d40238b527643e83e38dbc79e9739a88c",
    ),
    source_ref(
        "I04", "A", "industry_standard", "C2PA Technical Specification",
        "https://spec.c2pa.org/specifications/specifications/1.0/specs/C2PA_Specification.html",
        "current", "not_applicable", "industry_standard",
        ["content_provenance", "adjacent_technology"],
        published_at=None,
        digest="7b220209e866a612a2bb803ff45ca0788232b8dee13e357161300fa10cf00c38",
    ),
]


ledger_extra = [
    {
        "id": "C01", "tier": "A", "kind": "official_connect_lists",
        "title": "SSE/SZSE Southbound eligible-security snapshot",
        "publisher": "Shanghai Stock Exchange / Shenzhen Stock Exchange",
        "published_at": "2026-07-27", "retrieved_at": "2026-07-27",
        "url": "https://www.sse.com.cn/services/hkexsc/disclo/eligible/",
        "snapshot_sha256": None,
        "used_for": ["current Stock Connect eligibility"],
        "limitations": "Current frozen Seed master records eligibility in both Shanghai and Shenzhen southbound programs; broker/account permission is separate.",
    },
    {
        "id": "H01", "tier": "A", "kind": "official_filings_index",
        "title": "HKEX Listed Company Title Search: 03738",
        "publisher": "HKEX", "published_at": None, "retrieved_at": "2026-07-27",
        "url": "https://www1.hkexnews.hk/search/titlesearch.xhtml?category=0&lang=EN&market=SEHK&stockId=170283",
        "snapshot_sha256": None,
        "used_for": ["filing discovery", "release time", "event chronology"],
        "limitations": "Index entry locates filings; filing PDFs remain the fact source.",
    },
    {
        "id": "I05", "tier": "A-", "kind": "company_ir",
        "title": "Vobile Investor Relations Overview",
        "publisher": "Vobile Group", "published_at": None, "retrieved_at": "2026-07-27",
        "url": "https://vobile.com/overview?lang=en-us",
        "snapshot_sha256": None,
        "used_for": ["product map", "company-defined KPIs"],
        "limitations": "Company marketing and KPI presentation; use audited filings for financial facts.",
    },
]


source_ledger_sources = []
for row in source_refs:
    source_ledger_sources.append(
        {
            "id": row["id"],
            "tier": row["tier"],
            "kind": row["source_type"],
            "title": row["title"],
            "publisher": (
                "HKEX / Vobile" if row["id"].startswith("F") else
                "Yahoo Finance" if row["id"].startswith("M") else
                "SFC" if row["id"].startswith("S") else
                "YouTube" if row["id"] in {"I01", "I02"} else
                "U.S. Copyright Office" if row["id"] == "I03" else
                "C2PA"
            ),
            "published_at": row.get("published_at"),
            "retrieved_at": row["accessed_at"],
            "url": row["url"],
            "snapshot_sha256": row.get("content_sha256"),
            "used_for": row["covers"],
            "limitations": {
                "F03": "Preliminary, unaudited percentage changes; no absolute quarterly revenue, margin, profit or cash flow.",
                "F06": "Company-defined KPI deck; NRR, retention and active-asset definitions are not independently audited.",
                "F07": "Management transcript; claims are not audited facts.",
                "M01": "Third-party adjusted/unadjusted daily market data; corporate-action completeness not independently certified.",
                "M02": "Third-party Hang Seng Index benchmark snapshot; used only for event-window context, not as a primary industry or regulatory source.",
                "S01": "Only positions above statutory reporting thresholds; publication lag and hedging positions may exist.",
            }.get(
                row["id"],
                "Primary filing facts are used within their stated period, scope and assurance."
                if row["id"].startswith("F")
                else "Primary industry or regulatory source; it does not establish Vobile revenue or valuation.",
            ),
        }
    )
source_ledger_sources.extend(ledger_extra)


financial_rows = [
    {"period": "FY2021", "revenue": 686.528, "subscription": 205.786, "value_added": 480.742, "gross_profit": 348.771, "parent_net_income": -22.677, "cfo": -8.773, "ppe_capex": 25.852, "intangible_additions": 40.430, "free_cash_flow_after_all_capex": -75.055, "diluted_eps": -0.0119, "source_refs": "F10/F09"},
    {"period": "FY2022", "revenue": 1442.670, "subscription": 549.005, "value_added": 893.665, "gross_profit": 590.712, "parent_net_income": 42.002, "cfo": 37.608, "ppe_capex": 9.511, "intangible_additions": 95.575, "free_cash_flow_after_all_capex": -67.478, "diluted_eps": 0.0196, "source_refs": "F10"},
    {"period": "FY2023", "revenue": 2000.989, "subscription": 868.458, "value_added": 1132.531, "gross_profit": 850.157, "parent_net_income": -7.818, "cfo": 110.849, "ppe_capex": 33.971, "intangible_additions": 176.109, "free_cash_flow_after_all_capex": -99.231, "diluted_eps": -0.0035, "source_refs": "F09/F08"},
    {"period": "FY2024", "revenue": 2401.322, "subscription": 1103.693, "value_added": 1297.629, "gross_profit": 1051.463, "parent_net_income": 142.727, "cfo": 4.137, "ppe_capex": 13.128, "intangible_additions": 211.842, "free_cash_flow_after_all_capex": -220.833, "diluted_eps": 0.0588, "source_refs": "F08/F01"},
    {"period": "FY2025", "revenue": 2872.361, "subscription": 1223.536, "value_added": 1648.825, "gross_profit": 1285.992, "parent_net_income": 199.312, "cfo": 69.916, "ppe_capex": 5.634, "intangible_additions": 427.731, "free_cash_flow_after_all_capex": -363.449, "diluted_eps": 0.0775, "source_refs": "F01"},
]
for i, row in enumerate(financial_rows):
    row["gross_margin_pct"] = round(row["gross_profit"] / row["revenue"] * 100, 2)
    row["revenue_yoy_pct"] = None if i == 0 else round(pct(row["revenue"], financial_rows[i - 1]["revenue"]), 2)
write_csv(DATA / "financial-history.csv", financial_rows)


revenue_mix_rows = [
    {
        "period": r["period"], "subscription_hkd_m": r["subscription"],
        "value_added_and_other_hkd_m": r["value_added"],
        "subscription_share_pct": round(r["subscription"] / r["revenue"] * 100, 2),
        "value_added_share_pct": round(r["value_added"] / r["revenue"] * 100, 2),
    }
    for r in financial_rows
]
write_csv(DATA / "revenue-mix.csv", revenue_mix_rows)


interim_rows = [
    {"period": "2024H1", "revenue_hkd_m": 1180.634, "subscription_hkd_m": 545.431, "value_added_hkd_m": 635.203, "gross_profit_hkd_m": 504.117, "parent_profit_hkd_m": 41.474, "cfo_hkd_m": 11.018, "diluted_eps_hkd": 0.0171, "assurance": "unaudited comparative"},
    {"period": "2025H1", "revenue_hkd_m": 1456.315, "subscription_hkd_m": 609.902, "value_added_hkd_m": 846.413, "gross_profit_hkd_m": 642.730, "parent_profit_hkd_m": 102.344, "cfo_hkd_m": 8.910, "diluted_eps_hkd": 0.0412, "assurance": "unaudited"},
    {"period": "2025H2 derived", "revenue_hkd_m": 1416.046, "subscription_hkd_m": 613.634, "value_added_hkd_m": 802.412, "gross_profit_hkd_m": 643.262, "parent_profit_hkd_m": 96.968, "cfo_hkd_m": 61.006, "diluted_eps_hkd": None, "assurance": "FY minus H1; not a reported quarter"},
]
write_csv(DATA / "half-year-kpis.csv", interim_rows)


operating_kpis = [
    {"period": "2023FY", "active_assets_m": None, "subscription_mrr_usd_m": 9.0, "ai_asset_share_pct": None, "source": "F06"},
    {"period": "2024FY", "active_assets_m": 3.70, "subscription_mrr_usd_m": 12.0, "ai_asset_share_pct": 3.0, "source": "F06"},
    {"period": "2025Q1", "active_assets_m": 3.96, "subscription_mrr_usd_m": None, "ai_asset_share_pct": None, "source": "F06"},
    {"period": "2025Q2", "active_assets_m": 4.29, "subscription_mrr_usd_m": None, "ai_asset_share_pct": None, "source": "F02/F06"},
    {"period": "2025Q3", "active_assets_m": 4.69, "subscription_mrr_usd_m": None, "ai_asset_share_pct": 9.1, "source": "F06"},
    {"period": "2025Q4", "active_assets_m": 4.86, "subscription_mrr_usd_m": 15.0, "ai_asset_share_pct": 17.0, "source": "F06"},
    {"period": "2026Q1", "active_assets_m": 5.24, "subscription_mrr_usd_m": None, "ai_asset_share_pct": 16.6, "source": "F07"},
]
write_csv(DATA / "active-assets-mrr.csv", operating_kpis)


retention_rows = [
    {"period": "FY2025", "metric": "net_revenue_retention", "value_pct": 128.0, "scope": "company-defined", "source": "F06/I05", "limitation": "Cohort, denominator and currency normalization not fully disclosed."},
    {"period": "FY2025", "metric": "customer_retention", "value_pct": 98.2, "scope": "company-defined", "source": "F06/I05", "limitation": "Customer-count denominator and gross/logo retention methodology not fully disclosed."},
    {"period": "FY2025", "metric": "largest_customer_revenue_share", "value_pct": 13.0, "scope": "audited group", "source": "F01", "limitation": "Customer identity not disclosed."},
    {"period": "FY2025", "metric": "top_five_customer_revenue_share", "value_pct": 40.0, "scope": "audited group", "source": "F01", "limitation": "Concentration remains material despite high company-defined retention."},
]
write_csv(DATA / "retention-and-concentration.csv", retention_rows)


product_rows = [
    {"product_or_platform": "Rights ID", "role": "content protection and monetization workflow", "signal": "core operating platform", "web_traffic_relevance": "low", "source": "F01/I05"},
    {"product_or_platform": "Channel ID", "role": "channel and audience operations", "signal": "customer workflow", "web_traffic_relevance": "low", "source": "F01/I05"},
    {"product_or_platform": "Rights Data Network", "role": "rights data and asset discovery", "signal": "data/network hypothesis", "web_traffic_relevance": "low", "source": "F01/I05"},
    {"product_or_platform": "MediaWise", "role": "content identification and protection", "signal": "enterprise tooling", "web_traffic_relevance": "low", "source": "F01/I05"},
    {"product_or_platform": "Vobile X", "role": "AIGC and digital-asset services", "signal": "emerging AI-rights workflow", "web_traffic_relevance": "low", "source": "F01/F07"},
    {"product_or_platform": "Pex", "role": "music/audio fingerprint and rights identification", "signal": "acquired data/technology base", "web_traffic_relevance": "low", "source": "F01"},
]
write_csv(DATA / "products-platforms.csv", product_rows)


rd_rows = [
    {"period": "FY2024", "rd_expense_hkd_m": 270.947, "capitalized_development_hkd_m": 190.266, "total_rd_like_investment_hkd_m": 461.213, "capitalized_to_expensed_pct": 70.22, "source": "F01/F08"},
    {"period": "FY2025", "rd_expense_hkd_m": 320.832, "capitalized_development_hkd_m": 367.720, "total_rd_like_investment_hkd_m": 688.552, "capitalized_to_expensed_pct": 114.61, "source": "F01"},
]
write_csv(DATA / "rd-capitalization.csv", rd_rows)


owner_proxy_rows = [
    {
        "period": r["period"], "parent_net_income_hkd_m": r["parent_net_income"],
        "cfo_hkd_m": r["cfo"], "ppe_capex_hkd_m": r["ppe_capex"],
        "intangible_additions_hkd_m": r["intangible_additions"],
        "cash_proxy_hkd_m": r["free_cash_flow_after_all_capex"],
        "formula": "CFO - PPE capex - intangible additions",
        "owner_earnings_status": "unavailable",
    }
    for r in financial_rows
]
write_csv(DATA / "owner-earnings-cash-proxy.csv", owner_proxy_rows)


earnings_bridge_rows = [
    {"item": "reported_group_profit", "hkd_m": 211.692, "operator": "starting point", "scope": "consolidated group", "source": "F01"},
    {"item": "share_based_compensation", "hkd_m": 18.720, "operator": "company adds back", "scope": "group", "source": "F01"},
    {"item": "derecognition", "hkd_m": 2.584, "operator": "company adds back", "scope": "group", "source": "F01"},
    {"item": "transaction_cost", "hkd_m": 4.786, "operator": "company adds back", "scope": "group", "source": "F01"},
    {"item": "FVTPL_gain", "hkd_m": -6.038, "operator": "company subtracts", "scope": "group", "source": "F01"},
    {"item": "company_adjusted_group_profit", "hkd_m": 231.744, "operator": "result", "scope": "group, not parent-attributable", "source": "F01"},
    {"item": "reported_parent_profit", "hkd_m": 199.312, "operator": "separate reported denominator", "scope": "parent-attributable", "source": "F01"},
]
write_csv(DATA / "earnings-quality-bridge.csv", earnings_bridge_rows)


net_debt_rows = [
    {"item": "cash_and_cash_equivalents", "hkd_m": 1157.048, "sign": 1, "as_of": "2025-12-31", "source": "F01"},
    {"item": "restricted_cash", "hkd_m": 10.050, "sign": 1, "as_of": "2025-12-31", "source": "F01"},
    {"item": "bank_loans", "hkd_m": 401.006, "sign": -1, "as_of": "2025-12-31", "source": "F01"},
    {"item": "convertible_bond_liabilities", "hkd_m": 1608.554, "sign": -1, "as_of": "2025-12-31", "source": "F01"},
    {"item": "lease_liabilities", "hkd_m": 21.925, "sign": -1, "as_of": "2025-12-31", "source": "F01"},
    {"item": "reported_net_debt", "hkd_m": 842.462, "sign": None, "as_of": "2025-12-31", "source": "F01", "note": "Company net-debt definition excludes leases in cited bridge."},
]
write_csv(DATA / "net-debt-bridge.csv", net_debt_rows)


share_rows = [
    {"item": "issued_shares_excluding_treasury", "shares": 2592865836, "as_of": "2026-06-30", "treatment": "base", "source": "F05"},
    {"item": "outstanding_options", "shares": 165325000, "as_of": "2026-06-30", "treatment": "conservative legal overhang", "source": "F05"},
    {"item": "remaining_large_cb_conversion_shares", "shares": 248381602, "as_of": "2026-06-30", "treatment": "if converted at HK$5.87", "source": "F05"},
    {"item": "fully_diluted_legal_ceiling", "shares": 3006572438, "as_of": "2026-06-30", "treatment": "base + options + CB", "source": "F05"},
]
write_csv(DATA / "fully-diluted-share-bridge.csv", share_rows)


short_rows = [
    {"reporting_date": "2026-01-16", "reportable_short_shares": 141021535, "approx_pct_fixed_june_issued": 5.44, "market_value_hkd_m": 692.4, "source": "SFC archived weekly report"},
    {"reporting_date": "2026-04-10", "reportable_short_shares": 153398892, "approx_pct_fixed_june_issued": 5.92, "market_value_hkd_m": 589.1, "source": "SFC archived weekly report"},
    {"reporting_date": "2026-05-29", "reportable_short_shares": 132926071, "approx_pct_fixed_june_issued": 5.13, "market_value_hkd_m": 372.2, "source": "SFC archived weekly report"},
    {"reporting_date": "2026-07-17", "reportable_short_shares": 122802839, "approx_pct_fixed_june_issued": 4.74, "market_value_hkd_m": 278.762445, "source": "S01"},
]
write_csv(DATA / "short-positioning.csv", short_rows)


mapping_rows = [
    {"entity": "YouTube Content ID", "market": "United States/global", "mapping_type": "downstream_platform_internal_substitute", "relationship": "Platform-native rights matching and monetization; can complement or displace third-party layers.", "source": "I01"},
    {"entity": "Meta Rights Manager", "market": "United States/global", "mapping_type": "downstream_platform_internal_substitute", "relationship": "Platform-native rights tooling; not a listed pure-play comparable.", "source": "platform primary documentation"},
    {"entity": "C2PA / Content Credentials", "market": "global standard", "mapping_type": "thematic_adjacent_complement", "relationship": "Authenticity/provenance standard; does not by itself establish ownership or monetize rights.", "source": "I02/I04"},
    {"entity": "Veritone (NASDAQ: VERI)", "market": "United States", "mapping_type": "thematic_peer", "relationship": "AI/media workflow peer; business mix, scale and rights economics differ.", "source": "company public filings, not normalized here"},
    {"entity": "U.S. Copyright Office AI reports", "market": "United States", "mapping_type": "regulatory_lead_signal", "relationship": "Copyrightability, replicas and training policy shape demand and liability, not a company comparable.", "source": "I03"},
]
write_csv(DATA / "overseas-mapping.csv", mapping_rows)


def load_price(path: Path) -> list[dict]:
    raw = json.loads(path.read_text(encoding="utf-8"))["chart"]["result"][0]
    quote = raw["indicators"]["quote"][0]
    result = []
    for i, stamp in enumerate(raw["timestamp"]):
        if quote["close"][i] is None:
            continue
        day = datetime.fromtimestamp(stamp, tz=timezone.utc).date().isoformat()
        result.append({
            "date": day,
            "open": quote["open"][i],
            "high": quote["high"][i],
            "low": quote["low"][i],
            "close": quote["close"][i],
            "volume": quote["volume"][i],
        })
    return result


price_rows = load_price(TMP / "price-3738.json")
hsi_rows = load_price(TMP / "price-hsi.json")
write_csv(DATA / "price-history.csv", price_rows)
price_by_date = {r["date"]: i for i, r in enumerate(price_rows)}
hsi_by_date = {r["date"]: i for i, r in enumerate(hsi_rows)}


event_defs = [
    ("2025-05-23", "2025-05-26", "2025Q1 operating update", "H01", "operating_kpi"),
    ("2025-06-03", "2025-06-04", "Placement completion", "H01", "dilution"),
    ("2025-08-28", "2025-08-29", "2025H1 results", "F02", "earnings"),
    ("2025-09-23", "2025-09-23", "HK$1.6bn convertible proposed", "F04", "financing"),
    ("2025-09-29", "2025-09-30", "Convertible issue completion", "H01", "financing"),
    ("2025-11-05", "2025-11-06", "2025Q3 operating update", "H01", "operating_kpi"),
    ("2026-03-27", "2026-03-27", "FY2025 results", "F01", "earnings"),
    ("2026-05-19", "2026-05-20", "2026Q1 operating update", "F03", "operating_kpi"),
    ("2026-07-07", "2026-07-08", "June monthly return: CB repurchase", "F05", "financing"),
    ("2026-07-12", "2026-07-13", "Director change announcement", "H01", "governance"),
]
event_rows = []
for announced, effective, label, source, category in event_defs:
    i = price_by_date[effective]
    b = hsi_by_date.get(effective)
    pre = price_rows[i - 1]["close"]
    row = {
        "announcement_date": announced,
        "first_trading_date": effective,
        "event": label,
        "category": category,
        "source": source,
        "pre_close_hkd": round(pre, 4),
        "t0_close_hkd": round(price_rows[i]["close"], 4),
        "t0_return_pct": round(pct(price_rows[i]["close"], pre), 2),
        "t1_return_pct": round(pct(price_rows[min(i + 1, len(price_rows) - 1)]["close"], pre), 2),
        "t5_return_pct": round(pct(price_rows[min(i + 5, len(price_rows) - 1)]["close"], pre), 2),
        "hsi_t0_return_pct": None if b is None else round(pct(hsi_rows[b]["close"], hsi_rows[b - 1]["close"]), 2),
        "causal_confidence": "low_to_medium",
        "limitations": "Window overlaps market/sector/company events; price reaction is association, not proof of causality.",
    }
    row["t0_excess_vs_hsi_pct"] = None if row["hsi_t0_return_pct"] is None else round(row["t0_return_pct"] - row["hsi_t0_return_pct"], 2)
    event_rows.append(row)
write_csv(DATA / "event-price-reactions.csv", event_rows)


closes = [r["close"] for r in price_rows]
price_state_rows = []
for n in (20, 60, 200):
    price_state_rows.append({"metric": f"{n}d_sma", "value": round(sum(closes[-n:]) / n, 4), "unit": "HKD", "as_of": "2026-07-27", "formula": f"mean(last {n} daily closes)"})
price_state_rows.extend([
    {"metric": "last_close", "value": round(closes[-1], 4), "unit": "HKD", "as_of": "2026-07-27", "formula": "market close"},
    {"metric": "52w_high", "value": round(max(closes[-252:]), 4), "unit": "HKD", "as_of": "2026-07-27", "formula": "max(last 252 closes)"},
    {"metric": "52w_low", "value": round(min(closes[-252:]), 4), "unit": "HKD", "as_of": "2026-07-27", "formula": "min(last 252 closes)"},
    {"metric": "1y_return", "value": round(pct(closes[-1], closes[-253]), 2), "unit": "%", "as_of": "2026-07-27", "formula": "last close / close 252 sessions ago - 1"},
])
write_csv(DATA / "market-price-state.csv", price_state_rows)


dimension_sources = {
    "security_and_legal_subject": ["F01", "F05", "M01"],
    "control_and_beneficial_ownership": ["F01"],
    "business_model": ["F01", "F06", "F07"],
    "revenue_structure": ["F01", "F02"],
    "industry_chain_position": ["F01", "I01", "I02", "I03", "I04"],
    "product_and_unit_economics": ["F01", "F06"],
    "customers": ["F01", "F06"],
    "suppliers": ["F01"],
    "competition_structure": ["F01", "I01", "I02", "I04"],
    "durable_moat": ["F01", "F06", "F07", "I01"],
    "revenue_quality": ["F01", "F02"],
    "earnings_quality": ["F01"],
    "cash_conversion": ["F01", "F02", "F08", "F09", "F10"],
    "working_capital": ["F01"],
    "capital_intensity": ["F01", "F08"],
    "returns_on_capital": ["F01", "F08", "F09", "F10"],
    "balance_sheet_survival": ["F01", "F04", "F05"],
    "capital_allocation": ["F01", "F04", "F05"],
    "management": ["F01", "F07"],
    "governance_and_related_parties": ["F01"],
    "accounting_and_audit": ["F01", "F08", "F09", "F10"],
    "tax_and_legal": ["F01", "I03"],
    "per_share_economics": ["F01", "F04", "F05"],
    "valuation": ["F01", "F05", "M01"],
    "disconfirming_evidence": ["F01", "F03", "F04", "F05", "I01", "I02"],
}

dimension_summaries = {
    "security_and_legal_subject": "03738.HK 普通股、港元报价；截至 2026-06-30 已发行不含库存股 25.929 亿股，现为沪深南向合资格证券。",
    "control_and_beneficial_ownership": "创始人兼主席/CEO 王扬斌披露权益约 16.35%；主席与 CEO 合一，需要把执行力优势与监督风险同时保留。",
    "business_model": "向权利人和平台提供版权识别、保护、归因与变现；订阅与按资产变现相关的增值服务构成两条收入链。",
    "revenue_structure": "FY2025 订阅收入 12.235 亿港元、增值及其他 16.488 亿；后者占 57.4%，不能把全部收入当 ARR。",
    "industry_chain_position": "位于权利人—平台—用户生成内容之间；生成式 AI 扩张增加可识别资产，也加强平台自建与规则控制。",
    "product_and_unit_economics": "公司披露 MRR、活跃资产和留存，但未完整披露 CAC、单位毛利、分产品价格与 cohort 经济性。",
    "customers": "最大客户占 13%、前五占 40%；公司口径 NRR 128%、客户留存 98.2%，定义与分母仍需补证。",
    "suppliers": "平台、云/技术与专业服务是关键投入；前五供应商占 34%、最大 8%，但平台依赖不完全等于会计供应商集中度。",
    "competition_structure": "竞争不仅来自第三方版权技术商，也来自 YouTube/Meta 等平台内部工具及 C2PA 等相邻基础设施。",
    "durable_moat": "指纹库、历史权利数据、平台工作流与客户嵌入是护城河假设；平台 API/规则和并购形成的数据资产决定其耐久性。",
    "revenue_quality": "96.5% 收入按时间确认不等于 96.5% 可续费；应收净额 17.537 亿、同比增加 3.765 亿，是现金质量核心约束。",
    "earnings_quality": "法定归母利润 1.993 亿；公司调整利润为集团口径 2.317 亿，范围不同，不能直接做调整后每股收益。",
    "cash_conversion": "FY2025 CFO 0.699 亿，扣 PPE 与无形资产投入后现金代理为 -3.634 亿；五年均为负。",
    "working_capital": "应收和预付款增长吸收现金；合同负债/剩余履约义务只覆盖较短期限，不能自动等同长期 ARR。",
    "capital_intensity": "软件外观并不等于低投入：FY2025 资本化开发 3.677 亿，高于研发费用 3.208 亿。",
    "returns_on_capital": "并购、商誉、资本化研发和净债务快速变化使机械 ROIC 易失真；本版不输出伪精确经济 ROIC。",
    "balance_sheet_survival": "2026-09 到期大额可转债剩余本金 14.58 亿港元；低于 HK$5.87 时以偿付/再融资压力为主。",
    "capital_allocation": "2025 年多次发债、配股与并购扩张；必须用全摊薄每股现金收益审查，而非只看收入增长。",
    "management": "Q1 电话会披露活跃资产与平台政策影响，透明度有增量；但绝对季度利润和现金流仍未披露。",
    "governance_and_related_parties": "主席/CEO 合一、并购与激励规模需要持续监督；未发现并不等于不存在未披露的价值转移。",
    "accounting_and_audit": "审计报表可复核，但研发资本化、商誉减值和应收损失假设是高判断领域。",
    "tax_and_legal": "版权归属、AI 训练、数字替身及平台争议规则可能改变可变现资产和诉讼路径；本报告不是法律意见。",
    "per_share_economics": "6 月底保守法律稀释上限约 30.066 亿股，较基本股数高约 15.96%；未来方案额度不计入已授予稀释。",
    "valuation": "HK$2.39 对 FY2025 稀释 EPS 的静态 PE 约 30.84 倍；TTM、forward 和 DCF 因缺少可审计分母而保持 unavailable。",
    "disconfirming_evidence": "最强反方是：平台自建、规则改变、研发资本化与应收增长共同使会计增长无法转成全摊薄每股现金收益。",
}

indicator_gaps = {
    "product_and_unit_economics": ["缺 CAC、分产品毛利、cohort 留存和可复核单位经济性。"],
    "customers": ["NRR 与留存的 cohort、分母、汇率及并购口径未完整披露。"],
    "suppliers": ["没有把平台依赖、云/API 成本与会计供应商前五名完整映射。"],
    "returns_on_capital": ["资本化研发、并购商誉和维护/增长投入尚未标准化。"],
    "management": ["缺完整承诺—兑现逐年台账及具名客户独立访谈。"],
    "governance_and_related_parties": ["关联方、激励与并购定价仍需逐页人工复核。"],
    "valuation": ["缺无前视偏差历史 PE、标准化同行与可审计 owner earnings。"],
}


template = json.loads((REPO / "docs/company-research/templates/company-research-v2.example.json").read_text(encoding="utf-8"))
research_dimensions = []
for original in template["research_dimensions"]:
    key = original["dimension"]
    refs = dimension_sources[key]
    indicators = []
    for item in original["indicators"]:
        indicators.append({
            "id": item["id"],
            "status": "observed",
            "summary": dimension_summaries[key],
            "source_refs": refs,
            "source_gaps": indicator_gaps.get(key, []),
        })
    research_dimensions.append({
        "dimension": key,
        "status": "applicable",
        "summary": dimension_summaries[key],
        "indicators": indicators,
        "source_refs": refs,
        "positive_evidence": [dimension_summaries[key]],
        "counter_evidence": indicator_gaps.get(key, ["已观察到的证据不等于正面结论，仍需持续证伪。"]),
        "source_gaps": indicator_gaps.get(key, []),
    })


financial_periods = []
for r in financial_rows:
    source_ids = list(dict.fromkeys(r["source_refs"].split("/")))
    diluted_shares = {
        "FY2021": 1905.63, "FY2022": 2142.96, "FY2023": 2233.71,
        "FY2024": 2427.33, "FY2025": 2570.966,
    }[r["period"]]
    financial_periods.append({
        "period": r["period"], "period_type": "annual", "currency": "HKD", "unit": "million",
        "scope": "consolidated_group",
        "revenue": r["revenue"], "operating_profit": None,
        "parent_net_income": r["parent_net_income"], "cfo": r["cfo"],
        "capex": round(r["ppe_capex"] + r["intangible_additions"], 3),
        "free_cash_flow": r["free_cash_flow_after_all_capex"],
        "diluted_shares_m": diluted_shares, "diluted_eps": r["diluted_eps"],
        "source_refs": source_ids,
    })
financial_periods.append({
    "period": "2025H1", "period_type": "interim", "currency": "HKD", "unit": "million",
    "scope": "consolidated_group", "revenue": 1456.315, "operating_profit": None,
    "parent_net_income": 102.344, "cfo": 8.910, "capex": 120.088,
    "free_cash_flow": -111.178, "diluted_shares_m": 2484.1, "diluted_eps": 0.0412,
    "source_refs": ["F02"],
})


pe_reported = 2.39 / 0.0775
pe_adjusted_proxy = 2.39 / (231.744 / 2570.966)
combined = {
    "schema_version": "seed.stock-fundamentals-valuation.v2",
    "artifact_type": "stock_fundamentals_valuation",
    "artifact_role": "combined_public_research_snapshot",
    "status": "needs_human_review",
    "generated_at": "2026-07-27T18:45:00+08:00",
    "security": {
        "security_id": "XHKG:03738", "ticker": "03738.HK", "exchange": "HKEX",
        "company_name": "Vobile Group Limited", "company_name_zh": "阜博集团有限公司",
        "listing_type": "ordinary_share", "currency": "HKD", "fiscal_year_end": "31 December",
        "reporting_standard": "HKFRS",
    },
    "as_of": {
        "research_date": "2026-07-27", "price_date": "2026-07-27",
        "price": 2.39, "price_source_ref": "M01",
    },
    "methodology_refs": template["methodology_refs"],
    "source_refs": source_refs,
    "source_boundaries": {
        "facts": "HKEX filing and audited annual-report facts take precedence; every material balance-sheet and income statement claim keeps period, unit, scope and assurance.",
        "reported_claims": "Company presentations, MRR, active assets, NRR, retention and management transcripts remain company-defined claims unless independently corroborated.",
        "interpretations": "Moat, AI-rights opportunity, platform substitution, owner earnings and event attribution are research interpretations.",
        "assumptions": "Static valuation uses HKD price and reported HKD EPS; date-mixed EV/Sales and bond coverage are labelled stress proxies.",
        "source_gaps": "Do not fill missing CAC, product margins, cohort retention, Q1 absolute financials, borrowing costs, maintenance capex or daily short flow with zero.",
        "page_level_evidence": "Critical evidence uses PDF page plus checksum-bound Ghostscript text global approximate line ranges; line_scope is disclosed and must not be mistaken for a human page-local transcription.",
    },
    "evidence_locator_contract": {
        "path": "data/critical-evidence-locators.csv",
        "locator_type": "pdf_page_plus_checksum_bound_document_global_text_lines",
        "line_scope": "document_global_ghostscript_text_line_approximation",
        "limitations": "Line numbers are approximate global text lines in the frozen extraction; use PDF page and checksum for final human verification.",
    },
    "ownership_structure": {
        "controller": "Founder, chairperson and CEO Yangbin Bernard Wang disclosed 415,961,920 shares, about 16.35%, in FY2025.",
        "treasury_share_policy": "Treasury shares are excluded from current issued economic shares; future reissue can restore dilution.",
        "fully_diluted_share_bridge": {
            "as_of": "2026-06-30", "unit": "shares",
            "shares_excluding_treasury": 2592865836,
            "treasury_shares": 1445000,
            "outstanding_options": 165325000,
            "remaining_large_cb_conversion_shares": 248381602,
            "fully_diluted_legal_ceiling": 3006572438,
            "incremental_dilution_pct": 15.96,
            "formula": "2,592,865,836 + 165,325,000 + 248,381,602 = 3,006,572,438",
            "source_refs": ["F05"],
            "data_artifact": "data/fully-diluted-share-bridge.csv",
            "limitations": [
                "Conservative legal ceiling, not treasury-stock-method diluted EPS denominator.",
                "Unissued future scheme capacity is governance overhang but is not counted as currently granted dilution.",
                "Conversion scenario must remove converted debt; non-conversion scenario must retain redemption cash need.",
            ],
        },
    },
    "financial_history": {"periods": financial_periods},
    "returns_on_capital_screen": {
        "status": "unavailable",
        "reason": "Acquisitions, goodwill, R&D capitalization and rapidly changing debt make mechanical ROIC misleading before a normalized invested-capital bridge.",
        "limitations": ["No defensible maintenance/growth split.", "Incremental invested capital is distorted by acquisitions and capitalized development."],
    },
    "segment_data": {
        "status": "applicable",
        "segments": [
            {"name": "Subscription", "FY2025_revenue_hkd_m": 1223.536, "share_pct": 42.6},
            {"name": "Value-added and other", "FY2025_revenue_hkd_m": 1648.825, "share_pct": 57.4},
        ],
        "source_refs": ["F01"],
    },
    "research_dimensions": research_dimensions,
    "earnings_quality_bridge": {
        "period": "FY2025", "currency": "HKD", "unit": "million",
        "reported_group_profit": 211.692, "reported_parent_net_income": 199.312,
        "company_adjusted_group_profit": 231.744,
        "formula": "211.692 + 18.720 + 2.584 + 4.786 - 6.038 = 231.744",
        "disagreement": "Company-adjusted profit is group-scope, not parent-attributable; it cannot be divided by shares as a like-for-like adjusted EPS without a scope bridge.",
        "source_refs": ["F01"],
    },
    "capital_allocation": {
        "status": "reviewed_with_material_refinancing_risk",
        "period": "FY2021 to 2026-06-30",
        "uses": ["capitalized development", "acquisitions", "convertible debt", "placements", "working capital"],
        "per_share_test": "Judge reinvestment only by fully diluted per-share cash economics and bond coverage, not revenue growth alone.",
        "source_refs": ["F01", "F04", "F05"],
    },
    "balance_sheet_quality": {
        "status": "refinancing_stress",
        "currency": "HKD", "unit": "million",
        "net_debt_bridge": {
            "as_of": "2025-12-31", "cash_and_cash_equivalents": 1157.048,
            "restricted_cash": 10.050, "cash_and_restricted_cash": 1167.098,
            "bank_loans": 401.006, "convertible_bond_liabilities": 1608.554,
            "lease_liabilities": 21.925, "reported_net_debt": 842.462,
            "formula": "401.006 + 1,608.554 - 1,157.048 - 10.050 = 842.462",
            "source_refs": ["F01"], "data_artifact": "data/net-debt-bridge.csv",
        },
        "maturity_stress": {
            "as_of": "2026-06-30", "large_cb_remaining_principal_hkd_m": 1458.0,
            "maturity_date": "2026-09-27", "redemption_pct": 101.51,
            "estimated_maturity_cash_hkd_m": 1480.016,
            "fy2025_cash_hkd_m": 1157.048, "date_mixed_gap_hkd_m": -322.968,
            "source_refs": ["F01", "F04", "F05"],
            "limitations": "June cash, bank debt and operating cash are not disclosed in the monthly return; this is a date-mixed stress test, not a liquidity forecast.",
        },
        "convertible_three_path_scenarios": [
            {
                "path": "non_conversion_cash_redemption",
                "debt_treatment": "Retain remaining principal and redeem at about 101.51% at maturity.",
                "share_treatment": "No CB conversion shares; options remain separate.",
                "cash_or_dilution": "Approximate HK$1,480.016m cash need on the June remaining principal.",
            },
            {
                "path": "holder_elected_conversion",
                "debt_treatment": "Converted principal is removed from debt according to bond terms.",
                "share_treatment": "Up to 248,381,602 remaining conversion shares at HK$5.87 as of June.",
                "cash_or_dilution": "Lower redemption cash need but higher share count; conversion is not automatic above strike.",
            },
            {
                "path": "refinance_repurchase_or_restructure",
                "debt_treatment": "Replace, repurchase or amend the outstanding bond before maturity.",
                "share_treatment": "Depends on new instrument, placement, conversion-price or repurchase terms.",
                "cash_or_dilution": "Can trade near-term cash relief for interest cost, collateral, covenant or dilution.",
            },
        ],
    },
    "owner_earnings": {
        "status": "unavailable", "currency": "HKD", "range": [],
        "reason": "Maintenance versus growth development cost, normal working capital, acquisition scope and NCI attribution cannot be defensibly separated.",
        "limitations": [
            "CFO - PPE - intangible additions was -HK$363.449m in FY2025 and is shown only as a conservative cash proxy.",
            "Capitalized development may include both maintenance and growth; expensing all is conservative but not an owner-earnings estimate.",
        ],
    },
    "pe_matrix": [
        {
            "label": "reported_fy", "status": "calculated", "price": 2.39, "currency": "HKD",
            "price_as_of": "2026-07-27", "eps": 0.0775, "eps_period": "FY2025",
            "eps_type": "reported_diluted", "formula": "2.39 / 0.0775",
            "pe": pe_reported, "earnings_yield": 1 / pe_reported,
            "source_refs": ["F01", "M01"], "confidence": "high",
            "limitations": ["Static FY PE; not TTM or forward."],
        },
        {
            "label": "reported_ttm", "status": "unavailable", "price": 2.39, "currency": "HKD",
            "price_as_of": "2026-07-27", "eps": None, "eps_period": "TTM to 2026Q1",
            "eps_type": "reported_diluted", "formula": None, "pe": None,
            "source_refs": ["F01", "F03", "M01"], "confidence": "low",
            "reason": "Q1 update discloses percentage revenue/MRR changes but no absolute profit or EPS.",
        },
        {
            "label": "company_adjusted_group_proxy", "status": "calculated", "price": 2.39, "currency": "HKD",
            "price_as_of": "2026-07-27", "eps": 231.744 / 2570.966, "eps_period": "FY2025",
            "eps_type": "illustrative_group_scope_proxy", "formula": "2.39 / (231.744 / 2570.966)",
            "pe": pe_adjusted_proxy, "earnings_yield": 1 / pe_adjusted_proxy,
            "source_refs": ["F01", "M01"], "confidence": "low",
            "limitations": ["Scope mismatch: adjusted profit is group profit, while shares belong to parent owners. Not a true adjusted PE."],
        },
        {
            "label": "normalized_midcycle", "status": "unavailable", "price": 2.39, "currency": "HKD",
            "price_as_of": "2026-07-27", "eps": None, "eps_period": "midcycle",
            "eps_type": "normalized_diluted", "formula": None, "pe": None,
            "source_refs": ["F01", "M01"], "confidence": "low",
            "reason": "No normalized maintenance development, working-capital and acquisition bridge.",
        },
    ],
    "forward_scenarios": {
        "currency": "HKD", "price_anchor": 2.39,
        "scenarios": [
            {"scenario": "bear", "status": "unavailable", "forecast_eps": None, "implied_pe_at_current_price": None, "reason": "No audited H1 2026 earnings denominator; scenario is described qualitatively in HTML."},
            {"scenario": "base", "status": "unavailable", "forecast_eps": None, "implied_pe_at_current_price": None, "reason": "No audited H1 2026 earnings denominator; scenario is described qualitatively in HTML."},
            {"scenario": "upside", "status": "unavailable", "forecast_eps": None, "implied_pe_at_current_price": None, "reason": "No audited H1 2026 earnings denominator; scenario is described qualitatively in HTML."},
        ],
    },
    "intrinsic_value_scenarios": {
        "currency": "HKD",
        "scenarios": [
            {"scenario": "conservative", "status": "unavailable", "discount_rate_pct": None, "terminal_growth_pct": None, "intrinsic_value_per_share": None, "reason": "Owner earnings unavailable and 2026 bond outcome unresolved."},
            {"scenario": "base", "status": "unavailable", "discount_rate_pct": None, "terminal_growth_pct": None, "intrinsic_value_per_share": None, "reason": "Owner earnings unavailable and 2026 bond outcome unresolved."},
            {"scenario": "high", "status": "unavailable", "discount_rate_pct": None, "terminal_growth_pct": None, "intrinsic_value_per_share": None, "reason": "Owner earnings unavailable and 2026 bond outcome unresolved."},
        ],
    },
    "historical_valuation": {
        "status": "unavailable",
        "metric": "reported_ttm_pe",
        "current": None,
        "five_year_percentile": None,
        "look_ahead_control": "Historical PE requires EPS known on each historical date; current FY2025 EPS must not be backfilled.",
        "peer_comparison": "No normalized pure-play peer set; platform internal tools are substitutes, not valuation comparables.",
        "source_refs": ["M01", "F01"],
        "reason": "No point-in-time filing-availability EPS series has been built.",
    },
    "market_positioning": {
        "status": "below_medium_term_trend_short_position_easing",
        "as_of": "2026-07-27",
        "last_close_hkd": 2.39,
        "sma20_hkd": 2.3620, "sma60_hkd": 2.6340, "sma200_hkd": 4.0233,
        "one_year_return_pct": -36.94, "fifty_two_week_high_hkd": 6.64,
        "fifty_two_week_low_hkd": 2.22,
        "latest_reportable_short_shares": 122802839,
        "approx_pct_of_june_issued": 4.74,
        "interpretation": "Price is near its 20-day mean but below 60/200-day means. Reportable short positions declined from selected January/April observations, so persistent weakness cannot be attributed to rising disclosed shorts alone.",
        "source_refs": ["M01", "S01", "F05"],
        "limitations": ["Technical state describes supply/demand, not support/resistance certainty.", "SFC positions have thresholds and reporting lag."],
    },
    "price_move_attribution": {
        "status": "event_window_monitor",
        "as_of": "2026-07-27",
        "short_term_monitor_location": "report.html#event-monitor and data/event-price-reactions.csv",
        "rule": "T-1 close to T0/T+1/T+5, Hang Seng benchmark, excess return, overlapping events and causal confidence.",
        "source_refs": ["M01", "M02"],
    },
    "moat_evidence": {
        "positive_evidence": [
            "FY2025 revenue reached HK$2.872bn; subscription MRR rose from company-reported US$9m in 2023 to US$15m in 2025.",
            "Active monetizing assets rose from 3.70m at 2024Q4 to 5.24m at 2026Q1 on company definitions.",
            "Rights fingerprints, platform integrations, historical claims and customer workflow can create data and switching frictions.",
        ],
        "counter_evidence": [
            "YouTube is developing internal synthetic-singing and likeness identification within Content ID.",
            "Receivables, capitalized development and goodwill rose faster than cash conversion.",
            "Top-five customers are 40% of revenue and platform policy changes already affected monetization per management.",
        ],
        "missing_tests": [
            "Cohort NRR and gross retention by product/geography.",
            "Win/loss data against platform-native and third-party tools.",
            "Unit gross margin per active asset and incremental cash conversion.",
        ],
    },
    "red_team": [
        {"risk": "platform_internalization", "mechanism": "YouTube/Meta build identification, policy and monetization inside the platform.", "source_refs": ["I01", "I02", "F07"], "invalidation_test": "Platform releases do not reduce asset growth, NRR, pricing or monetization margin for four reporting periods."},
        {"risk": "accounting_growth_without_cash", "mechanism": "Capitalized development, acquisitions and receivable growth defer economic cost and absorb cash.", "source_refs": ["F01", "F02"], "invalidation_test": "CFO and cash proxy converge toward profit while receivable days and capitalization ratio decline."},
        {"risk": "convertible_refinancing", "mechanism": "Share price below HK$5.87 leaves the 2026 bond economically out of the money and shifts risk toward repayment/refinancing.", "source_refs": ["F04", "F05"], "invalidation_test": "Updated cash and committed facilities cover redemption without dilutive or expensive refinancing."},
        {"risk": "concentration_and_platform_rules", "mechanism": "Customer/platform decisions can alter value-added monetization independent of asset count.", "source_refs": ["F01", "F07"], "invalidation_test": "Customer concentration declines and policy changes do not compress recognized revenue per active asset."},
    ],
    "gates": [
        {"gate": "identity_and_source_integrity", "result": "pass_with_scope", "reason": "Security, audited filings, current share count, price snapshot and official source hierarchy are resolved; human page review remains required."},
        {"gate": "circle_of_competence", "result": "provisional", "reason": "Rights-management mechanics are mapped, but platform algorithms, contracts and legal outcomes are not fully observable."},
        {"gate": "business_economics", "result": "mixed", "reason": "Revenue and operating KPI growth are strong; receivables, capitalized development and negative all-in cash proxy weaken economic quality."},
        {"gate": "durable_moat", "result": "inconclusive", "reason": "Data/workflow and customer integration support a moat hypothesis, while platform-native substitutes and policy power remain unrefuted."},
        {"gate": "management_and_capital_allocation", "result": "provisional", "reason": "Management supplies operating KPIs, but acquisition, capitalization, issuance and bond outcomes need full per-share return evidence."},
        {"gate": "owner_earnings", "result": "range_only", "reason": "Only a conservative cash proxy is reproducible; maintenance development and normalized working capital cannot be separated."},
        {"gate": "survival_and_balance_sheet", "result": "provisional", "reason": "Large September 2026 redemption/refinancing need is material; June cash and committed funding are not disclosed in the monthly return."},
        {"gate": "intrinsic_value_and_margin_of_safety", "result": "range_only", "reason": "Static reported FY PE is reproducible, but TTM, normalized earnings and DCF are unavailable."},
        {"gate": "decision_and_disconfirming_evidence", "result": "inconclusive", "reason": "Package is research-ready for human review but not decision-ready; bond coverage, cash conversion and platform substitution remain decisive gaps."},
    ],
    "source_gaps": [
        "2026Q1 absolute revenue, gross margin, profit, cash flow and share denominator.",
        "June/July 2026 cash, bank facilities, covenant headroom and exact convertible redemption funding plan.",
        "Auditable CAC, cohort retention, product/geography margins, asset monetization yield and platform mix.",
        "Maintenance versus growth split for capitalized development and acquired intangibles.",
        "Point-in-time historical PE and normalized public peer set without look-ahead bias.",
        "Borrow fee, lendable inventory and daily free-float-adjusted short interest.",
    ],
    "invalidation_tests": [
        {"id": "INV-01", "claim": "Operating growth converts to owner economics.", "fail_if": "Two periods show profit growth while CFO after all development investment remains materially negative.", "next_evidence": "2026H1 results and cash-flow notes."},
        {"id": "INV-02", "claim": "Bond is manageable without value-destructive financing.", "fail_if": "No committed funding bridge before maturity, or new capital materially dilutes per-share economics.", "next_evidence": "Bond redemption/conversion/refinancing announcements."},
        {"id": "INV-03", "claim": "AI expands the rights-management opportunity more than it empowers substitutes.", "fail_if": "Active assets grow but NRR, revenue per asset or value-added margin declines after platform AI tools roll out.", "next_evidence": "Quarterly KPI and platform-policy updates."},
        {"id": "INV-04", "claim": "Moat rests on data/workflow rather than acquisitions alone.", "fail_if": "Organic revenue/cash returns lag while goodwill and capitalized development continue compounding.", "next_evidence": "Acquisition contribution and organic growth bridge."},
    ],
    "review": {
        "human_review_required": True, "status": "needs_human_review",
        "validator_status": "pending", "reviewer": None, "reviewed_at": None,
        "critical_gaps": [
            "September 2026 convertible repayment/refinancing bridge.",
            "Owner earnings unavailable due maintenance/growth and working-capital uncertainty.",
            "Platform substitution and customer concentration lack independent customer evidence.",
        ],
        "publication_state": "public_research_package_needs_named_human_review",
        "reviewed_for_publication": False,
    },
    "disclaimer": "Public research workflow for evidence audit and scenario monitoring only. This is not investment advice, legal advice, tax advice or accounting advice; no buy/sell/position instruction.",
}

gate_followups = {
    "identity_and_source_integrity": ("无具名人工逐页签字。", "人工复核 18 条关键页码、单位、范围和公式。"),
    "circle_of_competence": ("平台合同、算法与争议规则不公开。", "补客户/权利人访谈与平台条款变化记录。"),
    "business_economics": ("收入增长尚未稳定转成现金。", "核对 2026H1 应收、CFO、资本化研发和有机增长。"),
    "durable_moat": ("平台内部替代与跨平台数据优势均未被证实。", "跟踪平台发布前后 NRR、收入/资产和毛利。"),
    "management_and_capital_allocation": ("并购、发行与债务的每股回报缺口。", "建立承诺兑现和 fully diluted per-share return 台账。"),
    "owner_earnings": ("维护/增长开发与正常营运资本不可分。", "用 H1 附注重建维护投入区间和现金桥。"),
    "survival_and_balance_sheet": ("6 月现金、融资承诺和债券资金桥缺失。", "到期前核验现金、已承诺额度、赎回/转换及新融资。"),
    "intrinsic_value_and_margin_of_safety": ("TTM、正常化 owner earnings 和历史分位数缺失。", "先补可审计分母，再做无前视偏差估值。"),
    "decision_and_disconfirming_evidence": ("三个核心 Gate 仍为 provisional/range_only/inconclusive。", "完成债券、现金转化和平台替代三项反方测试后人工复核。"),
}
for gate in combined["gates"]:
    gate["blocking_gap"], gate["next_test"] = gate_followups[gate["gate"]]

dump_json(ROOT / "combined-artifact.v2.json", combined)
combined_sha = sha(ROOT / "combined-artifact.v2.json")


source_ledger = {
    "schema_version": "seed.company-research-source-ledger.v1",
    "company": {"name_zh": "阜博集团", "name_en": "Vobile Group Limited", "ticker": "03738.HK"},
    "research_snapshot_at": "2026-07-27T18:45:00+08:00",
    "market_data_cutoff": "2026-07-27",
    "policy": {
        "facts": "Audited filing and exchange announcements take precedence.",
        "management_claims": "Company-defined MRR, active assets, NRR, retention and transcript comments remain reported claims.",
        "public_proxies": "Website visits are not used as a primary KPI for this enterprise infrastructure business.",
        "hashes": "Local frozen files have SHA-256; live pages without a frozen copy remain null.",
        "investment_boundary": "Scenario analysis and market-state descriptions are not trading instructions.",
    },
    "sources": source_ledger_sources,
}
dump_json(ROOT / "source-ledger.json", source_ledger)


anchor_specs = [
    ("FUBO-CRIT-001", "fy2025.revenue", "F01", 59, "Revenue 2,872,361", "FY2025", "HKD thousand", "HKD", "consolidated_group", "audited", "directly_reported", 2018, 2048, "Consolidated statement of profit or loss"),
    ("FUBO-CRIT-002", "fy2025.parent_profit", "F01", 59, "Profit attributable to owners 199,312", "FY2025", "HKD thousand", "HKD", "parent_attributable", "audited", "directly_reported", 2018, 2048, "Consolidated statement of profit or loss"),
    ("FUBO-CRIT-003", "fy2025.cfo", "F01", 65, "Net cash from operating activities 69,916", "FY2025", "HKD thousand", "HKD", "consolidated_group", "audited", "directly_reported", 2205, 2240, "Consolidated statement of cash flows"),
    ("FUBO-CRIT-004", "fy2025.intangible_additions", "F01", 113, "Intangible asset additions 427,731", "FY2025", "HKD thousand", "HKD", "consolidated_group", "audited", "directly_reported", 3985, 4000, "Other intangible assets note"),
    ("FUBO-CRIT-005", "fy2025.receivables", "F01", 114, "Trade receivables net 1,753,741", "FY2025", "HKD thousand", "HKD", "consolidated_group", "audited", "1,800,071 - 46,330", 4041, 4050, "Trade receivables note"),
    ("FUBO-CRIT-006", "fy2025.revenue_mix", "F01", 97, "Subscription 1,223,536; value-added 1,648,825", "FY2025", "HKD thousand", "HKD", "revenue_disaggregation", "audited", "sum = 2,872,361", 3420, 3435, "Revenue note"),
    ("FUBO-CRIT-007", "fy2025.goodwill", "F01", 111, "Goodwill 1,315,908", "FY2025", "HKD thousand", "HKD", "consolidated_group", "audited", "directly_reported", 3918, 3945, "Goodwill impairment note"),
    ("FUBO-CRIT-008", "fy2025.five_year_history", "F01", 147, "Five-year revenue and profit summary", "FY2021-FY2025", "HKD thousand", "HKD", "consolidated_group", "audited", "directly_reported", 5133, 5150, "Five-year financial summary"),
    ("FUBO-CRIT-009", "h1_2025.financials", "F02", 12, "H1 revenue 1,456,315; parent profit 102,344", "2025H1", "HKD thousand", "HKD", "consolidated_group", "unaudited", "directly_reported", 994, 1010, "Interim statement of profit or loss"),
    ("FUBO-CRIT-010", "q1_2026.growth", "F03", 1, "Revenue approximately +21%; MRR approximately +29%", "2026Q1", "percent", "HKD", "company_operating_update", "unaudited", "directly_reported", 13, 17, "Unaudited operating data"),
    ("FUBO-CRIT-011", "cb.terms", "F04", 1, "HK$1.6bn; conversion HK$5.87; maturity 27 September 2026", "2025-09-23", "HKD", "HKD", "listed_security", "not_applicable", "directly_reported", 30, 60, "Principal terms of convertible bonds"),
    ("FUBO-CRIT-012", "shares.june_2026", "F05", 2, "Issued shares excluding treasury 2,592,865,836", "2026-06-30", "shares", "not_applicable", "listed_security", "not_applicable", "directly_reported", 20, 30, "Monthly return"),
    ("FUBO-CRIT-013", "cb.remaining_june_2026", "F05", 5, "Remaining principal HK$1.458bn; conversion price HK$5.87", "2026-06-30", "HKD", "HKD", "listed_security", "not_applicable", "directly_reported", 67, 73, "Monthly return convertible table"),
    ("FUBO-CRIT-014", "kpi.active_assets", "F06", 15, "Active assets 4.86m at 2025Q4", "2025Q4", "million assets", "not_applicable", "company_defined_kpi", "unaudited", "directly_reported", 350, 376, "Active monetizing assets chart"),
    ("FUBO-CRIT-015", "kpi.retention", "F06", 21, "NRR 128%; customer retention 98.2%", "FY2025", "percent", "not_applicable", "company_defined_kpi", "unaudited", "directly_reported", 499, 511, "Subscription KPI slide"),
    ("FUBO-CRIT-016", "q1_2026.active_assets", "F07", 1, "Active assets 5.24m; AI assets 16.6%", "2026Q1", "million assets / percent", "not_applicable", "management_claim", "unaudited", "directly_reported", 28, 32, "Management prepared remarks"),
    ("FUBO-CRIT-017", "short.2026_07_17", "S01", 21, "3738 VOBILE GROUP 122,802,839 shares", "2026-07-17", "shares", "HKD", "reportable_short_positions", "not_applicable", "directly_reported", 931, 931, "SFC aggregated reportable short positions"),
    ("FUBO-CRIT-018", "price.2026_07_27", "M01", None, "Close HK$2.39; volume 13,972,000", "2026-07-27", "HKD / shares", "HKD", "listed_security", "not_applicable", "daily chart API snapshot", 1, 1, "Yahoo chart API JSON"),
]

source_sha = {r["id"]: r.get("content_sha256") for r in source_refs}
text_sha = {
    "F01": "ff63b964c0326ec9bed057870d35f8f71ff2e15facc808f5cb27ef55ca9fbc7d",
    "F02": "cb9c1ad6d0653fc736ffcda0549ff41f9e67d0809609147f61fe872035659672",
    "F03": "7c0c892cce955aaa0ac633326eeb645e54ddb785536736557871112577a72191",
    "F04": "f20dd47ac8e3be3481cce59ee3fc52e24a35c7b9807c17cee2d5cdb7f07ebf07",
    "F05": "b61d95dfedc813022d17347f8ac70c3c8f1a4e242783b3bdbf0eb6e18422f776",
    "F06": "1d4d67d559d7d17600912f59347ac93a29a8e1a734a97f829e5bc5c3c0f82315",
    "F07": "cf578a05ed81155d1909e1c647c6a09512723f0b12d65a253f70ceb704faf856",
    "S01": "c2a9eafb331a276274daed305ad07f51774a415b452220bc835cca6c90bdc912",
    "M01": "e7873401f2aa541b476b0c318300c295779eb470a23ff6862a2092b788c3d60f",
}
anchors = []
for spec in anchor_specs:
    (
        evidence_id, claim_id, src, page, source_text, period, unit, currency,
        scope, audit_status, formula, line_start, line_end, section,
    ) = spec
    anchor = {
        "id": evidence_id, "claim_id": claim_id, "source_id": src,
        "document_sha256": source_sha[src], "page": page, "source_text": source_text,
        "period": period, "unit": unit, "currency": currency, "scope": scope,
        "audit_status": audit_status, "formula": formula, "critical": True,
        "price_move_attribution": "not_used_for_causal_price_attribution",
        "review": "machine_checked_needs_human_review",
        "disclaimer": "fact_evidence_not_investment_advice",
        "limitations": "Approximate global extracted-text lines; verify the PDF page and checksum.",
        "text_locator": {
            "locator_type": "pdf_page_plus_checksum_bound_document_global_text_lines",
            "section_or_table": section,
            "text_snapshot_sha256": text_sha[src],
            "page_text_sha256": text_sha[src],
            "page_line_start": line_start,
            "page_line_end": line_end,
            "line_scope": "document_global_ghostscript_text_line_approximation",
            "extraction_provider": "ghostscript-txtwrite",
            "extraction_library": "Ghostscript",
        },
    }
    if src == "M01":
        anchor["limitations"] = "JSON API snapshot has no stable PDF page or human page lines; page is null and line 1 only identifies the frozen single-line JSON."
        anchor["text_locator"]["locator_type"] = "checksum_bound_json_snapshot_single_line_no_page"
        anchor["text_locator"]["line_scope"] = "single_line_minified_json_snapshot_not_human_page_lines"
    anchors.append(anchor)

evidence_index = {
    "schema_version": "seed.company-research-evidence-index.v1",
    "company": "Vobile Group Limited", "security_id": "XHKG:03738",
    "as_of": "2026-07-27", "status": "needs_human_review",
    "combined_artifact": {"path": "combined-artifact.v2.json", "sha256": combined_sha},
    "anchors": anchors,
    "locator_contract": {
        "line_scope": "document_global_ghostscript_text_line_approximation",
        "instructions": "Open the official URL, verify PDF page, then use the approximate frozen-text line range and SHA-256.",
    },
}
dump_json(ROOT / "evidence-index.json", evidence_index)
dump_json(DATA / "critical-evidence-anchors.json", {"schema_version": "seed.company-research-critical-evidence.v1", "anchors": anchors})

locator_fields = [
    "id", "claim_id", "source_id", "document_sha256", "page",
    "section_or_table", "page_line_start", "page_line_end",
    "text_snapshot_sha256", "page_text_sha256", "period", "unit",
    "currency", "scope", "audit_status", "source_text", "formula", "limitations",
]
locator_rows = []
for a in anchors:
    loc = a["text_locator"]
    locator_rows.append({
        "id": a["id"], "claim_id": a["claim_id"], "source_id": a["source_id"],
        "document_sha256": a["document_sha256"], "page": a["page"],
        "section_or_table": loc["section_or_table"],
        "page_line_start": loc["page_line_start"], "page_line_end": loc["page_line_end"],
        "text_snapshot_sha256": loc["text_snapshot_sha256"],
        "page_text_sha256": loc["page_text_sha256"], "period": a["period"],
        "unit": a["unit"], "currency": a["currency"], "scope": a["scope"],
        "audit_status": a["audit_status"], "source_text": a["source_text"],
        "formula": a["formula"], "limitations": a["limitations"],
    })
write_csv(DATA / "critical-evidence-locators.csv", locator_rows, locator_fields)


red_team = {
    "schema_version": "seed.company-research-red-team.v1",
    "company": "Vobile Group Limited", "security_id": "XHKG:03738",
    "reviewer_or_agent": "independent Codex research subagent",
    "reviewed_at": "2026-07-27T18:45:00+08:00",
    "status": "needs_human_review",
    "counter_thesis": "阜博可能把 AI 内容数量增长误当成股东现金收益增长：平台可自建识别与规则层，应收、资本化研发和并购商誉吸收现金，而低股价使 2026 可转债从摊薄风险转成偿付/再融资风险。",
    "strongest_disconfirming_evidence": [
        {"claim_challenged": "AI 内容越多必然越利好阜博。", "evidence": "YouTube 已在 Content ID 内开发合成歌声及肖像识别，并自动识别部分 AI 内容。", "source_refs": ["I01", "I02"], "why_it_matters": "内容增量与平台内生替代可同时发生。"},
        {"claim_challenged": "软件收入增长等于轻资产现金复利。", "evidence": "FY2025 CFO 0.699 亿、无形资产投入 4.277 亿，扣全部投入后的现金代理为 -3.634 亿。", "source_refs": ["F01"], "why_it_matters": "研发资本化与营运资本使利润和现金显著分离。"},
        {"claim_challenged": "可转债高于转股价才有风险。", "evidence": "6 月末剩余本金 14.58 亿、转股价 HK$5.87、到期 2026-09-27；现价 HK$2.39。", "source_refs": ["F04", "F05", "M01"], "why_it_matters": "价外时转股动机弱，风险形态转向现金偿付或再融资。"},
        {"claim_challenged": "高留存足以证明护城河。", "evidence": "公司口径 NRR 128%、客户留存 98.2%，但前五客户占收入 40%，且指标定义未完全披露。", "source_refs": ["F01", "F06"], "why_it_matters": "高留存与集中度、并购口径和平台依赖可以并存。"},
    ],
    "failure_modes": [
        {"name": "platform_internalization", "mechanism": "平台把识别、标签、争议与变现封装在内部工具。", "observable_signals": ["NRR下降", "单资产收入下降", "平台API权限收紧", "增值收入增速落后资产数"]},
        {"name": "cash_conversion_failure", "mechanism": "应收、预付款、资本化研发和并购持续吸收现金。", "observable_signals": ["CFO/利润低位", "应收增速高于收入", "研发资本化率上升", "持续外部融资"]},
        {"name": "refinancing_or_dilution", "mechanism": "价外债券到期需要偿付或新融资；若股价上升则转为稀释。", "observable_signals": ["新配股/供股/债券", "转股价调整", "现金覆盖不足", "每股现金收益下降"]},
        {"name": "goodwill_impairment", "mechanism": "并购增长不达预期导致商誉/无形资产减值。", "observable_signals": ["CGU预测下修", "减值测试折现率上升", "有机增长落后", "商誉继续升高"]},
    ],
    "invalidation_conditions": [
        {"condition": "连续两期 CFO、扣全部开发投入后的现金代理和全摊薄每股现金收益同步改善。", "effect_on_counter_thesis": "削弱会计增长无法转成现金的反方。"},
        {"condition": "到期前以现有现金和已承诺低成本融资覆盖债券，且无重大摊薄。", "effect_on_counter_thesis": "削弱生存/再融资反方。"},
        {"condition": "平台推出内部 AI 权利工具后，公司 NRR、收入/资产和价值增值毛利仍稳定。", "effect_on_counter_thesis": "削弱平台替代反方。"},
    ],
    "unresolved_issues": combined["source_gaps"],
    "next_review": {
        "date": "2026-09-27", "event": "HK$1.6bn convertible bond maturity",
        "minimum_checks": ["remaining principal", "cash balance", "committed facilities", "repurchase/conversion", "new dilution", "covenant headroom"],
        "source_refs": ["F04", "F05"],
    },
    "source_refs": ["F01", "F03", "F04", "F05", "F06", "F07", "I01", "I02", "M01", "S01"],
    "disclaimer": "Independent red-team for evidence audit; not investment advice or named human approval.",
}
dump_json(ROOT / "red-team.json", red_team)


gate_rows = combined["gates"]
write_csv(DATA / "gate-results.csv", gate_rows)
dim_rows = []
for d in research_dimensions:
    for ind in d["indicators"]:
        dim_rows.append({
            "dimension": d["dimension"], "dimension_status": d["status"],
            "indicator": ind["id"], "indicator_status": ind["status"],
            "summary": d["summary"], "source_refs": "/".join(d["source_refs"]),
            "source_gaps": " | ".join(d["source_gaps"]),
        })
write_csv(DATA / "research-dimensions.csv", dim_rows)
write_csv(DATA / "invalidation-tests.csv", combined["invalidation_tests"])


def svg_bar_chart(rows: list[dict], keys: list[tuple[str, str]], title: str, max_value: float | None = None) -> str:
    width, height = 820, 310
    left, right, top, bottom = 70, 20, 42, 58
    plot_w, plot_h = width - left - right, height - top - bottom
    values = [float(r[k]) for r in rows for k, _ in keys if r.get(k) is not None]
    data_max = max(0.0, max(values))
    data_min = min(0.0, min(values))
    chart_max = max_value if max_value is not None else data_max * 1.12
    chart_max = max(chart_max, data_max * 1.02, 1.0)
    chart_min = data_min * 1.15 if data_min < 0 else 0.0
    span = chart_max - chart_min
    zero_y = top + plot_h * chart_max / span

    def y_scale(value: float) -> float:
        return top + plot_h * (chart_max - value) / span

    colors = ["#4f8cff", "#27c2a3", "#f2aa4c", "#e76f8a"]
    group_w = plot_w / len(rows)
    bar_w = group_w / (len(keys) + 1)
    parts = [f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{html.escape(title)}">']
    parts.append(f'<text x="{left}" y="22" class="chart-title">{html.escape(title)}</text>')
    for tick in range(5):
        y = top + plot_h * tick / 4
        value = chart_max - span * tick / 4
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}" class="grid"/>')
        parts.append(f'<text x="{left-8}" y="{y+4:.1f}" text-anchor="end" class="axis">{value:,.0f}</text>')
    parts.append(f'<line x1="{left}" y1="{zero_y:.1f}" x2="{width-right}" y2="{zero_y:.1f}" class="zero-axis"/>')
    for i, row in enumerate(rows):
        gx = left + group_w * i
        for j, (key, label) in enumerate(keys):
            value = row.get(key)
            if value is None:
                continue
            value_float = float(value)
            value_y = y_scale(value_float)
            h = abs(zero_y - value_y)
            x = gx + bar_w * (j + 0.55)
            y = min(zero_y, value_y)
            parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w*.78:.1f}" height="{h:.1f}" rx="3" fill="{colors[j]}"><title>{html.escape(row.get("period",""))} {html.escape(label)}: {value}</title></rect>')
        parts.append(f'<text x="{gx+group_w/2:.1f}" y="{height-30}" text-anchor="middle" class="axis">{html.escape(row.get("period",""))}</text>')
    for j, (_, label) in enumerate(keys):
        x = left + j * 170
        parts.append(f'<rect x="{x}" y="{height-13}" width="10" height="10" fill="{colors[j]}"/><text x="{x+15}" y="{height-4}" class="legend">{html.escape(label)}</text>')
    parts.append("</svg>")
    return "".join(parts)


def svg_line_chart(rows: list[dict], value_key: str, title: str, unit: str) -> str:
    clean = [r for r in rows if r.get(value_key) is not None]
    width, height = 820, 280
    left, right, top, bottom = 70, 24, 42, 48
    plot_w, plot_h = width-left-right, height-top-bottom
    values = [float(r[value_key]) for r in clean]
    lo, hi = min(values), max(values)
    pad = (hi-lo)*0.12 or 1
    lo -= pad
    hi += pad
    pts = []
    for i, r in enumerate(clean):
        x = left + plot_w * i / max(len(clean)-1, 1)
        y = top + plot_h * (hi-float(r[value_key])) / (hi-lo)
        pts.append((x, y, r))
    parts = [f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{html.escape(title)}"><text x="{left}" y="22" class="chart-title">{html.escape(title)}</text>']
    for tick in range(5):
        y = top + plot_h*tick/4
        value = hi-(hi-lo)*tick/4
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}" class="grid"/><text x="{left-8}" y="{y+4:.1f}" text-anchor="end" class="axis">{value:.2f}</text>')
    parts.append('<polyline fill="none" stroke="#4f8cff" stroke-width="3" points="' + " ".join(f"{x:.1f},{y:.1f}" for x,y,_ in pts) + '"/>')
    for x,y,r in pts:
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#27c2a3"><title>{html.escape(r["period"])}: {r[value_key]} {html.escape(unit)}</title></circle><text x="{x:.1f}" y="{height-20}" text-anchor="middle" class="axis">{html.escape(r["period"])}</text>')
    parts.append("</svg>")
    return "".join(parts)


def table(rows: list[dict], columns: list[tuple[str, str]], cls: str = "") -> str:
    head = "".join(f"<th>{html.escape(label)}</th>" for _, label in columns)
    body = []
    for row in rows:
        cells = []
        for key, _ in columns:
            value = row.get(key)
            if value is None:
                text = "—"
            elif isinstance(value, float):
                text = f"{value:,.2f}"
            else:
                text = str(value)
            cells.append(f"<td>{html.escape(text)}</td>")
        body.append("<tr>" + "".join(cells) + "</tr>")
    return f'<div class="table-wrap"><table class="{cls}"><thead><tr>{head}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'


status_legend = [
    {"layer": "发布状态", "term": "needs_human_review", "meaning": "自动校验已通过或待运行，但尚无具名人工签字；可读，不等于决策级。"},
    {"layer": "发布状态", "term": "production_reviewed", "meaning": "只有具名人工完成事实、公式、合规和发布范围复核后才可使用。"},
    {"layer": "维度状态", "term": "applicable", "meaning": "该研究维度适用于公司；不代表评价正面。"},
    {"layer": "维度状态", "term": "unknown", "meaning": "证据不足以判断该维度。"},
    {"layer": "维度状态", "term": "conflicting", "meaning": "主要证据相互冲突，需保留冲突。"},
    {"layer": "维度状态", "term": "not_applicable", "meaning": "该维度经说明后不适用；不等于未研究。"},
    {"layer": "指标状态", "term": "observed", "meaning": "已观察并记录相关证据；不代表指标良好。"},
    {"layer": "指标状态", "term": "not_disclosed", "meaning": "公司或主源未披露，不得填 0。"},
    {"layer": "指标状态", "term": "conflicting", "meaning": "指标口径或来源相互冲突。"},
    {"layer": "指标状态", "term": "not_applicable", "meaning": "该固定指标经说明后不适用；不能用来隐藏缺失披露。"},
    {"layer": "Gate", "term": "pass / pass_with_scope", "meaning": "在明确范围内通过；后者仍有边界。"},
    {"layer": "Gate", "term": "provisional", "meaning": "临时结论：已有可用证据，但重大验证尚未完成。"},
    {"layer": "Gate", "term": "mixed_positive / mixed / inconclusive", "meaning": "偏正但仍有反证 / 正反并存 / 暂不能下结论。"},
    {"layer": "Gate", "term": "range_only", "meaning": "只能给区间或代理，不能给单点精确值。"},
    {"layer": "Gate", "term": "research_ready / research_ready_not_decision_ready", "meaning": "研究材料可用 / 可用于继续研究但不能升级为决策结论。"},
    {"layer": "Gate", "term": "fail / outside_circle / blocked", "meaning": "关键条件失败 / 超出能力圈 / 关键证据阻断后续判断。"},
]

evidence_by_id = {a["id"]: a for a in anchors}
source_by_id = {r["id"]: r for r in source_ledger_sources}
evidence_cards = []
for a in anchors:
    src = source_by_id[a["source_id"]]
    loc = a["text_locator"]
    evidence_cards.append(
        f'<details class="evidence" data-evidence-id="{a["id"]}">'
        f'<summary><code>{a["id"]}</code> · {html.escape(a["claim_id"])} · '
        f'P{a["page"] if a["page"] is not None else "N/A"} · 约行 {loc["page_line_start"]}–{loc["page_line_end"]}</summary>'
        f'<p><strong>记录：</strong>{html.escape(a["source_text"])}；'
        f'<strong>期间/单位/范围：</strong>{html.escape(a["period"])} / {html.escape(a["unit"])} / {html.escape(a["scope"])}</p>'
        f'<p><strong>公式：</strong>{html.escape(str(a["formula"]))}；'
        f'<strong>定位：</strong>{html.escape(loc["line_scope"])}；'
        f'<strong>文档/快照 SHA-256：</strong><code>{a["document_sha256"]}</code></p>'
        f'<p><strong>限制：</strong>{html.escape(a["limitations"])}</p>'
        f'<p><a href="{html.escape(src["url"])}" rel="noreferrer">打开原始文件</a> · '
        f'<a href="data/critical-evidence-locators.csv">下载定位表</a></p></details>'
    )


source_table_rows = []
for s in source_ledger_sources:
    source_table_rows.append({
        "id": s["id"], "tier": s["tier"], "title": s["title"],
        "date": s.get("published_at") or "未披露",
        "link": s["url"], "hash": (s.get("snapshot_sha256") or "live/no frozen hash")[:16],
        "limitations": s["limitations"],
    })


financial_chart = svg_bar_chart(
    financial_rows,
    [("revenue", "收入"), ("gross_profit", "毛利"), ("parent_net_income", "归母利润")],
    "五年收入、毛利与归母利润（百万港元）",
)
cash_chart = svg_bar_chart(
    financial_rows,
    [("cfo", "CFO"), ("intangible_additions", "无形资产投入"), ("free_cash_flow_after_all_capex", "全投入现金代理")],
    "现金转化与开发投入（百万港元）",
    max_value=500,
)
active_chart = svg_line_chart(operating_kpis, "active_assets_m", "公司口径活跃资产趋势", "百万")
short_chart = svg_line_chart(
    [{"period": r["reporting_date"][5:], "short_pct": r["approx_pct_fixed_june_issued"]} for r in short_rows],
    "short_pct", "SFC 可申报空仓占固定 6 月股数比例", "%",
)


report = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>阜博集团 03738.HK｜公司底稿与事件监控</title>
<style>
:root{{--bg:#0b1020;--panel:#121a2e;--panel2:#17223b;--text:#edf3ff;--muted:#9eacc5;--line:#2a3857;--blue:#4f8cff;--green:#27c2a3;--amber:#f2aa4c;--red:#e76f8a;--shadow:0 18px 50px rgba(0,0,0,.24)}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;background:linear-gradient(180deg,#080d19,#0b1020 40%,#0c1324);color:var(--text);font:15px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif}}
a{{color:#82b1ff}}code{{font-size:.9em;word-break:break-all}}.shell{{max-width:1240px;margin:auto;padding:0 22px 80px}}header{{padding:58px 0 36px}}.eyebrow{{color:var(--green);letter-spacing:.14em;text-transform:uppercase;font-weight:700}}h1{{font-size:clamp(34px,6vw,72px);line-height:1.06;margin:.2em 0}}h2{{font-size:30px;margin:0 0 18px}}h3{{font-size:21px;margin:26px 0 12px}}p{{max-width:920px}}.lead{{font-size:20px;color:#c8d4ea;max-width:980px}}.chips{{display:flex;gap:8px;flex-wrap:wrap;margin:20px 0}}.chip,.status{{border:1px solid var(--line);border-radius:999px;padding:5px 10px;background:#10192c;color:#c9d5e9}}.status.amber{{border-color:#775a2d;color:#ffd08a}}.status.red{{border-color:#7c3548;color:#ff9db3}}nav{{position:sticky;top:0;z-index:5;background:rgba(8,13,25,.92);backdrop-filter:blur(12px);border-top:1px solid var(--line);border-bottom:1px solid var(--line);margin:0 -22px;padding:12px 22px;display:flex;gap:16px;overflow:auto;white-space:nowrap}}nav a{{color:#b9c6dd;text-decoration:none}}section{{margin:34px 0;padding:28px;background:rgba(18,26,46,.82);border:1px solid var(--line);border-radius:18px;box-shadow:var(--shadow)}}.grid{{display:grid;grid-template-columns:repeat(12,1fr);gap:16px}}.card{{grid-column:span 4;background:var(--panel2);border:1px solid var(--line);border-radius:14px;padding:18px}}.card.wide{{grid-column:span 6}}.card.full{{grid-column:1/-1}}.metric{{font-size:30px;font-weight:760}}.muted{{color:var(--muted)}}.good{{color:var(--green)}}.warn{{color:var(--amber)}}.bad{{color:var(--red)}}.callout{{border-left:4px solid var(--amber);background:#1d2231;padding:14px 16px;border-radius:8px}}.table-wrap{{overflow:auto;border:1px solid var(--line);border-radius:12px;margin:14px 0}}table{{width:100%;border-collapse:collapse;min-width:760px;background:#10182a}}th,td{{padding:10px 12px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}}th{{position:sticky;top:0;background:#18233b;color:#dfe8f7}}tbody tr:hover{{background:#151f35}}svg{{width:100%;height:auto;background:#0f1729;border:1px solid var(--line);border-radius:12px;margin:12px 0}}.chart-title{{fill:#dce7f9;font-size:15px;font-weight:650}}.grid{{stroke:#263451;stroke-width:1}}.zero-axis{{stroke:#7181a0;stroke-width:1.6}}.axis,.legend{{fill:#8fa0bd;font-size:10px}}details{{border:1px solid var(--line);border-radius:10px;margin:10px 0;background:#10182a}}summary{{cursor:pointer;padding:12px 14px;color:#dbe6f7}}details p{{padding:0 14px}}.two-col{{columns:2;column-gap:28px}}.risk-list li{{margin:8px 0}}.footer{{color:var(--muted);font-size:13px;margin-top:40px}}.source-link{{word-break:break-all}}
@media(max-width:860px){{.card,.card.wide{{grid-column:1/-1}}section{{padding:19px}}.two-col{{columns:1}}h2{{font-size:25px}}}}
</style>
</head>
<body>
<div class="shell">
<header>
  <div class="eyebrow">Vobile Group · 03738.HK · Research snapshot 2026-07-27</div>
  <h1>阜博集团：AI 版权需求<br>与现金、平台和到期债务的赛跑</h1>
  <p class="lead">结论先行：业务 KPI 与收入在增长，但现阶段还不能把它升级为可审计的“高质量现金复利”。真正的近中期闸门不是 AI 内容数量本身，而是 <strong>2026 年 9 月可转债资金桥</strong>、应收与研发资本化后的现金转化，以及平台自建版权工具是否压缩阜博的变现权。</p>
  <div class="chips"><span class="status amber">needs_human_review</span><span class="chip">25 维度</span><span class="chip">50 指标</span><span class="chip">9 gates</span><span class="chip">18 条页码/约行证据</span><span class="chip">5 年财务</span><span class="chip">10 个事件窗口</span></div>
  <div class="callout"><strong>这不是买卖建议。</strong> “provisional”表示临时结论；“applicable”只表示维度适用；“observed”只表示已经观察证据。三者都不代表公司好、估值便宜或具有投资适用性。</div>
</header>
<nav><a href="#summary">摘要</a><a href="#legend">图例</a><a href="#long-term">长期底稿</a><a href="#ai-thesis">AI版权</a><a href="#market-pricing">估值/市场</a><a href="#event-monitor">事件监控</a><a href="#dimensions">25维度</a><a href="#evidence">证据</a><a href="#sources">来源</a></nav>

<section id="summary">
<h2>一页结论</h2>
<div class="grid">
  <div class="card"><div class="muted">FY2025 收入</div><div class="metric">HK$28.72亿</div><div class="good">同比 +19.6%</div></div>
  <div class="card"><div class="muted">FY2025 归母利润</div><div class="metric">HK$1.99亿</div><div>稀释 EPS HK$0.0775</div></div>
  <div class="card"><div class="muted">全投入现金代理</div><div class="metric bad">-HK$3.63亿</div><div>CFO − PPE − 无形资产投入</div></div>
  <div class="card"><div class="muted">现价 / 静态 FY PE</div><div class="metric">2.39 / 30.84×</div><div>不是 TTM 或 forward</div></div>
  <div class="card"><div class="muted">剩余大额可转债</div><div class="metric warn">HK$14.58亿</div><div>2026-09-27 到期；转股价 HK$5.87</div></div>
  <div class="card"><div class="muted">SFC 申报空仓</div><div class="metric">4.74%</div><div>2026-07-17；按 6 月末固定股数估算</div></div>
</div>
<h3>核心判断</h3>
<ul class="risk-list">
  <li><strong>业务是真业务：</strong>收入五年复合增长明显，订阅 MRR、活跃资产和公司口径留存支持客户工作流价值。</li>
  <li><strong>但利润质量还没过关：</strong>应收净额 17.54 亿、资本化开发 3.68 亿、商誉 13.16 亿；FY2025 CFO 仅 0.70 亿。</li>
  <li><strong>AI 是双向变量：</strong>更多生成内容提高识别、归属和许可需求；同一趋势也让 YouTube/Meta 自建识别与政策层，平台可能拿走利润池。</li>
  <li><strong>近期最大非业务风险是债务：</strong>现价显著低于转股价，并非“高于 5.87 自动转股”；持有人是否转换取决于条款和选择，价外时更应审查偿付/再融资。</li>
  <li><strong>小盘弹性来自事件与流动性：</strong>财报、平台规则、版权诉讼、可转债、配售、港股通/指数和空仓变化均可在低流动性下放大波动。</li>
</ul>
</section>

<section id="legend">
<h2>状态图例：先读这个再看表</h2>
<p class="muted">等级不是从差到好的一条直线。发布状态描述复核阶段；维度/指标状态描述证据覆盖；Gate 描述是否满足研究闸门。</p>
{table(status_legend,[("layer","层级"),("term","状态"),("meaning","含义")])}
</section>

<section id="long-term">
<h2>长期公司底稿</h2>
<h3>五年三表主干：增长与现金分离</h3>
{financial_chart}
{table(financial_rows,[("period","期间"),("revenue","收入"),("revenue_yoy_pct","同比%"),("gross_profit","毛利"),("gross_margin_pct","毛利率%"),("parent_net_income","归母利润"),("cfo","CFO"),("intangible_additions","无形资产投入"),("free_cash_flow_after_all_capex","全投入现金代理"),("diluted_eps","稀释EPS")])}
<p class="muted">单位除 EPS/百分比外为百万港元。FY2023 CFO 使用后期报表重分类后的 110.849 百万；不同年报中的利息现金流分类可能造成小差异。全投入现金代理 = CFO − PPE 购置 − 无形资产投入，不等于精确 owner earnings。</p>
{cash_chart}
<div class="callout"><strong>Owner earnings：unavailable。</strong> 不是因为没有公式，而是维护/增长研发、并购范围、NCI 和正常营运资本无法可信拆分。给出漂亮单点 DCF 会制造精确幻觉。</div>

<h3>收入来源：订阅只是 42.6%</h3>
{svg_bar_chart(revenue_mix_rows,[("subscription_hkd_m","订阅"),("value_added_and_other_hkd_m","增值及其他")],"五年收入构成（百万港元)")}
{table(revenue_mix_rows,[("period","期间"),("subscription_hkd_m","订阅"),("subscription_share_pct","订阅占比%"),("value_added_and_other_hkd_m","增值及其他"),("value_added_share_pct","增值占比%")])}
<p>增值及其他服务与内容识别、归因和变现相关，受平台规则、资产量及授权结果影响。FY2025 96.5% 收入按时间确认，<strong>不等于 96.5% 订阅或可续费 ARR</strong>。</p>

<h3>Q1 / H1：能比较什么，不能比较什么</h3>
{table(interim_rows,[("period","期间"),("revenue_hkd_m","收入"),("subscription_hkd_m","订阅"),("value_added_hkd_m","增值"),("gross_profit_hkd_m","毛利"),("parent_profit_hkd_m","归母利润"),("cfo_hkd_m","CFO"),("diluted_eps_hkd","稀释EPS"),("assurance","口径")])}
<p>2025H1 收入同比 +23.3%，归母利润 +146.8%，但 CFO 同比 -19.1%。2025H2 是 FY 减 H1 的派生半年，不是季度。2026Q1 只披露收入约 +21%、中国约 +22%、MRR 约 +29%，没有绝对收入、毛利、利润或现金流，因此不能构造真实 TTM PE。</p>

<h3>产品矩阵与 KPI</h3>
{table(product_rows,[("product_or_platform","产品/平台"),("role","角色"),("signal","研究信号"),("web_traffic_relevance","网站流量相关性"),("source","来源")])}
{active_chart}
{table(operating_kpis,[("period","期间"),("active_assets_m","活跃资产(百万)"),("subscription_mrr_usd_m","订阅MRR(百万美元)"),("ai_asset_share_pct","AI资产占比%"),("source","来源")])}
<p>网站访问量没有用来替代经营 KPI：阜博是企业版权基础设施，不是以网站漏斗直接变现的消费者 App。更相关的趋势是活跃可变现资产、MRR、NRR、客户留存、单资产收入和现金转化；后两项目前披露不足。</p>

<h3>留存、集中与应收</h3>
{table(retention_rows,[("metric","指标"),("value_pct","值%"),("scope","范围"),("source","来源"),("limitation","限制")])}
<p>FY2025 应收净额 17.537 亿港元，约为收入的 61.1%；全年应收增加 3.765 亿。高 NRR 与高应收/客户集中可以同时成立，必须结合回款和平台账期检查。</p>

<h3>研发资本化、商誉与盈利质量</h3>
{table(rd_rows,[("period","期间"),("rd_expense_hkd_m","研发费用"),("capitalized_development_hkd_m","资本化开发"),("total_rd_like_investment_hkd_m","合计"),("capitalized_to_expensed_pct","资本化/费用化%"),("source","来源")])}
{table(earnings_bridge_rows,[("item","项目"),("hkd_m","百万港元"),("operator","公司桥接处理"),("scope","范围"),("source","来源")])}
<p>FY2025 资本化开发高于费用化研发；商誉 13.159 亿，包含 Content Monetization、Content Protection、Particle 与 Pex CGU。公司调整利润 2.317 亿是<strong>集团利润口径</strong>，法定归母 1.993 亿是<strong>母公司股东口径</strong>，不能混做“真实 EPS”。</p>

<h3>债务与完全摊薄</h3>
{table(net_debt_rows,[("item","项目"),("hkd_m","百万港元"),("as_of","日期"),("source","来源"),("note","备注")])}
{table(share_rows,[("item","项目"),("shares","股数"),("as_of","日期"),("treatment","处理"),("source","来源")])}
<div class="callout"><strong>可转债不是自动转股。</strong> 6 月末大额债券剩余本金 14.58 亿，转股价 5.87；现价 2.39。若不转股，到期按约 101.51% 赎回，粗算需约 14.80 亿现金。用 2025 年底现金 11.57 亿对比会有约 3.23 亿缺口，但日期混合且不知道 6 月现金、银行额度和其后经营现金，只能叫压力测试。</div>
{table([
{"path":"未转股现金赎回","debt":"保留债务并按约101.51%赎回","shares":"不新增CB转股股数；期权另计","effect":"按6月本金粗算约需HK$14.80亿现金"},
{"path":"持有人选择转股","debt":"按条款移除已转换本金","shares":"6月剩余最多248,381,602股，转股价HK$5.87","effect":"降低赎回现金，但增加股数；不是价格高于转股价就自动转换"},
{"path":"再融资/回购/重组","debt":"以新债、回购或条款修改替换","shares":"取决于新工具、配售及转股价条款","effect":"短期缓解现金，可换来利息、担保、契约或摊薄成本"},
],[("path","路径"),("debt","债务处理"),("shares","股数处理"),("effect","现金/摊薄影响")])}
</section>

<section id="ai-thesis">
<h2>AI 版权应用：增长机会还是被平台包住？</h2>
<div class="grid">
<div class="card wide"><h3>利好链</h3><p>AI 生成内容增多 → 侵权/授权/数字替身争议增多 → 识别、证据、权利归属与许可需求增加 → 活跃资产、MRR 和增值变现扩大。模型更强、推理更便宜可加速内容供给，阜博不需承担前沿模型训练成本。</p></div>
<div class="card wide"><h3>利空链</h3><p>平台拥有上传入口、Content ID、流量和争议规则 → 平台内部自动检测和 C2PA 标签强化 → 第三方工具被压价、API 权限收紧或只能做后台服务 → 资产量增长但单资产收入、毛利和现金转化下降。</p></div>
</div>
<h3>模型降价/能力提升的净效应</h3>
<p><strong>短期偏需求利好、长期取决于议价权。</strong> 降价增加生成内容供给和权利冲突，扩大需要治理的“面”；但也降低识别模型门槛，让平台和竞争者更容易自建。最终必须观察 <code>NRR × 单资产收入 × 毛利 × CFO</code>，不能只观察 AI 资产占比。</p>
<h3>美国与海外映射</h3>
{table(mapping_rows,[("entity","实体"),("market","市场"),("mapping_type","映射类型"),("relationship","与阜博关系"),("source","来源")])}
<p class="muted">YouTube Content ID 与 Meta Rights Manager 是下游平台内部替代，不是同经济敞口的上市公司；C2PA 是相邻标准；Veritone 仅为主题 peer。映射不能当等价替代或估值可比。</p>
<h3>未来三种路径</h3>
{table([
{"scenario":"压力","mechanism":"平台内建识别/争议闭环，价值增值规则收紧；债券再融资抬升资本成本。","observable":"NRR/单资产收入下滑、CFO继续弱、新融资摊薄。"},
{"scenario":"中性","mechanism":"订阅与资产保持增长，但平台拿走部分利润池；现金转化缓慢改善。","observable":"收入约20%增长、毛利稳定、CFO改善但低于利润。"},
{"scenario":"向上","mechanism":"AI权利标准与许可市场扩张，阜博数据/工作流成为跨平台中间层。","observable":"NRR稳定高位、单资产收入和毛利上升、全摊薄每股现金收益转正。"},
],[("scenario","情景"),("mechanism","机制"),("observable","必须观察")])}
</section>

<section id="market-pricing">
<h2>估值与宏观拉长的市场状态</h2>
<div class="grid">
<div class="card"><div class="muted">收盘价</div><div class="metric">HK$2.39</div><div>2026-07-27</div></div>
<div class="card"><div class="muted">20 / 60 / 200 日均线</div><div class="metric">2.36 / 2.63 / 4.02</div><div>描述趋势，不是买卖点</div></div>
<div class="card"><div class="muted">52 周区间</div><div class="metric">2.22—6.64</div><div>当前接近区间下沿</div></div>
</div>
<h3>PE 分母矩阵</h3>
{table([
{"denominator":"FY2025 reported diluted","eps":"0.0775","pe":"30.84×","status":"calculated","limitation":"静态 FY，不是 TTM"},
{"denominator":"TTM to 2026Q1","eps":"—","pe":"—","status":"unavailable","limitation":"Q1 无利润/EPS"},
{"denominator":"company adjusted group proxy","eps":"0.0901","pe":"26.51×","status":"illustrative only","limitation":"集团利润/母公司股数范围错配"},
{"denominator":"normalized / owner earnings","eps":"—","pe":"—","status":"unavailable","limitation":"维护研发和正常营运资本不可审计"},
],[("denominator","分母"),("eps","EPS"),("pe","PE"),("status","状态"),("limitation","限制")])}
<p><strong>高估/低估空间暂不输出。</strong> 当前 FY PE 可复算，但没有 TTM、forward、owner earnings 或无前视偏差历史分位数。价格低于 200 日均线和 52 周高点只能说明中期趋势弱、历史套牢供给可能存在，不能推出“低估”。</p>
<h3>为什么近期在 2.2—2.5 一带，而不是此前的 4？</h3>
<p>截至本快照，价格靠近 20 日均线但显著低于 60/200 日均线；过去一年下跌约 36.9%。已披露空仓从 4 月样本 5.92% 回落至 4.74%，因此不能把弱势简单归因于空头加仓。更一致的解释是：2025 年的 AI 版权增长预期已部分反转，而 2026Q1 只有增长百分比，现金/利润和 9 月债券资金桥尚未被正式财报验证。</p>
{short_chart}
{table(short_rows,[("reporting_date","SFC日期"),("reportable_short_shares","申报空仓股数"),("approx_pct_fixed_june_issued","占6月固定股数%"),("market_value_hkd_m","市值百万港元"),("source","来源")])}
<p class="muted">SFC 只覆盖超过法定阈值的申报净空仓，且有发布滞后和对冲用途；不是全部 short interest，也不是当日卖空成交。</p>
</section>

<section id="event-monitor">
<h2>短期事件监控：不只看最近 20 日</h2>
<p>每个已发生事件使用公告后的首个交易日，以 T−1 收盘为基准计算 T0/T+1/T+5，并列出恒指 T0。窗口重叠、行业与宏观因素会污染因果，因此统一标记低至中等因果置信。</p>
{table(event_rows,[("announcement_date","公告日"),("first_trading_date","首交易日"),("event","事件"),("category","类别"),("t0_return_pct","T0%"),("t1_return_pct","T+1%"),("t5_return_pct","T+5%"),("hsi_t0_return_pct","恒指T0%"),("t0_excess_vs_hsi_pct","T0超额%"),("causal_confidence","因果置信")])}
<h3>未来容易放大小盘波动的事件</h3>
<ul class="two-col risk-list">
<li>可转债赎回、回购、转换、转股价调整或新融资</li><li>中报/年报中的 CFO、应收、资本化研发与减值</li>
<li>YouTube/Meta 版权与 AI 内容规则改变</li><li>版权诉讼、数字替身和 AI 训练法规</li>
<li>大客户合同、平台 API、计费或结算变化</li><li>并购、商誉减值与关键高管变动</li>
<li>港股通资格、指数调入调出及被动资金</li><li>配股、期权行权、库存股再发行与限售解禁</li>
<li>流动性、借券成本、空仓集中和 margin call</li><li>美元/港元利率、风险偏好和 AI 应用主题轮动</li>
</ul>
<p><strong>港股通：</strong>2026-07-27 冻结的 SSE/SZSE 官方南向名单均记录 03738 为 eligible。资格不保证资金流入，也不等于经纪商/账户一定可交易。</p>
</section>

<section id="dimensions">
<h2>25 维度 × 50 指标与九道 Gate</h2>
<p class="muted">所有 25 个维度均为 applicable；这只代表适用且已观察证据，不代表通过。每个维度下固定两个指标，共 50 个。</p>
{table(dim_rows,[("dimension","维度"),("dimension_status","维度状态"),("indicator","指标"),("indicator_status","指标状态"),("summary","结论"),("source_refs","来源"),("source_gaps","缺口")])}
<h3>九道 Gate</h3>
{table(gate_rows,[("gate","Gate"),("result","结果"),("reason","理由"),("blocking_gap","阻断缺口"),("next_test","下一验证")])}
</section>

<section>
<h2>失效条件与下一证据</h2>
{table(combined["invalidation_tests"],[("id","ID"),("claim","待验证主张"),("fail_if","失效条件"),("next_evidence","下一证据")])}
<div class="callout">本报告最接近“决策升级”的路径不是再加一个目标价，而是：补齐 2026H1 现金流与应收、形成可转债资金桥、按全摊薄股数重建每股现金收益，再用平台规则变化做前后对照。</div>
</section>

<section id="evidence">
<h2>关键证据抽屉：页码 + 约行 + SHA-256</h2>
<p>行号是冻结 Ghostscript 文本的<strong>全局约行</strong>，不是 PDF 页内行；核验顺序是打开原始 PDF → 到指定页 → 对照短文本 → 必要时用校验和确认文件版本。</p>
{"".join(evidence_cards)}
</section>

<section id="sources">
<h2>来源账本</h2>
<div class="table-wrap"><table><thead><tr><th>ID</th><th>层级</th><th>标题/原始链接</th><th>发布日期</th><th>快照哈希前16位</th><th>限制</th></tr></thead><tbody>
{"".join(f'<tr><td>{html.escape(r["id"])}</td><td>{html.escape(r["tier"])}</td><td><a class="source-link" href="{html.escape(r["link"])}" rel="noreferrer">{html.escape(r["title"])}</a></td><td>{html.escape(str(r["date"]))}</td><td><code>{html.escape(r["hash"])}</code></td><td>{html.escape(r["limitations"])}</td></tr>' for r in source_table_rows)}
</tbody></table></div>
</section>

<section>
<h2>方法论：后续可套用</h2>
<ol>
<li><strong>身份与主源：</strong>先冻结证券、报告主体、期间、币种、股数、价格日与官方原文。</li>
<li><strong>五年三表：</strong>收入→利润→CFO→全部维护/增长投入；重分类和范围变化单独记录。</li>
<li><strong>业务 KPI：</strong>把客户、订阅、资产、MRR、留存与收入/现金连接，未披露项保持 unknown。</li>
<li><strong>每股桥：</strong>基本股、库存股、期权、奖励、可转债与未来方案额度分开；债转股必须与债务移除配对。</li>
<li><strong>估值矩阵：</strong>reported FY、TTM、adjusted、forward、normalized 分母并列；不可审计就 unavailable。</li>
<li><strong>行业双向性：</strong>技术进步同时检查需求扩张、成本下降、进入壁垒下降和上游平台打包。</li>
<li><strong>事件监控：</strong>不用 20 日形态代替事件；记录公告时刻、首交易日、T0/T+1/T+5、基准与重叠事件。</li>
<li><strong>反方与失效：</strong>先写最强替代解释，再明确下一条什么证据会推翻当前判断。</li>
<li><strong>九 Gate 发布：</strong>机器通过不等于人工通过；没有具名 reviewer 就保持 needs_human_review。</li>
</ol>
</section>

<p class="footer">Research snapshot: 2026-07-27 · Combined artifact SHA-256: <code>{combined_sha}</code><br>本报告用于证据审计与情景监控，不构成投资、法律、税务或会计建议。</p>
</div>
</body>
</html>
"""
(ROOT / "report.html").write_text(report, encoding="utf-8")


readme = f"""# 阜博集团（03738.HK）公司研究包

状态：`needs_human_review`。自动 validator 通过只代表结构、公式与公开证据链接契约通过，不代表具名人工批准或投资结论。

入口：

- [交互式报告](./report.html)
- [v2 combined artifact](./combined-artifact.v2.json)
- [来源账本](./source-ledger.json)
- [关键证据索引](./evidence-index.json)
- [独立 red-team](./red-team.json)
- [validator 结果](./validator-results.json)

报告公开展示：

- 25 个研究维度、50 个固定指标、9 道 Gate 与完整状态图例；
- FY2021–FY2025 财务、2025H1/派生 H2、2026Q1 经营更新边界；
- 收入/利润来源、MRR、活跃资产、留存、客户集中、应收、资本化研发、商誉；
- owner earnings 缺口、静态 PE 分母矩阵、净债务及完全摊薄股数桥；
- 2026-09 可转债偿付/转股双情景；
- AI 版权应用、平台替代、海外映射、港股通、空仓与小盘风险；
- 十个已发生事件的 T0/T+1/T+5 价格窗口；
- 页码、冻结文本全局约行、原始链接和 SHA-256 证据抽屉。

关键边界：

- `provisional` 是临时结论，不是通过；
- `applicable` 只是维度适用，不是评价正面；
- `observed` 只是已经观察证据，不是指标优秀；
- 网站流量不是该 B2B 版权基础设施业务的首要经营代理；
- 全部金额默认百万港元，除非表中另列；
- 无具名人工 reviewer，不能升级为 `production_reviewed`。

Combined artifact checksum: `{combined_sha}`
"""
(ROOT / "README.md").write_text(readme, encoding="utf-8")


methodology = """# 上市公司长期底稿 + 短期事件监控模板

## 两个入口

1. 公司长期底稿：身份、五年三表、收入/利润来源、客户/供应商、护城河、治理、每股经济、估值和失效条件。
2. 短期事件监控：已发生/待发生事件、公告时刻、首交易日、T0/T+1/T+5、基准、超额、重叠事件和因果置信。

## 不可省略的桥

- 报表利润 → 归母利润 → 公司调整口径 → 研究调整口径；
- CFO → 营运资本 → 维护/增长投入 → owner earnings；
- 期末基本股 → 库存股 → 期权/奖励 → 可转债 → fully diluted；
- 未转债务偿付情景与转股稀释情景必须分别计算；
- reported FY / TTM / adjusted / forward / normalized PE 必须并列，缺失保持 unavailable；
- 历史估值必须使用当时已经公开的 EPS，禁止用今天财报回填历史。

## 技术/AI 公司额外检查

- 模型进步的四条路径：需求扩张、成本下降、进入壁垒下降、上游平台打包；
- 研发费用化与资本化并看；
- 平台依赖与会计供应商集中度分开；
- 消费 App 看下载/排名/MAU/付费，B2B 基础设施优先看 MRR、NRR、客户留存、资产量、单资产收入和现金回款；
- 网站访问量只有在与获客/使用/付费有明确机制时才作为辅助信号。

## 状态语义

- applicable ≠ positive
- observed ≠ good
- provisional ≠ pass
- validator passed ≠ human reviewed
"""
(ROOT / "methodology.md").write_text(methodology, encoding="utf-8")

print(f"built {ROOT}")
print(f"combined_sha256={combined_sha}")
