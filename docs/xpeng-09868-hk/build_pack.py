#!/usr/bin/env python3
# ruff: noqa: E501
"""Build the public XPeng 09868.HK evidence-linked research package."""

from __future__ import annotations

import copy
import csv
import hashlib
import html
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
DATA = ROOT / "data"
DATA.mkdir(parents=True, exist_ok=True)

RESEARCH_DATE = "2026-08-10"
PRICE_DATE = "2026-08-07"
PRICE_HKD = 46.64
HKD_CNY = 0.86601
BASIC_SHARES = 1_916_096_781
RSU_SHARES = 63_496_420
DIDI_CONTINGENT_SHARES = 28_331_126
FD_SHARES = BASIC_SHARES + RSU_SHARES + DIDI_CONTINGENT_SHARES


def implied_price_from_ev_sales(
    revenue_rmb_bn: float,
    ev_sales: float,
    net_cash_rmb_bn: float,
) -> float:
    """Convert an EV/sales scenario into an HKD price per fully diluted share."""
    equity_value_hkd_bn = (revenue_rmb_bn * ev_sales + net_cash_rmb_bn) / HKD_CNY
    return round(equity_value_hkd_bn * 1_000_000_000 / FD_SHARES, 2)


THREE_MONTH_SCENARIOS = [
    {
        "horizon": "3个月",
        "case": "bear",
        "probability_pct": 35,
        "price_low_hkd": 32.0,
        "price_high_hkd": 40.0,
        "return_low_pct": round((32.0 / PRICE_HKD - 1) * 100, 1),
        "return_high_pct": round((40.0 / PRICE_HKD - 1) * 100, 1),
        "trigger": "Q2 vehicle margin低于12%、亏损仍大或Q3指引/交付失速；弱势趋势延续。",
        "basis": "事件与情绪区间；不是DCF。",
    },
    {
        "horizon": "3个月",
        "case": "base",
        "probability_pct": 45,
        "price_low_hkd": 42.0,
        "price_high_hkd": 55.0,
        "return_low_pct": round((42.0 / PRICE_HKD - 1) * 100, 1),
        "return_high_pct": round((55.0 / PRICE_HKD - 1) * 100, 1),
        "trigger": "Q2收入落在指引、亏损环比收窄，但Q3同比与现金质量仍未完全确认。",
        "basis": "当前价附近的财报后再定价区间。",
    },
    {
        "horizon": "3个月",
        "case": "bull",
        "probability_pct": 20,
        "price_low_hkd": 60.0,
        "price_high_hkd": 75.0,
        "return_low_pct": round((60.0 / PRICE_HKD - 1) * 100, 1),
        "return_high_pct": round((75.0 / PRICE_HKD - 1) * 100, 1),
        "trigger": "Q2 margin/亏损/现金同时优于门槛，8—10月交付重新加速并触发空头回补。",
        "basis": "盈利拐点预期重建；仍低于历史高位。",
    },
]

TWELVE_MONTH_SCENARIOS = [
    {
        "horizon": "12个月",
        "case": "bear",
        "probability_pct": 35,
        "revenue_low_rmb_bn": 78.0,
        "revenue_high_rmb_bn": 82.0,
        "ev_sales_low": 0.45,
        "ev_sales_high": 0.60,
        "net_cash_low_rmb_bn": 13.0,
        "net_cash_high_rmb_bn": 16.0,
        "price_low_hkd": implied_price_from_ev_sales(78.0, 0.45, 13.0),
        "price_high_hkd": implied_price_from_ev_sales(82.0, 0.60, 16.0),
        "trigger": "产品修复不持续、vehicle margin回落、费用和库存吞噬现金，扭亏再次后移。",
        "basis": "下一12个月收入×EV/Sales＋净现金，再除已知充分摊薄股数。",
    },
    {
        "horizon": "12个月",
        "case": "base",
        "probability_pct": 45,
        "revenue_low_rmb_bn": 90.0,
        "revenue_high_rmb_bn": 100.0,
        "ev_sales_low": 0.75,
        "ev_sales_high": 0.90,
        "net_cash_low_rmb_bn": 18.0,
        "net_cash_high_rmb_bn": 22.0,
        "price_low_hkd": implied_price_from_ev_sales(90.0, 0.75, 18.0),
        "price_high_hkd": implied_price_from_ev_sales(100.0, 0.90, 22.0),
        "trigger": "交付恢复同比增长，vehicle margin稳定在12%—14%，亏损收窄且现金大致稳定。",
        "basis": "下一12个月收入×EV/Sales＋净现金，再除已知充分摊薄股数。",
    },
    {
        "horizon": "12个月",
        "case": "bull",
        "probability_pct": 20,
        "revenue_low_rmb_bn": 105.0,
        "revenue_high_rmb_bn": 120.0,
        "ev_sales_low": 1.00,
        "ev_sales_high": 1.15,
        "net_cash_low_rmb_bn": 22.0,
        "net_cash_high_rmb_bn": 28.0,
        "price_low_hkd": implied_price_from_ev_sales(105.0, 1.00, 22.0),
        "price_high_hkd": implied_price_from_ev_sales(120.0, 1.15, 28.0),
        "trigger": "多车型与海外/大众技术收入共同放量，vehicle margin不低于14%，季度盈利和owner earnings可持续。",
        "basis": "盈利拐点确认后的成长型EV/Sales区间；不是历史高点回归假设。",
    },
]

for row in TWELVE_MONTH_SCENARIOS:
    row["return_low_pct"] = round((row["price_low_hkd"] / PRICE_HKD - 1) * 100, 1)
    row["return_high_pct"] = round((row["price_high_hkd"] / PRICE_HKD - 1) * 100, 1)

THREE_MONTH_EXPECTED_MIDPOINT = round(
    sum(((row["price_low_hkd"] + row["price_high_hkd"]) / 2) * row["probability_pct"] / 100 for row in THREE_MONTH_SCENARIOS),
    2,
)
TWELVE_MONTH_EXPECTED_MIDPOINT = round(
    sum(((row["price_low_hkd"] + row["price_high_hkd"]) / 2) * row["probability_pct"] / 100 for row in TWELVE_MONTH_SCENARIOS),
    2,
)

MARKET_STATE = [
    {"metric": "最新收盘", "value": 46.64, "unit": "HKD", "as_of": "2026-08-07", "comparison": "—"},
    {"metric": "900日最高收盘", "value": 108.50, "unit": "HKD", "as_of": "2025-11-11", "comparison": "至今-57.0%"},
    {"metric": "5日收益", "value": -7.83, "unit": "%", "as_of": "2026-08-07", "comparison": "HSTECH +0.60%"},
    {"metric": "20日收益", "value": -9.00, "unit": "%", "as_of": "2026-08-07", "comparison": "HSTECH +2.89%"},
    {"metric": "60日收益", "value": -25.50, "unit": "%", "as_of": "2026-08-07", "comparison": "HSTECH -4.19%"},
    {"metric": "最新成交量/20日均量", "value": 0.81, "unit": "x", "as_of": "2026-08-07", "comparison": "12.29m / 15.18m"},
]

CONSENSUS_DIAGNOSTICS = {
    "as_of": "2026-07-31",
    "security": "NYSE:XPEV ADS",
    "source_provider": "StockAnalysis page citing S&P Global",
    "analyst_count": 25,
    "target_low_usd": 15.04,
    "target_average_usd": 22.04,
    "target_median_usd": 22.05,
    "target_high_usd": 28.11,
    "use": "Secondary sentiment cross-check only; not Seed fair value and not mechanically converted into the HK scenario bands.",
}


def dump_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict], fields: list[str] | None = None) -> None:
    if fields is None:
        fields = list(dict.fromkeys(key for row in rows for key in row))
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source(
    source_id: str,
    tier: str,
    source_type: str,
    title: str,
    url: str,
    published_at: str,
    period: str,
    audit_status: str,
    scope: str,
    covers: list[str],
    content_sha256: str,
) -> dict:
    return {
        "id": source_id,
        "tier": tier,
        "source_type": source_type,
        "title": title,
        "url": url,
        "published_at_status": "known",
        "published_at": published_at,
        "accessed_at": RESEARCH_DATE,
        "period": period,
        "audit_status": audit_status,
        "scope": scope,
        "covers": covers,
        "content_sha256": content_sha256,
    }


SOURCES = [
    source(
        "F01",
        "A",
        "sec_filing",
        "XPeng Inc. 2025 Form 20-F",
        "https://www.sec.gov/Archives/edgar/data/1810997/000119312526157849/d36361d20f.htm",
        "2026-04-16",
        "FY2025",
        "audited",
        "consolidated_group",
        [
            "financial_statements",
            "business",
            "revenue_mix",
            "cash_flow",
            "working_capital",
            "share_capital",
            "governance",
            "customers",
            "suppliers",
        ],
        "67830eaad667ed28361941559c87db8e82d3c8251dcf350680c3ddb82bbdfc4f",
    ),
    source(
        "F02",
        "A",
        "sec_xbrl",
        "SEC Companyfacts — XPeng Inc.",
        "https://data.sec.gov/api/xbrl/companyfacts/CIK0001810997.json",
        "2026-04-16",
        "FY2021-FY2025",
        "audited",
        "consolidated_group_xbrl_facts",
        ["five_year_financials", "cash_flow", "research_expense"],
        "ed50d828d7069636d4de76e3428f53dda39ea85510b200373227dcdefff361f8",
    ),
    source(
        "F03",
        "A",
        "sec_filing",
        "XPeng Q1 2026 unaudited financial results",
        "https://www.sec.gov/Archives/edgar/data/1810997/000119312526243143/d139430d6k.htm",
        "2026-05-28",
        "2026Q1",
        "unaudited",
        "consolidated_group",
        [
            "quarterly_financials",
            "deliveries",
            "margin",
            "cash",
            "inventory",
            "guidance",
            "management_comments",
        ],
        "2a118814890dc969b0858f129a22bb272f27d00af769d7ce7630ae671e682f8d",
    ),
    source(
        "F04",
        "A",
        "sec_filing",
        "XPeng Q2 2026 vehicle delivery results",
        "https://www.sec.gov/Archives/edgar/data/1810997/000119312526293394/d114872d6k.htm",
        "2026-07-02",
        "2026Q2",
        "unaudited",
        "company_operating_kpi",
        ["deliveries", "products", "q2_guidance_check"],
        "cb189cb10e5fdfd896efb517cbfaff93c74229be1462d358dcca232c27691ab0",
    ),
    source(
        "F05",
        "A",
        "hkex_monthly_return",
        "XPeng Monthly Return for June 2026",
        "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0707/2026070701078.pdf",
        "2026-07-07",
        "2026-06-30",
        "not_applicable",
        "listed_security",
        ["issued_shares", "public_float_compliance", "share_awards"],
        "059e348df0ed5c5cc0d90cb2c751b049a323e6a7dd399feddec828f0b318dfb7",
    ),
    source(
        "F06",
        "A",
        "hkex_announcement",
        "XPeng April 2026 grant of restricted share units",
        "https://www.hkexnews.hk/listedco/listconews/sehk/2026/0417/2026041701171.pdf",
        "2026-04-17",
        "2026-04-17",
        "not_applicable",
        "listed_security",
        ["share_awards", "vesting", "dilution", "performance_conditions"],
        "703fb4fd83d4817bde71cf7711dd2c8347339e2b46ad7bb4824811abd5eb904f",
    ),
    source(
        "F07",
        "A",
        "regulatory_dataset",
        "SFC reportable short positions — 31 July 2026",
        "https://www.sfc.hk/-/media/EN/pdf/spr/2026/07/31/Short_Position_Reporting_Aggregated_Data_20260731.csv",
        "2026-08-07",
        "2026-07-31",
        "not_applicable",
        "reportable_short_positions",
        ["short_position"],
        "b4a6ccc0aacb65283adb725a4a2d58a22f8df22bf4c3adca83dfc617b0243e2c",
    ),
    source(
        "F08",
        "A",
        "hkex_announcement",
        "XPeng Q1 2025 unaudited financial results and Q2 guidance",
        "https://www1.hkexnews.hk/listedco/listconews/sehk/2025/0521/2025052100660.pdf",
        "2025-05-21",
        "2025Q1_and_2025Q2_guidance",
        "unaudited",
        "consolidated_group",
        ["historical_guidance", "deliveries", "revenue", "margin"],
        "916c9be66a2a75d47b7968651a33429ee57d37f2636b8ceb23540325b1ba4646",
    ),
    source(
        "F09",
        "A",
        "hkex_announcement",
        "XPeng Q2 2025 unaudited financial results",
        "https://www1.hkexnews.hk/listedco/listconews/sehk/2025/0819/2025081900612.pdf",
        "2025-08-19",
        "2025Q2",
        "unaudited",
        "consolidated_group",
        ["historical_results", "deliveries", "revenue", "margin", "cash", "guidance"],
        "fcdb9db5d0a59149657e09eb094439f23144563dd4e9eebdd96467da1392323e",
    ),
    source(
        "F10",
        "A",
        "hkex_announcement",
        "XPeng controlling shareholder shareholding increase",
        "https://www1.hkexnews.hk/listedco/listconews/sehk/2025/0821/2025082101163.pdf",
        "2025-08-21",
        "2025-08-20_to_2025-08-21",
        "not_applicable",
        "controlling_shareholder_transaction",
        ["insider_action", "shareholding", "event_attribution"],
        "96dd421e3f115ffda12d0e81405e01a2d55274be4e497823d81276e22ba309df",
    ),
    source(
        "F11",
        "A",
        "hkex_announcement",
        "XPeng August 2025 delivery results and New P7 launch",
        "https://www1.hkexnews.hk/listedco/listconews/sehk/2025/0901/2025090100103.pdf",
        "2025-09-01",
        "2025-08",
        "not_applicable",
        "company_operating_kpi",
        ["deliveries", "new_p7_launch", "event_attribution"],
        "249a8bdff2c08a568c4a7feed873b5ffdc3e4610cac58a61d8906f0863a10d54",
    ),
    source(
        "F12",
        "A",
        "hkex_announcement",
        "XPeng July 2026 vehicle delivery results",
        "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0803/2026080303094.pdf",
        "2026-08-03",
        "2026-07",
        "not_applicable",
        "company_operating_kpi",
        ["deliveries", "products", "q3_growth_check"],
        "22eaa67ac177213417162023835df8cb2ef8a7c4e117987843e773eff9d6e91f",
    ),
    source(
        "F13",
        "A",
        "hkex_announcement",
        "XPeng notice of board meeting for Q2 2026 results",
        "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0804/2026080401150.pdf",
        "2026-08-04",
        "2026Q2_results_date",
        "not_applicable",
        "listed_security",
        ["earnings_date", "board_meeting", "conference_call"],
        "7a85eb7b17d8f7b2cdd828499563f75e1e73ad7309f6fb047ddf3db62278cc75",
    ),
    source(
        "F14",
        "A",
        "issuer_distributed_press_release",
        "XPeng July 2026 delivery release dated August 1",
        "https://www.prnewswire.com/news-releases/xpeng-announces-vehicle-delivery-results-for-july-2026-302840496.html",
        "2026-08-01",
        "2026-07",
        "not_applicable",
        "company_operating_kpi",
        ["delivery_release_date", "deliveries", "products"],
        "3979bb9b51692e46c297760c7e7754d5c7a332ce9f7bf9baac4233e7176f1f2d",
    ),
    source(
        "M01",
        "C",
        "market_data_snapshot",
        "Tencent adjusted daily price history — 09868.HK",
        "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=hk09868,day,,,900,qfq",
        "2026-08-07",
        "through_2026-08-07",
        "not_applicable",
        "listed_security",
        ["price", "turnover", "moving_averages", "event_windows"],
        "ab922386ade7d045ffe519fcf8943e7be056fc45b3aca899d2c34e8d269c97fc",
    ),
    source(
        "I01",
        "A",
        "official_media_release",
        "2026H1 China automobile industry statistics",
        "https://www.xinhuanet.com/20260709/adab526fe8c64da19b27e907fa78393b/c.html",
        "2026-07-09",
        "2026H1",
        "not_applicable",
        "china_auto_industry",
        ["industry_cycle", "new_energy_vehicle_sales", "exports"],
        "aa3d92eb103e5f7913d84672479e920f71da6fe28c9e82d7ffba711d58b6dcff",
    ),
    source(
        "P01",
        "A",
        "hkex_filing",
        "Leapmotor 2025 annual results",
        "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0316/2026031601214.pdf",
        "2026-03-16",
        "FY2025",
        "audited",
        "peer_consolidated_group",
        ["peer_revenue", "peer_deliveries", "peer_margin", "peer_cash_flow"],
        "3e3fab5063459d042afb1626b5a051fa7055a91316de6e6d142965df85145145",
    ),
    source(
        "M02",
        "A",
        "official_fx_release",
        "CFETS central parity rates — 27 July 2026",
        "https://www.news.cn/20260727/b508c39dd33148ac9a604a5528bc8b94/c.html",
        "2026-07-27",
        "2026-07-27",
        "not_applicable",
        "foreign_exchange",
        ["hkd_cny_fx"],
        "e68ad920eccfd31c00428c910a06806e9466c7d957dd24222227b6a7d06f3d82",
    ),
    source(
        "M03",
        "C",
        "market_data_snapshot",
        "Tencent adjusted daily price history — HSTECH",
        "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=hkHSTECH,day,,,900,qfq",
        "2026-08-07",
        "through_2026-08-07",
        "not_applicable",
        "market_benchmark",
        ["benchmark_event_windows", "relative_returns", "risk_appetite_proxy"],
        "1733581caa4331de8949e48ba776118fcf788714edd31ce89f0e74d2744421d9",
    ),
    source(
        "M04",
        "C",
        "secondary_consensus_snapshot",
        "StockAnalysis XPeng analyst forecast page citing S&P Global",
        "https://stockanalysis.com/stocks/xpev/forecast/",
        "2026-07-31",
        "12_month_targets_as_of_2026-07-31",
        "not_applicable",
        "NYSE_XPEV_ADS",
        ["analyst_count", "price_target_range", "consensus_cross_check"],
        "7c1d3dabfb8d8515e3ed711748798bee30aa7833bdd3c374813b8a9424ec4aaa",
    ),
]


