#!/usr/bin/env python3
# ruff: noqa: E501
"""Build the public Horizon Robotics Buffett–Munger research package."""

from __future__ import annotations

import csv
import hashlib
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
DATA = ROOT / "data"
DATA.mkdir(parents=True, exist_ok=True)

RESEARCH_DATE = "2026-07-29"
PRICE_DATE = "2026-07-29"
PRICE_TIME = "2026-07-29 11:59:59 HKT"
PRICE_HKD = 5.20
HKD_CNY = 0.86627  # 2026-07-28 CFETS midpoint; one-day timing mismatch is disclosed.


def dump_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict], fields: list[str] | None = None) -> None:
    if fields is None:
        fields = list(dict.fromkeys(key for row in rows for key in row))
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(rows: list[dict], columns: list[tuple[str, str]]) -> str:
    head = "".join(f"<th>{html.escape(label)}</th>" for _, label in columns)
    body = []
    for row in rows:
        cells = []
        for key, _ in columns:
            value = row.get(key)
            if value is None:
                rendered = "—"
            elif isinstance(value, float):
                rendered = f"{value:,.2f}"
            else:
                rendered = str(value)
            cells.append(f"<td>{html.escape(rendered)}</td>")
        body.append("<tr>" + "".join(cells) + "</tr>")
    return (
        '<div class="table-wrap"><table><thead><tr>'
        + head
        + "</tr></thead><tbody>"
        + "".join(body)
        + "</tbody></table></div>"
    )


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


sources = [
    source(
        "H01",
        "A",
        "exchange_filing",
        "Horizon Robotics Annual Report 2025",
        "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0430/2026043001830.pdf",
        "2026-04-30",
        "FY2025",
        "audited",
        "consolidated_group",
        [
            "financial_statements",
            "revenue",
            "cash_flow",
            "operating_kpis",
            "customers",
            "suppliers",
            "share_capital",
            "governance",
        ],
        "0667e8c87a9c468ee661ddf9c42df733f860ac27c598894a7e17076e54dbaba2",
    ),
    source(
        "H02",
        "A",
        "exchange_filing",
        "Horizon Robotics Annual Report 2024",
        "https://www1.hkexnews.hk/listedco/listconews/sehk/2025/0421/2025042100203.pdf",
        "2025-04-21",
        "FY2024",
        "audited",
        "consolidated_group",
        ["financial_statements", "cash_flow", "historical_comparatives"],
        "bf7ae5c187555a7f07ada9a416c74c631cdf76034d3eb3b4a611e0f754b2a69d",
    ),
    source(
        "H03",
        "A",
        "exchange_announcement",
        "Update on Financial Performance for 2026H1",
        "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0721/2026072100145.pdf",
        "2026-07-21",
        "2026H1",
        "unaudited",
        "continuing_operations_preliminary",
        ["revenue", "gross_profit", "adjusted_loss", "scope_change"],
        "90c28ab22371807a57f500b4e80f1f961a88f177f72e148cde903884ed49ede5",
    ),
    source(
        "H04",
        "A",
        "exchange_announcement",
        "Amendment to CARIAD Convertible Loan Agreement",
        "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0722/2026072200813.pdf",
        "2026-07-22",
        "2026-07-22",
        "not_applicable",
        "listed_security",
        ["convertible_loan", "cash_payment", "dilution", "lock_up"],
        "9299edf67c5c79cf2a84434ce2dd99fb19e7fb861b0d85b2d0b61e6f1490ecfe",
    ),
    source(
        "H05",
        "A",
        "exchange_announcement",
        "US$450m Zero-Coupon Convertible Bonds due 2027",
        "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0723/2026072300027.pdf",
        "2026-07-23",
        "2026-07-23",
        "not_applicable",
        "listed_security",
        ["convertible_bond", "conversion_price", "dilution", "use_of_proceeds"],
        "0f535ba2e7cfd76a58f00c4879a63254b20ecab583a61f88c2125486dc9d16eb",
    ),
    source(
        "H06",
        "A",
        "exchange_announcement",
        "Grant of Awards under Post-IPO Share Incentive Plan",
        "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0726/2026072600115.pdf",
        "2026-07-26",
        "2026-07-26",
        "not_applicable",
        "listed_security",
        ["share_awards", "vesting", "dilution", "governance"],
        "b4474eb3648482f6d3e706b234dfdd03028bdfdae62f20952bbaaa468051438f",
    ),
    source(
        "H07",
        "A",
        "monthly_return",
        "Monthly Return for June 2026",
        "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0707/2026070700556.pdf",
        "2026-07-07",
        "2026-06-30",
        "not_applicable",
        "listed_security",
        ["issued_shares", "treasury_shares", "awards", "convertible_loan"],
        "abf43ab7dce878f14dd39a36456f28f5a8a520da6ebc8b9246e6ea1bb330f1b6",
    ),
    source(
        "H08",
        "A",
        "prospectus_section",
        "Horizon Robotics Prospectus — Business",
        "https://www1.hkexnews.hk/listedco/listconews/sehk/2024/1016/11405812/2024101600041.pdf",
        "2024-10-16",
        "IPO",
        "not_applicable",
        "issuer_business_disclosure",
        [
            "design_win_conversion",
            "customer_validation_cycle",
            "supply_chain",
            "revenue_recognition",
        ],
        "fb5db62c903ef286c5b2fbaa30d41d18cc06d96456b011ae06b45003b588c860",
    ),
    source(
        "M01",
        "C",
        "market_data_snapshot",
        "Tencent 09660.HK quote snapshot",
        "https://qt.gtimg.cn/q=r_hk09660",
        "2026-07-29",
        PRICE_TIME,
        "not_applicable",
        "listed_security",
        ["price", "share_count", "market_cap", "volume"],
        "57e0ae1a74e9549c1baf9d568504a7bda92d2d0e195db6dbf006f98b371d7c26",
    ),
    source(
        "M02",
        "C",
        "market_data_snapshot",
        "Tencent 09660.HK daily k-line snapshot",
        "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=hk09660,day,,,640,qfq",
        "2026-07-28",
        "2024-10-24 to 2026-07-28",
        "not_applicable",
        "listed_security",
        ["price_history"],
        "946aca087665b805068bec6775dfed837fd4c1d67668b01b039a45481b7bdf1e",
    ),
    source(
        "M03",
        "B",
        "official_rate_republication",
        "CFETS-authorized RMB midpoint for 2026-07-28",
        "https://www.news.cn/20260728/b7ed4efa8ff94386901232d6bfca1df4/c.html",
        "2026-07-28",
        "2026-07-28",
        "not_applicable",
        "fx_midpoint",
        ["fx"],
        "8f7c99f440b784b57551ba069dced369f8501e35faa22a10e25dc5fbc5e4ebe2",
    ),
    source(
        "P01",
        "A",
        "exchange_filing",
        "Black Sesame International Annual Report 2025",
        "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0427/2026042701016.pdf",
        "2026-04-27",
        "FY2025",
        "audited",
        "peer_consolidated_group",
        ["peer_revenue", "peer_business", "peer_loss"],
        "ea8319cbb3bacf837fe92595d48e27dfddcb7a6e56170073ff50e69765bc9be4",
    ),
    source(
        "M04",
        "C",
        "market_data_snapshot",
        "Tencent 02533.HK quote snapshot",
        "https://qt.gtimg.cn/q=r_hk02533",
        "2026-07-29",
        "2026-07-29 11:59:59 HKT",
        "not_applicable",
        "peer_listed_security",
        ["peer_price", "peer_market_cap"],
        "a5e563f1e90b152cf40aca497ced9a4c0696fd0f95d60b5b8dc2fc502e9f1c5d",
    ),
    source(
        "P02",
        "A",
        "sec_10k",
        "Mobileye Global Inc. 2025 Form 10-K",
        "https://www.sec.gov/Archives/edgar/data/1910139/000110465926014300/mbly-20251227x10k.htm",
        "2026-02-12",
        "FY2025",
        "audited",
        "peer_consolidated_group",
        ["peer_revenue", "peer_cash_flow", "peer_business"],
        "fd30bf23b6d500166c51d2e465cc12fa3c00da2780d6a82290024d7d72405738",
    ),
    source(
        "P03",
        "A",
        "sec_10k",
        "Ambarella Inc. FY2026 Form 10-K",
        "https://www.sec.gov/Archives/edgar/data/1280263/000119312526119321/amba-20260131.htm",
        "2026-03-23",
        "FY2026",
        "audited",
        "peer_consolidated_group",
        ["peer_revenue", "peer_business", "peer_loss"],
        "aaf36816a758ddf734ca21dfa7cb8a3e33ac8e7661124d0395701da05e9fb82d",
    ),
]


financial_rows = [
    {
        "period": "FY2021",
        "revenue_rmb_m": 466.720,
        "gross_profit_rmb_m": 330.986,
        "operating_loss_rmb_m": -1335.333,
        "adjusted_net_loss_rmb_m": -1103.197,
        "cfo_rmb_m": None,
        "cash_owner_earnings_proxy_rmb_m": None,
        "source_refs": "H01",
    },
    {
        "period": "FY2022",
        "revenue_rmb_m": 905.676,
        "gross_profit_rmb_m": 627.713,
        "operating_loss_rmb_m": -2132.016,
        "adjusted_net_loss_rmb_m": -1891.363,
        "cfo_rmb_m": None,
        "cash_owner_earnings_proxy_rmb_m": None,
        "source_refs": "H01",
    },
    {
        "period": "FY2023",
        "revenue_rmb_m": 1551.607,
        "gross_profit_rmb_m": 1094.310,
        "operating_loss_rmb_m": -2030.522,
        "adjusted_net_loss_rmb_m": -1635.168,
        "cfo_rmb_m": -1744.508,
        "cash_owner_earnings_proxy_rmb_m": -2198.480,
        "source_refs": "H01/H02",
    },
    {
        "period": "FY2024",
        "revenue_rmb_m": 2383.554,
        "gross_profit_rmb_m": 1841.354,
        "operating_loss_rmb_m": -2144.240,
        "adjusted_net_loss_rmb_m": -1681.155,
        "cfo_rmb_m": 17.603,
        "cash_owner_earnings_proxy_rmb_m": -894.314,
        "source_refs": "H01/H02",
    },
    {
        "period": "FY2025",
        "revenue_rmb_m": 3758.268,
        "gross_profit_rmb_m": 2425.680,
        "operating_loss_rmb_m": -3338.791,
        "adjusted_net_loss_rmb_m": -2811.776,
        "cfo_rmb_m": -2106.052,
        "cash_owner_earnings_proxy_rmb_m": -2807.291,
        "source_refs": "H01",
    },
]
write_csv(DATA / "financial-history.csv", financial_rows)

owner_earnings_rows = [
    {
        "period": "FY2023",
        "cfo_rmb_m": -1744.508,
        "ppe_cash_capex_rmb_m": 259.446,
        "intangible_cash_capex_rmb_m": 194.526,
        "cash_oe_proxy_rmb_m": -2198.480,
        "lease_principal_interest_rmb_m": 60.140,
        "interest_income_rmb_m": 167.473,
        "strict_core_oe_proxy_rmb_m": -2426.093,
        "source_refs": "H02",
    },
    {
        "period": "FY2024",
        "cfo_rmb_m": 17.603,
        "ppe_cash_capex_rmb_m": 534.724,
        "intangible_cash_capex_rmb_m": 377.193,
        "cash_oe_proxy_rmb_m": -894.314,
        "lease_principal_interest_rmb_m": 64.639,
        "interest_income_rmb_m": 383.231,
        "strict_core_oe_proxy_rmb_m": -1342.184,
        "source_refs": "H01/H02",
    },
    {
        "period": "FY2025",
        "cfo_rmb_m": -2106.052,
        "ppe_cash_capex_rmb_m": 471.590,
        "intangible_cash_capex_rmb_m": 229.649,
        "cash_oe_proxy_rmb_m": -2807.291,
        "lease_principal_interest_rmb_m": 84.131,
        "interest_income_rmb_m": 399.608,
        "strict_core_oe_proxy_rmb_m": -3291.030,
        "source_refs": "H01",
    },
]
write_csv(DATA / "owner-earnings.csv", owner_earnings_rows)