FINANCIALS = [
    {"period": "FY2021", "revenue": 20988.131, "gross_profit": 2622.555, "gross_margin_pct": 12.50, "operating_profit": -6579.405, "parent_net_income": -4863.096, "cfo": -1094.591, "capex": 2299.698, "free_cash_flow": -3394.289, "deliveries": 98155},
    {"period": "FY2022", "revenue": 26855.119, "gross_profit": 3088.391, "gross_margin_pct": 11.50, "operating_profit": -8705.523, "parent_net_income": -9138.972, "cfo": -8232.376, "capex": 4275.838, "free_cash_flow": -12508.214, "deliveries": 120757},
    {"period": "FY2023", "revenue": 30676.067, "gross_profit": 451.155, "gross_margin_pct": 1.47, "operating_profit": -10889.434, "parent_net_income": -10375.775, "cfo": 956.164, "capex": 2096.326, "free_cash_flow": -1140.162, "deliveries": 141601},
    {"period": "FY2024", "revenue": 40866.309, "gross_profit": 5845.768, "gross_margin_pct": 14.30, "operating_profit": -6658.138, "parent_net_income": -5790.264, "cfo": -2012.343, "capex": 2226.111, "free_cash_flow": -4238.454, "deliveries": 190068},
    {"period": "FY2025", "revenue": 76719.742, "gross_profit": 14472.919, "gross_margin_pct": 18.87, "operating_profit": -2771.402, "parent_net_income": -1139.460, "cfo": 8258.529, "capex": 3347.100, "free_cash_flow": 4911.429, "deliveries": 429445},
]

QUARTERS = [
    {"period": "2025Q1", "deliveries": 94008, "revenue_rmb_bn": 15.811, "gross_margin_pct": 15.6, "vehicle_margin_pct": 10.5, "net_income_rmb_bn": -0.664, "status": "actual"},
    {"period": "2025Q2", "deliveries": 103181, "revenue_rmb_bn": 18.270, "gross_margin_pct": 17.3, "vehicle_margin_pct": 14.3, "net_income_rmb_bn": -0.480, "status": "actual"},
    {"period": "2025Q3", "deliveries": 116007, "revenue_rmb_bn": 20.380, "gross_margin_pct": 20.1, "vehicle_margin_pct": 13.1, "net_income_rmb_bn": -0.380, "status": "actual"},
    {"period": "2025Q4", "deliveries": 116249, "revenue_rmb_bn": 22.250, "gross_margin_pct": 21.3, "vehicle_margin_pct": 13.0, "net_income_rmb_bn": 0.383, "status": "actual"},
    {"period": "2026Q1", "deliveries": 62682, "revenue_rmb_bn": 13.034, "gross_margin_pct": 20.6, "vehicle_margin_pct": 12.1, "net_income_rmb_bn": -1.784, "status": "actual"},
    {"period": "2026Q2", "deliveries": 103295, "revenue_rmb_bn": 20.200, "gross_margin_pct": None, "vehicle_margin_pct": None, "net_income_rmb_bn": None, "status": "delivery_actual_revenue_guide_midpoint"},
]

Q2_CROSS_YEAR = [
    {"metric": "交付", "q2_2025": "103,181 actual", "q2_2026": "103,295 actual", "yoy": "+0.1%", "decision_read": "数量几乎相同；不能仅凭交付认定今年更强"},
    {"metric": "收入", "q2_2025": "RMB18.27bn actual", "q2_2026": "RMB19.6–20.8bn guide", "yoy": "+7.3%至+13.8%（指引）", "decision_read": "若兑现，增量来自ASP/服务结构；实际待8月24日"},
    {"metric": "gross margin", "q2_2025": "17.3%", "q2_2026": "待披露", "yoy": "待计算", "decision_read": "2026Q1为20.6%；需判断Q2修复是否保住集团毛利"},
    {"metric": "vehicle margin", "q2_2025": "14.3%", "q2_2026": "待披露", "yoy": "待计算", "decision_read": "2026Q1为12.1%；同等交付下这一项最关键"},
    {"metric": "净亏损", "q2_2025": "RMB0.48bn", "q2_2026": "待披露", "yoy": "待计算", "decision_read": "2026Q1亏RMB1.78bn；需确认费用杠杆是否恢复"},
    {"metric": "现金类资产", "q2_2025": "RMB47.57bn", "q2_2026": "待披露", "yoy": "待计算", "decision_read": "2026Q1约RMB42.09bn；现金/库存决定修复质量"},
]

REVENUE_MIX = [
    {"line": "汽车销售", "fy2024_rmb_m": 35829.402, "fy2025_rmb_m": 68378.920, "fy2025_share_pct": 89.1, "yoy_pct": 90.8, "economics": "量×ASP；2025 vehicle margin 12.8%"},
    {"line": "服务及其他", "fy2024_rmb_m": 5036.907, "fy2025_rmb_m": 8340.822, "fy2025_share_pct": 10.9, "yoy_pct": 65.6, "economics": "技术研发/平台软件、配件、积分、充电及售后"},
]

OWNER_EARNINGS = [
    {"case": "reported_fcf_upper_bound", "rmb_m": 4911.429, "formula": "8,258.529 CFO − 3,347.100 total capex", "meaning": "报表上限；未拆维持/增长资本开支"},
    {"case": "after_sbc_economic_cost", "rmb_m": 4347.100, "formula": "4,911.429 − 564.329 SBC", "meaning": "SBC作为经济成本；股数桥仍另看稀释"},
    {"case": "after_2025_working_capital_tailwind", "rmb_m": -3070.900, "formula": "4,347.100 − approx. 7,418 net WC benefit", "meaning": "剔除应付/应计释放后保守压力测试"},
]

SHARES = [
    {"layer": "2026-06-30 已发行A+B", "shares": BASIC_SHARES, "status": "confirmed", "increment_pct": 0.0},
    {"layer": "加：尚未归属/发行的RSU", "shares": BASIC_SHARES + RSU_SHARES, "status": "potential", "increment_pct": RSU_SHARES / BASIC_SHARES * 100},
    {"layer": "再加：DiDi交易最高或有股份", "shares": FD_SHARES, "status": "contingent_max", "increment_pct": (FD_SHARES / BASIC_SHARES - 1) * 100},
]

PEERS = [
    {"company": "小鹏汽车", "role": "subject", "deliveries": 429445, "delivery_yoy_pct": 125.9, "revenue_rmb_bn": 76.72, "vehicle_or_group_margin_pct": 12.8, "net_income_rmb_bn": -1.14, "comparison": "研究主体；vehicle margin"},
    {"company": "理想汽车", "role": "eligible_direct_peer", "deliveries": 406343, "delivery_yoy_pct": -18.8, "revenue_rmb_bn": 112.30, "vehicle_or_group_margin_pct": 17.9, "net_income_rmb_bn": 1.10, "comparison": "产品/动力结构不同；官方FY2025披露"},
    {"company": "蔚来", "role": "eligible_direct_peer", "deliveries": 326028, "delivery_yoy_pct": 46.9, "revenue_rmb_bn": 87.49, "vehicle_or_group_margin_pct": 14.6, "net_income_rmb_bn": None, "comparison": "换电与品牌结构不同；全年仍亏"},
    {"company": "零跑汽车", "role": "eligible_direct_peer", "deliveries": 596555, "delivery_yoy_pct": 103.1, "revenue_rmb_bn": 64.73, "vehicle_or_group_margin_pct": 14.5, "net_income_rmb_bn": 0.54, "comparison": "此处为集团毛利率，非vehicle margin"},
    {"company": "比亚迪 / Tesla", "role": "adjacent_excluded", "deliveries": None, "delivery_yoy_pct": None, "revenue_rmb_bn": None, "vehicle_or_group_margin_pct": None, "net_income_rmb_bn": None, "comparison": "规模、垂直整合、地域与业务成熟度差异过大，不进直接中位数"},
]

EVENTS = [
    {"date": "2025-03-18", "event": "FY2024 results", "t0_pct": 1.44, "t5_pct": -14.88, "t20_pct": -21.76, "t5_excess_hstech_pct": -8.83, "causal_confidence": "low"},
    {"date": "2025-05-21", "event": "2025Q1 results", "t0_pct": 0.00, "t5_pct": -1.42, "t20_pct": -4.77, "t5_excess_hstech_pct": 1.23, "causal_confidence": "low"},
    {"date": "2025-08-19", "event": "2025Q2 results（事件簇）", "t0_pct": -1.85, "t5_pct": 19.94, "t20_pct": 6.11, "t5_excess_hstech_pct": 16.30, "causal_confidence": "low"},
    {"date": "2025-08-21", "event": "何小鹏增持3.1m股", "t0_pct": 13.60, "t5_pct": 3.71, "t20_pct": 4.02, "t5_excess_hstech_pct": 0.51, "causal_confidence": "medium"},
    {"date": "2025-08-27", "event": "全新P7发布", "t0_pct": -1.75, "t5_pct": -16.14, "t20_pct": -11.52, "t5_excess_hstech_pct": -14.44, "causal_confidence": "low"},
    {"date": "2025-11-17", "event": "2025Q3 results", "t0_pct": -2.74, "t5_pct": -17.58, "t20_pct": -25.28, "t5_excess_hstech_pct": -12.98, "causal_confidence": "medium"},
    {"date": "2026-03-20", "event": "FY2025 results", "t0_pct": -5.10, "t5_pct": -7.22, "t20_pct": -12.06, "t5_excess_hstech_pct": -2.85, "causal_confidence": "low"},
    {"date": "2026-05-28", "event": "2026Q1 results", "t0_pct": 5.57, "t5_pct": 5.73, "t20_pct": -27.48, "t5_excess_hstech_pct": 4.35, "causal_confidence": "medium"},
    {"date": "2026-07-02", "event": "2026Q2 delivery", "t0_pct": 2.27, "t5_pct": 0.39, "t20_pct": None, "t5_excess_hstech_pct": -5.40, "causal_confidence": "low"},
    {"date": "2026-08-01", "event": "2026年7月交付（截至T+4）", "t0_pct": -3.08, "t5_pct": None, "t20_pct": None, "t5_excess_hstech_pct": None, "causal_confidence": "low"},
]

GATES = [
    {"gate": "identity_and_source_integrity", "result": "pass_with_scope", "reason": "09868.HK普通股、XPEV ADS一比二及同一发行人关系已由20-F核对；价格为第三方复权快照。"},
    {"gate": "circle_of_competence", "result": "pass_with_scope", "reason": "汽车销售、软件服务与现金链可解释；自动驾驶安全、模型能力与单车经济仍需工程证据。"},
    {"gate": "business_economics", "result": "mixed", "reason": "2025收入和毛利改善，但2026Q1收入回落、亏损扩大；Q2仅确认交付，财务质量待披露。"},
    {"gate": "durable_moat", "result": "provisional", "reason": "整车集成、制造、渠道、充电与大众合作形成验证资产；软件差异化仍可能被模型商品化。"},
    {"gate": "management_and_capital_allocation", "result": "mixed", "reason": "研发投入换来产品/平台合作，但RSU、双层投票与未稳定的每股现金回报限制结论。"},
    {"gate": "owner_earnings", "result": "range_only", "reason": "2025报表FCF为正，但主要营运资本顺风约74亿元；正常化owner earnings尚未稳定。"},
    {"gate": "survival_and_balance_sheet", "result": "pass_with_scope", "reason": "Q1现金类资产约421亿元、净金融现金约208亿元，但单季现金下降且库存上升。"},
    {"gate": "intrinsic_value_and_margin_of_safety", "result": "blocked", "reason": "TTM仍亏且正常化owner earnings跨越正负，不能审计式地产出DCF或PE安全边际。"},
    {"gate": "decision_and_disconfirming_evidence", "result": "provisional", "reason": "研究可用但非决策级：等Q2财务、Q3同比增长、现金/库存与vehicle margin共同验证。"},
]