revenue_mix_rows = [
    {
        "line": "汽车产品解决方案",
        "fy2024_rmb_m": 664.237,
        "fy2025_rmb_m": 1622.274,
        "fy2025_share_pct": 43.2,
        "fy2025_gross_margin_pct": 34.5,
        "adjusted_product_gm_ex_domain_controllers_pct": 42.5,
    },
    {
        "line": "汽车许可及服务",
        "fy2024_rmb_m": 1647.466,
        "fy2025_rmb_m": 1934.913,
        "fy2025_share_pct": 51.4,
        "fy2025_gross_margin_pct": 94.5,
        "adjusted_product_gm_ex_domain_controllers_pct": None,
    },
    {
        "line": "非汽车解决方案",
        "fy2024_rmb_m": 71.851,
        "fy2025_rmb_m": 201.081,
        "fy2025_share_pct": 5.4,
        "fy2025_gross_margin_pct": 18.1,
        "adjusted_product_gm_ex_domain_controllers_pct": None,
    },
]
write_csv(DATA / "revenue-mix.csv", revenue_mix_rows)

operating_rows = [
    {"stage": "车型定点/design-win", "metric": "2025新增", "value": ">110", "evidence_class": "正式披露，但非订单", "source_refs": "H01/H08"},
    {"stage": "HSD定点", "metric": "OEM/车型", "value": "10个品牌/>20款", "evidence_class": "定点，待逐款SOP", "source_refs": "H01"},
    {"stage": "实际出货", "metric": "Journey硬件", "value": "401万套/+38.8%", "evidence_class": "实际交付", "source_refs": "H01"},
    {"stage": "高阶结构", "metric": "NOA硬件占比", "value": "45%/出货4.8倍", "evidence_class": "公司年报披露", "source_refs": "H01"},
    {"stage": "HSD量产", "metric": "2025年11月后一个多月", "value": ">2.2万套", "evidence_class": "实际交付", "source_refs": "H01"},
    {"stage": "收入", "metric": "产品/许可", "value": "16.22亿/19.35亿元", "evidence_class": "审计收入", "source_refs": "H01"},
    {"stage": "回款代理", "metric": "应收净额/OCF", "value": "17.68亿元/-21.06亿元", "evidence_class": "现金尚未闭环", "source_refs": "H01"},
]
write_csv(DATA / "operating-funnel.csv", operating_rows)

customer_rows = [
    {"metric": "最大客户", "fy2024_pct": 31.50, "fy2025_pct": 18.11, "interpretation": "单一客户下降，但仍重大"},
    {"metric": "前四个>10%客户合计", "fy2024_pct": 52.49, "fy2025_pct": 56.01, "interpretation": "审计披露可直接相加"},
    {"metric": "前五客户", "fy2024_pct": None, "fy2025_pct": 60.4, "interpretation": "年报管理层披露"},
    {"metric": "CARIZON关联销售/总收入", "fy2024_pct": None, "fy2025_pct": 18.11, "interpretation": "由6.806亿元/37.583亿元推算；客户A身份是推断"},
]
write_csv(DATA / "customer-concentration.csv", customer_rows)

basic_shares = 14_571_723_185
cariad_shares = 1_301_763_486
cb_shares = 635_635_135
june_awards = 68_340_978
july_awards = 90_608_252
fd_shares = basic_shares + cariad_shares + cb_shares + june_awards + july_awards

dilution_rows = [
    {
        "stage": "最新确认已发行（不含库存股）",
        "shares": basic_shares,
        "incremental_shares": 0,
        "status": "已确认",
        "market_cap_hkd_bn_at_5_20": basic_shares * PRICE_HKD / 1e9,
    },
    {
        "stage": "CARIAD交割备考",
        "shares": basic_shares + cariad_shares,
        "incremental_shares": cariad_shares,
        "status": "截至截止日未见完成公告",
        "market_cap_hkd_bn_at_5_20": (basic_shares + cariad_shares) * PRICE_HKD / 1e9,
    },
    {
        "stage": "新CB按HK$5.55全转备考",
        "shares": basic_shares + cariad_shares + cb_shares,
        "incremental_shares": cb_shares,
        "status": "条件性潜在股份",
        "market_cap_hkd_bn_at_5_20": (basic_shares + cariad_shares + cb_shares) * PRICE_HKD / 1e9,
    },
    {
        "stage": "既有及7月奖励全计",
        "shares": fd_shares,
        "incremental_shares": june_awards + july_awards,
        "status": "已授予/尚未发行或转出",
        "market_cap_hkd_bn_at_5_20": fd_shares * PRICE_HKD / 1e9,
    },
]
write_csv(DATA / "dilution-bridge.csv", dilution_rows)

peer_rows = [
    {
        "company": "Mobileye",
        "ticker": "MBLY",
        "qualification": "直接全球ADAS芯片/系统；更成熟且现金为正",
        "market_cap_local_bn": 6.55218,
        "revenue_local_bn": 1.894,
        "ps": 3.46,
        "profitability": "2025 OCF US$602m",
        "source_refs": "P02/二级市值快照",
    },
    {
        "company": "Ambarella",
        "ticker": "AMBA",
        "qualification": "邻近边缘AI SoC；汽车仅部分收入",
        "market_cap_local_bn": 2.97519,
        "revenue_local_bn": 0.390702,
        "ps": 7.61,
        "profitability": "FY2026仍经营亏损",
        "source_refs": "P03/二级市值快照",
    },
    {
        "company": "黑芝麻智能",
        "ticker": "02533.HK",
        "qualification": "中国汽车智能SoC最直接同业",
        "market_cap_local_bn": 8.03093,
        "revenue_local_bn": 0.94929,
        "ps": 8.46,
        "profitability": "2025仍亏损",
        "source_refs": "P01/M04/M03",
    },
    {
        "company": "地平线机器人（当前股本）",
        "ticker": "09660.HK",
        "qualification": "主标的；未计已知潜在股份",
        "market_cap_local_bn": 75.77296,
        "revenue_local_bn": 4.33842,
        "ps": 17.47,
        "profitability": "2025现金OE为负",
        "source_refs": "H01/M01/M03",
    },
    {
        "company": "地平线机器人（已知全摊薄）",
        "ticker": "09660.HK FD",
        "qualification": "CARIAD+新CB全转+已授予奖励",
        "market_cap_local_bn": 86.67397,
        "revenue_local_bn": 4.33842,
        "ps": 19.98,
        "profitability": "备考，不是法定已发行股本",
        "source_refs": "H04/H05/H06/H07/M01/M03",
    },
]
write_csv(DATA / "peer-valuation.csv", peer_rows)

reverse_rows = [
    {"terminal_ps": 10.0, "revenue_needed_rmb_bn": 7.5083, "five_year_revenue_cagr_pct": 14.84, "revenue_needed_for_10pct_equity_return_rmb_bn": 12.0922, "five_year_cagr_for_10pct_return_pct": 26.33},
    {"terminal_ps": 7.615, "revenue_needed_rmb_bn": 9.8599, "five_year_revenue_cagr_pct": 21.28, "revenue_needed_for_10pct_equity_return_rmb_bn": 15.8795, "five_year_cagr_for_10pct_return_pct": 33.40},
    {"terminal_ps": 5.0, "revenue_needed_rmb_bn": 15.0166, "five_year_revenue_cagr_pct": 31.92, "revenue_needed_for_10pct_equity_return_rmb_bn": 24.1844, "five_year_cagr_for_10pct_return_pct": 45.11},
    {"terminal_ps": 3.46, "revenue_needed_rmb_bn": 21.7003, "five_year_revenue_cagr_pct": 42.00, "revenue_needed_for_10pct_equity_return_rmb_bn": 34.9486, "five_year_cagr_for_10pct_return_pct": 56.20},
]
write_csv(DATA / "reverse-valuation.csv", reverse_rows)

one_year_rows = [
    {
        "scenario": "审慎",
        "own_revenue_assumption_rmb_bn": 4.3,
        "fd_ps": 75.0831 / 4.3,
        "required_evidence": "定点转SOP偏慢；应收/库存仍快于收入；调整亏损未收窄",
        "status": "不可用PE",
    },
    {
        "scenario": "基准",
        "own_revenue_assumption_rmb_bn": 5.0,
        "fd_ps": 75.0831 / 5.0,
        "required_evidence": "HSD/J6出货增长；产品毛利约40%附近；现金损耗改善但未转正",
        "status": "不可用PE",
    },
    {
        "scenario": "强势",
        "own_revenue_assumption_rmb_bn": 5.8,
        "fd_ps": 75.0831 / 5.8,
        "required_evidence": "多个HSD车型SOP；高毛利许可扩散；亏损绝对额与营运资本同步改善",
        "status": "不可用PE",
    },
]
write_csv(DATA / "one-year-scenarios.csv", one_year_rows)

ten_year_rows = [
    {
        "required_equity_return_pct": 10,
        "terminal_owner_earnings_multiple": 20,
        "assumed_owner_earnings_margin_pct": 25,
        "year10_equity_value_rmb_bn": 194.746,
        "year10_owner_earnings_rmb_bn": 9.737,
        "year10_revenue_rmb_bn": 38.949,
        "revenue_multiple_vs_2025": 10.36,
        "ten_year_revenue_cagr_pct": 26.34,
    },
    {
        "required_equity_return_pct": 12,
        "terminal_owner_earnings_multiple": 18,
        "assumed_owner_earnings_margin_pct": 25,
        "year10_equity_value_rmb_bn": 233.197,
        "year10_owner_earnings_rmb_bn": 12.955,
        "year10_revenue_rmb_bn": 51.821,
        "revenue_multiple_vs_2025": 13.79,
        "ten_year_revenue_cagr_pct": 30.00,
    },
]
write_csv(DATA / "ten-year-reverse.csv", ten_year_rows)

cycle_rows = [
    {"stage": "BPU/算法/软件架构研发", "typical_time": "多年持续", "capital_or_risk": "研发人员、云训练、EDA/IP", "substitutability": "下一代平台高", "source_refs": "H01/H08"},
    {"stage": "芯片流片与量产准备", "typical_time": "代际性", "capital_or_risk": "tape-out、技术服务、耗材", "substitutability": "客户尚未锁定", "source_refs": "H01"},
    {"stage": "定点→合同", "typical_time": "2–4个月", "capital_or_risk": "方案、价格、合同谈判", "substitutability": "中高", "source_refs": "H08"},
    {"stage": "合同→SOP", "typical_time": "8–36个月", "capital_or_risk": "适配、验证、功能安全", "substitutability": "逐步下降", "source_refs": "H08"},
    {"stage": "晶圆制造+封装测试", "typical_time": "约5–7个月", "capital_or_risk": "单一代工来源、预付款、库存", "substitutability": "短期低", "source_refs": "H08"},
    {"stage": "已SOP当前车型", "typical_time": "车型平台生命周期", "capital_or_risk": "质量、供货、OTA", "substitutability": "中低", "source_refs": "H08"},
    {"stage": "下一代车型/中央计算", "typical_time": "重新RFQ", "capital_or_risk": "技术代际与价格重置", "substitutability": "再次升高", "source_refs": "H08"},
]
write_csv(DATA / "cycle-substitution.csv", cycle_rows)


crosswalk = json.loads(
    (
        REPO
        / "skills/research-buffett-munger-company/references/"
        "methodology-implementation-crosswalk.json"
    ).read_text(encoding="utf-8")
)
crosswalk_by_id = {row["id"]: row for row in crosswalk["dimensions"]}

dimension_specs = {
    "security_and_legal_subject": ("09660.HK是开曼注册WVR发行人；B股一票，A股十票。价格、股本、币种按日期绑定。", ["H01", "H07", "M01"], []),
    "control_and_beneficial_ownership": ("俞凯为最终控制人兼董事长/CEO；WVR与关联结构提高资本配置及少数股东监督要求。", ["H01", "H04", "H06"], ["未建立逐年投票权与所有受益安排变化的完整图。"]),
    "business_model": ("硬件出货叠加BPU、算法、基础模型和工具链许可；收入需经过定点、合同、验证、SOP、出货与回款。", ["H01", "H08"], []),
    "revenue_structure": ("2025产品43.2%、许可服务51.4%、非汽车5.4%；D-Robotics 2026年出表后持续经营口径发生变化。", ["H01", "H03"], ["尚无审计的2026H1完整分部与现金流。"]),
    "industry_chain_position": ("无晶圆厂Tier 2/生态赋能者；95%以上出货经生态伙伴，利润池在芯片、软件许可、Tier 1与OEM间分配。", ["H01", "H08"], []),
    "product_and_unit_economics": ("出货401万套、NOA占45%、单车价值量+75%；产品毛利降至34.5%，剔除低加价域控为42.5%。", ["H01"], []),
    "customers": ("前五客户占60.4%；CARIZON销售占比约18.11%与客户A相符，但客户身份仅为推断。", ["H01"], ["缺逐客户SOP、车型销量、取消率与回款。"]),
    "suppliers": ("招股书披露单一晶圆制造来源、预付款及约5–7个月制造封测周期；2025年报未明确证明已多元化。", ["H01", "H08"], ["2025供应商集中表无法单独识别晶圆代工。"]),
    "competition_structure": ("RFQ前替代性高；SOP后验证成本使替代性下降；下一代平台重新竞争。Mobileye、黑芝麻、Qualcomm、NVIDIA、华为和OEM自研构成不同层替代。", ["H01", "H08", "P01", "P02", "P03"], []),
    "durable_moat": ("可观察护城河是量产工程、软硬件协同、工具链与生态，而非不可替代的单颗芯片。", ["H01", "H08", "P01", "P02"], ["缺平台续标率、定点转SOP率与非关联客户留存。"]),
    "revenue_quality": ("审计收入增长57.7%，但应收约+151%、库存+82.6%，现金转换显著落后。", ["H01"], []),
    "earnings_quality": ("2024盈利和2026H1预告盈利受金融负债公允价值影响；调整后净亏损仍扩大，PE没有经济解释力。", ["H01", "H03"], []),
    "cash_conversion": ("2025 OCF为-21.06亿元；OCF减固定及无形投入为-28.07亿元，核心现金OE仍为负。", ["H01", "H02"], []),
    "working_capital": ("应收与库存增速快于收入；合同负债2.66亿元、未履约交易价10.12亿元不是完整硬件订单簿。", ["H01"], []),
    "capital_intensity": ("公司不自建晶圆厂，但研发、云服务、流片、IP/EDA、预付款、库存和客户验证形成真实资本周期。", ["H01", "H08"], []),
    "returns_on_capital": ("持续亏损、快速扩股及经营范围变化使ROIC暂不可作为正面质量证据。", ["H01", "H03", "H04", "H05"], ["维持/增长研发与正常营运资本尚未拆分。"]),
    "balance_sheet_survival": ("2025年末现金及定存208.25亿元，但旧CARIAD负债、3.989亿美元现金支付及新CB必须同时纳入。", ["H01", "H04", "H05"], []),
    "capital_allocation": ("2025配售、CARIAD重组、新CB及股份奖励把验证时间换成稀释/再融资成本；应以全摊薄每股OE衡量。", ["H01", "H04", "H05", "H06", "H07"], []),
    "management": ("管理层已兑现HSD首款量产及出货，但定点、合作意向与未来车型仍须按SOP和回款复核。", ["H01", "H03", "H08"], ["缺完整承诺—兑现逐年台账。"]),
    "governance_and_related_parties": ("WVR、创始人兼任董事长/CEO、CARIZON关联收入、创始人贷款及无业绩目标奖励均需持续监督。", ["H01", "H04", "H06"], []),
    "accounting_and_audit": ("FY2025获无保留审计意见；机器事实包仍有法定身份、股本规范化及比较期解析QA缺口。", ["H01", "H02"], ["公开包为needs_human_review，非具名人工签字。"]),
    "tax_and_legal": ("安全、数据、出口管制、功能安全和产品责任是主要尾部风险；本报告不提供法律判断。", ["H01", "H08"], ["未完成逐法域诉讼、制裁与数据合规清单。"]),
    "per_share_economics": ("最新已发行145.72亿股；CARIAD、新CB与已授予奖励全计为166.68亿股，潜在增幅14.39%。", ["H04", "H05", "H06", "H07", "M01"], []),
    "valuation": ("亏损期不使用PE；HK$5.20对应当前P/S约17.47倍、已知全摊薄约19.98倍，远高于三家校准中位约7.62倍。", ["H01", "H04", "H05", "H06", "H07", "M01", "M03", "P01", "P02", "P03", "M04"], ["P/S只能校准预期，不能代替owner earnings价值。"]),
    "disconfirming_evidence": ("最强反证是收入增长尚未转化为经营杠杆、现金OE或稳定每股分母；OEM自研和平台竞争会在下一代车型重新开启。", ["H01", "H03", "H08", "P01", "P02", "P03"], []),
}

research_dimensions = []
for dimension_id in [row["id"] for row in crosswalk["dimensions"]]:
    summary, refs, gaps = dimension_specs[dimension_id]
    indicators = []
    for indicator_id in crosswalk_by_id[dimension_id]["required_indicator_ids"]:
        indicators.append(
            {
                "id": indicator_id,
                "status": "observed",
                "summary": summary,
                "source_refs": refs,
                "source_gaps": gaps,
            }
        )
    research_dimensions.append(
        {
            "dimension": dimension_id,
            "status": "applicable",
            "summary": summary,
            "indicators": indicators,
            "source_refs": refs,
            "positive_evidence": [summary],
            "counter_evidence": gaps or ["观察到事实不等于正面结论，仍需按失效条件持续证伪。"],
            "source_gaps": gaps,
        }
    )

methodology_refs = [
    {
        "id": "berkshire_1986_letter",
        "title": "1986 Chairman's Letter",
        "url": "https://www.berkshirehathaway.com/letters/1986.html",
        "use": "Owner earnings definition and maintenance-capital discipline.",
    },
    {
        "id": "berkshire_1996_letter",
        "title": "1996 Chairman's Letter",
        "url": "https://www.berkshirehathaway.com/letters/1996.html",
        "use": "Circle-of-competence and predictable long-term economics gate.",
    },
    {
        "id": "berkshire_2007_letter",
        "title": "2007 Chairman's Letter",
        "url": "https://www.berkshirehathaway.com/letters/2007ltr.pdf",
        "use": "Durable moat, pricing power and capital-intensity interpretation.",
    },
]

gates = [
    {"gate": "identity_and_source_integrity", "result": "pass_with_scope", "reason": "证券、WVR、股本和主源已绑定；机器事实包仍需人工复核法定身份与股本规范化。"},
    {"gate": "circle_of_competence", "result": "pass_with_scope", "reason": "定点到现金的链条可解释；自动驾驶算法性能与安全尾部风险仍超出纯财务分析。"},
    {"gate": "business_economics", "result": "mixed_positive", "reason": "真实出货、ASP和许可增长成立，但产品毛利、应收、库存与亏损尚未证明经营杠杆。"},
    {"gate": "durable_moat", "result": "provisional", "reason": "量产工程和生态形成粘性，但下一代车型RFQ会重新开放竞争。"},
    {"gate": "management_and_capital_allocation", "result": "mixed", "reason": "管理层推进量产，同时配售、可转债、奖励和关联结构显著改变每股经济。"},
    {"gate": "owner_earnings", "result": "fail", "reason": "2023–2025两套现金OE代理均为负；不能用非现金公允价值利润替代。"},
    {"gate": "survival_and_balance_sheet", "result": "mixed", "reason": "现金储备提供验证时间，但CARIAD现金支付与新CB不能从净现金叙事中遗漏；负现金OE使其不能被表述成通过。"},
    {"gate": "intrinsic_value_and_margin_of_safety", "result": "blocked", "reason": "正的可持续owner earnings分母尚不存在；只能做P/S校准与反向预期。"},
    {"gate": "decision_and_disconfirming_evidence", "result": "inconclusive", "reason": "研究证据足以进入重点观察与条件晋级，但owner earnings与安全边际两道硬门禁未通过，当前不可形成价值投资决策。"},
]
write_csv(DATA / "gate-results.csv", gates)

dimension_csv_rows = []
for dimension in research_dimensions:
    for indicator in dimension["indicators"]:
        dimension_csv_rows.append(
            {
                "dimension": dimension["dimension"],
                "dimension_status": dimension["status"],
                "indicator": indicator["id"],
                "indicator_status": indicator["status"],
                "summary": dimension["summary"],
                "source_refs": "/".join(dimension["source_refs"]),
                "source_gaps": " | ".join(dimension["source_gaps"]),
            }
        )
write_csv(DATA / "research-dimensions.csv", dimension_csv_rows)

financial_periods = [
    {
        "period": row["period"],
        "period_type": "annual",
        "currency": "CNY",
        "unit": "million",
        "scope": "consolidated_group",
        "revenue": row["revenue_rmb_m"],
        "gross_profit": row["gross_profit_rmb_m"],
        "operating_profit": row["operating_loss_rmb_m"],
        "parent_net_income": None,
        "cfo": row["cfo_rmb_m"],
        "capex": None,
        "free_cash_flow": row["cash_owner_earnings_proxy_rmb_m"],
        "source_refs": list(dict.fromkeys(row["source_refs"].split("/"))),
    }
    for row in financial_rows
]