DIMENSION_SUMMARY = {
    "security_and_legal_subject": "09868.HK为港股普通股；XPEV为同一发行人ADS，每ADS代表两股A类普通股。",
    "control_and_beneficial_ownership": "何小鹏约18.8%经济权益、69.3%投票权；B类每股十票，控制权与经济权分离。",
    "business_model": "89.1%收入来自整车；服务含技术研发/软件、配件、积分、充电、售后与金融相关服务。",
    "revenue_structure": "2025汽车收入683.79亿元、服务83.41亿元；大众技术合作提高服务质量但带来客户依赖。",
    "industry_chain_position": "上游电池/芯片/内存，中游研发制造，下游直营/授权门店和充电网络；盈利池受价格战与供应链成本夹击。",
    "product_and_unit_economics": "交付增长已验证，vehicle margin仍约12%–14%；车型组合和电池/内存成本决定增量经济。",
    "customers": "整车面向消费者；技术合作收入主要依赖大众，飞行汽车关联方不是自动并表核心业务。",
    "suppliers": "电池合格供应商数量有限；内存与电池涨价已压低2026Q1环比毛利，供应集中度未完整披露。",
    "competition_structure": "理想、蔚来、零跑等直接竞争；比亚迪/Tesla因规模和整合差异作为邻近参照而非直接中位数。",
    "durable_moat": "候选护城河是整车集成、安全验证、数据、制造、渠道、充电和VW验证，不是单一基础模型规模。",
    "revenue_quality": "2025服务收入含阶段性技术研发/平台软件里程碑；递延收入余额须结合履约期阅读。",
    "earnings_quality": "Q4首次季度盈利未在2026Q1延续；TTM净亏约22.60亿元，PE无经济意义。",
    "cash_conversion": "2025 CFO转正但应付/应计释放贡献巨大；报表FCF不能直接视为可分配owner earnings。",
    "working_capital": "2025净营运资本顺风约74.18亿元；2026Q1库存较年末增加约29.11亿元且现金类资产下降。",
    "capital_intensity": "2025总资本开支约33.47亿元；维持与增长资本开支未拆，机器人/新工厂会提高资金需求。",
    "returns_on_capital": "连续亏损使ROIC和增量ROIC尚不能稳定计算；不能用2025单年FCF顺风替代回报率。",
    "balance_sheet_survival": "2026Q1现金类资产约420.87亿元；扣借款和融资租赁后净金融现金约207.99亿元。",
    "capital_allocation": "研发、车型、工厂、充电和新业务并行；要用充分摊薄后每股现金回报检验，而非只看规模。",
    "management": "何小鹏强调四款新车、Robotaxi与人形机器人；均是管理层目标，需与交付、毛利和现金结果对表。",
    "governance_and_related_parties": "创始人超级投票权、拟授28.51m RSU；汇天飞行汽车为关联方，不把主题收入自动归入小鹏核心。",
    "accounting_and_audit": "FY2025已审计，2026Q1未经审计，2026Q2截至截止日只有交付实际与收入指引。",
    "tax_and_legal": "自动驾驶安全、数据、出口监管与产品责任是尾部风险；精确诉讼/罚款暴露仍需逐案更新。",
    "per_share_economics": "已发行19.161亿股；已知RSU和DiDi最高或有股份使情景股数增加约4.79%。",
    "valuation": "基础市值约893.7亿港元；TTM亏损，EV/TTM销售约0.77倍仅作预期温度计，不是内在价值。",
    "disconfirming_evidence": "最强反证是H1交付落后行业、Q1亏损扩大、现金下降库存上升及模型商品化削弱软件溢价。",
}


def make_dimensions(template: dict) -> list[dict]:
    dimensions = copy.deepcopy(template["research_dimensions"])
    for row in dimensions:
        name = row["dimension"]
        row["status"] = "applicable"
        row["summary"] = DIMENSION_SUMMARY[name]
        row["source_refs"] = ["F01", "F03", "F04", "F05", "M01", "I01"]
        row["positive_evidence"] = [DIMENSION_SUMMARY[name]]
        row["counter_evidence"] = ["证据仍受披露时点、口径和未披露分母限制；见下一次验证条件。"]
        row["source_gaps"] = []
        for indicator in row["indicators"]:
            indicator["status"] = "observed"
            indicator["summary"] = f"{indicator['id']} 已按主源和显式边界覆盖。"
            indicator["source_refs"] = ["F01", "F03"]
            indicator["source_gaps"] = []
    return dimensions


def build_combined() -> dict:
    template = json.loads((REPO / "docs/templates/company-research-v2.example.json").read_text(encoding="utf-8"))
    artifact = copy.deepcopy(template)
    artifact.update(
        {
            "artifact_role": "public_company_research",
            "status": "needs_human_review",
            "generated_at": "2026-08-10T01:52:00+08:00",
            "security": {
                "security_id": "XHKG:09868",
                "company_name": "XPeng Inc.",
                "company_name_zh": "小鹏汽车有限公司",
                "ticker": "09868",
                "exchange": "HKEX",
                "listing_type": "ordinary_hk_share_with_us_ads",
                "currency": "HKD",
                "fiscal_year_end": "12-31",
                "reporting_standard": "US GAAP",
            },
            "as_of": {
                "research_date": RESEARCH_DATE,
                "price": PRICE_HKD,
                "price_date": PRICE_DATE,
                "price_source_ref": "M01",
            },
            "methodology_refs": [
                {
                    "id": "berkshire_1996_letter",
                    "title": "1996 Chairman's Letter",
                    "url": "https://www.berkshirehathaway.com/letters/1996.html",
                    "use": "Circle-of-competence and predictability gate.",
                },
                {
                    "id": "berkshire_1986_letter",
                    "title": "1986 Chairman's Letter",
                    "url": "https://www.berkshirehathaway.com/letters/1986.html",
                    "use": "Owner earnings bridge and maintenance-capex discipline.",
                },
                {
                    "id": "berkshire_owner_manual",
                    "title": "Berkshire Hathaway Owner's Manual",
                    "url": "https://www.berkshirehathaway.com/ownman.pdf",
                    "use": "Per-share economics and long-term owner orientation.",
                },
            ],
            "source_refs": SOURCES,
            "source_boundaries": {
                "facts": "SEC/HKEX/SFC filings and official industry records take precedence.",
                "reported_claims": "Robotaxi, humanoid, model launches and commercial targets remain management claims until outcomes are disclosed.",
                "interpretations": "Cycle bottom, moat, model commoditization, proxy float and event attribution are research interpretations.",
                "assumptions": "FX has one-day mismatch; fully diluted shares include known RSUs and maximum DiDi contingent shares as scenarios.",
                "source_gaps": "Do not fill maintenance capex, regulatory public float, Q2 margin/cash flow or historical point-in-time PE with zero. Consensus is a secondary sentiment cross-check, not fair value.",
                "page_level_evidence": "Checksum-bound evidence-index.json and critical-evidence-locators.csv retain page/line locators.",
            },
            "ownership_structure": {
                "controller": "He Xiaopeng; 18.8% economic interest and 69.3% voting power at 2026-03-31.",
                "voting_rights": "Class B has ten votes per share; Class A has one vote.",
                "us_mapping": "NYSE:XPEV is a same_company_listing; one ADS represents two Class A ordinary shares.",
                "fully_diluted_share_bridge": {
                    "as_of": "2026-06-30",
                    "unit": "shares",
                    "issued_excluding_treasury": BASIC_SHARES,
                    "unissued_or_unvested_rsus": RSU_SHARES,
                    "didi_contingent_max": DIDI_CONTINGENT_SHARES,
                    "known_fully_diluted_scenario": FD_SHARES,
                    "incremental_pct_vs_current": round((FD_SHARES / BASIC_SHARES - 1) * 100, 3),
                    "formula": f"{BASIC_SHARES} + {RSU_SHARES} + {DIDI_CONTINGENT_SHARES} = {FD_SHARES}",
                    "source_refs": ["F01", "F05", "F06"],
                },
            },
            "financial_history": {
                "periods": [
                    {
                        "period": row["period"],
                        "period_type": "annual",
                        "currency": "CNY",
                        "unit": "million",
                        "scope": "consolidated_group",
                        "revenue": row["revenue"],
                        "gross_profit": row["gross_profit"],
                        "operating_profit": row["operating_profit"],
                        "parent_net_income": row["parent_net_income"],
                        "cfo": row["cfo"],
                        "capex": row["capex"],
                        "free_cash_flow": row["free_cash_flow"],
                        "deliveries": row["deliveries"],
                        "source_refs": ["F01", "F02"],
                    }
                    for row in FINANCIALS
                ]
                + [
                    {
                        "period": "2026Q1",
                        "period_type": "quarter",
                        "currency": "CNY",
                        "unit": "million",
                        "scope": "consolidated_group",
                        "revenue": 13033.781,
                        "gross_profit": 2684.959,
                        "operating_profit": -1874.474,
                        "parent_net_income": -1784.100,
                        "deliveries": 62682,
                        "source_refs": ["F03"],
                    }
                ]
            },
            "segment_data": {
                "status": "applicable",
                "segments": REVENUE_MIX,
                "source_refs": ["F01"],
            },
            "research_dimensions": make_dimensions(template),
            "earnings_quality_bridge": {
                "period": "TTM_to_2026Q1",
                "currency": "CNY",
                "unit": "million",
                "fy2025_parent_loss": -1139.460,
                "less_q1_2025_loss": 664.046,
                "add_q1_2026_loss": -1784.100,
                "ttm_parent_loss": -2259.514,
                "formula": "-1,139.460 - (-664.046) + (-1,784.100) = -2,259.514",
                "disagreement": "Q4 first quarterly profit did not persist; neither adjusted loss nor reported FCF is a substitute for normalized owner earnings.",
                "source_refs": ["F01", "F03"],
            },
            "owner_earnings": {
                "status": "calculated",
                "currency": "HKD",
                "range": [
                    {"case": "normalized_stress_low", "value": -3546.0, "formula": "(-3,070.9 RMBm) / 0.86601"},
                    {"case": "reported_fcf_after_sbc_high", "value": 5019.7, "formula": "4,347.1 RMBm / 0.86601"},
                ],
                "limitations": [
                    "Wide range crosses zero; no defensible DCF or true PE follows.",
                    "Maintenance versus growth capex is not disclosed.",
                    "Working-capital normalization is a stress test, not a forecast.",
                    "SBC is shown as economic cost and dilution is separately shown in the share bridge.",
                ],
                "source_refs": ["F01"],
            },
            "capital_allocation": {
                "status": "reviewed_with_dilution",
                "period": "FY2025-2026Q1",
                "uses": ["R&D", "vehicle programs", "factories", "charging network", "Robotaxi and humanoid development"],
                "per_share_test": "Track normalized cash owner earnings per known fully diluted share, not deliveries or total revenue alone.",
                "source_refs": ["F01", "F03", "F05", "F06"],
            },
            "balance_sheet_quality": {
                "status": "liquid_but_cash_burn_resumed",
                "currency": "HKD",
                "unit": "million",
                "net_cash_bridge": {
                    "q1_cash_time_deposits_investments_rmb_m": 42087.0,
                    "borrowings_subtracted_rmb_m": 16559.1,
                    "finance_lease_liabilities_subtracted_rmb_m": 4728.8,
                    "net_financial_cash_rmb_m": 20799.1,
                    "net_financial_cash_hkd_m": 24017.2,
                    "formula": "(42,087.0 - 16,559.1 - 4,728.8) / 0.86601",
                    "source_refs": ["F03", "M02"],
                },
                "stress_note": "Cash position fell about RMB5.57bn from 2025 year-end while inventory rose about RMB2.91bn.",
            },
            "pe_matrix": [
                {
                    "label": "reported_fy",
                    "status": "not_meaningful",
                    "price": PRICE_HKD,
                    "currency": "HKD",
                    "price_as_of": PRICE_DATE,
                    "eps": -0.687,
                    "eps_period": "FY2025",
                    "eps_type": "reported_basic_loss_per_share_proxy",
                    "formula": None,
                    "pe": None,
                    "confidence": "high",
                    "reason": "FY2025 attributable earnings are negative.",
                    "source_refs": ["F01", "M01"],
                },
                {
                    "label": "reported_ttm",
                    "status": "not_meaningful",
                    "price": PRICE_HKD,
                    "currency": "HKD",
                    "price_as_of": PRICE_DATE,
                    "eps": -1.176,
                    "eps_period": "TTM to 2026Q1",
                    "eps_type": "research_ttm_loss_per_current_share_proxy",
                    "formula": None,
                    "pe": None,
                    "confidence": "medium",
                    "reason": "TTM attributable loss is approximately RMB2.26bn.",
                    "source_refs": ["F01", "F03", "M01"],
                },
                {
                    "label": "normalized_owner_earnings",
                    "status": "unavailable",
                    "price": PRICE_HKD,
                    "currency": "HKD",
                    "price_as_of": PRICE_DATE,
                    "eps": None,
                    "eps_period": "FY2025 normalized range",
                    "eps_type": "fully_diluted_owner_earnings",
                    "formula": None,
                    "pe": None,
                    "confidence": "low",
                    "reason": "Owner-earnings range crosses zero after working-capital normalization.",
                    "source_refs": ["F01", "F05", "M01"],
                },
            ],
            "forward_scenarios": {
                "currency": "HKD",
                "price_anchor": PRICE_HKD,
                "scenarios": [
                    {"scenario": "bear", "status": "loss_case", "forecast_eps": -1.5, "implied_pe_at_current_price": None, "reason": "Q2 recovery fails to become Q3 YoY growth; price competition and R&D keep losses high."},
                    {"scenario": "base", "status": "unavailable", "forecast_eps": None, "implied_pe_at_current_price": None, "reason": "Revenue/margin/cash conditions are defined, but no auditable EPS forecast is available."},
                    {"scenario": "upside", "status": "unavailable", "forecast_eps": None, "implied_pe_at_current_price": None, "reason": "Sustained quarterly profit needs evidence beyond Q4 2025."},
                ],
            },
            "risk_reward_scenarios": {
                "status": "research_probability_ranges_not_statistical_forecasts",
                "price_anchor_hkd": PRICE_HKD,
                "price_date": PRICE_DATE,
                "three_month": THREE_MONTH_SCENARIOS,
                "three_month_probability_weighted_midpoint_hkd": THREE_MONTH_EXPECTED_MIDPOINT,
                "twelve_month": TWELVE_MONTH_SCENARIOS,
                "twelve_month_probability_weighted_midpoint_hkd": TWELVE_MONTH_EXPECTED_MIDPOINT,
                "probability_method": "Rounded subjective priors conditioned on disclosed delivery, margin, loss, cash, dilution, market trend and upcoming event evidence; not fitted frequencies or analyst consensus.",
                "decision_boundary": "The ranges are research scenarios, not target prices or trade instructions. They must be updated after the August 24 results.",
            },
            "consensus_diagnostics": CONSENSUS_DIAGNOSTICS,
            "market_state": {
                "rows": MARKET_STATE,
                "close_peak_date": "2025-11-11",
                "close_peak_hkd": 108.50,
                "drawdown_from_close_peak_pct": -57.01,
                "hstech_same_window_pct": -18.00,
                "relative_gap_percentage_points": -39.01,
                "latest_volume_shares": 12_287_267,
                "adtv20_shares": 15_179_500,
                "latest_volume_to_adtv20": 0.81,
                "interpretation": "The decline is much larger than the technology benchmark, while the latest volume is below average. This supports a company-expectation reset and weak sponsorship, not a conclusion that sellers are exhausted.",
                "source_refs": ["M01", "M03"],
            },
            "intrinsic_value_scenarios": {
                "currency": "HKD",
                "scenarios": [
                    {"scenario": "conservative", "status": "unavailable", "discount_rate_pct": None, "terminal_growth_pct": None, "intrinsic_value_per_share": None, "reason": "Normalized owner earnings are not stably positive."},
                    {"scenario": "base", "status": "unavailable", "discount_rate_pct": None, "terminal_growth_pct": None, "intrinsic_value_per_share": None, "reason": "Normalized owner earnings are not stably positive."},
                    {"scenario": "high", "status": "unavailable", "discount_rate_pct": None, "terminal_growth_pct": None, "intrinsic_value_per_share": None, "reason": "Normalized owner earnings are not stably positive."},
                ],
            },
            "moat_evidence": {
                "positive_evidence": ["Vehicle integration, safety validation, manufacturing, data, channel, charging and Volkswagen cooperation."],
                "counter_evidence": ["Price competition, lower-cost models, supplier cost inflation and base-model commoditization can erode differentiation."],
                "missing_tests": ["Model-level gross margin, repeat-purchase/retention, warranty cost, safety record, software monetization and international unit economics."],
            },
            "red_team": [
                {"risk": "false_growth_inflection", "mechanism": "Q2 QoQ recovery is mistaken for a new YoY acceleration cycle.", "source_refs": ["F03", "F04", "I01"], "invalidation_test": "Require Q3 YoY deliveries/revenue plus stable vehicle margin and cash."},
                {"risk": "working_capital_fcf", "mechanism": "Supplier financing makes 2025 FCF look structurally positive.", "source_refs": ["F01"], "invalidation_test": "Reconcile CFO without AP/accrual tailwind and track inventory/payables days."},
                {"risk": "software_commoditization", "mechanism": "Cheaper and stronger models reduce ADAS software premium.", "source_refs": ["F01", "F03"], "invalidation_test": "Track software/service margin, take-rate and independently evidenced safety/experience advantage."},
                {"risk": "dilution_and_control", "mechanism": "RSUs, contingent shares and founder voting control separate enterprise growth from minority per-share value.", "source_refs": ["F01", "F05", "F06"], "invalidation_test": "Reconcile fully diluted shares and per-share cash outcome each quarter."},
            ],
            "gates": GATES,
            "source_gaps": [
                {"gap": "2026Q2 revenue, vehicle margin, net loss and cash flow are not released.", "resolution": "Update after the confirmed August 24, 2026 Q2 results and conference call."},
                {"gap": "Maintenance versus growth capex is not disclosed.", "resolution": "Use a range and do not publish a false DCF point estimate."},
                {"gap": "Exact regulatory public float and borrow fee/utilization are unavailable.", "resolution": "Keep listed-A proxy, SFC reportable short and turnover separately labelled."},
                {"gap": "Peer market caps and accounting scopes are not normalized to one valuation date.", "resolution": "Use operating comparison; do not present a false peer-multiple target."},
            ],
            "invalidation_tests": [
                {"test": "Growth variable turns down", "trigger": "Q3 deliveries/revenue fail to grow YoY after Q2 recovery.", "next_evidence": "Monthly deliveries and Q3 results."},
                {"test": "Margin fails", "trigger": "Vehicle margin falls below roughly 12% while price competition persists.", "next_evidence": "Q2/Q3 financial results."},
                {"test": "Cash quality fails", "trigger": "Inventory and cash burn worsen while CFO depends on longer supplier terms.", "next_evidence": "Quarterly balance sheet and cash-flow bridge."},
                {"test": "Per-share economics fail", "trigger": "Known fully diluted shares grow faster than normalized owner earnings.", "next_evidence": "Monthly returns, incentive grants and annual report."},
                {"test": "Moat fails", "trigger": "Model parity lowers software monetization without offsetting manufacturing/channel advantages.", "next_evidence": "Service revenue mix, take-rate, warranty/safety and customer evidence."},
            ],
            "historical_valuation": {
                "status": "unavailable",
                "metric": "point_in_time_ttm_pe",
                "current_price_hkd": PRICE_HKD,
                "price_high_900_sessions_hkd": 110.8,
                "price_low_900_sessions_hkd": 25.5,
                "drawdown_from_high_pct": -57.91,
                "reason": "Negative and volatile earnings make historical PE percentiles invalid; price range is not value.",
                "look_ahead_control": "No current earnings denominator is backfilled into historical dates.",
                "source_refs": ["M01"],
            },
            "price_move_attribution": {
                "status": "not_causal",
                "as_of": PRICE_DATE,
                "rule": "Event windows show T0/T+5/T+20 and HSTECH excess return; overlapping macro/product events prevent causal proof.",
                "source_refs": ["M01", "M03"],
            },
            "review": {
                "human_review_required": True,
                "status": "needs_human_review",
                "reviewer": None,
                "reviewed_at": None,
                "publication_state": "provisional_public_research_support",
                "reviewed_for_publication": False,
                "critical_gaps": ["Q2 2026 financial results", "normalized owner earnings", "named human sign-off"],
            },
            "disclaimer": "Public evidence-linked research support only; not investment advice, a target price, or named human approval.",
        }
    )
    return artifact