combined = {
    "schema_version": "seed.stock-fundamentals-valuation.v2",
    "artifact_type": "stock_fundamentals_valuation",
    "artifact_role": "combined_public_research_snapshot",
    "status": "needs_human_review",
    "generated_at": "2026-07-29T12:20:00+08:00",
    "security": {
        "security_id": "XHKG:09660",
        "ticker": "09660.HK",
        "exchange": "HKEX",
        "company_name": "Horizon Robotics",
        "company_name_zh": "地平线机器人",
        "listing_type": "Class B ordinary share with WVR",
        "currency": "HKD",
        "fiscal_year_end": "31 December",
        "reporting_standard": "IFRS",
    },
    "as_of": {
        "research_date": RESEARCH_DATE,
        "price_date": PRICE_DATE,
        "price": PRICE_HKD,
        "price_source_ref": "M01",
    },
    "methodology_refs": methodology_refs,
    "source_refs": sources,
    "source_boundaries": {
        "facts": "HKEX audited filings and exchange announcements take precedence. Design wins, planned SOP and management outlook retain their stated evidence class.",
        "reported_claims": "Market-share statistics and company press releases remain issuer claims unless independently corroborated.",
        "interpretations": "Moat, substitutability, cycle position, customer-A identity, peer qualification and reverse valuation are research interpretations.",
        "assumptions": "P/S uses a 2026-07-29 intraday HKD price and 2026-07-28 CFETS midpoint; fully diluted shares are event-scenario, not confirmed legal issued shares.",
        "source_gaps": "Do not fill missing order quantities, cancellation rates, customer-level SOP, maintenance capex, audited 2026H1 cash flow or pro-forma post-deconsolidation net cash with zero.",
    },
    "ownership_structure": {
        "controller": "Dr. Kai Yu; WVR beneficiary, chairman and CEO.",
        "voting_rights": "Class A carries ten votes per share except reserved matters; Class B carries one vote.",
        "fully_diluted_share_bridge": {
            "as_of": RESEARCH_DATE,
            "unit": "shares",
            "issued_excluding_treasury": basic_shares,
            "cariad_pro_forma": cariad_shares,
            "new_cb_full_conversion": cb_shares,
            "existing_unissued_awards": june_awards,
            "july_2026_awards": july_awards,
            "known_fully_diluted_scenario": fd_shares,
            "incremental_pct_vs_current": (fd_shares / basic_shares - 1) * 100,
            "old_holder_dilution_pct_of_enlarged": (1 - basic_shares / fd_shares) * 100,
            "source_refs": ["H04", "H05", "H06", "H07"],
            "limitations": [
                "CARIAD issuance and new CB conversion are pro-forma/potential as of the cut-off.",
                "Future ungranted scheme capacity is excluded.",
                "CARIAD existing shares and redeemed 716m conversion rights are not double counted.",
            ],
        },
    },
    "financial_history": {"periods": financial_periods},
    "segment_data": {
        "status": "applicable",
        "segments": [
            {"name": "Automotive product solutions", "FY2025_revenue_rmb_m": 1622.274, "gross_margin_pct": 34.5},
            {"name": "Automotive license and services", "FY2025_revenue_rmb_m": 1934.913, "gross_margin_pct": 94.5},
            {"name": "Non-automotive solutions", "FY2025_revenue_rmb_m": 201.081, "gross_margin_pct": 18.1},
        ],
        "source_refs": ["H01"],
    },
    "research_dimensions": research_dimensions,
    "earnings_quality_bridge": {
        "period": "FY2025",
        "currency": "CNY",
        "unit": "million",
        "reported_loss": -10469.366,
        "fair_value_loss_preferred_and_other_liabilities": -6664.051,
        "share_based_payments": 992.844,
        "adjusted_net_loss": -2811.776,
        "disagreement": "Share-based compensation is not free: base cash OE does not subtract it twice, while the economic cost is carried through the fully diluted share denominator.",
        "source_refs": ["H01"],
    },
    "owner_earnings": {
        "status": "calculated",
        "currency": "HKD",
        "range": [
            {
                "case": "strict_core_proxy_fy2025",
                "value": -3291.030 / HKD_CNY,
                "formula": "(CFO - PP&E cash capex - intangible cash capex - lease principal/interest - interest income) / 0.86627",
            },
            {
                "case": "reported_cash_proxy_fy2025",
                "value": -2807.291 / HKD_CNY,
                "formula": "(CFO - PP&E cash capex - intangible cash capex) / 0.86627",
            },
        ],
        "limitations": [
            "Both values are negative cash proxies, not a positive normalized earning-power estimate.",
            "Maintenance and growth capex are not disclosed separately.",
            "Investment purchases/sales and deposits are excluded; interest income is removed only in the strict core proxy.",
            "SBC is not double-subtracted from CFO; dilution is captured in the per-share bridge.",
        ],
        "source_refs": ["H01", "H02", "M03"],
    },
    "capital_allocation": {
        "status": "reviewed_with_dilution_and_refinancing",
        "uses": ["R&D", "cloud and technical services", "tape-out", "working capital", "associates", "CARIAD settlement"],
        "financing": ["2025 placements", "CARIAD share settlement", "US$450m convertible bond", "share awards"],
        "per_share_test": "Use known fully diluted shares and core owner earnings; do not treat financing proceeds as operating success.",
        "source_refs": ["H01", "H04", "H05", "H06", "H07"],
    },
    "balance_sheet_quality": {
        "status": "liquid_but_event_adjusted",
        "currency": "CNY",
        "unit": "million",
        "fy2025_cash_and_equivalents": 20188.070,
        "fy2025_term_deposits": 636.922,
        "bank_borrowings": 527.998,
        "lease_liabilities": 117.328,
        "cariad_convertible_loan_fv_liability": 12504.235,
        "d_robotics_preferred_fv_liability": 2403.463,
        "cariad_cash_payment_usd_m": 398.9,
        "new_cb_gross_usd_m": 450.0,
        "new_cb_net_usd_m": 445.5,
        "source_refs": ["H01", "H04", "H05"],
        "limitations": "The 2025 balance sheet predates D-Robotics deconsolidation and July transactions; no false pro-forma net-cash point estimate is presented.",
    },
    "pe_matrix": [
        {
            "label": "reported_fy",
            "status": "not_meaningful",
            "price": PRICE_HKD,
            "currency": "HKD",
            "price_as_of": PRICE_DATE,
            "eps": -0.81,
            "eps_period": "FY2025",
            "eps_type": "reported_basic_loss_per_share",
            "formula": None,
            "pe": None,
            "confidence": "high",
            "reason": "FY2025 earnings are negative and dominated by fair-value changes; PE has no economic meaning.",
            "source_refs": ["H01", "M01"],
        },
        {
            "label": "reported_ttm",
            "status": "unavailable",
            "price": PRICE_HKD,
            "currency": "HKD",
            "price_as_of": PRICE_DATE,
            "eps": None,
            "eps_period": "TTM to 2026H1 preliminary",
            "eps_type": "reported_diluted",
            "formula": None,
            "pe": None,
            "confidence": "low",
            "reason": "2026H1 update is preliminary and fair-value-driven; a comparable continuing-operations TTM EPS is unavailable.",
            "source_refs": ["H01", "H03", "M01"],
        },
        {
            "label": "normalized_owner_earnings",
            "status": "not_meaningful",
            "price": PRICE_HKD,
            "currency": "HKD",
            "price_as_of": PRICE_DATE,
            "eps": -2807.291 / HKD_CNY / (fd_shares / 1e6),
            "eps_period": "FY2025 cash proxy",
            "eps_type": "fully_diluted_cash_owner_earnings_proxy",
            "formula": None,
            "pe": None,
            "confidence": "medium",
            "reason": "Fully diluted owner-earnings proxy per share is negative.",
            "source_refs": ["H01", "H04", "H05", "H06", "H07", "M01", "M03"],
        },
    ],
    "forward_scenarios": {
        "currency": "HKD",
        "price_anchor": PRICE_HKD,
        "scenarios": [
            {"scenario": "bear", "status": "unavailable", "forecast_eps": None, "implied_pe_at_current_price": None, "reason": "One-year scenario uses revenue and cash-conversion conditions, not unsupported EPS."},
            {"scenario": "base", "status": "unavailable", "forecast_eps": None, "implied_pe_at_current_price": None, "reason": "One-year scenario uses revenue and cash-conversion conditions, not unsupported EPS."},
            {"scenario": "upside", "status": "unavailable", "forecast_eps": None, "implied_pe_at_current_price": None, "reason": "One-year scenario uses revenue and cash-conversion conditions, not unsupported EPS."},
        ],
    },
    "intrinsic_value_scenarios": {
        "currency": "HKD",
        "scenarios": [
            {"scenario": "conservative", "status": "unavailable", "discount_rate_pct": None, "terminal_growth_pct": None, "intrinsic_value_per_share": None, "reason": "Positive normalized owner earnings do not yet exist."},
            {"scenario": "base", "status": "unavailable", "discount_rate_pct": None, "terminal_growth_pct": None, "intrinsic_value_per_share": None, "reason": "Positive normalized owner earnings do not yet exist."},
            {"scenario": "high", "status": "unavailable", "discount_rate_pct": None, "terminal_growth_pct": None, "intrinsic_value_per_share": None, "reason": "Positive normalized owner earnings do not yet exist."},
        ],
    },
    "moat_evidence": {
        "positive_evidence": ["401万套实际出货", "HSD实际量产", "许可服务94.5%毛利率", "10–40个月汽车项目验证链"],
        "counter_evidence": ["定点不保证订单", "产品毛利率下降", "OEM自研和多平台替代", "下一代车型重新RFQ"],
        "missing_tests": ["定点转SOP率", "平台续标率", "独立客户留存", "非关联许可收入", "安全事件长期记录"],
    },
    "red_team": [
        {"risk": "growth_without_owner_earnings", "evidence": "Revenue +57.7% while adjusted operating loss +58.7% and cash OE remained negative.", "source_refs": ["H01"]},
        {"risk": "design_win_conversion", "evidence": "Prospectus says design-win does not guarantee a sales order.", "source_refs": ["H08"]},
        {"risk": "dilution", "evidence": "Known pro-forma/potential claims increase shares by 14.39% versus current issued shares.", "source_refs": ["H04", "H05", "H06", "H07"]},
    ],
    "gates": gates,
    "source_gaps": [
        {"gap": "No customer-level design-win → contract → SOP → shipment → revenue → cash ledger."},
        {"gap": "No audited 2026H1 full financial statements or continuing-operations cash flow at cut-off."},
        {"gap": "No maintenance/growth R&D and capex split."},
        {"gap": "No completed pro-forma balance sheet after D-Robotics deconsolidation and July financing."},
        {"gap": "No named human approval; machine fact pack remains reconciliation_pending."},
    ],
    "invalidation_tests": [
        {"test": "Two consecutive half-years of actual HSD/J6 shipment and SOP growth."},
        {"test": "Product gross margin excluding pass-through controllers remains near or above 40%."},
        {"test": "Receivables and inventory growth fall to no faster than revenue growth."},
        {"test": "Adjusted operating loss absolute amount declines and core CFO approaches break-even."},
        {"test": "Fully diluted per-share owner earnings becomes positive without fair-value or financing gains."},
        {"test": "Non-related-party license revenue and next-generation platform renewals are independently evidenced."},
    ],
    "historical_valuation": {
        "status": "unavailable",
        "metric": "point_in_time_ttm_pe",
        "listing_date": "2024-10-24",
        "price_history": {
            "ipo_first_close_hkd": 4.10,
            "observed_close_low_hkd": 3.33,
            "observed_close_high_hkd": 10.81,
            "through": "2026-07-28",
        },
        "reason": "Short listing history and negative/fair-value-distorted earnings make historical PE invalid; current FY2025 EPS is not backfilled into past dates.",
        "source_refs": ["H01", "M02"],
    },
    "price_move_attribution": {
        "status": "not_causal",
        "reason": "The report does not infer causality from short-term price moves; July disclosures and market price are shown as dated events.",
        "source_refs": ["H03", "H04", "H05", "H06", "M01", "M02"],
    },
    "review": {
        "human_review_required": True,
        "machine_fact_pack_state": "evidence_extracted_reconciliation_pending",
        "publication_state": "needs_human_review",
    },
    "disclaimer": "Public evidence-linked research support only; not investment advice, a target price, or a named human approval.",
}
dump_json(ROOT / "combined-artifact.v2.json", combined)

source_ledger = {
    "schema_version": "seed.company-research-source-ledger.v1",
    "company": "Horizon Robotics",
    "security_id": "XHKG:09660",
    "as_of": RESEARCH_DATE,
    "sources": [
        {
            "id": row["id"],
            "tier": row["tier"],
            "kind": row["source_type"],
            "title": row["title"],
            "publisher": (
                "HKEX / issuer"
                if row["id"].startswith("H")
                else "SEC / issuer"
                if row["id"] in {"P02", "P03"}
                else "HKEX / peer issuer"
                if row["id"] == "P01"
                else "Tencent"
                if row["id"] in {"M01", "M02", "M04"}
                else "Xinhua / CFETS"
            ),
            "published_at": row["published_at"],
            "retrieved_at": RESEARCH_DATE,
            "url": row["url"],
            "snapshot_sha256": row["content_sha256"],
            "used_for": row["covers"],
            "limitations": (
                "Intraday third-party market snapshot; not an HKEX official close."
                if row["id"] in {"M01", "M04"}
                else "Third-party daily market snapshot; corporate-action completeness not independently certified."
                if row["id"] == "M02"
                else "One-day timing mismatch versus the 2026-07-29 intraday price."
                if row["id"] == "M03"
                else "Primary filing or exchange announcement used within its stated period, scope and assurance."
            ),
        }
        for row in sources
    ],
}
dump_json(ROOT / "source-ledger.json", source_ledger)