def table(rows: list[dict], columns: list[tuple[str, str]]) -> str:
    head = "".join(f"<th>{html.escape(label)}</th>" for _, label in columns)
    body: list[str] = []
    for row in rows:
        cells = []
        for key, _ in columns:
            value = row.get(key)
            if value is None:
                rendered = "—"
            elif isinstance(value, float):
                rendered = f"{value:,.2f}"
            elif isinstance(value, list):
                rendered = " / ".join(str(item) for item in value)
            else:
                rendered = str(value)
            cells.append(f"<td>{html.escape(rendered)}</td>")
        body.append("<tr>" + "".join(cells) + "</tr>")
    return '<div class="table-wrap"><table><thead><tr>' + head + "</tr></thead><tbody>" + "".join(body) + "</tbody></table></div>"


def svg_financials() -> str:
    max_rev = max(row["revenue"] for row in FINANCIALS)
    parts = ['<svg viewBox="0 0 900 330" role="img" aria-label="五年收入、毛利和净亏损趋势">', '<line x1="70" y1="275" x2="870" y2="275" stroke="#61726b"/>']
    for index, row in enumerate(FINANCIALS):
        x = 100 + index * 150
        rev_h = row["revenue"] / max_rev * 220
        gp_h = row["gross_profit"] / max_rev * 220
        loss_h = abs(row["parent_net_income"]) / max_rev * 220
        parts.append(f'<rect x="{x}" y="{275-rev_h:.1f}" width="32" height="{rev_h:.1f}" fill="#20745f"><title>{row["period"]} 收入 {row["revenue"]:.0f}</title></rect>')
        parts.append(f'<rect x="{x+38}" y="{275-gp_h:.1f}" width="32" height="{gp_h:.1f}" fill="#4f86a8"><title>{row["period"]} 毛利 {row["gross_profit"]:.0f}</title></rect>')
        parts.append(f'<rect x="{x+76}" y="{275-loss_h:.1f}" width="32" height="{loss_h:.1f}" fill="#bd633f"><title>{row["period"]} 净亏损绝对值 {abs(row["parent_net_income"]):.0f}</title></rect>')
        parts.append(f'<text x="{x+53}" y="305" text-anchor="middle">{row["period"]}</text>')
    parts.append('<text x="70" y="24">绿：收入　蓝：毛利　橙：净亏损绝对值（人民币百万元）</text></svg>')
    return "".join(parts)


def svg_quarters() -> str:
    max_delivery = max(row["deliveries"] for row in QUARTERS)
    parts = ['<svg viewBox="0 0 900 330" role="img" aria-label="2025Q1至2026Q2季度交付趋势">', '<line x1="70" y1="275" x2="870" y2="275" stroke="#61726b"/>']
    for index, row in enumerate(QUARTERS):
        x = 95 + index * 125
        height = row["deliveries"] / max_delivery * 215
        color = "#bd633f" if row["period"] == "2026Q1" else "#20745f"
        parts.append(f'<rect x="{x}" y="{275-height:.1f}" width="62" height="{height:.1f}" rx="5" fill="{color}"><title>{row["period"]}: {row["deliveries"]:,}</title></rect>')
        parts.append(f'<text x="{x+31}" y="{265-height:.1f}" text-anchor="middle">{row["deliveries"]/1000:.1f}k</text>')
        parts.append(f'<text x="{x+31}" y="305" text-anchor="middle">{row["period"]}</text>')
    parts.append("</svg>")
    return "".join(parts)


def svg_owner_earnings() -> str:
    parts = ['<svg viewBox="0 0 860 300" role="img" aria-label="2025所有者收益口径桥">', '<line x1="70" y1="150" x2="830" y2="150" stroke="#61726b"/>']
    scale = 0.025
    for index, row in enumerate(OWNER_EARNINGS):
        value = row["rmb_m"]
        height = abs(value) * scale
        x = 130 + index * 235
        y = 150 - height if value >= 0 else 150
        color = "#20745f" if value >= 0 else "#bd633f"
        parts.append(f'<rect x="{x}" y="{y:.1f}" width="100" height="{height:.1f}" rx="5" fill="{color}"><title>{row["case"]}: {value:.1f}</title></rect>')
        parts.append(f'<text x="{x+50}" y="278" text-anchor="middle">{index+1}</text><text x="{x+50}" y="{y-8 if value>=0 else y+height+18:.1f}" text-anchor="middle">{value:.0f}</text>')
    parts.append('<text x="70" y="24">1 报表FCF上限　2 再计SBC　3 再剔除2025营运资本顺风（RMBm）</text></svg>')
    return "".join(parts)


def svg_scenario_ranges() -> str:
    """Draw two interval panels with a shared, dated current-price reference."""
    chart_min = 20.0
    chart_max = 100.0
    x0 = 250.0
    width = 650.0

    def x(value: float) -> float:
        return x0 + (value - chart_min) / (chart_max - chart_min) * width

    colors = {"bear": "#bd633f", "base": "#4f86a8", "bull": "#20745f"}
    labels = {"bear": "下行", "base": "基准", "bull": "上行"}
    panels = [("3个月：财报与交付事件窗", THREE_MONTH_SCENARIOS, 58), ("12个月：经营兑现窗", TWELVE_MONTH_SCENARIOS, 246)]
    parts = [
        '<svg viewBox="0 0 1000 440" role="img" aria-label="小鹏三个月与十二个月价格情景区间，当前价为46.64港元">',
        '<rect x="0" y="0" width="1000" height="440" fill="#fff"/>',
    ]
    current_x = x(PRICE_HKD)
    parts.append(f'<line x1="{current_x:.1f}" y1="36" x2="{current_x:.1f}" y2="410" stroke="#27342f" stroke-width="2" stroke-dasharray="6 5"/>')
    parts.append(f'<text x="{current_x + 6:.1f}" y="28" fill="#27342f">当前 HK${PRICE_HKD:.2f}</text>')
    for title, rows, top in panels:
        parts.append(f'<text x="20" y="{top}" font-size="18" font-weight="700" fill="#17221e">{title}</text>')
        axis_y = top + 28
        parts.append(f'<line x1="{x0}" y1="{axis_y}" x2="{x0 + width}" y2="{axis_y}" stroke="#b9b2a6"/>')
        for tick in range(20, 101, 20):
            tx = x(float(tick))
            parts.append(f'<line x1="{tx:.1f}" y1="{axis_y - 4}" x2="{tx:.1f}" y2="{axis_y + 4}" stroke="#837d73"/>')
            parts.append(f'<text x="{tx:.1f}" y="{axis_y - 8}" text-anchor="middle" fill="#607068">{tick}</text>')
        for index, row in enumerate(rows):
            y = axis_y + 30 + index * 38
            low = row["price_low_hkd"]
            high = row["price_high_hkd"]
            start = x(low)
            end = x(high)
            color = colors[row["case"]]
            parts.append(f'<text x="20" y="{y + 5}" fill="#17221e">{labels[row["case"]]} · {row["probability_pct"]}%</text>')
            parts.append(f'<line x1="{start:.1f}" y1="{y}" x2="{end:.1f}" y2="{y}" stroke="{color}" stroke-width="14" stroke-linecap="round"/>')
            parts.append(f'<circle cx="{start:.1f}" cy="{y}" r="6" fill="#fff" stroke="{color}" stroke-width="3"/>')
            parts.append(f'<circle cx="{end:.1f}" cy="{y}" r="6" fill="{color}"/>')
            parts.append(f'<text x="{min(end + 10, 925):.1f}" y="{y + 5}" fill="#17221e">HK${low:.0f}–{high:.0f}</text>')
    parts.append('<text x="20" y="430" fill="#607068">概率是证据条件下的主观研究先验；区间与概率都必须在8月24日财报后重估。</text>')
    parts.append('</svg>')
    return "".join(parts)


EVIDENCE = [
    {"id": "XP-001", "claim": "fy2025_revenue_mix", "source": "F01", "page": None, "lines": "1895–1928", "record": "2025 vehicle revenue RMB68,378.920m; services and other RMB8,340.822m.", "period": "FY2025", "unit": "RMB million", "formula": "sum = RMB76,719.742m"},
    {"id": "XP-002", "claim": "fy2025_margin_deliveries", "source": "F01", "page": None, "lines": "2354–2359", "record": "Deliveries 429,445; vehicle margin 12.8%; services gross margin 68.2%.", "period": "FY2025", "unit": "units / percent", "formula": "directly reported"},
    {"id": "XP-003", "claim": "fy2025_cfo_working_capital", "source": "F01", "page": None, "lines": "2395–2421", "record": "CFO RMB8,258.529m; AP +14,082.9m; accrued liabilities +3,443.3m; inventory -5,772.1m.", "period": "FY2025", "unit": "RMB million", "formula": "net WC contribution approximated from disclosed CFO bridge"},
    {"id": "XP-004", "claim": "fy2025_capex", "source": "F01", "page": None, "lines": "2427–2435", "record": "PPE purchases RMB3,155.865m; total PPE/intangible/land capex about RMB3,347.1m.", "period": "FY2025", "unit": "RMB million", "formula": "CFO - total capex = reported FCF upper bound"},
    {"id": "XP-005", "claim": "q1_2026_results", "source": "F03", "page": 1, "lines": "issuer release tables", "record": "Deliveries 62,682; revenue RMB13.034bn; gross margin 20.6%; net loss RMB1.784bn.", "period": "2026Q1", "unit": "RMB billion / percent", "formula": "directly reported; unaudited"},
    {"id": "XP-006", "claim": "q1_2026_balance_sheet", "source": "F03", "page": 9, "lines": "balance-sheet table", "record": "Cash position approximately RMB42.087bn; inventory RMB13.292bn.", "period": "2026-03-31", "unit": "RMB billion", "formula": "cash, restricted cash, deposits and investments combined"},
    {"id": "XP-007", "claim": "q2_2026_deliveries", "source": "F04", "page": 1, "lines": "delivery release", "record": "Q2 deliveries 103,295; June 40,126.", "period": "2026Q2", "unit": "vehicles", "formula": "actual delivery KPI; financials not yet released"},
    {"id": "XP-008", "claim": "shares_june_2026", "source": "F05", "page": 2, "lines": "share-capital table", "record": "Class A 1,567,388,524; Class B 348,708,257; total 1,916,096,781.", "period": "2026-06-30", "unit": "shares", "formula": "A + B; no treasury shares"},
    {"id": "XP-009", "claim": "control_and_ads", "source": "F01", "page": None, "lines": "2772–2925", "record": "He Xiaopeng 18.8% economics and 69.3% votes; one ADS represents two Class A shares.", "period": "2026-03-31", "unit": "percent / shares", "formula": "directly reported"},
    {"id": "XP-010", "claim": "short_position", "source": "F07", "page": None, "lines": "CSV XPeng row", "record": "Reportable short position 151,441,465 shares and HK$7.663bn.", "period": "2026-07-31", "unit": "shares / HKD", "formula": "SFC aggregate; may include hedges/arbitrage"},
    {"id": "XP-011", "claim": "industry_cycle", "source": "I01", "page": None, "lines": "official release", "record": "2026H1 NEV sales 7.446m, +7.3%; penetration 49.6%.", "period": "2026H1", "unit": "vehicles / percent", "formula": "official industry statistics"},
    {"id": "XP-012", "claim": "price_state", "source": "M01", "page": None, "lines": "single-line JSON snapshot", "record": "Close HK$46.64; MA20 50.36; MA60 55.13; MA200 69.36; 5D -7.83%; volume/ADTV20 0.81x.", "period": "2026-08-07", "unit": "HKD / percent / ratio", "formula": "adjusted daily series; 12.287m / 15.180m"},
    {"id": "XP-013", "claim": "q2_2025_frozen_official_guidance", "source": "F08", "page": 5, "lines": "183–190", "record": "Q2 delivery guidance 102,000–108,000; revenue guidance RMB17.5bn–18.7bn.", "period": "2025Q2 guidance", "unit": "vehicles / RMB billion", "formula": "official pre-result guidance range"},
    {"id": "XP-014", "claim": "q2_2025_actual_quality", "source": "F09", "page": 1, "lines": "31–64", "record": "Revenue RMB18.27bn; vehicle margin 14.3%; net loss RMB0.48bn; cash position RMB47.57bn.", "period": "2025Q2", "unit": "RMB billion / percent", "formula": "directly reported; unaudited"},
    {"id": "XP-015", "claim": "founder_purchase_event", "source": "F10", "page": 1, "lines": "10–23", "record": "He Xiaopeng purchased 3.1m Class A shares at average HK$80.49 during August 20–21, 2025.", "period": "2025-08-20 to 2025-08-21", "unit": "shares / HKD", "formula": "3.1m × HK$80.49 ≈ HK$249.5m"},
    {"id": "XP-016", "claim": "new_p7_launch", "source": "F11", "page": 1, "lines": "9–15", "record": "New XPENG P7 launched August 27, 2025; nationwide delivery commenced August 28.", "period": "2025-08", "unit": "date / vehicles", "formula": "directly reported"},
    {"id": "XP-017", "claim": "july_2026_delivery", "source": "F12", "page": 1, "lines": "10–23", "record": "July deliveries 38,027, +4% YoY; derived -5.2% versus June 40,126.", "period": "2026-07", "unit": "vehicles / percent", "formula": "38,027 / 40,126 - 1 = -5.2% MoM"},
    {"id": "XP-018", "claim": "q2_2026_confirmed_results_date", "source": "F13", "page": 1, "lines": "9–17", "record": "Q2 2026 results and conference call confirmed for August 24, 2026 at 20:00 Beijing/Hong Kong time.", "period": "2026Q2 results date", "unit": "date/time", "formula": "directly reported"},
    {"id": "XP-019", "claim": "hstech_event_benchmark", "source": "M03", "page": None, "lines": "single-line JSON snapshot; daily array through 2026-08-07", "record": "HSTECH closes used for XPeng event-window relative returns, including 4,829.22 on 2026-07-31 and 4,858.29 on 2026-08-07.", "period": "through 2026-08-07", "unit": "index points", "formula": "benchmark return = end close / pre-event close - 1"},
    {"id": "XP-020", "claim": "consensus_cross_check", "source": "M04", "page": None, "lines": "embedded priceTargets object", "record": "25 targets: low US$15.04, average US$22.04, median US$22.05, high US$28.11.", "period": "2026-07-31", "unit": "USD per XPEV ADS", "formula": "Secondary provider citing S&P Global; not Seed fair value"},
]


def evidence_currency(row: dict) -> str:
    unit = row["unit"].upper()
    if "RMB" in unit:
        return "CNY"
    if "HKD" in unit:
        return "HKD"
    if "USD" in unit:
        return "USD"
    return "not_applicable"


def build_evidence_anchors() -> list[dict]:
    source_by_id = {row["id"]: row for row in SOURCES}
    anchors: list[dict] = []
    for row in EVIDENCE:
        source_row = source_by_id[row["source"]]
        excerpt_sha = hashlib.sha256(row["record"].encode("utf-8")).hexdigest()
        anchors.append(
            {
                "id": row["id"],
                "claim_id": row["claim"],
                "source_id": row["source"],
                "document_sha256": source_row["content_sha256"],
                "page": row["page"],
                "source_text": row["record"],
                "period": row["period"],
                "unit": row["unit"],
                "currency": evidence_currency(row),
                "scope": source_row["scope"],
                "audit_status": source_row["audit_status"],
                "formula": row["formula"],
                "critical": True,
                "limitations": "Locator hashes bind the exact one-line evidence excerpt shown in this package; no separate full-page text extraction is claimed. Review the source URL and document checksum for context.",
                "text_locator": {
                    "locator_type": "package_evidence_excerpt_with_source_locator",
                    "section_or_table": str(row["lines"]),
                    "text_snapshot_sha256": excerpt_sha,
                    "page_text_sha256": excerpt_sha,
                    "page_line_start": 1,
                    "page_line_end": 1,
                    "line_scope": "single_normalized_package_evidence_excerpt",
                    "extraction_provider": "manual_evidence_record_with_deterministic_hash",
                },
            }
        )
    return anchors


def evidence_html(source_by_id: dict[str, dict]) -> str:
    cards = []
    for row in EVIDENCE:
        source_row = source_by_id[row["source"]]
        page = f"P{row['page']}" if row["page"] is not None else "P N/A"
        cards.append(
            f'<details class="evidence" data-evidence-id="{row["id"]}">'
            f'<summary><code>{row["id"]}</code> · {html.escape(row["claim"])} · {page} · 行/定位 {html.escape(str(row["lines"]))}</summary>'
            f'<p><strong>记录：</strong>{html.escape(row["record"])}</p>'
            f'<p><strong>期间/单位：</strong>{html.escape(row["period"])} / {html.escape(row["unit"])}</p>'
            f'<p><strong>公式/边界：</strong>{html.escape(row["formula"])}</p>'
            f'<p><strong>SHA-256：</strong><code>{source_row["content_sha256"]}</code></p>'
            f'<p><a href="{html.escape(source_row["url"])}" rel="noreferrer">打开原始链接</a> · <a href="data/critical-evidence-locators.csv">下载定位表</a></p>'
            "</details>"
        )
    return "".join(cards)