anchor_specs = [
    ("HR-001", "fy2025.financials", "H01", 140, "Revenue 3,758,268; gross profit 2,425,680; operating loss (3,338,791)", "FY2025", "RMB thousand", "CNY", "consolidated_group", "audited", "directly reported"),
    ("HR-002", "fy2025.cash_flow", "H01", 146, "OCF (2,106,052); PP&E payments (471,590); intangible payments (229,649)", "FY2025", "RMB thousand", "CNY", "consolidated_group", "audited", "cash OE proxy = CFO - PP&E - intangible"),
    ("HR-003", "fy2025.revenue_mix", "H01", 164, "Product 1,622,274; license/services 1,934,913; non-auto 201,081", "FY2025", "RMB thousand", "CNY", "revenue_disaggregation", "audited", "sum = total revenue"),
    ("HR-004", "fy2025.product_margin", "H01", 12, "Product gross margin 34.5%; adjusted 42.5% excluding low-markup integrated units", "FY2025", "percent", "CNY", "automotive_product_solutions", "audited", "company adjustment"),
    ("HR-005", "fy2025.shipments", "H01", 6, "Journey shipments 4.01m; +38.8%; NOA-capable 45%; dollar content +75%", "FY2025", "units / percent", "CNY", "company_operating_kpi", "audited", "reported operating KPI"),
    ("HR-006", "fy2025.customers", "H01", 165, "Customer A 18.11%; B 14.58%; C 12.45%; D 10.87%", "FY2025", "percent of revenue", "CNY", "consolidated_group", "audited", "directly reported"),
    ("HR-007", "fy2025.performance_obligations", "H01", 166, "Unsatisfied performance obligations 1,011,788; next 12 months 1,000,273", "2025-12-31", "RMB thousand", "CNY", "contract_revenue", "audited", "directly reported; not total hardware backlog"),
    ("HR-008", "fy2025.balance_sheet", "H01", 142, "Cash 20,188,070; term deposits 636,922; receivables 1,760,048; inventory 1,069,224", "2025-12-31", "RMB thousand", "CNY", "consolidated_group", "audited", "directly reported"),
    ("HR-009", "h1_2026.preliminary", "H03", 1, "Continuing revenue 1.93–2.08bn; adjusted net loss 1.4–1.7bn", "2026H1", "RMB million", "CNY", "continuing_operations_preliminary", "unaudited", "company preliminary range"),
    ("HR-010", "cariad.amendment", "H04", 2, "1,301,763,486 new B shares plus US$398.9m cash payment", "2026-07-22", "shares / USD", "HKD", "listed_security", "not_applicable", "transaction terms; completion pending at cut-off"),
    ("HR-011", "new_cb.terms", "H05", 1, "US$450m zero-coupon CB; HK$5.55 initial conversion; 635,635,135 shares", "2026-07-23", "USD / HKD / shares", "HKD", "listed_security", "not_applicable", "full-conversion scenario"),
    ("HR-012", "awards.july_2026", "H06", 1, "90,608,252 new B share awards to 1,202 grantees; no performance targets", "2026-07-26", "shares", "HKD", "listed_security", "not_applicable", "directly reported"),
    ("HR-013", "shares.june_2026", "H07", 2, "Issued excluding treasury 14,571,723,185; treasury B shares 80,161,800", "2026-06-30", "shares", "HKD", "listed_security", "not_applicable", "A+B excluding treasury"),
    ("HR-014", "design_win.conversion_cycle", "H08", 38, "Design-win does not guarantee sales order; design-win to contract 2–4 months; contract to SOP 8–36 months", "IPO", "months", "HKD", "issuer_business_process", "not_applicable", "directly disclosed process"),
    ("HR-015", "peer.black_sesame", "P01", 5, "FY2025 revenue RMB822.328m, +73.4%", "FY2025", "RMB million", "CNY", "peer_consolidated_group", "audited", "directly reported"),
    ("HR-016", "peer.mobileye", "P02", 1, "FY2025 revenue US$1.894bn; operating cash flow US$602m", "FY2025", "USD million", "USD", "peer_consolidated_group", "audited", "directly reported"),
    ("HR-017", "peer.ambarella", "P03", 50, "FY2026 revenue US$390.702m; operating loss US$82.5m", "FY2026", "USD million", "USD", "peer_consolidated_group", "audited", "directly reported"),
    ("HR-018", "price.snapshot", "M01", None, "09660.HK HK$5.20 at 2026-07-29 11:59:59 HKT", PRICE_TIME, "HKD", "HKD", "listed_security", "not_applicable", "third-party intraday quote snapshot"),
]

source_by_id = {row["id"]: row for row in sources}
anchors = []
for spec in anchor_specs:
    (
        evidence_id,
        claim_id,
        source_id,
        page,
        source_text,
        period,
        unit,
        currency,
        scope,
        audit_status,
        formula,
    ) = spec
    anchors.append(
        {
            "id": evidence_id,
            "claim_id": claim_id,
            "source_id": source_id,
            "document_sha256": source_by_id[source_id]["content_sha256"],
            "page": page,
            "source_text": source_text,
            "period": period,
            "unit": unit,
            "currency": currency,
            "scope": scope,
            "audit_status": audit_status,
            "formula": formula,
            "critical": True,
            "review": "machine_checked_needs_human_review",
            "limitations": "Verify the official source page and checksum; market and scenario anchors retain stated timing and scope.",
        }
    )

evidence_index = {
    "schema_version": "seed.company-research-evidence-index.v1",
    "company": "Horizon Robotics",
    "security_id": "XHKG:09660",
    "as_of": RESEARCH_DATE,
    "status": "needs_human_review",
    "combined_artifact": {
        "path": "combined-artifact.v2.json",
        "sha256": sha(ROOT / "combined-artifact.v2.json"),
    },
    "anchors": anchors,
}
dump_json(ROOT / "evidence-index.json", evidence_index)

red_team = {
    "schema_version": "seed.company-research-red-team.v1",
    "company": "Horizon Robotics",
    "security_id": "XHKG:09660",
    "reviewer_or_agent": "independent Codex research subagent",
    "reviewed_at": "2026-07-29T11:30:00+08:00",
    "status": "needs_human_review",
    "counter_thesis": "地平线可能已证明产品商业化，却尚未证明收入增长可穿过研发、营运资本、关联结构和稀释，转成充分摊薄后的每股owner earnings。",
    "strongest_disconfirming_evidence": [
        {"claim_challenged": "收入高增长自然带来经营杠杆。", "evidence": "FY2025收入+57.7%，调整后经营亏损+58.7%；2026H1调整后净亏损预告仍扩大。", "source_refs": ["H01", "H03"]},
        {"claim_challenged": "定点数量可视为订单。", "evidence": "招股书明确design-win不保证销售订单，合同后到SOP仍需8–36个月。", "source_refs": ["H08"]},
        {"claim_challenged": "现金多就不存在每股资本成本。", "evidence": "CARIAD、新CB和已授予奖励形成14.39%的已知潜在股数增幅。", "source_refs": ["H04", "H05", "H06", "H07"]},
        {"claim_challenged": "高毛利许可足以证明护城河。", "evidence": "客户集中、关联销售、OEM自研与多平台替代仍存在，且非关联许可留存未披露。", "source_refs": ["H01", "H08", "P01", "P02", "P03"]},
    ],
    "failure_modes": [
        {"name": "conversion_gap", "mechanism": "定点未按期转SOP、出货和回款。", "observable_signals": ["SOP车型数", "实际出货", "取消率", "应收增速"]},
        {"name": "margin_and_cash_failure", "mechanism": "低毛利硬件、价格竞争和研发投入吞噬许可利润。", "observable_signals": ["产品毛利率", "调整经营亏损", "OCF/收入", "现金OE"]},
        {"name": "platform_substitution", "mechanism": "下一代车型改用华为、Mobileye、Qualcomm、NVIDIA、黑芝麻或OEM自研。", "observable_signals": ["续标率", "客户下一代平台", "同车型第二供应源"]},
        {"name": "per_share_dilution", "mechanism": "融资与激励增长快于经济收益。", "observable_signals": ["全摊薄股本", "SBC", "新配售/债券", "每股现金OE"]},
    ],
    "invalidation_conditions": [
        {"condition": "连续两个半年度同口径毛利增速高于经营费用增速，调整经营亏损绝对额下降。", "effect_on_counter_thesis": "削弱增长无经营杠杆的反方。"},
        {"condition": "TTM核心OCF与扣维持投入后的充分摊薄每股OE转正。", "effect_on_counter_thesis": "削弱现金复利尚未成立的反方。"},
        {"condition": "定点转SOP、出货、非关联许可收入与回款同步增长。", "effect_on_counter_thesis": "削弱定点质量和关联依赖反方。"},
    ],
    "unresolved_issues": combined["source_gaps"],
    "next_review": {
        "event": "2026H1 full interim results and July transaction completion notices",
        "minimum_checks": ["continuing revenue mix", "adjusted operating loss", "CFO", "receivables", "inventory", "CARIAD closing", "CB issuance", "fully diluted shares"],
        "source_refs": ["H03", "H04", "H05", "H06", "H07"],
    },
    "source_refs": ["H01", "H03", "H04", "H05", "H06", "H07", "H08", "P01", "P02", "P03"],
    "disclaimer": "Independent evidence red-team; not investment advice or named human approval.",
}
dump_json(ROOT / "red-team.json", red_team)


def svg_grouped_financials() -> str:
    rows = financial_rows
    max_value = 4000
    parts = ['<svg viewBox="0 0 860 330" role="img" aria-label="FY2021至FY2025收入、毛利与经营亏损">']
    parts.append('<line x1="70" y1="270" x2="830" y2="270" stroke="#61726b"/>')
    colors = {"revenue_rmb_m": "#20745f", "gross_profit_rmb_m": "#4f86a8", "operating_loss_rmb_m": "#bd633f"}
    for index, row in enumerate(rows):
        group_x = 95 + index * 145
        for offset, key in enumerate(("revenue_rmb_m", "gross_profit_rmb_m", "operating_loss_rmb_m")):
            value = row[key]
            height = abs(value) / max_value * 205
            x = group_x + offset * 32
            y = 270 - height if value >= 0 else 270
            parts.append(
                f'<rect x="{x}" y="{y:.1f}" width="24" height="{height:.1f}" rx="3" fill="{colors[key]}">'
                f"<title>{row['period']} {key}: {value}</title></rect>"
            )
        parts.append(f'<text x="{group_x+34}" y="309" text-anchor="middle">{row["period"]}</text>')
    parts.append('<text x="70" y="24">绿：收入　蓝：毛利　橙：经营亏损绝对值（人民币百万元）</text>')
    parts.append("</svg>")
    return "".join(parts)


def svg_owner_earnings() -> str:
    parts = ['<svg viewBox="0 0 760 310" role="img" aria-label="FY2023至FY2025两套现金所有者收益代理">']
    parts.append('<line x1="70" y1="55" x2="730" y2="55" stroke="#61726b"/>')
    scale = 0.06
    for index, row in enumerate(owner_earnings_rows):
        x = 120 + index * 210
        a = abs(row["cash_oe_proxy_rmb_m"]) * scale
        b = abs(row["strict_core_oe_proxy_rmb_m"]) * scale
        parts.append(f'<rect x="{x}" y="55" width="52" height="{a:.1f}" fill="#bd633f"><title>{row["period"]} 现金OE代理 {row["cash_oe_proxy_rmb_m"]}</title></rect>')
        parts.append(f'<rect x="{x+65}" y="55" width="52" height="{b:.1f}" fill="#8a3f3a"><title>{row["period"]} 严格核心OE {row["strict_core_oe_proxy_rmb_m"]}</title></rect>')
        parts.append(f'<text x="{x+58}" y="292" text-anchor="middle">{row["period"]}</text>')
    parts.append('<text x="70" y="24">两套代理均为负；浅橙：OCF−固定/无形投入，深红：再扣租赁与利息收入</text>')
    parts.append("</svg>")
    return "".join(parts)


def svg_dilution() -> str:
    max_shares = fd_shares / 1e9
    parts = ['<svg viewBox="0 0 860 300" role="img" aria-label="已发行至已知完全摊薄股本桥">']
    for index, row in enumerate(dilution_rows):
        value = row["shares"] / 1e9
        width = value / max_shares * 690
        y = 48 + index * 58
        parts.append(f'<rect x="145" y="{y}" width="{width:.1f}" height="32" rx="6" fill="#315f8f"><title>{row["stage"]}: {value:.3f}bn</title></rect>')
        parts.append(f'<text x="136" y="{y+22}" text-anchor="end">{index+1}</text><text x="{150+width:.1f}" y="{y+22}">{value:.3f}bn</text>')
    parts.append('<text x="145" y="280">1 已发行　2 CARIAD备考　3 新CB全转　4 再计已授予奖励</text></svg>')
    return "".join(parts)