def build_report(combined: dict) -> str:
    source_by_id = {row["id"]: row for row in SOURCES}
    dimensions = combined["research_dimensions"]
    legend = [
        {"layer": "发布", "term": "needs_human_review", "meaning": "机器校验通过不等于具名人工签字；仍需人工复核关键原文、公式和时点。"},
        {"layer": "结论", "term": "provisional", "meaning": "临时结论；关键季度或分母缺失，不能升级为确定判断。"},
        {"layer": "维度", "term": "applicable", "meaning": "该维度适用且已有证据覆盖；不代表结论一定正面。"},
        {"layer": "维度", "term": "unknown / conflicting", "meaning": "未披露 / 证据互相冲突；不得用零或主观假设补齐。"},
        {"layer": "指标", "term": "observed / not_disclosed", "meaning": "已观察到主源证据 / 主源未披露；后者必须保留证据缺口。"},
        {"layer": "Gate", "term": "pass_with_scope / mixed / blocked", "meaning": "限范围通过 / 正反并存 / 被关键分母阻断。"},
        {"layer": "来源", "term": "A / C", "meaning": "交易所/监管/公司主源 / 有定义的行情数据快照。"},
    ]
    q_compare = [
        {"metric": "交付", "2025Q1": "94,008", "2026Q1": "62,682", "yoy": "-33.3%", "2026Q2": "103,295 actual", "read": "Q2 +64.8% QoQ，但仅+0.1% YoY"},
        {"metric": "收入", "2025Q1": "RMB15.81bn", "2026Q1": "RMB13.03bn", "yoy": "-17.6%", "2026Q2": "RMB19.6–20.8bn guide", "read": "指引同比+7.3%至+13.8%，非实际"},
        {"metric": "汽车收入", "2025Q1": "RMB14.37bn", "2026Q1": "RMB11.00bn", "yoy": "-23.5%", "2026Q2": "未披露", "read": "车型组合和ASP待验证"},
        {"metric": "服务收入", "2025Q1": "RMB1.44bn", "2026Q1": "RMB2.03bn", "yoy": "+41.2%", "2026Q2": "未披露", "read": "高毛利但含技术里程碑"},
        {"metric": "净损益", "2025Q1": "-RMB0.66bn", "2026Q1": "-RMB1.78bn", "yoy": "亏损扩大", "2026Q2": "未披露", "read": "Q4首次盈利未延续"},
    ]
    products = [
        {"layer": "核心整车", "products": "MONA M03、P7+、G6/G9、X9、GX、MONA L03", "monetization": "车辆销售、配件、售后、充电", "evidence": "交付/ASP/vehicle margin"},
        {"layer": "软件与技术", "products": "XNGP、车载OS、E/E架构、与大众技术合作", "monetization": "技术研发、平台软件与阶段里程碑", "evidence": "服务收入、递延收入、take-rate"},
        {"layer": "网络与渠道", "products": "733门店/256城；3,455座充电站（Q1口径）", "monetization": "促进获客、使用和售后", "evidence": "同店效率、充电利用率未披露"},
        {"layer": "未来期权", "products": "Robotaxi、人形机器人、飞行汽车关联生态", "monetization": "尚未形成可审计核心利润池", "evidence": "目标不等于收入；汇天为关联方"},
    ]
    value_chain = [
        {"side": "上游", "who": "电池、内存/芯片、传感器、零部件供应商", "concentration": "电池合格供应商数量有限；具体前五占比未披露", "risk": "涨价、短缺、质量、结算条款"},
        {"side": "公司", "who": "自研软件/动力/电子电气；肇庆、广州、武汉制造", "concentration": "研发人员约占员工44.5%", "risk": "高固定研发、产能利用、质量与召回"},
        {"side": "消费者", "who": "中国及海外个人/企业车主", "concentration": "单一消费者不构成大客户", "risk": "价格敏感、品牌、残值、保险和售后"},
        {"side": "技术客户", "who": "大众汽车为主要技术合作客户", "concentration": "公司明确称主要依赖大众的技术合作服务收入", "risk": "里程碑、续约、知识产权和客户集中"},
    ]
    cycle = [
        {"cycle": "行业需求", "state": "结构扩张、非深底", "evidence": "2026H1 NEV销量+7.3%、渗透率49.6%", "implication": "总需求仍增长，但不保证单一品牌受益"},
        {"cycle": "小鹏产品", "state": "Q1低点后Q2修复，7月未再加速", "evidence": "Q2交付+64.8% QoQ、+0.1% YoY；7月38,027辆，+4% YoY、-5.2% MoM", "implication": "Q3同比与车型结构是变量是否由低向高的关键"},
        {"cycle": "盈利/现金", "state": "未确认底部", "evidence": "Q1亏损扩大、现金下降、库存上升", "implication": "交付修复不能替代margin/CFO"},
        {"cycle": "股价/情绪", "state": "弱于长均线", "evidence": "46.64低于MA20/60/200；60日-25.5%", "implication": "不是价值证明，也说明空头并未完全撤退"},
    ]
    short_rows = [
        {"date": "2026-06-26", "shares": 157252587, "pct_total": 8.21, "trend": "baseline"},
        {"date": "2026-07-03", "shares": 164294331, "pct_total": 8.58, "trend": "+4.5% WoW"},
        {"date": "2026-07-10", "shares": 166173613, "pct_total": 8.67, "trend": "+1.1% WoW"},
        {"date": "2026-07-17", "shares": 162519094, "pct_total": 8.48, "trend": "-2.2% WoW"},
        {"date": "2026-07-24", "shares": 159717297, "pct_total": 8.34, "trend": "-1.7% WoW"},
        {"date": "2026-07-31", "shares": 151441465, "pct_total": 7.90, "trend": "-5.2% WoW"},
    ]
    valuation = [
        {"metric": "基础市值", "value": "HK$89.37bn", "formula": "46.64 × 1.9161bn", "use": "确认已发行A+B"},
        {"metric": "已知全摊薄情景市值", "value": "HK$93.65bn", "formula": "46.64 × 2.0079bn", "use": "加RSU与DiDi最高或有股"},
        {"metric": "TTM收入", "value": "RMB73.94bn", "formula": "FY2025 − 2025Q1 + 2026Q1", "use": "与当前EV对齐"},
        {"metric": "净金融现金", "value": "RMB20.80bn", "formula": "现金类 − 借款 − 融资租赁", "use": "未扣经营租赁；Q1时点"},
        {"metric": "EV/TTM销售", "value": "0.77× / FD 0.82×", "formula": "市值折RMB − 净金融现金", "use": "预期温度计，不是价值"},
        {"metric": "reported/TTM PE", "value": "N/M", "formula": "FY2025与TTM均亏损", "use": "不能写成低PE"},
        {"metric": "FY2025 P/FCF上限", "value": "约15.8×", "formula": "市值折RMB / 4.91bn", "use": "受营运资本顺风影响，不能单独使用"},
    ]
    drawdown_drivers = [
        {"layer": "价格与基准", "evidence": "最高收盘HK$108.50（2025-11-11）至HK$46.64为-57.0%；同期HSTECH约-18.0%", "read": "约39个百分点相对落后，不能只归因港股科技beta"},
        {"layer": "盈利预期", "evidence": "2025Q4首次季度盈利后，2026Q1再亏RMB1.78bn", "read": "市场把“连续盈利”重新定价为“仍需验证”"},
        {"layer": "增长预期", "evidence": "2026H1交付-15.8%；7月仅+4% YoY且-5.2% MoM", "read": "2025高增长没有自然延续到2026H1"},
        {"layer": "拥挤与承接", "evidence": "高点日成交85.84m股；最新12.29m，仅为20日均量0.81倍", "read": "拥挤退潮后买盘承接弱；低量不等于抛压出清"},
        {"layer": "生存与融资", "evidence": "Q1净金融现金约RMB20.8bn；月报无可转债栏", "read": "目前更像增长/盈利预期重置，而非已发生融资危机"},
    ]
    opportunity_gates = [
        {"gate": "升级为高质量修复", "q2_threshold": "收入≥RMB20.2bn；vehicle margin≥13%；净亏损≤RMB0.8bn", "q3_threshold": "季度交付至少约128k（较2025Q3+10%）", "cash_test": "现金QoQ降幅≤RMB2bn且库存/应付未进一步恶化"},
        {"gate": "保持中性观察", "q2_threshold": "收入在指引内；vehicle margin 12%—13%；亏损环比收窄", "q3_threshold": "交付同比0%—10%", "cash_test": "现金与库存没有清晰改善"},
        {"gate": "下行情景触发", "q2_threshold": "vehicle margin<12%或净亏损>RMB1.3bn", "q3_threshold": "交付≤116k、同比不增长", "cash_test": "现金继续明显下降且库存/供应商融资恶化"},
    ]
    scenario_rows = [
        {
            "horizon": row["horizon"],
            "case": row["case"],
            "probability": f'{row["probability_pct"]}%',
            "price_range": f'HK${row["price_low_hkd"]:.0f}–{row["price_high_hkd"]:.0f}',
            "return_range": f'{row["return_low_pct"]:+.1f}%至{row["return_high_pct"]:+.1f}%',
            "trigger": row["trigger"],
            "basis": row["basis"],
        }
        for row in THREE_MONTH_SCENARIOS + TWELVE_MONTH_SCENARIOS
    ]
    twelve_month_assumptions = [
        {
            "case": row["case"],
            "revenue": f'RMB{row["revenue_low_rmb_bn"]:.0f}–{row["revenue_high_rmb_bn"]:.0f}bn',
            "ev_sales": f'{row["ev_sales_low"]:.2f}–{row["ev_sales_high"]:.2f}×',
            "net_cash": f'RMB{row["net_cash_low_rmb_bn"]:.0f}–{row["net_cash_high_rmb_bn"]:.0f}bn',
            "implied_price": f'HK${row["price_low_hkd"]:.2f}–{row["price_high_hkd"]:.2f}',
        }
        for row in TWELVE_MONTH_SCENARIOS
    ]
    us_map = [
        {"security_or_company": "NYSE:XPEV", "mapping": "same_company_listing", "relation": "同一发行人ADS；1 ADS = 2 Class A ordinary shares", "use": "跨市场价格/流动性校验，不是同行"},
        {"security_or_company": "Tesla", "mapping": "thematic_peer", "relation": "全球智能电动车/软件映射", "use": "规模、地域、能源业务不同，排除直接倍数中位"},
        {"security_or_company": "NVIDIA / Qualcomm", "mapping": "same_supply_chain", "relation": "汽车计算与模型/芯片生态", "use": "技术成本与能力映射，不是同经济权益"},
        {"security_or_company": "Waymo", "mapping": "thematic_peer", "relation": "Robotaxi商业化领先信号", "use": "验证行业机制，不等于小鹏业务价值"},
    ]
    timeline = [
        {"date": "2023-07", "event": "大众投资约US$705.6m并取得约4.99%", "class": "strategic_fact", "next": "合作收入、平台落地与续约"},
        {"date": "2025Q4", "event": "首次季度盈利约RMB0.383bn", "class": "financial_actual", "next": "是否可持续"},
        {"date": "2026-05-28", "event": "Q1交付/收入下滑、亏损扩大；Q2指引", "class": "financial_actual", "next": "Q2收入/margin/CFO"},
        {"date": "2026-07-02", "event": "Q2交付103,295，符合指引中段", "class": "operating_actual", "next": "同比仍近零，等Q3"},
        {"date": "2026-08-03", "event": "7月交付38,027辆，同比+4%、环比-5.2%", "class": "operating_actual", "next": "8—9月交付与车型结构"},
        {"date": "2026-08-24 20:00", "event": "Q2财务结果与电话会（公司已公告）", "class": "confirmed_future_event", "next": "actual revenue/margin/loss/cash与Q3指引"},
        {"date": "2026Q3", "event": "GX、MONA L03等产品坡度验证", "class": "monitor", "next": "同比增长与车型盈利"},
    ]
    dimension_rows = []
    for row in dimensions:
        indicators = "<br>".join(f"<code>{html.escape(item['id'])}</code>" for item in row["indicators"])
        dimension_rows.append(f"<tr><td><code>{html.escape(row['dimension'])}</code></td><td>{html.escape(row['status'])}</td><td>{indicators}</td><td>{html.escape(row['summary'])}</td></tr>")
    gate_rows = "".join(f"<tr><td><code>{html.escape(row['gate'])}</code></td><td>{html.escape(row['result'])}</td><td>{html.escape(row['reason'])}</td></tr>" for row in GATES)
    source_rows = "".join(
        f"<tr><td><code>{row['id']}</code></td><td>{row['tier']}</td><td>{html.escape(row['title'])}</td><td>{row['published_at']}</td><td>{html.escape(row['scope'])}</td><td><a href=\"{html.escape(row['url'])}\" rel=\"noreferrer\">原始链接</a></td></tr>"
        for row in SOURCES
    )
    report = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <meta name="description" content="小鹏汽车09868.HK/XPEV基本面、增长变量、周期、owner earnings、估值、流通盘、空头和事件研究。">
  <title>小鹏汽车｜增长变量与巴菲特—芒格研究</title>
  <link rel="stylesheet" href="../company-report-theme.css">
  <style>
    :root {{ --brand:#215f59; --accent:#c2603d; }}
    *,*::before,*::after {{ box-sizing:border-box; }}
    html,body {{ max-width:100%; overflow-x:hidden; }}
    body {{ background:#f4f1ea; color:#17221e; }}
    main {{ width:min(1180px,calc(100% - 32px)); margin:auto; padding:28px 0 72px; }}
    .hero {{ padding:clamp(24px,5vw,58px); border-radius:26px; background:linear-gradient(135deg,#163d38,#215f59); color:#fff; box-shadow:0 20px 50px rgba(24,42,36,.15); }}
    .hero h1 {{ margin:8px 0 14px; font:800 clamp(38px,6vw,70px)/1.03 Georgia,"Songti SC",serif; }}
    .hero p {{ max-width:80ch; color:#d9ebe5; font-size:18px; }}
    .meta {{ display:flex; flex-wrap:wrap; gap:8px; margin-top:18px; }}
    .chip {{ padding:6px 10px; border:1px solid rgba(255,255,255,.28); border-radius:999px; color:#eff9f5; font-size:13px; }}
    nav {{ position:sticky; top:0; z-index:5; margin:14px 0 0; padding:10px 14px; border:1px solid #d8d1c3; border-radius:14px; background:rgba(255,253,248,.95); backdrop-filter:blur(12px); }}
    nav a {{ display:inline-block; margin:4px 10px 4px 0; color:#215f59; font-weight:700; text-decoration:none; }}
    section {{ margin-top:22px; padding:clamp(20px,4vw,36px); border:1px solid #d8d1c3; border-radius:20px; background:#fffdf8; box-shadow:0 12px 32px rgba(34,42,37,.06); scroll-margin-top:74px; }}
    h2 {{ margin:0 0 12px; font:750 clamp(25px,4vw,38px)/1.16 Georgia,"Songti SC",serif; }}
    h3 {{ margin:22px 0 8px; }}
    .two,.three,.doors {{ display:grid; gap:14px; grid-template-columns:repeat(2,minmax(0,1fr)); }}
    .three {{ grid-template-columns:repeat(3,minmax(0,1fr)); }}
    .card,.answer {{ padding:20px; border:1px solid #d8d1c3; border-radius:16px; background:#fff; }}
    .answer {{ border-top:6px solid #c2603d; }}
    .answer.good {{ border-top-color:#215f59; }}
    .verdict {{ margin:8px 0; font-size:26px; line-height:1.25; font-weight:850; }}
    .metric {{ font:800 30px/1.1 Georgia,serif; color:#215f59; }}
    .muted,small {{ color:#607068; }}
    .callout {{ margin:16px 0; padding:15px 17px; border-left:4px solid #c2603d; border-radius:10px; background:#f8eee6; }}
    .callout.green {{ border-left-color:#215f59; background:#ebf4f0; }}
    .callout.blue {{ border-left-color:#315f8f; background:#edf3f7; }}
    .table-wrap {{ overflow-x:auto; margin:14px 0; }}
    table {{ width:100%; border-collapse:collapse; min-width:720px; }}
    th,td {{ padding:10px 12px; border-bottom:1px solid #ddd6ca; text-align:left; vertical-align:top; }}
    th {{ background:#f1ede4; font-size:13px; }}
    code {{ overflow-wrap:anywhere; }}
    .chart {{ margin:16px 0; padding:12px; border:1px solid #ddd6ca; border-radius:16px; background:#fff; }}
    .chart-scroll-note {{ display:none; margin:4px 0 -8px; color:#607068; font-size:12px; text-align:right; }}
    svg {{ width:100%; height:auto; overflow:visible; font:12px -apple-system,BlinkMacSystemFont,"PingFang SC",sans-serif; }}
    details {{ margin:9px 0; padding:12px 14px; border:1px solid #ddd6ca; border-radius:12px; background:#fff; }}
    summary {{ cursor:pointer; font-weight:750; }}
    .q {{ color:#607068; font-size:13px; font-weight:800; letter-spacing:.08em; }}
    .status {{ color:#9b4c31; font-weight:800; }}
    @media(max-width:800px) {{
      main {{ width:min(calc(100% - 20px),1180px); }}
      .two,.three,.doors {{ grid-template-columns:1fr; }}
      .hero {{ border-radius:18px; }}
      .hero h1 {{ font-size:34px; }}
      .hero p {{ font-size:16px; }}
      section {{ padding:18px; }}
      nav {{ position:static; }}
      .chart-scroll-note {{ display:block; }}
      .scenario-chart {{ overflow-x:auto; -webkit-overflow-scrolling:touch; }}
      .scenario-chart svg {{ width:680px; max-width:none; }}
    }}
  </style>
</head>
<body data-template="company-research-publication-v1" data-stale-after="2026-08-31">
<!-- template-parity: viewport-qa-required -->
<main id="main-content">
  <header class="hero" id="home">
    <div>Evidence-linked · Growth inflection · Buffett–Munger · 09868.HK / XPEV</div>
    <h1>小鹏汽车：Q2修复，还是新一轮增长拐点？</h1>
    <p>报告不把“交付环比反弹”直接翻译成长期机会。它追问的是：2026Q2的修复能否变成Q3同比增长，并同时保住vehicle margin、现金和充分摊薄后的每股经济收益。</p>
    <div class="meta"><span class="chip">研究日 2026-08-10</span><span class="chip">最新收盘 HK$46.64 · 2026-08-07</span><span class="chip">provisional</span><span class="chip">needs_human_review</span></div>
  </header>

  <nav aria-label="报告导航">
    <a href="#summary">结论</a><a href="#risk-reward">胜率/赔率</a><a href="#drawdown">回撤归因</a><a href="#quarter">Q1/Q2</a><a href="#cycle">周期</a><a href="#financials">五年财务</a>
    <a href="#owner-earnings">Owner earnings</a><a href="#market-pricing">估值</a><a href="#capital">流通/稀释</a>
    <a href="#event-monitor">事件</a><a href="#dimensions">25×50×9</a><a href="#evidence">证据</a>
  </nav>

  <section id="status-legend">
    <h2>图例：先理解程度词，再读结论</h2>
    {table(legend, [("layer","层"),("term","状态词"),("meaning","读法")])}
    <p class="muted"><code>applicable</code>只代表维度适用且已有证据，不代表结果正面；<code>provisional</code>代表关键季度或分母尚未闭环。当前包不是<code>production_reviewed</code>。</p>
  </section>

  <section id="report-doors">
    <h2>两个入口：长期底稿与近期变量分开</h2>
    <div class="doors">
      <a class="card" href="#long-term"><strong>长期公司底稿</strong><p>业务、产品、客户、供应链、护城河、五年财务、owner earnings和每股经济。</p></a>
      <a class="card" href="#event-monitor"><strong>近期事件监控</strong><p>Q2财报、Q3交付、车型爬坡、行业价格战、空头与市场事件窗口。</p></a>
    </div>
  </section>

  <section id="summary">
    <h2>Executive Summary｜现在是不是好机会？</h2>
    <div class="two">
      <article class="answer good"><div class="q">未来十年每股价值靠什么</div><div class="verdict">靠产品—毛利—费用杠杆—现金穿透，不靠“智能车”标签。</div><p>小鹏需要把新车型竞争力转成交付与ASP，再把vehicle margin、技术服务收入和规模效应转成充分摊薄后的owner earnings。整车集成、制造、渠道、充电和大众合作比纯软件更难被模型直接取代，但这条复利链仍未被稳定盈利和现金验证。</p></article>
      <article class="answer"><div class="q">按当前价格，回报和下行是否合算</div><div class="verdict">赔率已改善，胜率仍只是中等；不是“跌多了就便宜”。</div><p>HK$46.64较最高收盘回撤57.0%，但TTM仍亏、2026H1交付同比下降且Q1现金/库存变差。三个月主观上涨胜率约50%，概率加权中点约HK${THREE_MONTH_EXPECTED_MIDPOINT:.0f}；十二个月非下行情景合计65%，概率加权中点约HK${TWELVE_MONTH_EXPECTED_MIDPOINT:.0f}，同时仍有约三成概率遭遇20%以上回撤。</p></article>
    </div>
    <div class="three">
      <div class="card"><div class="metric">−57.0%</div><p>从2025-11-11最高收盘至今；同期HSTECH约−18.0%。</p></div>
      <div class="card"><div class="metric">≈50%</div><p>三个月收在当前价之上的主观概率；财报前不是高胜率事件点。</p></div>
      <div class="card"><div class="metric">60%–65%</div><p>十二个月取得正回报的主观概率区间；依赖盈利修复兑现。</p></div>
    </div>
    <div class="callout green"><strong>直接结论：</strong>它更像“高波动、赔率开始可研究的拐点期权”，还不是“高胜率、低下行的价值机会”。真正改善胜率的不是股价再跌一点，而是8月24日同时出现vehicle margin、亏损、现金和Q3增长四项验证。</div>
  </section>

  <section id="risk-reward">
    <h2>胜率与潜在收益：短期事件赔率一般，十二个月赔率更好</h2>
    <p><strong>三个月：</strong>财报和月度交付决定重估方向，主观上涨胜率约50%，概率加权中点HK${THREE_MONTH_EXPECTED_MIDPOINT:.2f}，相对当前约{(THREE_MONTH_EXPECTED_MIDPOINT / PRICE_HKD - 1) * 100:+.1f}%。<strong>十二个月：</strong>非下行情景合计65%，概率加权中点HK${TWELVE_MONTH_EXPECTED_MIDPOINT:.2f}，相对当前约{(TWELVE_MONTH_EXPECTED_MIDPOINT / PRICE_HKD - 1) * 100:+.1f}%；但bear路径仍可到HK${TWELVE_MONTH_SCENARIOS[0]["price_low_hkd"]:.0f}–{TWELVE_MONTH_SCENARIOS[0]["price_high_hkd"]:.0f}。</p>
    <p class="chart-scroll-note">手机端可左右滑动查看完整区间 →</p>
    <div class="chart scenario-chart">{svg_scenario_ranges()}</div>
    {table(scenario_rows, [("horizon","窗口"),("case","情景"),("probability","主观概率"),("price_range","价格区间"),("return_range","相对HK$46.64"),("trigger","触发条件"),("basis","估值/事件口径")])}
    <h3>十二个月价格区间的可复算输入</h3>
    {table(twelve_month_assumptions, [("case","情景"),("revenue","下一12个月收入"),("ev_sales","EV/Sales"),("net_cash","期末净现金"),("implied_price","充分摊薄每股价格")])}
    <p class="muted">概率不是历史频率、期权隐含概率或券商一致预期，而是基于已披露交付、毛利、亏损、现金、稀释、趋势和事件窗口形成的取整研究先验。十二个月价格公式为：（下一12个月收入 × EV/Sales + 净现金）÷ HKD/CNY ÷ 2.0079bn充分摊薄股数。倍数以当前约0.82× FD EV/TTM销售为中心：bear压缩、base大致维持、bull才小幅扩张；没有使用同行中位数或“回到高点”倒推。这不是目标价，也不构成收益承诺。</p>
    <h3>8月24日后，什么数字会真正改变胜率</h3>
    {table(opportunity_gates, [("gate","状态"),("q2_threshold","Q2硬门槛"),("q3_threshold","Q3增长门槛"),("cash_test","现金质量门槛")])}
    <div class="callout"><strong>关键风险收益比：</strong>当前价的上行尾部确实大于高位，但下行仍不是“现金托底到没有风险”。只要盈利时间表继续后移，市场可以同时下调收入倍数和净现金，两层一起压价。</div>
  </section>

  <section id="drawdown">
    <h2>为什么从高位跌下来：不是单纯跟随指数，而是盈利预期被重置</h2>
    {table(drawdown_drivers, [("layer","层"),("evidence","可核对证据"),("read","正确读法")])}
    <p>最高收盘日到现在，小鹏约跌57.0%，同期HSTECH约跌18.0%，相对落后约39个百分点。最合理的组合解释是：2025的高交付增长、首次季度盈利和AI/智能驾驶期权被提前定价，随后Q1亏损恢复、H1交付下滑和现金/库存压力让市场撤回这部分预期。它不证明公司永久变差，但说明HK$108.50不是应当自动回归的“正常价格”。</p>
  </section>

  <section id="long-term">
    <h2>长期底稿：真正要买的是哪条变量链</h2>
    <p>新车型/改款竞争力 → 订单与交付 → 车型组合与ASP → vehicle margin → 研发/销售费用杠杆 → CFO → 扣维持投入后的充分摊薄每股owner earnings。任何一段断裂，都可能出现“销量增长、股东每股价值不增长”。</p>
    <div class="three">
      <div class="card"><div class="metric">429,445</div><p>2025交付，+125.9%；规模拐点已发生。</p></div>
      <div class="card"><div class="metric">12.8%</div><p>2025 vehicle margin；仍低于理想17.9%，也低于蔚来14.6%。</p></div>
      <div class="card"><div class="metric">−15.8%</div><p>2026H1交付同比；目前还不是持续加速。</p></div>
    </div>
  </section>

  <section id="business">
    <h2>业务与产品：小鹏不只有一款车，也不只有卖车</h2>
    {table(products, [("layer","层"),("products","产品/资产"),("monetization","怎么变现"),("evidence","关键证据")])}
    {table(REVENUE_MIX, [("line","收入线"),("fy2024_rmb_m","2024 RMBm"),("fy2025_rmb_m","2025 RMBm"),("fy2025_share_pct","2025占比%"),("yoy_pct","同比%"),("economics","经济性")])}
    <p>主业仍是整车，服务收入不是纯SaaS：包含技术研发/平台软件、配件、碳积分、充电、维护、金融和二手车等。大众技术合作验证能力，也形成单一合作方依赖。</p>
  </section>

  <section id="customers">
    <h2>客户、上游和价值链：谁付款、谁卡住现金</h2>
    {table(value_chain, [("side","位置"),("who","公司/客户类别"),("concentration","集中度"),("risk","观察风险")])}
    <div class="callout"><strong>关系边界：</strong>大众是股东兼主要技术合作客户；汇天飞行汽车由何小鹏显著影响，是关联方。飞行汽车主题不能自动计入小鹏并表整车收入和估值。</div>
  </section>

  <section id="quarter">
    <h2>最关键的Q1/Q2变化：Q2交付已知，财务仍未知</h2>
    {table(q_compare, [("metric","指标"),("2025Q1","2025Q1"),("2026Q1","2026Q1"),("yoy","同比"),("2026Q2","2026Q2"),("read","读法")])}
    <div class="chart">{svg_quarters()}</div>
    <p>Q1服务收入增长且综合毛利率上升，但汽车收入下滑、经营和净亏损扩大，现金类资产较年末下降约55.7亿元、库存上升约29.1亿元。Q2收入指引只是一条管理层区间，不能冒充实际结果。</p>
    <h3>2025Q2对比2026Q2：数量相同，质量尚未揭晓</h3>
    {table(Q2_CROSS_YEAR, [("metric","指标"),("q2_2025","2025Q2实际"),("q2_2026","2026Q2已知/指引"),("yoy","同比"),("decision_read","决策读法")])}
    <p class="callout blue"><strong>2025Q2算不算“很惊喜”？</strong>交付103,181辆和收入RMB18.27bn都落在此前官方指引内，分别较指引中点约−1.7%和+0.9%，因此量和收入不是大幅超指引；真正改善的是vehicle margin从Q1的10.5%升至14.3%、净亏损环比收窄约28.1%。2026Q2交付几乎复制去年，但毛利、亏损、现金和Q3指引要到8月24日才知道。</p>
  </section>

  <section id="cycle">
    <h2>行业是否在周期底部：分四个周期回答</h2>
    {table(cycle, [("cycle","周期"),("state","状态"),("evidence","证据"),("implication","含义")])}
    <p>中国汽车总量在2026H1同比下滑，但NEV仍增长并接近50%渗透率。小鹏更像“公司产品周期可能见底”，不是“行业需求深度见底”。如果行业增长而公司H1下滑，不能把行业beta当成公司alpha。</p>
  </section>

  <section id="ai">
    <h2>模型降价、开源与能力增强：对小鹏是利好还是利空</h2>
    <div class="two">
      <div class="card"><h3>利好机制</h3><ul><li>训练/推理成本下降，缩短功能迭代。</li><li>更强模型提升座舱、感知、规划和机器人能力。</li><li>大众等合作方更容易验证平台商业价值。</li></ul></div>
      <div class="card"><h3>利空机制</h3><ul><li>基础模型商品化，软件溢价和营销差异缩小。</li><li>大厂/芯片厂/开源方案降低OEM自研门槛。</li><li>若安全、体验和成本没有领先，研发投入难回收。</li></ul></div>
    </div>
    <div class="callout blue"><strong>净判断：</strong>模型厂商很难直接替代整车制造、认证、渠道、售后和充电网络，因此“被模型直接取代”的风险低于纯AI应用；但模型会压缩ADAS软件差异。最终护城河必须落在整车集成、安全验证、数据闭环、制造质量、成本、品牌、渠道和VW验证。</div>
  </section>

  <section id="financials">
    <h2>五年财务：2025大幅改善，但一个好年份还不是稳定复利</h2>
    {table(FINANCIALS, [("period","年度"),("deliveries","交付"),("revenue","收入 RMBm"),("gross_profit","毛利 RMBm"),("gross_margin_pct","毛利率%"),("operating_profit","经营损益 RMBm"),("parent_net_income","归属净损益 RMBm"),("cfo","OCF RMBm"),("free_cash_flow","FCF RMBm")])}
    <div class="chart">{svg_financials()}</div>
    <p>2023毛利率触底1.47%，2025回升至18.87%；经营亏损从2023年的108.89亿元收窄至27.71亿元。Q4首次盈利后，2026Q1又亏17.84亿元，因此利润拐点尚未确认。</p>
  </section>

  <section id="owner-earnings">
    <h2>Owner earnings桥：为什么2025正FCF不能直接年化</h2>
    {table(OWNER_EARNINGS, [("case","口径"),("rmb_m","RMBm"),("formula","公式"),("meaning","边界")])}
    <div class="chart">{svg_owner_earnings()}</div>
    <p>2025 CFO中的应付账款、应计负债与递延收入增加贡献，部分被库存、分期应收和预付款吸收，净顺风约74.18亿元。上限口径正、压力测试口径负，说明目前最诚实的结论是“分母不稳定”，而不是挑一个看起来便宜的倍数。</p>
  </section>

  <section id="capital">
    <h2>股本、流通稀缺度与潜在供给</h2>
    {table(SHARES, [("layer","股本层"),("shares","股份数"),("status","状态"),("increment_pct","相对当前新增%")])}
    <p>最新确认A类15.674亿股、B类3.487亿股；监管公开流通量只确认至少25%合规，精确值未披露。研究代理在扣除创始人A股、Brian Gu和大众战略持股后约14.25亿A股，约等于86个20日平均成交日，<strong>不是</strong>监管free float。</p>
    <div class="callout"><strong>已知供给：</strong>剩余RSU约6,349.6万股，DiDi交易最高或有2,833.1万股，合计情景稀释约4.79%。截至月报，可转债栏为not applicable；风险来自奖励与或有股份，不是“低于某转股价就还钱”的CB结构。</div>
  </section>

  <section id="short">
    <h2>空头力量：连续三周回落，但买盘还没有接力</h2>
    {table(short_rows, [("date","申报日"),("shares","SFC空仓股数"),("pct_total","占总经济股本%"),("trend","周变化")])}
    <p>2026-07-31报告空仓约1.514亿股，相当于总股本7.90%、上市A股约9.66%，约10个最新20日平均成交日；较7月10日高点减少约8.9%。这降低了边际空头供给，但同期股价仍弱、最新成交量只有20日均量0.81倍，更像“空头减仓但多头承接不足”，不是独立买入信号。SFC汇总还可能包含对冲/套利，不能等同净方向空头或借券费。</p>
  </section>

  <section id="market-pricing">
    <h2>估值与长周期价格位置：低于高点，不等于低估</h2>
    {table(MARKET_STATE, [("metric","市场指标"),("value","值"),("unit","单位"),("as_of","日期"),("comparison","对照")])}
    {table(valuation, [("metric","指标"),("value","值"),("formula","公式"),("use","使用边界")])}
    <p>股价低于MA20、MA60和MA200，过去60个交易日约-25.5%；相对900日最高收盘回撤57.0%，相对盘中高点回撤57.9%。这说明趋势和情绪偏弱，不说明内在价值。由于TTM仍亏且owner earnings跨越正负，历史PE分位数不可用。</p>
    <h3>外部一致预期只作情绪交叉检查</h3>
    {table([CONSENSUS_DIAGNOSTICS], [("as_of","日期"),("security","证券"),("analyst_count","目标价数量"),("target_low_usd","低值USD"),("target_average_usd","均值USD"),("target_median_usd","中位USD"),("target_high_usd","高值USD"),("use","边界")])}
    <p>二级页面引用S&amp;P Global的25个XPEV ADS目标价，区间US$15.04–28.11、均值US$22.04。跨度接近一倍，说明分析师对扭亏速度分歧很大；它只验证“上行想象仍在”，不能替代本报告的经营门槛和充分摊薄计算。</p>
  </section>

  <section id="peers">
    <h2>同行比较：小鹏增长快，但利润和vehicle margin还未领先</h2>
    {table(PEERS, [("company","公司"),("role","可比角色"),("deliveries","2025交付"),("delivery_yoy_pct","同比%"),("revenue_rmb_bn","收入 RMBbn"),("vehicle_or_group_margin_pct","vehicle/集团毛利率%"),("net_income_rmb_bn","净损益 RMBbn"),("comparison","边界")])}
    <p>零跑使用集团毛利率，不能与vehicle margin直接横比；理想和蔚来的产品/服务结构也不同。该表用于识别“规模—毛利—盈利”的相对位置，不据此机械套目标倍数。比亚迪和Tesla因规模、整合及业务范围差异被排除。</p>
    <p class="muted">理想与蔚来数字来自各自2025官方业绩发布，尚未进入本包的正文快照哈希；零跑已用HKEX主源冻结。下一版应补齐同日市值、净现金和会计口径后再做相对估值。</p>
  </section>

  <section id="us-mapping">
    <h2>美国映射：同一上市、供应链与主题不能混写</h2>
    {table(us_map, [("security_or_company","美股/公司"),("mapping","映射类型"),("relation","关系"),("use","正确用法")])}
    <p>XPEV不是美国同行，而是同一经济主体的ADS。跨市场价差必须先按1 ADS=2 A股和汇率换算，再考虑交易时段、流动性与可转换性，不能把两边市值相加。</p>
  </section>

  <section id="event-monitor">
    <h2>大事件与5/20日股价窗口：只记录共振，不伪造因果</h2>
    {table(EVENTS, [("date","日期"),("event","事件"),("t0_pct","T0%"),("t5_pct","T+5%"),("t20_pct","T+20%"),("t5_excess_hstech_pct","T+5超额HSTECH%"),("causal_confidence","因果置信")])}
    <p>2025Q2后五日反应最强，2025Q3后最弱；但产品发布、宏观、行业价格战和指数波动重叠。事件窗用于衡量市场如何重新定价，不证明单一公告造成全部涨跌。</p>
  </section>

  <section id="timeline">
    <h2>时间线与下一硬催化</h2>
    {table(timeline, [("date","日期"),("event","事件"),("class","证据类别"),("next","下一验证")])}
    <p>公司已确认在2026年8月24日20:00（北京时间）发布Q2结果并举行电话会。7月交付38,027辆，同比+4%但环比6月下降约5.2%；因此当前证据是“低点修复”，还不是“增速重新抬升”。</p>
  </section>

  <section id="buffett">
    <h2>巴菲特—芒格式解释：好公司与好价格都尚未完成证明</h2>
    <div class="two">
      <div class="card"><h3>最强正方</h3><ul><li>2025交付、收入、毛利改善幅度大。</li><li>整车+软件+充电网络比纯模型应用更难被直接替代。</li><li>大众股权和技术合作提供外部验证。</li><li>净金融现金提供产品周期调整时间。</li></ul></div>
      <div class="card"><h3>最强反方</h3><ul><li>Q1收入/交付下滑、亏损扩大，Q4盈利未持续。</li><li>2025现金质量高度依赖供应商融资。</li><li>价格战、成本涨价与模型商品化压缩差异。</li><li>双层投票、RSU和或有股份影响少数股东每股结果。</li></ul></div>
    </div>
    <p>“买变量”在这里的含义不是抢先押注，而是预先写出晋级条件：Q3同比增长、vehicle margin不弱于约12%–14%、R&D/销售费用率下降、库存和现金稳定、充分摊薄每股owner earnings转正。任何一项不能被披露验证，就保留provisional。</p>
  </section>

  <section id="monitor">
    <h2>未来趋势与失效条件：下一次只检查这些</h2>
    {table(combined["invalidation_tests"], [("test","测试"),("trigger","触发"),("next_evidence","下一证据")])}
    <div class="callout green"><strong>未来12个月基准路径：</strong>Q2收入在指引内、亏损环比收窄；Q3由环比恢复进入同比增长；车型组合支撑vehicle margin；现金消耗趋稳。缺一项，都不能把产品周期低点升级为盈利周期反转。</div>
  </section>

  <section id="dimensions">
    <h2>公开研究契约：25维度、50指标、九道Gate</h2>
    <p>下表把方法论显式展示给读者，而不是只留在JSON。25个维度严格各含2个指标，共50个；结果是覆盖状态，不是评分。</p>
    <div class="table-wrap"><table><thead><tr><th>维度</th><th>状态</th><th>两个指标</th><th>本公司结论</th></tr></thead><tbody>{''.join(dimension_rows)}</tbody></table></div>
    <h3>九道证据闸门</h3>
    <div class="table-wrap"><table><thead><tr><th>Gate</th><th>结果</th><th>理由</th></tr></thead><tbody>{gate_rows}</tbody></table></div>
  </section>

  <section id="methodology">
    <h2>方法论与可复算资产</h2>
    <p>长期公司底稿与短期事件监控分开；先对齐证券、期间、货币与股数，再搭报表利润→现金→owner earnings桥；估值在分母可靠后才执行。周期判断同时拆行业、公司产品、盈利现金和市场情绪。</p>
    <p><a href="../listed-company-fundamentals-event-research-methodology.html">完整方法论</a> · <a href="combined-artifact.v2.json">组合研究artifact</a> · <a href="source-ledger.json">来源账本</a> · <a href="evidence-index.json">证据索引</a> · <a href="validator-results.json">校验结果</a></p>
  </section>

  <section id="evidence">
    <h2>关键证据抽屉：页码、行号、期间、公式与哈希</h2>
    <p>SEC HTML使用本次冻结快照的近似全局行号；PDF使用页码/表名；API为单行JSON。所有定位都需配合原文与SHA-256复核。</p>
    {evidence_html(source_by_id)}
  </section>

  <section id="sources">
    <h2>来源账本</h2>
    <div class="table-wrap"><table><thead><tr><th>ID</th><th>层级</th><th>来源</th><th>日期</th><th>范围</th><th>链接</th></tr></thead><tbody>{source_rows}</tbody></table></div>
    <p class="muted">公开研究支持，不是投资建议、目标价或具名人工批准。状态：<span class="status">needs_human_review</span>。</p>
  </section>
</main>
</body>
</html>
"""
    return report


def main() -> None:
    combined = build_combined()
    evidence_anchors = build_evidence_anchors()
    dump_json(ROOT / "combined-artifact.v2.json", combined)

    write_csv(DATA / "financial-history.csv", FINANCIALS)
    write_csv(DATA / "quarterly-inflection.csv", QUARTERS)
    write_csv(DATA / "revenue-mix.csv", REVENUE_MIX)
    write_csv(DATA / "owner-earnings-bridge.csv", OWNER_EARNINGS)
    write_csv(DATA / "fully-diluted-share-bridge.csv", SHARES)
    write_csv(DATA / "peer-operating-comparison.csv", PEERS)
    write_csv(DATA / "event-price-reactions.csv", EVENTS)
    write_csv(DATA / "market-state.csv", MARKET_STATE)
    write_csv(DATA / "risk-reward-scenarios.csv", THREE_MONTH_SCENARIOS + TWELVE_MONTH_SCENARIOS)
    write_csv(DATA / "consensus-diagnostics.csv", [CONSENSUS_DIAGNOSTICS])
    write_csv(DATA / "gate-results.csv", GATES)
    write_csv(
        DATA / "research-dimensions.csv",
        [
            {
                "dimension": row["dimension"],
                "status": row["status"],
                "indicator_1": row["indicators"][0]["id"],
                "indicator_2": row["indicators"][1]["id"],
                "summary": row["summary"],
            }
            for row in combined["research_dimensions"]
        ],
    )
    write_csv(
        DATA / "critical-evidence-locators.csv",
        [
            {
                "id": row["id"],
                "claim_id": row["claim_id"],
                "source_id": row["source_id"],
                "document_sha256": row["document_sha256"],
                "page": row["page"],
                "section_or_table": row["text_locator"]["section_or_table"],
                "page_line_start": row["text_locator"]["page_line_start"],
                "page_line_end": row["text_locator"]["page_line_end"],
                "text_snapshot_sha256": row["text_locator"]["text_snapshot_sha256"],
                "page_text_sha256": row["text_locator"]["page_text_sha256"],
                "period": row["period"],
                "unit": row["unit"],
                "currency": row["currency"],
                "scope": row["scope"],
                "audit_status": row["audit_status"],
                "source_text": row["source_text"],
                "formula": row["formula"],
                "limitations": row["limitations"],
            }
            for row in evidence_anchors
        ],
        [
            "id",
            "claim_id",
            "source_id",
            "document_sha256",
            "page",
            "section_or_table",
            "page_line_start",
            "page_line_end",
            "text_snapshot_sha256",
            "page_text_sha256",
            "period",
            "unit",
            "currency",
            "scope",
            "audit_status",
            "source_text",
            "formula",
            "limitations",
        ],
    )
    dump_json(
        DATA / "critical-evidence-anchors.json",
        {
            "schema_version": "seed.company-critical-evidence-anchors.v1",
            "generated_at": "2026-08-10T01:52:00+08:00",
            "company": {"name": "XPeng Inc.", "ticker": "09868", "exchange": "HKEX"},
            "status": "needs_human_review",
            "anchors": evidence_anchors,
        },
    )

    report = build_report(combined)
    (ROOT / "report.html").write_text(report, encoding="utf-8")
    subprocess.run(
        [sys.executable, str(REPO / "docs/company-event-timeline/build_timeline.py"), "--company", "xpeng"],
        check=True,
        cwd=REPO,
    )

    source_ledger = {
        "schema_version": "seed.company-research-source-ledger.v1",
        "company": "XPeng Inc.",
        "security_id": "XHKG:09868",
        "as_of": RESEARCH_DATE,
        "sources": [
            {
                "id": row["id"],
                "tier": row["tier"],
                "kind": row["source_type"],
                "title": row["title"],
                "published_at": row["published_at"],
                "retrieved_at": RESEARCH_DATE,
                "url": row["url"],
                "snapshot_sha256": row["content_sha256"],
                "used_for": row["covers"],
                "limitations": "Used within stated period, audit status and scope; market data remains a third-party snapshot." if row["tier"] == "C" else "Primary record used within stated period, audit status and scope.",
            }
            for row in SOURCES
        ],
    }
    dump_json(ROOT / "source-ledger.json", source_ledger)

    evidence_index = {
        "schema_version": "seed.company-research-evidence-index.v1",
        "company": "XPeng Inc.",
        "security_id": "XHKG:09868",
        "as_of": RESEARCH_DATE,
        "status": "needs_human_review",
        "combined_artifact": {
            "path": "combined-artifact.v2.json",
            "sha256": sha(ROOT / "combined-artifact.v2.json"),
        },
        "anchors": [
            {
                **row,
                "price_move_attribution": "not_used_for_causal_price_attribution",
                "review": "machine_checked_needs_human_review",
                "disclaimer": "fact_evidence_not_investment_advice",
            }
            for row in evidence_anchors
        ],
    }
    dump_json(ROOT / "evidence-index.json", evidence_index)

    red_team = {
        "schema_version": "seed.company-research-red-team.v1",
        "company": "XPeng Inc.",
        "security_id": "XHKG:09868",
        "reviewed_at": "2026-08-10T01:52:00+08:00",
        "status": "needs_human_review",
        "reviewer_or_agent": "codex-independent-adversarial-review-agent",
        "counter_thesis": "Q2交付环比修复可能只是车型和基数效应；价格战、成本、研发与营运资本可能继续阻断每股owner earnings。",
        "strongest_disconfirming_evidence": combined["red_team"],
        "next_review": {
            "event": "2026Q2 financial results and 2026Q3 deliveries",
            "minimum_checks": ["revenue", "vehicle margin", "net loss", "CFO", "inventory", "cash", "fully diluted shares"],
        },
        "unresolved_issues": [
            "2026Q2财务结果尚未发布，收入、vehicle margin、亏损、现金流和Q3指引均待验证。",
            "维持与增长资本开支未拆分，正常化owner earnings仍跨越正负。",
            "同行市值、净现金和盈利口径尚未统一到同一价格日，不使用精确同行倍数中位数。",
            "监管public float与借券费/利用率不可得，SFC空仓可能包含对冲和套利。",
            "尚无具名人工reviewer批准本反方结论。",
        ],
        "disclaimer": "Independent evidence red-team; not investment advice or named human approval.",
    }
    dump_json(ROOT / "red-team.json", red_team)

    readme = """# 小鹏汽车 09868.HK / XPEV 公开研究包

入口：[`report.html`](report.html)

本包以 2026-08-10 为研究截止日，最新可得港股收盘为 2026-08-07 的 HK$46.64；主证券为港股 09868.HK，NYSE:XPEV 是同一发行人的 ADS 映射，不作为同行重复计价。

核心结论：相对最高收盘回撤 57.0% 后，赔率已经改善，但胜率仍只属中等。三个月主观上涨概率约 50%；十二个月正回报概率约 60%—65%，同时仍有约三成概率遭遇 20% 以上回撤。2026Q2 交付只确认环比修复，下一次必须用 Q2 财务、Q3 同比交付、vehicle margin、现金/库存和充分摊薄每股 owner earnings 联合验证。

状态：`provisional / needs_human_review`。公开研究支持，不是投资建议。
"""
    (ROOT / "README.md").write_text(readme, encoding="utf-8")

    sys.path.insert(0, str(REPO / "skills/research-buffett-munger-company/scripts"))
    from company_research_validation import validation_summary
    from validate_report_template_parity import validate_report_html

    validation = validation_summary(
        combined,
        artifact_path="docs/xpeng-09868-hk/combined-artifact.v2.json",
    )
    parity = validate_report_html(ROOT / "report.html")
    validator_results = {
        "schema_version": "seed.company-research-validator-results.v1",
        "generated_at": "2026-08-10T01:52:00+08:00",
        "directory": ROOT.name,
        "artifact_status": combined["status"],
        "valid": validation["valid"] and parity["valid"],
        "publication_ready": validation["valid"] and parity["valid"],
        "production_reviewed_ready": False,
        "core_validation": validation,
        "template_parity": parity,
        "counts": {
            "sources": len(SOURCES),
            "dimensions": len(combined["research_dimensions"]),
            "indicators": sum(len(row["indicators"]) for row in combined["research_dimensions"]),
            "gates": len(combined["gates"]),
            "evidence_anchors": len(EVIDENCE),
        },
        "errors": validation["errors"] + parity["errors"],
        "warnings": validation["warnings"] + parity["warnings"],
    }
    dump_json(ROOT / "validator-results.json", validator_results)
    if not validator_results["valid"]:
        raise SystemExit(json.dumps(validator_results["errors"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