def svg_peer_ps() -> str:
    selected = [peer_rows[0], peer_rows[1], peer_rows[2], peer_rows[4]]
    parts = ['<svg viewBox="0 0 820 320" role="img" aria-label="地平线与三个合格或近似同业P/S">']
    for index, row in enumerate(selected):
        width = row["ps"] / 20.0 * 600
        y = 45 + index * 65
        color = "#bd633f" if "地平线" in row["company"] else "#315f8f"
        parts.append(f'<text x="180" y="{y+23}" text-anchor="end">{html.escape(row["company"])}</text>')
        parts.append(f'<rect x="195" y="{y}" width="{width:.1f}" height="34" rx="6" fill="{color}"><title>{row["ps"]:.2f}x</title></rect>')
        parts.append(f'<text x="{205+width:.1f}" y="{y+23}">{row["ps"]:.2f}x</text>')
    parts.append("</svg>")
    return "".join(parts)


legend_rows = [
    {"layer": "发布", "term": "needs_human_review", "meaning": "已做机器校验，尚无具名人工签字。"},
    {"layer": "发布", "term": "production_reviewed", "meaning": "只有具名人工完成事实、公式与发布范围复核后才可标记。"},
    {"layer": "维度", "term": "applicable / unknown", "meaning": "适用并已研究 / 证据不足，不能填零。"},
    {"layer": "指标", "term": "observed / not_disclosed", "meaning": "已观察到证据 / 主源未披露。"},
    {"layer": "结论", "term": "provisional", "meaning": "临时结论，尚需关键证据升级。"},
    {"layer": "Gate", "term": "pass_with_scope / mixed / fail / blocked", "meaning": "限范围通过 / 正反并存 / 失败 / 被关键分母阻断。"},
]

dimension_rows_html = []
for dimension in research_dimensions:
    label = crosswalk_by_id[dimension["dimension"]]["label_zh"]
    indicators = "<br>".join(
        f"<code>{html.escape(indicator['id'])}</code>" for indicator in dimension["indicators"]
    )
    refs = " / ".join(dimension["source_refs"])
    dimension_rows_html.append(
        "<tr>"
        f"<td><code>{html.escape(dimension['dimension'])}</code><br>{html.escape(label)}</td>"
        f"<td>{indicators}</td>"
        f"<td>{html.escape(dimension['summary'])}</td>"
        f"<td>{html.escape(refs)}</td>"
        "</tr>"
    )

gate_rows_html = "".join(
    "<tr>"
    f"<td><code>{html.escape(row['gate'])}</code></td>"
    f"<td>{html.escape(row['result'])}</td>"
    f"<td>{html.escape(row['reason'])}</td>"
    "</tr>"
    for row in gates
)

evidence_cards = []
for anchor in anchors:
    source_row = source_by_id[anchor["source_id"]]
    page = anchor["page"] if anchor["page"] is not None else "N/A"
    evidence_cards.append(
        f'<details class="evidence" data-evidence-id="{anchor["id"]}">'
        f'<summary><code>{anchor["id"]}</code> · {html.escape(anchor["claim_id"])} · P{page}</summary>'
        f'<p><strong>记录：</strong>{html.escape(anchor["source_text"])}</p>'
        f'<p><strong>期间/单位/范围：</strong>{html.escape(anchor["period"])} / '
        f'{html.escape(anchor["unit"])} / {html.escape(anchor["scope"])}</p>'
        f'<p><strong>公式/边界：</strong>{html.escape(str(anchor["formula"]))}</p>'
        f'<p><strong>SHA-256：</strong><code>{anchor["document_sha256"]}</code></p>'
        f'<p><a href="{html.escape(source_row["url"])}" rel="noreferrer">打开主源</a></p>'
        "</details>"
    )

source_rows = [
    {
        "id": row["id"],
        "tier": row["tier"],
        "title": row["title"],
        "date": row["published_at"],
        "scope": row["scope"],
        "url": row["url"],
    }
    for row in sources
]
source_table_html = (
    '<div class="table-wrap"><table><thead><tr><th>ID</th><th>层级</th><th>来源</th>'
    "<th>日期</th><th>范围</th><th>链接</th></tr></thead><tbody>"
    + "".join(
        "<tr>"
        f"<td><code>{html.escape(row['id'])}</code></td>"
        f"<td>{html.escape(row['tier'])}</td>"
        f"<td>{html.escape(row['title'])}</td>"
        f"<td>{html.escape(row['date'])}</td>"
        f"<td>{html.escape(row['scope'])}</td>"
        f'<td><a href="{html.escape(row["url"])}" rel="noreferrer">打开</a></td>'
        "</tr>"
        for row in source_rows
    )
    + "</tbody></table></div>"
)

report = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <meta name="description" content="地平线机器人09660.HK巴菲特—芒格两问研究：业务、订单转化、所有者收益、竞争、周期、稀释与反向估值。">
  <title>地平线机器人｜巴菲特—芒格两问研究</title>
  <link rel="stylesheet" href="../company-report-theme.css">
  <style>
    :root {{ --brand: #235f56; --accent: #bd633f; }}
    *,*::before,*::after {{ box-sizing:border-box; }}
    html,body {{ max-width:100%; overflow-x:hidden; }}
    body {{ background: #f4f1ea; color: #17221e; }}
    main {{ width: min(1180px, calc(100% - 32px)); margin: auto; padding: 28px 0 72px; }}
    .hero {{ padding: clamp(24px,5vw,58px); border-radius: 26px; background: #173a34; color: #fff; box-shadow: 0 20px 50px rgba(24,42,36,.15); }}
    .hero h1 {{ max-width:none; margin: 8px 0 14px; overflow-wrap:anywhere; font: 800 clamp(38px,6vw,70px)/1.03 Georgia,"Songti SC",serif; }}
    .hero p {{ max-width: 78ch; color: #d1e4dc; font-size: 18px; }}
    .meta,.chips {{ display:flex; flex-wrap:wrap; gap:8px; margin-top:18px; }}
    .chip {{ padding:6px 10px; border:1px solid rgba(255,255,255,.28); border-radius:999px; color:#eff9f5; font-size:13px; }}
    nav {{ position:sticky; top:0; z-index:5; margin:14px 0 0; padding:10px 14px; border:1px solid #d8d1c3; border-radius:14px; background:rgba(255,253,248,.94); backdrop-filter:blur(12px); }}
    nav a {{ display:inline-block; margin:4px 10px 4px 0; color:#235f56; font-weight:700; text-decoration:none; }}
    section {{ margin-top:22px; padding:clamp(20px,4vw,36px); border:1px solid #d8d1c3; border-radius:20px; background:#fffdf8; box-shadow:0 12px 32px rgba(34,42,37,.06); scroll-margin-top:74px; }}
    h2 {{ margin:0 0 12px; font:750 clamp(25px,4vw,38px)/1.16 Georgia,"Songti SC",serif; }}
    h3 {{ margin:22px 0 8px; }}
    .dek {{ color:#607068; max-width:82ch; }}
    .two,.three,.doors {{ display:grid; gap:14px; grid-template-columns:repeat(2,minmax(0,1fr)); }}
    .three {{ grid-template-columns:repeat(3,minmax(0,1fr)); }}
    .card,.answer {{ padding:20px; border:1px solid #d8d1c3; border-radius:16px; background:#fff; }}
    .answer {{ border-top:6px solid #bd633f; }}
    .answer.good {{ border-top-color:#235f56; }}
    .answer .q {{ color:#607068; font-size:13px; font-weight:800; letter-spacing:.08em; }}
    .answer .verdict {{ margin:8px 0; font-size:26px; line-height:1.25; font-weight:850; }}
    .metric {{ font:800 30px/1.1 Georgia,serif; color:#235f56; }}
    .muted,small {{ color:#607068; }}
    .callout {{ margin:16px 0; padding:15px 17px; border-left:4px solid #bd633f; border-radius:10px; background:#f8eee6; }}
    .callout.blue {{ border-left-color:#315f8f; background:#edf3f7; }}
    .callout.green {{ border-left-color:#235f56; background:#ebf4f0; }}
    .table-wrap {{ overflow-x:auto; margin:14px 0; }}
    table {{ width:100%; border-collapse:collapse; min-width:680px; }}
    th,td {{ padding:10px 12px; border-bottom:1px solid #ddd6ca; text-align:left; vertical-align:top; }}
    th {{ background:#f1ede4; font-size:13px; }}
    code {{ overflow-wrap:anywhere; }}
    .chart {{ margin:16px 0; padding:12px; border:1px solid #ddd6ca; border-radius:16px; background:#fff; }}
    svg {{ width:100%; height:auto; overflow:visible; font:12px -apple-system,BlinkMacSystemFont,"PingFang SC",sans-serif; }}
    details {{ margin:9px 0; padding:12px 14px; border:1px solid #ddd6ca; border-radius:12px; background:#fff; }}
    summary {{ cursor:pointer; font-weight:750; }}
    .status {{ font-weight:800; color:#9b4c31; }}
    .foot {{ margin-top:26px; color:#607068; font-size:13px; }}
    @media (max-width:800px) {{
      main {{ width:min(calc(100% - 20px),1180px); }}
      .two,.three,.doors {{ grid-template-columns:1fr; }}
      .hero {{ border-radius:18px; }}
      .hero h1 {{ font-size:34px; }}
      .hero p {{ font-size:16px; }}
      section {{ padding:18px; }}
      nav {{ position:static; }}
    }}
  </style>
</head>
<body data-template="company-research-publication-v1">
<!-- template-parity: viewport-qa-required -->
<main id="main-content">
  <header class="hero" id="home">
    <div>Evidence-linked · Buffett–Munger · 09660.HK</div>
    <h1>地平线机器人：先回答两问</h1>
    <p>这不是把“高增长”直接翻译成“好投资”。报告先追问未来十年每股所有者收益能否复利，再追问 HK$5.20 的价格是否已经留下可证明的安全边际。</p>
    <div class="meta">
      <span class="chip">研究日 2026-07-29</span>
      <span class="chip">价格快照 HK$5.20 · 11:59:59 HKT</span>
      <span class="chip">needs_human_review</span>
      <span class="chip">港股通研究范围</span>
    </div>
  </header>

  <nav aria-label="报告导航">
    <a href="#summary">两问</a><a href="#orders">订单转化</a><a href="#financials">财务</a>
    <a href="#owner-earnings">所有者收益</a><a href="#competition">竞争</a>
    <a href="#capital">稀释</a><a href="#market-pricing">估值</a>
    <a href="#monitor">晋级门槛</a><a href="#evidence">证据</a>
  </nav>

  <section id="status-legend">
    <h2>先读状态，不把“有资料”误当“结论成立”</h2>
    {table(legend_rows, [("layer","层"),("term","状态词"),("meaning","含义")])}
    <p class="muted">本包是 <code>needs_human_review</code>。公司主源已冻结，报告结构与公式会做确定性校验；机器事实包仍处于 <code>evidence_extracted_reconciliation_pending</code>，不是 <code>production_reviewed</code>。</p>
  </section>

  <section id="report-doors">
    <h2>两个阅读入口</h2>
    <div class="doors">
      <a class="card" href="#long-term"><strong>长期公司底稿</strong><p>业务、客户、供应链、竞争、周期、owner earnings、稀释和十年反向考题。</p></a>
      <a class="card" href="#event-monitor"><strong>近期事件监控</strong><p>2026H1预告、D-Robotics出表、CARIAD旧贷重组、新CB与股份奖励。</p></a>
    </div>
  </section>

  <section id="summary">
    <h2>结论先行：最终就是两问</h2>
    <div class="two">
      <article class="answer good">
        <div class="q">问题一 · 十年每股 owner earnings</div>
        <div class="verdict">业务增长机制可理解；每股现金复利尚未证明。</div>
        <p>真实出货、HSD量产、NOA占比与许可收入说明商业化不是PPT；但研发超过收入、现金OE连续为负、应收库存快于收入、已知潜在股数增加14.39%，说明“收入→每股现金”尚未闭环。</p>
      </article>
      <article class="answer">
        <div class="q">问题二 · 当前价格的安全边际</div>
        <div class="verdict">现有证据不能证明；状态是重点观察、条件晋级。</div>
        <p>PE无意义。HK$5.20对应当前P/S约17.47倍、已知全摊薄约19.98倍；三家合格/近似同业中位约7.62倍。不是断言公司必然高估，而是当前价格把很强的未来现金复利写进了考题。</p>
      </article>
    </div>
    <div class="callout green"><strong>一句话：</strong>地平线不是“没有真实业务的概念公司”，也还不是“已证明能复利的价值公司”；它是商业验证很强、但仍需跨过经营杠杆、owner earnings和充分稀释估值三道闸门的重点观察对象。</div>
  </section>

  <section id="long-term">
    <h2>长期底稿：十年复利机制到底是什么</h2>
    <p class="dek">可证伪链条是：更多车型定点 → 合同与验证 → SOP → 芯片/软件实际出货 → NOA占比与单车价值上升 → 许可扩散 → 收入 → 回款 → 扣维持投入后的充分摊薄每股owner earnings。</p>
    <div class="three">
      <div class="card"><div class="metric">401万套</div><p>2025 Journey硬件实际出货，+38.8%。</p></div>
      <div class="card"><div class="metric">45%</div><p>NOA硬件占出货；出货约为2024年的4.8倍。</p></div>
      <div class="card"><div class="metric">94.5%</div><p>许可及服务毛利率；潜在高质量利润池。</p></div>
    </div>
    <div class="callout"><strong>关键缺口：</strong>高毛利许可能否在非关联客户中持续扩散，以及产品放量后研发、营运资本与稀释是否下降，决定这条链能否从商业故事升级为每股复利。</div>
  </section>

  <section id="business">
    <h2>公司怎么赚钱：硬件规模与许可质量并存</h2>
    {table(revenue_mix_rows, [("line","业务线"),("fy2024_rmb_m","2024收入 RMBm"),("fy2025_rmb_m","2025收入 RMBm"),("fy2025_share_pct","收入占比%"),("fy2025_gross_margin_pct","毛利率%"),("adjusted_product_gm_ex_domain_controllers_pct","剔除低加价域控后%")])}
    <p>产品收入增长144.2%，但产品毛利率由46.4%降至34.5%；公司剔除低加价域控制器后给出42.5%。许可服务收入增长17.4%，毛利率94.5%。因此真正的长期质量不是“硬件越多越好”，而是硬件规模能否带来不被定制交付和价格竞争吞噬的许可经济。</p>
  </section>

  <section id="orders">
    <h2>定点不是订单：把漏斗放在估值前面</h2>
    {table(operating_rows, [("stage","阶段"),("metric","指标"),("value","披露"),("evidence_class","证据等级"),("source_refs","来源")])}
    <div class="callout blue"><strong>招股书边界：</strong><code>design-win does not guarantee sales order</code>；定点至合同通常2–4个月，合同至SOP还需8–36个月。合作意向、定点、生命周期名义量、SOP、实际出货、收入和现金不得互换。</div>
  </section>

  <section id="customers">
    <h2>客户、关联方与回款：增长最容易失真的地方</h2>
    {table(customer_rows, [("metric","指标"),("fy2024_pct","2024%"),("fy2025_pct","2025%"),("interpretation","读法")])}
    <p>CARIZON销售6.806亿元约等于总收入18.11%，与最大客户A的比例吻合；这是强研究推断，不是年报在客户表中具名确认。CARIZON同时带来权益法亏损、研发承诺和关联交易，不能只看其收入。</p>
    <div class="callout"><strong>现金警报：</strong>应收净额约增长151%，库存增长82.6%，均快于收入57.7%。未履约交易价10.12亿元是已签合同中的收入确认余额，不是完整硬件订单簿。</div>
  </section>

  <section id="competition">
    <h2>护城河与可替代性：不是垄断，而是量产工程粘性</h2>
    {table(cycle_rows, [("stage","环节"),("typical_time","周期"),("capital_or_risk","资本/风险"),("substitutability","替代性"),("source_refs","来源")])}
    <p>RFQ前，OEM可在地平线、Mobileye、黑芝麻、Qualcomm、NVIDIA、华为与自研方案间选择；进入SOP后，更换供应商要重新设计、功能安全验证与OTA适配，替代性下降；到下一代车型或中央计算架构，竞争再次开放。</p>
    <div class="callout green"><strong>当前最可验证护城河：</strong>中国场景算法+BPU+工具链+Tier 1/OEM生态+量产交付。持续性要由HSD实际出货、定点转SOP率、下一代平台续标率、产品毛利与现金消耗验证。</div>
  </section>

  <section id="financials">
    <h2>五年财务：收入放量，经营亏损并未收敛</h2>
    {table(financial_rows, [("period","年度"),("revenue_rmb_m","收入 RMBm"),("gross_profit_rmb_m","毛利 RMBm"),("operating_loss_rmb_m","经营损益 RMBm"),("adjusted_net_loss_rmb_m","调整净损益 RMBm"),("cfo_rmb_m","OCF RMBm"),("cash_owner_earnings_proxy_rmb_m","现金OE代理 RMBm")])}
    <div class="chart">{svg_grouped_financials()}</div>
    <p>2025收入+57.7%、毛利+31.7%，但调整后经营亏损扩大58.7%，调整后净亏损扩大67.3%。规模已被证明，经营杠杆尚未被证明。</p>
  </section>

  <section id="earnings-quality">
    <h2>盈利质量：为什么2024与2026H1“盈利”不能拿来算PE</h2>
    <p>FY2024 IFRS利润23.47亿元包含金融负债公允价值收益46.77亿元；FY2025 IFRS亏损104.69亿元包含相反方向的公允价值损失66.64亿元。2026H1预计利润35–40亿元主要也来自CARIAD可转贷公允价值变化，而调整后净亏损仍预计14–17亿元。</p>
    <div class="callout"><strong>结论：</strong>PE不是“高还是低”，而是当前没有可用经济分母。应从经营现金、持续经营口径、投资/利息剔除和充分稀释每股收益重新搭桥。</div>
  </section>

  <section id="owner-earnings">
    <h2>三年owner earnings：真正自己赚的钱仍为负</h2>
    {table(owner_earnings_rows, [("period","年度"),("cfo_rmb_m","OCF"),("ppe_cash_capex_rmb_m","固定资产现金投入"),("intangible_cash_capex_rmb_m","无形资产现金投入"),("cash_oe_proxy_rmb_m","现金OE代理"),("lease_principal_interest_rmb_m","租赁本金/利息"),("interest_income_rmb_m","利息收入"),("strict_core_oe_proxy_rmb_m","严格核心OE")])}
    <div class="chart">{svg_owner_earnings()}</div>
    <p>投资类现金流全部排除：股权法投资、FVTPL买卖与定存不是汽车业务资本开支；严格口径反向剔除现金/投资产生的利息收入。SBC不在现金OE里重复扣一次，其经济成本由完全摊薄分母承接。</p>
  </section>

  <section id="capital">
    <h2>完全摊薄股本：先分“已发行、交割备考、全转备考”</h2>
    {table(dilution_rows, [("stage","层级"),("shares","股份数"),("incremental_shares","本层新增"),("status","状态"),("market_cap_hkd_bn_at_5_20","同价市值 HK$bn")])}
    <div class="chart">{svg_dilution()}</div>
    <p>全计为166.68亿股，相对最新确认已发行股数增加14.386%；扩大后原股东被稀释12.577%。不重复计算CARIAD原有2.697亿股、已赎回约7.16亿旧转换权、2018计划已发行底层股份或未来尚未授予额度。</p>
    <div class="callout blue"><strong>时点边界：</strong>截至研究截止日，最新确认已发行仍为145.72亿股。CARIAD新股与新CB须分别标为交割备考和全转潜在股份，不能写成已经发行。</div>
  </section>

  <section id="market-pricing">
    <h2>当前估值：用P/S校准预期，不把它冒充价值</h2>
    {table(peer_rows, [("company","公司"),("ticker","代码"),("qualification","可比资格"),("market_cap_local_bn","本币市值bn"),("revenue_local_bn","本币收入bn"),("ps","P/S"),("profitability","盈利/现金")])}
    <div class="chart">{svg_peer_ps()}</div>
    <p>三家合格或近似同业的P/S中位约7.62倍；地平线已知全摊薄约19.98倍，约为中位数2.62倍。Mobileye更成熟且现金为正，Ambarella仅邻近边缘AI，黑芝麻最直接但规模较小；因此中位数只做预期校准，不是目标倍数。</p>
    <small>换算使用2026-07-28 CFETS中间价1 HKD=0.86627 RMB；主标的价格是2026-07-29 11:59:59 HKT第三方盘中快照，存在一天汇率错位。</small>
  </section>

  <section id="reverse-valuation">
    <h2>五年反向估值：当前价格要求什么</h2>
    {table(reverse_rows, [("terminal_ps","五年后P/S"),("revenue_needed_rmb_bn","维持当前市值所需收入 RMBbn"),("five_year_revenue_cagr_pct","收入CAGR%"),("revenue_needed_for_10pct_equity_return_rmb_bn","若股权年化10%所需收入"),("five_year_cagr_for_10pct_return_pct","对应CAGR%")])}
    <p>如果五年后估值回到同业中位7.615倍，仅维持当前全摊薄市值也要求收入约98.60亿元、五年复合增长21.3%；若还要求股权价值年化10%，收入需约158.79亿元、复合增长33.4%。这只是数学考题，尚未扣未来融资、回购或净现金变化。</p>
  </section>

  <section id="event-monitor">
    <h2>近期事件监控：2026H1与七月资本动作</h2>
    <div class="two">
      <div class="card"><strong>2026H1预告</strong><p>持续经营收入19.3–20.8亿元，同比+24.8%–34.5%；调整后净亏损14–17亿元，同比扩大5.1%–27.6%。未经审计、未获审计委员会复核。</p></div>
      <div class="card"><strong>D-Robotics出表</strong><p>2026-03-31起终止合并并列作终止经营；仍是最大单一股东并改用权益法。报表改善不等于经济风险归零。</p></div>
      <div class="card"><strong>CARIAD旧贷重组</strong><p>13.018亿新B股抵6.624亿美元本息，另付3.989亿美元现金并赎回约7.16亿潜在转换股；交割未确认完成。</p></div>
      <div class="card"><strong>新CB与奖励</strong><p>4.5亿美元零息CB主要用于CARIAD支付；全转6.356亿股。7月另授予0.906亿股、无业绩目标。</p></div>
    </div>
  </section>

  <section id="one-year">
    <h2>未来一年：不是点预测，而是三条可验证路径</h2>
    {table(one_year_rows, [("scenario","情景"),("own_revenue_assumption_rmb_bn","研究假设收入 RMBbn"),("fd_ps","同价全摊薄P/S"),("required_evidence","必须同时看到"),("status","PE状态")])}
    <p>收入假设是研究情景，不是管理层指引。真正升级信号是多个HSD车型SOP、剔除代采后的产品毛利稳定、调整亏损绝对额下降、应收库存与现金损耗同步改善。</p>
  </section>

  <section id="ten-year">
    <h2>未来十年：把当前价格翻译成终局考题</h2>
    {table(ten_year_rows, [("required_equity_return_pct","要求年化%"),("terminal_owner_earnings_multiple","终值OE倍数"),("assumed_owner_earnings_margin_pct","OE利润率假设%"),("year10_equity_value_rmb_bn","十年后股权价值 RMBbn"),("year10_owner_earnings_rmb_bn","十年后OE RMBbn"),("year10_revenue_rmb_bn","十年后收入 RMBbn"),("revenue_multiple_vs_2025","较2025倍数"),("ten_year_revenue_cagr_pct","收入CAGR%")])}
    <p>在25% owner-earnings利润率这一强假设下，年化10%仍要求十年收入约389.5亿元、是2025年的10.36倍；年化12%则要求约518.2亿元、13.79倍。若长期现金利润率只有20%，要求会更高。该表忽略未来净现金变化，目的只是显示当前价格对“高增长+高利润率+低稀释”的联合依赖。</p>
  </section>

  <section id="buffett">
    <h2>巴菲特—芒格式解释：为什么现在不是简单的“选或不选”</h2>
    <div class="two">
      <div class="card"><h3>最强正方</h3><ul><li>真实大规模出货与HSD量产。</li><li>软硬件双轮，许可毛利率高。</li><li>SOP后的安全验证与适配形成粘性。</li><li>现金储备提供验证时间。</li></ul></div>
      <div class="card"><h3>最强反方</h3><ul><li>增长尚未产生经营杠杆与现金OE。</li><li>产品毛利下降、应收库存吸收现金。</li><li>客户集中、关联收入和下一代平台替代。</li><li>配售、可转债与奖励改变每股分母。</li></ul></div>
    </div>
    <p>价值投资不是把所有未盈利公司一票否决，而是要求它们按证据晋级：商业验证 → 经济性 → owner earnings → 估值。地平线已通过第一层的大部分测试，尚未通过第三层。</p>
  </section>

  <section id="timeline">
    <h2>关键时间线</h2>
    {table([
      {"date":"2024-10-24","event":"港交所上市","meaning":"开始形成公开价格历史；短历史不支持无偏历史PE。"},
      {"date":"2025-11","event":"HSD首款量产","meaning":"一个多月交付超过2.2万套，商业化进入实际出货。"},
      {"date":"2026-03-31","event":"D-Robotics出表","meaning":"持续经营口径重列；经济风险未自动归零。"},
      {"date":"2026-07-21","event":"H1业绩更新","meaning":"收入增长、调整亏损仍扩大。"},
      {"date":"2026-07-22","event":"CARIAD旧贷修订","meaning":"股权+现金提前结算，交割待确认。"},
      {"date":"2026-07-23","event":"新CB定价","meaning":"主要为CARIAD支付再融资。"},
      {"date":"2026-07-26","event":"股份奖励","meaning":"0.906亿新B股、无业绩目标。"},
      {"date":"2026-07-29","event":"研究价格快照","meaning":"HK$5.20盘中；不是港交所官方收盘。"},
    ], [("date","日期"),("event","事件"),("meaning","研究含义")])}
  </section>

  <section id="monitor">
    <h2>四级晋级门槛：避免“永远一个股都选不到”</h2>
    <div class="two">
      <div class="card"><h3>1 商业验证</h3><p>HSD/J6连续两个半年度实际出货与SOP增长；定点拆成合同、SOP、出货、收入与回款；剔除低加价域控后产品毛利约40%以上。</p></div>
      <div class="card"><h3>2 经济性</h3><p>毛利增速高于经营费用；调整经营亏损绝对额下降；应收库存不再快于收入；非关联许可收入可验证。</p></div>
      <div class="card"><h3>3 Owner earnings</h3><p>TTM核心OCF转正；扣维持投入后现金OE为正；不依赖公允价值、利息、出表收益或新融资；充分稀释后每股仍为正。</p></div>
      <div class="card"><h3>4 估值</h3><p>基于完成交易和已授予奖励后的分母；熊/基准/强势均明确收入、利润率、资本强度和终值；不依赖单一极强路径。</p></div>
    </div>
  </section>

  <section id="invalidation">
    <h2>失效条件：哪些事实会让十年复利假设降级</h2>
    <ul>
      <li>连续两个半年度定点增长，但SOP与实际NOA出货停滞。</li>
      <li>剔除代采组件后的产品毛利长期低于约40%，许可收入无法补偿。</li>
      <li>收入增长超过25%，调整经营亏损绝对额仍连续扩大。</li>
      <li>应收与库存持续显著快于收入，或主要客户回款恶化。</li>
      <li>CARIZON等关联收入占比上升，非关联许可收入不能增长。</li>
      <li>D-Robotics出表后仍有大额资金支持或权益法损失而未计入价值。</li>
      <li>下一代平台续标失败、OEM自研扩散，或发生重大安全/召回/认证事件。</li>
    </ul>
  </section>

  <section id="dimensions">
    <h2>研究合同：25个维度 × 50个指标族 × 九道gate</h2>
    <p class="dek">每个维度的两个固定指标ID都在HTML与JSON中可见；“observed”只表示有证据，不代表评价良好。</p>
    <div class="table-wrap"><table><thead><tr><th>维度</th><th>固定指标族</th><th>本公司结论</th><th>来源</th></tr></thead><tbody>{''.join(dimension_rows_html)}</tbody></table></div>
    <h3>九道gate结果</h3>
    <div class="table-wrap"><table><thead><tr><th>Gate</th><th>结果</th><th>原因</th></tr></thead><tbody>{gate_rows_html}</tbody></table></div>
  </section>

  <section id="methodology">
    <h2>方法边界：PE、投资收益与行业周期如何处理</h2>
    <ul>
      <li>亏损期PE为<code>not_meaningful</code>，不因低价或高增长强行造分母。</li>
      <li>投资买卖、定存与公允价值变化排除出汽车业务owner earnings；利息收入在严格核心口径中剔除。</li>
      <li>SBC不因非现金就免费；现金OE不重复扣，经济成本进入全摊薄股本。</li>
      <li>“扩产”不是自建晶圆厂，而是研发、云、流片、验证、供应链前置期、库存与客户项目的组合周期。</li>
      <li>同业先做资格审查；中位P/S是校准，不是目标估值。</li>
    </ul>
    <p><a href="../listed-company-fundamentals-event-research-methodology.html">阅读完整V2.5方法论</a></p>
  </section>

  <section id="evidence">
    <h2>关键证据抽屉：18个两跳可审计锚点</h2>
    {''.join(evidence_cards)}
  </section>

  <section id="sources">
    <h2>来源账本</h2>
    {source_table_html}
    <p>可下载：<a href="combined-artifact.v2.json">combined artifact</a> · <a href="source-ledger.json">source ledger</a> · <a href="evidence-index.json">evidence index</a> · <a href="red-team.json">red team</a> · <a href="validator-results.json">validator results</a>。</p>
  </section>

  <p class="foot">公开研究辅助，不构成投资建议、目标价或具名人工审批。市场价格会变化；交易完成状态、2026H1完整财报与后续股本必须在使用前刷新。</p>
</main>
</body>
</html>
"""
(ROOT / "report.html").write_text(report, encoding="utf-8")

readme = f"""# 地平线机器人（09660.HK）巴菲特—芒格两问研究

截至 {RESEARCH_DATE} 的公开、证据关联研究包。首页先回答：

1. 未来十年充分稀释后的每股 owner earnings 复利机制是否可理解、可观察、可证伪？
2. 以 {PRICE_TIME} 的 HK${PRICE_HKD:.2f} 快照计，是否已有可证明的安全边际？

当前结论：商业化机制可理解，真实出货已验证；每股 owner earnings 与当前价格的安全边际尚未被证明。研究状态是 `needs_human_review`，适合继续观察与条件晋级，不是投资指令。

## 文件

- `report.html`：中文公开报告
- `combined-artifact.v2.json`：25维度、50指标、九道gate的机器可读底稿
- `source-ledger.json`：来源、时间、范围与SHA-256
- `evidence-index.json`：18个关键证据锚点
- `red-team.json`：独立反方与失效条件
- `data/*.csv`：财务、owner earnings、漏斗、客户、稀释、同业、反向估值和情景表
- `validator-results.json`：确定性校验结果

## 重要边界

- CARIAD新股与新可转债截至截止日为备考/潜在，不是最新确认已发行股本。
- PE因负盈利和公允价值扰动无意义；P/S只用于预期校准。
- 2026-07-29价格为第三方盘中快照，非港交所官方收盘。
- 尚无具名人工审批，本包不是`production_reviewed`。
"""
(ROOT / "README.md").write_text(readme, encoding="utf-8")

analytics_manifest = {
    "version": 1,
    "title": "地平线机器人（09660.HK）巴菲特—芒格两问研究",
    "surface": "report",
    "description": "公开主源支持的业务、现金所有者收益、稀释、同业与反向估值报告。",
    "generatedAt": "2026-07-29T12:20:00+08:00",
    "blocks": [
        {"id": "intro", "type": "markdown", "body": "# 地平线机器人（09660.HK）巴菲特—芒格两问研究\n业务增长机制可理解，但每股 owner earnings 与当前价格安全边际尚未被证明。"},
        {"id": "financial-heading", "type": "markdown", "body": "## 五年财务\n收入快速增长，经营亏损并未同步收敛。"},
        {"id": "financial-chart", "type": "chart", "chartId": "financial-trend"},
        {"id": "oe-heading", "type": "markdown", "body": "## 现金所有者收益\n两套代理在2023—2025年均为负。"},
        {"id": "oe-chart", "type": "chart", "chartId": "owner-earnings"},
        {"id": "valuation-heading", "type": "markdown", "body": "## 估值校准\nPE无意义；P/S只能校准市场预期。"},
        {"id": "peer-table-block", "type": "table", "tableId": "peer-table"},
    ],
    "charts": [
        {
            "id": "financial-trend",
            "title": "FY2021—FY2025收入、毛利与经营损益",
            "type": "bar",
            "dataset": "financial_tidy",
            "encodings": {"x": {"field": "period"}, "y": {"field": "value"}, "color": {"field": "series"}},
            "options": {"grouping": "grouped"},
        },
        {
            "id": "owner-earnings",
            "title": "FY2023—FY2025现金所有者收益代理",
            "type": "bar",
            "dataset": "owner_earnings_tidy",
            "encodings": {"x": {"field": "period"}, "y": {"field": "value"}, "color": {"field": "series"}},
            "options": {"grouping": "grouped"},
        },
    ],
    "tables": [
        {
            "id": "peer-table",
            "title": "同业P/S资格与校准",
            "dataset": "peer_valuation",
            "columns": [
                {"field": "company", "label": "公司"},
                {"field": "qualification", "label": "资格"},
                {"field": "ps", "label": "P/S", "format": "number"},
                {"field": "profitability", "label": "盈利/现金"},
            ],
            "defaultSort": {"field": "ps", "direction": "asc"},
        }
    ],
    "sources": [
        {"id": row["id"], "label": row["title"], "href": row["url"]}
        for row in sources
        if row["id"] in {"H01", "H03", "H04", "H05", "H06", "H07", "H08", "P01", "P02", "P03", "M01", "M03"}
    ],
}
financial_tidy = []
for row in financial_rows:
    for key, label in (
        ("revenue_rmb_m", "收入"),
        ("gross_profit_rmb_m", "毛利"),
        ("operating_loss_rmb_m", "经营损益"),
    ):
        financial_tidy.append({"period": row["period"], "series": label, "value": row[key]})
oe_tidy = []
for row in owner_earnings_rows:
    oe_tidy.extend(
        [
            {"period": row["period"], "series": "现金OE代理", "value": row["cash_oe_proxy_rmb_m"]},
            {"period": row["period"], "series": "严格核心OE", "value": row["strict_core_oe_proxy_rmb_m"]},
        ]
    )
analytics_snapshot = {
    "version": 1,
    "status": "ready",
    "generatedAt": "2026-07-29T12:20:00+08:00",
    "datasets": {
        "financial_tidy": financial_tidy,
        "owner_earnings_tidy": oe_tidy,
        "peer_valuation": [
            {
                "company": row["company"],
                "qualification": row["qualification"],
                "ps": row["ps"],
                "profitability": row["profitability"],
            }
            for row in peer_rows
        ],
    },
}
dump_json(ROOT / "analytics-manifest.json", analytics_manifest)
dump_json(ROOT / "analytics-snapshot.json", analytics_snapshot)

print(
    json.dumps(
        {
            "directory": str(ROOT),
            "combined_sha256": sha(ROOT / "combined-artifact.v2.json"),
            "report_sha256": sha(ROOT / "report.html"),
            "sources": len(sources),
            "evidence_anchors": len(anchors),
            "dimensions": len(research_dimensions),
            "indicators": sum(len(row["indicators"]) for row in research_dimensions),
            "gates": len(gates),
        },
        ensure_ascii=False,
        indent=2,
    )
)
