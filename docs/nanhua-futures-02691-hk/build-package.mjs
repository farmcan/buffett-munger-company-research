import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";

const root = path.dirname(fileURLToPath(import.meta.url));
const dataDir = path.join(root, "data");
fs.mkdirSync(dataDir, { recursive: true });
const writeJson = (name, value) =>
  fs.writeFileSync(path.join(root, name), `${JSON.stringify(value, null, 2)}\n`);
const esc = (value) => {
  const text = value == null ? "" : String(value);
  return /[",\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
};
const writeCsv = (name, headers, rows) =>
  fs.writeFileSync(
    path.join(dataDir, name),
    `${headers.join(",")}\n${rows.map((row) => headers.map((h) => esc(row[h])).join(",")).join("\n")}\n`,
  );
const sha = (text) => crypto.createHash("sha256").update(text).digest("hex");
const round = (number, digits = 4) => Number(number.toFixed(digits));

const generatedAt = "2026-07-27T18:10:00+08:00";
const researchDate = "2026-07-27";
const price = 6.65;
const fx = 0.86601;
const postCapShares = 1038.14454;

const sources = [
  {
    id: "F01", tier: "A", source_type: "audited_annual_report",
    title: "Nanhua Futures Co., Ltd. Annual Report 2025",
    url: "https://www.hkexnews.hk/listedco/listconews/sehk/2026/0329/2026032900007.pdf",
    published_at_status: "known", published_at: "2026-03-29", accessed_at: researchDate,
    period: "FY2025 with FY2022-FY2024 comparatives", audit_status: "audited",
    scope: "consolidated group and regulatory-capital disclosures",
    covers: ["identity", "financial_statements", "income_mix", "segments", "client_equity", "regulatory_capital", "governance"],
    content_sha256: "2a270e32d1985b2b79bdba032fa758e7a7d0d98d975acbe698c26da3014f9355",
  },
  {
    id: "F02", tier: "A", source_type: "quarterly_report",
    title: "Nanhua Futures Co., Ltd. 2026 First Quarterly Report",
    url: "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0421/2026042100045.pdf",
    published_at_status: "known", published_at: "2026-04-21", accessed_at: researchDate,
    period: "2026Q1 with 2025Q1 comparatives", audit_status: "unaudited",
    scope: "consolidated group and parent-company regulatory indicators",
    covers: ["quarterly_financials", "earnings_bridge", "cash_flow", "regulatory_capital", "ownership"],
    content_sha256: "547df87edb1af642394d538f921fe145cfdc2ca5fbd914ce2f624bb8bd88daad",
  },
  {
    id: "F03", tier: "A", source_type: "preliminary_profit_alert",
    title: "Estimated Increase in Operating Results for the First Half of 2026",
    url: "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0707/2026070701683.pdf",
    published_at_status: "known", published_at: "2026-07-07", accessed_at: researchDate,
    period: "2026H1", audit_status: "unaudited", scope: "preliminary parent profit range",
    covers: ["h1_profit_range", "derived_q2", "management_explanation"],
    content_sha256: "7bf00824d35527be5ba9469026cfbe0049e07505a83511f19385b8ed6c73afd2",
  },
  {
    id: "F04", tier: "A", source_type: "exchange_announcement",
    title: "Voluntary Announcement in Relation to H Share Repurchase Plan",
    url: "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0624/2026062401186.pdf",
    published_at_status: "known", published_at: "2026-06-24", accessed_at: researchDate,
    period: "2026 H-share repurchase mandate", audit_status: "not_applicable",
    scope: "listed H shares", covers: ["repurchase_authorization", "capital_allocation"],
    content_sha256: "8b24ca3ebc09a248ef79659041e40e0624a6da802570fb01fed523beeca436d0",
  },
  {
    id: "F05", tier: "A", source_type: "egm_results",
    title: "Poll Results of the 2026 First Extraordinary General Meeting",
    url: "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0716/2026071601063.pdf",
    published_at_status: "known", published_at: "2026-07-16", accessed_at: researchDate,
    period: "2026-07-16", audit_status: "not_applicable", scope: "shareholder approvals and issued shares",
    covers: ["repurchase_approval", "issued_shares", "treasury_shares"],
    content_sha256: "cb34d807a98ce834260e16342d4ca1b61950e68130c711900d018cfb4238ee66",
  },
  {
    id: "F06", tier: "A", source_type: "agm_circular",
    title: "Circular of the 2025 Annual General Meeting",
    url: "https://www.hkexnews.hk/listedco/listconews/sehk/2026/0522/2026052201694.pdf",
    published_at_status: "known", published_at: "2026-05-22", accessed_at: researchDate,
    period: "2026 capital actions", audit_status: "not_applicable", scope: "A/H share capital",
    covers: ["capitalisation_issue", "post_cap_share_count", "convertible_bond_proposal", "stock_connect"],
    content_sha256: "267eb1b7914c63352e2073ce8fe27ef41c9bd7e094106c5c0b50e8a6152eabb1",
  },
  {
    id: "F07", tier: "A", source_type: "monthly_return",
    title: "Monthly Return for the Month Ended 30 June 2026",
    url: "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0706/2026070601140.pdf",
    published_at_status: "known", published_at: "2026-07-06", accessed_at: researchDate,
    period: "2026-06-30", audit_status: "not_applicable", scope: "issued H shares and treasury shares",
    covers: ["share_count", "treasury_share_status"],
    content_sha256: "f181bef3475a2d89486335fee8f7ffa8b3ebbb2a0f0fb0eedf9c9528cbdfd8e2",
  },
  {
    id: "F09", tier: "A", source_type: "official_stock_connect_adjustment",
    title: "关于沪港通下港股通标的调整的通知",
    url: "https://big5.sse.com.cn/site/cht/www.sse.com.cn/services/hkexsc/disclo/announ/c/c_20260116_10805364.shtml",
    published_at_status: "known", published_at: "2026-01-16", accessed_at: researchDate,
    period: "effective 2026-01-19", audit_status: "not_applicable", scope: "Shanghai Southbound inclusion event",
    covers: ["stock_connect_inclusion_event"],
    content_sha256: "007e45815488316c060175be0aae974cb914aec6f3f05c74123cdc0be0173a32",
  },
  {
    id: "S01", tier: "A", source_type: "official_stock_connect_current_list",
    title: "上海证券交易所港股通股票名单（研究日冻结快照）",
    url: "https://www.sse.com.cn/services/hkexsc/disclo/eligible/",
    published_at_status: "not_disclosed", published_at: null, date_reason: "动态名单无单独发布日期；按研究日冻结。",
    accessed_at: researchDate, period: "as of 2026-07-27", audit_status: "not_applicable",
    scope: "Shanghai Southbound current eligibility", covers: ["stock_connect_current_status"],
    content_sha256: "db5f11d11554a4d984cc184f864a1bb9d95243ad8692789455f9948fbeaa0d8e",
  },
  {
    id: "S02", tier: "A", source_type: "official_stock_connect_current_list",
    title: "深圳证券交易所港股通标的证券名单（研究日冻结快照）",
    url: "https://www.szse.cn/szhk/hkbussiness/underlylist/",
    published_at_status: "not_disclosed", published_at: null, date_reason: "动态名单无单独发布日期；按研究日冻结。",
    accessed_at: researchDate, period: "as of 2026-07-27", audit_status: "not_applicable",
    scope: "Shenzhen Southbound current eligibility", covers: ["stock_connect_current_status"],
    content_sha256: "a56de882ba72cc7ddf3f2b1b5d1d87bb8092a139f36fe199ccb495edbed1d541",
  },
  {
    id: "F10", tier: "A", source_type: "official_stock_connect_rules",
    title: "上海证券交易所沪港通业务实施办法（2024年修订）",
    url: "https://www.sse.com.cn/lawandrules/sselawsrules2025/global/hkexsc/c/c_20251017_10795123.shtml",
    published_at_status: "known", published_at: "2024-06-14", accessed_at: researchDate,
    period: "current rules checked 2026-07-27", audit_status: "not_applicable",
    scope: "Shanghai Southbound eligibility and removal conditions", covers: ["stock_connect_rules", "exit_risk"],
    content_sha256: "ef88727f17828c6697995b1478f964e0c77dea0591e1056dbb8467fead14dcf2",
  },
  {
    id: "F11", tier: "A", source_type: "regulatory_measure",
    title: "关于对南华期货采取出具警示函措施的决定",
    url: "https://www.csrc.gov.cn/zhejiang/c103952/c7623963/content.shtml",
    published_at_status: "known", published_at: "2026-04-01", accessed_at: researchDate,
    period: "2026-04-01", audit_status: "not_applicable", scope: "PRC futures operations",
    covers: ["internal_controls", "employee_conduct", "remediation"],
    content_sha256: "470df067a6b9947b8777cf30645cd080c17a960bf1b5c7d07315607352644ace",
  },
  {
    id: "F12", tier: "A", source_type: "official_industry_statistics",
    title: "2025年全国期货市场交易情况",
    url: "https://www.cfachina.org/servicesupport/researchandpublishin/statisticalsdata/monthlytransactiondata/202601/t20260109_85987.html",
    published_at_status: "known", published_at: "2026-01-09", accessed_at: researchDate,
    period: "FY2025", audit_status: "not_applicable", scope: "PRC futures market",
    covers: ["industry_volume", "industry_turnover"],
    content_sha256: "6f833a557885cea781954b3df7a26ec06623766788ae9a46c97218d68b3382b5",
  },
  {
    id: "F13", tier: "A", source_type: "official_industry_statistics",
    title: "2026年上半年全国期货市场交易情况",
    url: "https://www.cfachina.org/servicesupport/researchandpublishin/statisticalsdata/monthlytransactiondata/202607/t20260713_89336.html",
    published_at_status: "known", published_at: "2026-07-13", accessed_at: researchDate,
    period: "2026H1", audit_status: "not_applicable", scope: "PRC futures market",
    covers: ["industry_volume", "industry_turnover"],
    content_sha256: "86f993d120ec7620cef110674d7d975f20da8b754d9144bfaa5d5de6bd185611",
  },
  {
    id: "G01", tier: "A", source_type: "exchange_announcement",
    title: "Proposed Change of Auditors",
    url: "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0327/2026032704532.pdf",
    published_at_status: "known", published_at: "2026-03-27", accessed_at: researchDate,
    period: "FY2026 audit appointment", audit_status: "not_applicable", scope: "group audit governance",
    covers: ["auditor_change", "audit_monitor"],
    content_sha256: "ecf7d52a0bf5fff0fecd9356cc7a743575092dff5b704d3df6435295d6600b44",
  },
  {
    id: "G02", tier: "A", source_type: "connected_transaction_announcement",
    title: "Revision of Annual Cap for Continuing Connected Transaction",
    url: "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0327/2026032703520.pdf",
    published_at_status: "known", published_at: "2026-03-27", accessed_at: researchDate,
    period: "2026-2027", audit_status: "not_applicable", scope: "procurement from controller group",
    covers: ["related_party_procurement", "annual_cap"],
    content_sha256: "4580bb67f1a81eb401fdf8cd92b93f7edef5583ed499a241a493e5d76478aea5",
  },
  {
    id: "G03", tier: "A", source_type: "dividend_policy_announcement",
    title: "Shareholders' Dividend Return Plan for 2026-2028",
    url: "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0327/2026032703402.pdf",
    published_at_status: "known", published_at: "2026-03-27", accessed_at: researchDate,
    period: "2026-2028", audit_status: "not_applicable", scope: "parent-company distributable profit",
    covers: ["dividend_policy", "regulatory_conditions"],
    content_sha256: "7f1f3db38b2d45a5384b2fc86f47715ef9c45d65a13c0b41354a6a0d4e01745e",
  },
  {
    id: "G04", tier: "A", source_type: "accounting_estimate_announcement",
    title: "Change in Accounting Estimates",
    url: "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0327/2026032703310.pdf",
    published_at_status: "known", published_at: "2026-03-27", accessed_at: researchDate,
    period: "effective 2026-01-01", audit_status: "not_applicable", scope: "expected-credit-loss estimates",
    covers: ["accounting_estimate_change", "earnings_quality"],
    content_sha256: "063ccd0222c1d84c84eb01ea136c4299dd854b149bad8afeeae97cf569aceb58",
  },
  {
    id: "P01", tier: "B", source_type: "secondary_market_daily_prices",
    title: "Tencent market data daily adjusted K-line for HK02691",
    url: "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=hk02691,day,2025-12-01,2026-07-27,400,qfq",
    published_at_status: "not_applicable", published_at: null, date_reason: "行情接口为动态响应。",
    accessed_at: researchDate, period: "2025-12-22 to 2026-07-27", audit_status: "not_applicable",
    scope: "HKEX H-share secondary-market OHLCV", covers: ["price", "event_windows", "liquidity"],
    content_sha256: "5e133b9d93e2287384d7a65fdb5539949739c284eb1dc16aa1ec07c384bf9b84",
  },
  {
    id: "P02", tier: "A", source_type: "official_fx_reference",
    title: "国家外汇管理局人民币汇率中间价查询（2026-07-27 HKD）",
    url: "https://www.safe.gov.cn/AppStructured/hlw/RMBQuery.do",
    published_at_status: "known", published_at: "2026-07-27", accessed_at: researchDate,
    period: "2026-07-27", audit_status: "not_applicable", scope: "CNY per HKD reference rate",
    covers: ["fx", "valuation_currency_conversion"],
    content_sha256: "488d01ee9a0b2c7db836665bd7faa00792d6541c8fe2093d2623097dc85e4381",
  },
  {
    id: "U01", tier: "A", source_type: "sec_10k",
    title: "CME Group Inc. 2025 Form 10-K",
    url: "https://www.sec.gov/Archives/edgar/data/1156375/000115637526000009/cme-20251231.htm",
    published_at_status: "known", published_at: "2026-02-27", accessed_at: researchDate,
    period: "FY2025", audit_status: "audited", scope: "US exchange and clearing infrastructure peer",
    covers: ["thematic_peer", "market_infrastructure"],
    content_sha256: "14c97feff07f9393b6d6e0711daae61d27a58461525a0c8382d893ed4387ff0d",
  },
  {
    id: "U02", tier: "A", source_type: "sec_10k",
    title: "Interactive Brokers Group, Inc. 2025 Form 10-K",
    url: "https://www.sec.gov/Archives/edgar/data/1381197/000138119726000062/ibkr-20251231.htm",
    published_at_status: "known", published_at: "2026-02-27", accessed_at: researchDate,
    period: "FY2025", audit_status: "audited", scope: "global electronic brokerage thematic peer",
    covers: ["thematic_peer", "brokerage", "net_interest"],
    content_sha256: "027c4025b6d6530f9df6fc28c1202ecc668b3588840d9bac85e4244cdac700ed",
  },
];

const annual = [
  { period: "FY2021", operating_income_rmb_m: "", parent_profit_rmb_m: 242.603, total_assets_rmb_m: "", parent_equity_rmb_m: "", client_payables_rmb_m: "", eps_pre_cap_rmb: "", roe_pct: "", cfo_rmb_m: "", scope_note: "五年利润序列；2021口径来自公司历史披露，未与HKFRS operating income逐项重列" },
  { period: "FY2022", operating_income_rmb_m: 954.406, parent_profit_rmb_m: 246.060, total_assets_rmb_m: 34189.185, parent_equity_rmb_m: 3316.559, client_payables_rmb_m: 27505.794, eps_pre_cap_rmb: 0.40, roe_pct: 7.75, cfo_rmb_m: "", scope_note: "经审计比较数" },
  { period: "FY2023", operating_income_rmb_m: 1292.872, parent_profit_rmb_m: 401.855, total_assets_rmb_m: 36325.522, parent_equity_rmb_m: 3703.377, client_payables_rmb_m: 29039.353, eps_pre_cap_rmb: 0.66, roe_pct: 11.46, cfo_rmb_m: 1152.500, scope_note: "经审计" },
  { period: "FY2024", operating_income_rmb_m: 1354.843, parent_profit_rmb_m: 457.972, total_assets_rmb_m: 48863.397, parent_equity_rmb_m: 4115.254, client_payables_rmb_m: 42596.980, eps_pre_cap_rmb: 0.75, roe_pct: 11.71, cfo_rmb_m: -700.408, scope_note: "经审计；CFO受客户保证金影响" },
  { period: "FY2025", operating_income_rmb_m: 1387.511, parent_profit_rmb_m: 486.264, total_assets_rmb_m: 65472.642, parent_equity_rmb_m: 5595.853, client_payables_rmb_m: 57191.041, eps_pre_cap_rmb: 0.80, roe_pct: 11.30, cfo_rmb_m: 1782.044, scope_note: "经审计；CFO受客户保证金影响" },
];
const quarterly = [
  { metric: "operating_revenue", q1_2025_rmb_m: 269.603, q1_2026_rmb_m: 433.131, yoy_pct: 60.66, h1_2025_rmb_m: "", h1_2026_rmb_m: "", q2_2025_rmb_m: "", implied_q2_2026_rmb_m: "", audit_status: "Q1 unaudited" },
  { metric: "parent_profit", q1_2025_rmb_m: 85.738, q1_2026_rmb_m: 204.763, yoy_pct: 138.82, h1_2025_rmb_m: 231.254, h1_2026_rmb_m: "375-405", q2_2025_rmb_m: 145.516, implied_q2_2026_rmb_m: "170.237-200.237", audit_status: "H1 preliminary; Q2 derived" },
  { metric: "deducted_parent_profit", q1_2025_rmb_m: "", q1_2026_rmb_m: "", yoy_pct: "", h1_2025_rmb_m: 231.784, h1_2026_rmb_m: "377-407", q2_2025_rmb_m: "", implied_q2_2026_rmb_m: "", audit_status: "H1 preliminary" },
];
const income = [
  { item: "net_fee_and_commission", fy2024_rmb_m: 542.397, fy2025_rmb_m: 605.560, yoy_pct: 11.65, fy2025_mix_pct: 43.64 },
  { item: "net_interest", fy2024_rmb_m: 681.800, fy2025_rmb_m: 572.343, yoy_pct: -16.05, fy2025_mix_pct: 41.25 },
  { item: "net_investment_gains", fy2024_rmb_m: 70.336, fy2025_rmb_m: 148.070, yoy_pct: 110.52, fy2025_mix_pct: 10.67 },
  { item: "net_trading", fy2024_rmb_m: "", fy2025_rmb_m: 1.347, yoy_pct: "", fy2025_mix_pct: 0.10 },
  { item: "other_operating_income", fy2024_rmb_m: "", fy2025_rmb_m: 60.191, yoy_pct: "", fy2025_mix_pct: 4.34 },
];
const fees = [
  { item: "futures_brokerage", fy2024_rmb_m: 446.298, fy2025_rmb_m: 500.313, yoy_pct: 12.10, share_of_net_fees_pct: 82.62 },
  { item: "asset_management", fy2024_rmb_m: 25.763, fy2025_rmb_m: 40.287, yoy_pct: 56.37, share_of_net_fees_pct: 6.65 },
  { item: "fund_management", fy2024_rmb_m: 58.093, fy2025_rmb_m: 54.613, yoy_pct: -5.99, share_of_net_fees_pct: 9.02 },
  { item: "other", fy2024_rmb_m: "", fy2025_rmb_m: 10.347, yoy_pct: "", share_of_net_fees_pct: 1.71 },
];
const segments = [
  { segment: "PRC_futures_brokerage", fy2024_income_rmb_m: 494.386, fy2025_income_rmb_m: 474.628, fy2024_pbt_rmb_m: 35.210, fy2025_pbt_rmb_m: 51.627 },
  { segment: "wealth_management", fy2024_income_rmb_m: 68.220, fy2025_income_rmb_m: 64.979, fy2024_pbt_rmb_m: -3.366, fy2025_pbt_rmb_m: -24.066 },
  { segment: "risk_management", fy2024_income_rmb_m: 127.686, fy2025_income_rmb_m: 79.978, fy2024_pbt_rmb_m: 16.857, fy2025_pbt_rmb_m: 6.318 },
  { segment: "overseas_financial_services", fy2024_income_rmb_m: 654.204, fy2025_income_rmb_m: 757.506, fy2024_pbt_rmb_m: 464.814, fy2025_pbt_rmb_m: 501.010 },
  { segment: "other", fy2024_income_rmb_m: 10.347, fy2025_income_rmb_m: 10.420, fy2024_pbt_rmb_m: 8.144, fy2025_pbt_rmb_m: 10.420 },
];
const geography = [
  { geography: "Mainland_China", fy2025_income_rmb_m: 630.005, share_pct: 45.41, yoy_pct: -10.10 },
  { geography: "United_States", fy2025_income_rmb_m: 113.412, share_pct: 8.17, yoy_pct: "" },
  { geography: "Hong_Kong", fy2025_income_rmb_m: 359.135, share_pct: 25.88, yoy_pct: "" },
  { geography: "Singapore", fy2025_income_rmb_m: 148.079, share_pct: 10.67, yoy_pct: "" },
  { geography: "United_Kingdom", fy2025_income_rmb_m: 136.880, share_pct: 9.86, yoy_pct: "" },
];
const q1Bridge = [
  { item: "net_fee_and_commission", q1_2025_rmb_m: 106.601, q1_2026_rmb_m: 187.355, change_rmb_m: 80.754, interpretation: "交易活跃和客户规模扩张的主经营贡献" },
  { item: "net_interest", q1_2025_rmb_m: 143.052, q1_2026_rmb_m: 193.121, change_rmb_m: 50.069, interpretation: "客户资金规模上升抵消部分利率下行" },
  { item: "investment_gains", q1_2025_rmb_m: 13.457, q1_2026_rmb_m: 107.406, change_rmb_m: 93.949, interpretation: "高波动、不可直接线性外推" },
  { item: "fair_value_change", q1_2025_rmb_m: 2.516, q1_2026_rmb_m: -44.740, change_rmb_m: -47.256, interpretation: "抵消投资收益" },
  { item: "foreign_exchange", q1_2025_rmb_m: 0.718, q1_2026_rmb_m: -14.488, change_rmb_m: -15.206, interpretation: "跨境业务的汇率波动" },
  { item: "credit_impairment_expense", q1_2025_rmb_m: 7.098, q1_2026_rmb_m: -23.301, change_rmb_m: -30.399, interpretation: "负费用为转回；约30.4百万元顺风" },
  { item: "general_and_admin_expense", q1_2025_rmb_m: 156.419, q1_2026_rmb_m: 208.199, change_rmb_m: 51.780, interpretation: "规模扩张成本增加" },
];
const riskCapital = [
  { period: "FY2024", net_capital_rmb_m: 1509.670, net_capital_to_risk_pct: 166, net_capital_to_net_assets_pct: 48, current_assets_to_current_liabilities_pct: 525, liabilities_to_net_assets_pct: 28, clearing_settlement_rmb_m: 1160.380 },
  { period: "FY2025", net_capital_rmb_m: 2744.257, net_capital_to_risk_pct: 240, net_capital_to_net_assets_pct: 65, current_assets_to_current_liabilities_pct: 696, liabilities_to_net_assets_pct: 23, clearing_settlement_rmb_m: 601.474 },
  { period: "2026Q1", net_capital_rmb_m: 1750.832, net_capital_to_risk_pct: 137, net_capital_to_net_assets_pct: 41, current_assets_to_current_liabilities_pct: 536, liabilities_to_net_assets_pct: 23, clearing_settlement_rmb_m: 457.710 },
  { period: "regulatory_minimum", net_capital_rmb_m: 30, net_capital_to_risk_pct: 100, net_capital_to_net_assets_pct: 20, current_assets_to_current_liabilities_pct: 100, liabilities_to_net_assets_pct: "", clearing_settlement_rmb_m: 26.8 },
];
const shareBridge = [
  { scenario: "pre_capitalisation_issued", shares_m: 717.724893, treatment: "A 610.065893m + H 107.659m", included_in_base_valuation: "no" },
  { scenario: "post_capitalisation_expected", shares_m: 1038.144540, treatment: "A 882.038990m + H 156.105550m; 4.5-for-10", included_in_base_valuation: "yes" },
  { scenario: "employee_treasury_shares_reactivated", shares_m: 1043.825774, treatment: "adds 5.681234m A treasury shares", included_in_base_valuation: "scenario only" },
  { scenario: "illustrative_CB_full_conversion", shares_m: 1114.045868, treatment: "adds 75.901328m illustrative shares; final terms unknown", included_in_base_valuation: "scenario only" },
  { scenario: "employee_plus_CB", shares_m: 1119.727102, treatment: "both optional dilution paths", included_in_base_valuation: "scenario only" },
];
const events = [
  { event: "IPO", disclosure_date: "2025-12-22", event_type: "listing", status: "occurred", source_id: "F01", expected_or_actual: "actual" },
  { event: "Stock Connect inclusion", disclosure_date: "2026-01-16", event_type: "stock_connect", status: "occurred", source_id: "F09", expected_or_actual: "actual" },
  { event: "Annual results and governance announcements", disclosure_date: "2026-03-27", event_type: "earnings_governance", status: "occurred", source_id: "F01;G01;G02;G03;G04", expected_or_actual: "actual" },
  { event: "CSRC warning letter", disclosure_date: "2026-04-01", event_type: "regulatory", status: "occurred", source_id: "F11", expected_or_actual: "actual" },
  { event: "2026Q1 report", disclosure_date: "2026-04-21", event_type: "earnings", status: "occurred", source_id: "F02", expected_or_actual: "actual" },
  { event: "H-share repurchase plan", disclosure_date: "2026-06-24", event_type: "capital_allocation", status: "authorized_not_executed", source_id: "F04;F05", expected_or_actual: "actual_authorization" },
  { event: "2026H1 profit alert", disclosure_date: "2026-07-07", event_type: "earnings", status: "occurred", source_id: "F03", expected_or_actual: "preliminary" },
  { event: "Expected capitalisation H shares begin trading", disclosure_date: "2026-08-11", event_type: "share_capital", status: "future_expected", source_id: "F06", expected_or_actual: "expected_not_completed_as_of_research_date" },
  { event: "Formal 2026 interim results", disclosure_date: "TBA", event_type: "earnings", status: "unknown", source_id: "F03", expected_or_actual: "not_found_as_of_research_date" },
];
const eventWindows = [
  { event: "IPO", t_minus_1_date: "", t_minus_1_close: "", t0_date: "2025-12-22", t0_close: 9.10, t_plus_5_date: "2025-12-31", t_plus_5_close: 9.91, t0_return_pct: "", t0_to_t5_pct: 8.90, tminus1_to_t5_pct: "", t0_volume: 7945500, prior20_avg_volume: "", volume_ratio: "", adjustment_note: "上市首日" },
  { event: "Stock Connect inclusion", t_minus_1_date: "2026-01-16", t_minus_1_close: 12.29, t0_date: "2026-01-19", t0_close: 11.41, t_plus_5_date: "2026-01-26", t_plus_5_close: 11.37, t0_return_pct: -7.16, t0_to_t5_pct: -0.35, tminus1_to_t5_pct: -7.49, t0_volume: 5446500, prior20_avg_volume: 2187265, volume_ratio: 2.49, adjustment_note: "公告后下一完整交易日为T0" },
  { event: "Annual results and governance package", t_minus_1_date: "2026-03-27", t_minus_1_close: 10.86, t0_date: "2026-03-30", t0_close: 11.04, t_plus_5_date: "2026-04-09", t_plus_5_close: 10.90, t0_return_pct: 1.66, t0_to_t5_pct: -1.27, tminus1_to_t5_pct: 0.37, t0_volume: 4013000, prior20_avg_volume: 2720550, volume_ratio: 1.48, adjustment_note: "多项公告同日，无法单独归因" },
  { event: "Regulatory warning", t_minus_1_date: "2026-04-01", t_minus_1_close: 11.25, t0_date: "2026-04-02", t0_close: 10.60, t_plus_5_date: "2026-04-14", t_plus_5_close: 10.96, t0_return_pct: -5.78, t0_to_t5_pct: 3.40, tminus1_to_t5_pct: -2.58, t0_volume: 1678500, prior20_avg_volume: 2498925, volume_ratio: 0.67, adjustment_note: "相关不代表因果" },
  { event: "2026Q1 report", t_minus_1_date: "2026-04-20", t_minus_1_close: 11.42, t0_date: "2026-04-21", t0_close: 10.86, t_plus_5_date: "2026-04-28", t_plus_5_close: 10.18, t0_return_pct: -4.90, t0_to_t5_pct: -6.26, tminus1_to_t5_pct: -10.86, t0_volume: 4279000, prior20_avg_volume: 1574325, volume_ratio: 2.72, adjustment_note: "强利润增长未对应正向短窗" },
  { event: "H-share repurchase plan", t_minus_1_date: "2026-06-24", t_minus_1_close: 6.17, t0_date: "2026-06-25", t0_close: 6.28, t_plus_5_date: "2026-07-03", t_plus_5_close: 6.18, t0_return_pct: 1.78, t0_to_t5_pct: -1.59, tminus1_to_t5_pct: 0.16, t0_volume: 2535500, prior20_avg_volume: 2143250, volume_ratio: 1.18, adjustment_note: "授权方案不等于实际成交" },
  { event: "2026H1 profit alert", t_minus_1_date: "2026-07-07", t_minus_1_close: 6.03, t0_date: "2026-07-08", t0_close: 6.09, t_plus_5_date: "2026-07-15", t_plus_5_close: 6.21, t0_return_pct: 1.00, t0_to_t5_pct: 1.97, tminus1_to_t5_pct: 2.99, t0_volume: 818000, prior20_avg_volume: 1722625, volume_ratio: 0.47, adjustment_note: "预告未经审计" },
  { event: "EGM repurchase approval", t_minus_1_date: "2026-07-16", t_minus_1_close: 6.41, t0_date: "2026-07-17", t0_close: 6.45, t_plus_5_date: "2026-07-24", t_plus_5_close: 6.64, t0_return_pct: 0.62, t0_to_t5_pct: 2.95, tminus1_to_t5_pct: 3.59, t0_volume: 5501000, prior20_avg_volume: 1531450, volume_ratio: 3.59, adjustment_note: "仍未发现实际回购披露" },
];
const industry = [
  { period: "FY2025", market_volume_billion_lots: 9.074, volume_yoy_pct: 17.40, turnover_trillion_rmb: 766.254, turnover_yoy_pct: 23.74, source_id: "F12" },
  { period: "2026H1", market_volume_billion_lots: 5.105, volume_yoy_pct: 25.23, turnover_trillion_rmb: 482.701, turnover_yoy_pct: 42.08, source_id: "F13" },
  { period: "2026-06", market_volume_billion_lots: "", volume_yoy_pct: "", turnover_trillion_rmb: "", turnover_yoy_pct: 52.72, source_id: "F13" },
];
const smallCap = [
  { risk: "监管资本缓冲压缩", likelihood: "high", impact: "high", evidence: "净资本/风险资本由240%降至137%", monitor: "正式中报净资本、风险资本及业务扩张" },
  { risk: "采购内控与员工行为整改", likelihood: "medium", impact: "high", evidence: "浙江证监局警示函", monitor: "整改结果、后续监管措施" },
  { risk: "境外利润集中", likelihood: "high", impact: "high", evidence: "2025境外PBT占集团约91.9%", monitor: "美国/香港/新加坡业务利润和监管变化" },
  { risk: "客户保证金利率敏感", likelihood: "high", impact: "medium_high", evidence: "2025客户权益上升但净利息收入下降16.05%", monitor: "客户权益、计息收益率、政策利率" },
  { risk: "投资与公允价值波动", likelihood: "high", impact: "medium_high", evidence: "2026Q1投资收益+107.4m、公允价值-44.7m", monitor: "投资损益和OCI拆分" },
  { risk: "可转债潜在摊薄", likelihood: "medium", impact: "medium_high", evidence: "拟发行不超过RMB1.2bn，示例转股75.9m股", monitor: "审批、发行、最终转股价与用途" },
  { risk: "H股流动性与上市历史短", likelihood: "high", impact: "medium_high", evidence: "上市不足一年；2026-07-27成交37.25万股，低于20日均量约140.20万股", monitor: "成交量、价差、南向持股和股本事件" },
  { risk: "回购执行不确定", likelihood: "medium", impact: "medium", evidence: "授权已通过但截至研究日未发现成交披露", monitor: "next-day disclosure和月报表" },
  { risk: "港股通资格变化", likelihood: "low_current_conditional", impact: "high", evidence: "研究日沪深两份名单均eligible；规则含A股风险警示/退市等条件", monitor: "沪深当前名单和A股状态" },
  { risk: "会计估计与审计师同年变化", likelihood: "high_as_event", impact: "medium_high", evidence: "预期信用损失估计变更；拟更换为安永", monitor: "2026中报会计影响和新审计师报告" },
];
const ownerSensitivity = [
  { case: "high_retention", reported_parent_profit_rmb_m: 486.264, assumed_regulatory_retention_pct: 70, candidate_distributable_rmb_m: 145.879, status: "sensitivity_not_owner_earnings" },
  { case: "base_retention", reported_parent_profit_rmb_m: 486.264, assumed_regulatory_retention_pct: 55, candidate_distributable_rmb_m: 218.819, status: "sensitivity_not_owner_earnings" },
  { case: "low_retention", reported_parent_profit_rmb_m: 486.264, assumed_regulatory_retention_pct: 40, candidate_distributable_rmb_m: 291.758, status: "sensitivity_not_owner_earnings" },
];
const valuation = [
  { label: "reported_fy", profit_basis_rmb_m: 486.264, eps_rmb: round(486.264 / postCapShares, 6), eps_hkd: round(486.264 / postCapShares / fx, 6), price_hkd: price, pe_x: round(price / (486.264 / postCapShares / fx), 2), pb_x: round(price / (5595.853 / postCapShares / fx), 2), status: "calculated" },
  { label: "reported_ttm", profit_basis_rmb_m: 605.289, eps_rmb: round(605.289 / postCapShares, 6), eps_hkd: round(605.289 / postCapShares / fx, 6), price_hkd: price, pe_x: round(price / (605.289 / postCapShares / fx), 2), pb_x: round(price / (5595.853 / postCapShares / fx), 2), status: "calculated" },
  { label: "normalized_2022_2025_average", profit_basis_rmb_m: 398.038, eps_rmb: round(398.038 / postCapShares, 6), eps_hkd: round(398.038 / postCapShares / fx, 6), price_hkd: price, pe_x: round(price / (398.038 / postCapShares / fx), 2), pb_x: round(price / (5595.853 / postCapShares / fx), 2), status: "simple_cycle_average_not_forecast" },
];
const usMapping = [
  { company: "CME Group", ticker: "CME", relationship: "thematic_peer", comparable_mechanism: "交易所与清算基础设施，受衍生品交易活跃度影响", non_comparable_boundary: "CME是市场基础设施，不是期货经纪商，也不是南华同一公司或同等经济敞口", source_id: "U01" },
  { company: "Interactive Brokers", ticker: "IBKR", relationship: "thematic_peer", comparable_mechanism: "电子经纪、客户资产与净利息收入", non_comparable_boundary: "客户结构、监管资本、产品与地域组合不同；不是南华同一公司或同等经济敞口", source_id: "U02" },
];

writeCsv("annual-financials.csv", Object.keys(annual[0]), annual);
writeCsv("quarterly-financials.csv", Object.keys(quarterly[0]), quarterly);
writeCsv("income-composition.csv", Object.keys(income[0]), income);
writeCsv("fee-breakdown.csv", Object.keys(fees[0]), fees);
writeCsv("segment-results.csv", Object.keys(segments[0]), segments);
writeCsv("geographic-revenue.csv", Object.keys(geography[0]), geography);
writeCsv("earnings-quality-bridge.csv", Object.keys(q1Bridge[0]), q1Bridge);
writeCsv("risk-capital.csv", Object.keys(riskCapital[0]), riskCapital);
writeCsv("fully-diluted-share-bridge.csv", Object.keys(shareBridge[0]), shareBridge);
writeCsv("event-timeline.csv", Object.keys(events[0]), events);
writeCsv("event-price-windows.csv", Object.keys(eventWindows[0]), eventWindows);
writeCsv("industry-cycle.csv", Object.keys(industry[0]), industry);
writeCsv("small-cap-risk-register.csv", Object.keys(smallCap[0]), smallCap);
writeCsv("owner-earnings-sensitivity.csv", Object.keys(ownerSensitivity[0]), ownerSensitivity);
writeCsv("pe-pb-normalized-matrix.csv", Object.keys(valuation[0]), valuation);
writeCsv("share-capital-valuation.csv", ["item","value","unit","status","as_of","source_id","note"], [
  { item: "H_share_close", value: 6.65, unit: "HKD", status: "secondary_market_frozen", as_of: researchDate, source_id: "P01", note: "2026-07-27 close" },
  { item: "pre_capitalisation_total_issued", value: 717.724893, unit: "million_shares", status: "official", as_of: "2026-05-22", source_id: "F06", note: "includes 5.681234m A treasury shares" },
  { item: "capitalisation_eligible_base", value: 712.043659, unit: "million_shares", status: "derived_from_official", as_of: "2026-05-22", source_id: "F06", note: "717.724893 - 5.681234" },
  { item: "capitalisation_new_shares", value: 320.419647, unit: "million_shares", status: "derived_from_official", as_of: "2026-05-22", source_id: "F06", note: "712.043659 × 4.5 / 10, rounded" },
  { item: "post_capitalisation_total_issued", value: 1038.144540, unit: "million_shares", status: "official_expected", as_of: "2026-08-11", source_id: "F06", note: "final registration controls; 717.724893 + 320.419647" },
  { item: "FY2025_post_cap_EPS", value: round(486.264/postCapShares,6), unit: "RMB_per_share", status: "derived_audited_numerator", as_of: "2025-12-31", source_id: "F01;F06", note: "486.264 / 1,038.144540" },
  { item: "FY2025_post_cap_BVPS", value: round(5595.853/postCapShares,6), unit: "RMB_per_share", status: "derived_audited_numerator", as_of: "2025-12-31", source_id: "F01;F06", note: "5,595.853 / 1,038.144540" },
  { item: "FY2025_PE", value: valuation[0].pe_x, unit: "x", status: "derived", as_of: researchDate, source_id: "F01;F06;P01;P02", note: "currency-consistent post-cap denominator" },
  { item: "FY2025_PB", value: valuation[0].pb_x, unit: "x", status: "derived", as_of: researchDate, source_id: "F01;F06;P01;P02", note: "currency-consistent post-cap denominator" },
  { item: "proposed_CB_max_principal", value: 1200, unit: "RMB_million", status: "proposed_not_issued", as_of: researchDate, source_id: "F06", note: "final terms unknown" },
  { item: "illustrative_CB_conversion_shares", value: 75.901328, unit: "million_shares", status: "illustrative_only", as_of: researchDate, source_id: "F06", note: "RMB1,200m / RMB15.81 per A share" },
]);
writeCsv("us-thematic-mapping.csv", Object.keys(usMapping[0]), usMapping);
writeCsv("stock-connect-status.csv", ["security_id", "ticker", "as_of", "shanghai_southbound", "shenzhen_southbound", "combined_status", "relationship", "source_ids"], [
  { security_id: "XHKG:02691", ticker: "02691", as_of: researchDate, shanghai_southbound: "eligible", shenzhen_southbound: "eligible", combined_status: "eligible", relationship: "same_company_listing_with_603093.SH", source_ids: "S01;S02;F10" },
]);
writeCsv("operating-kpis.csv", ["period", "metric", "value", "unit", "source_id", "scope_note"], [
  { period: "FY2025", metric: "domestic_client_equity", value: 38.982, unit: "RMBbn", source_id: "F01", scope_note: "segregated client equity" },
  { period: "FY2025", metric: "overseas_client_net_equity", value: 23.306, unit: "HKDbn", source_id: "F01", scope_note: "overseas operations" },
  { period: "FY2025", metric: "overseas_AUM", value: 4.812, unit: "HKDbn", source_id: "F01", scope_note: "overseas asset management" },
  { period: "FY2025", metric: "domestic_AUM", value: 1.081, unit: "RMBbn", source_id: "F01", scope_note: "domestic asset management" },
  { period: "FY2025", metric: "public_fund_scale", value: 19.136, unit: "RMBbn", source_id: "F01", scope_note: "Nanhua Fund" },
  { period: "FY2025", metric: "OTC_new_notional", value: 74.9, unit: "RMBbn", source_id: "F01", scope_note: "risk-management subsidiary" },
  { period: "FY2025", metric: "insurance_futures_projects", value: "75+", unit: "projects", source_id: "F01", scope_note: "management disclosure" },
  { period: "FY2025", metric: "risk_protection", value: 1.881, unit: "RMBbn", source_id: "F01", scope_note: "management disclosure" },
]);
writeCsv("governance-events.csv", ["date", "event", "fact", "interpretation", "source_id"], [
  { date: "2026-03-27", event: "accounting_estimate_change", fact: "ECL low-risk counterparty pools revised prospectively; expected FY2026 PBT effect no more than RMB40m", interpretation: "Q1 exact contribution not disclosed; normalize cautiously", source_id: "G04" },
  { date: "2026-03-27", event: "auditor_change", fact: "proposed Pan-China/Confucius International to EY Hua Ming/EY; no disagreement stated", interpretation: "monitor transition and 2026 audit, not automatic misconduct evidence", source_id: "G01" },
  { date: "2026-03-27", event: "connected_procurement_cap", fact: "2026/27 annual cap revised RMB1m to RMB7m", interpretation: "sevenfold increase but small absolute amount; review pricing and oversight", source_id: "G02" },
  { date: "2026-03-27", event: "dividend_plan", fact: "cash dividend no less than 10% of distributable profit if profit and capital conditions met", interpretation: "conditional floor, not unconditional cash commitment", source_id: "G03" },
  { date: "2026-04-01", event: "regulatory_warning", fact: "procurement/internal controls and employee-conduct management deficiencies; written remediation required", interpretation: "survival and governance monitor", source_id: "F11" },
]);
writeCsv("financial-source-definitions.csv", ["metric", "definition", "unit", "scope", "formula_or_boundary", "source_id"], [
  { metric: "operating_income", definition: "HKFRS net operating income for financial institution", unit: "RMBm", scope: "consolidated", formula_or_boundary: "not equivalent to PRC gross commodity sales revenue", source_id: "F01" },
  { metric: "parent_profit", definition: "profit attributable to equity shareholders of the parent", unit: "RMBm", scope: "consolidated attribution", formula_or_boundary: "used for EPS numerator", source_id: "F01" },
  { metric: "client_payables", definition: "amounts payable to clients backed by segregated client assets", unit: "RMBm", scope: "customer funds", formula_or_boundary: "not ordinary corporate funding", source_id: "F01" },
  { metric: "TTM_parent_profit", definition: "FY2025 + 2026Q1 - 2025Q1", unit: "RMBm", scope: "derived", formula_or_boundary: "486.264+204.763-85.738=605.289", source_id: "F01;F02" },
  { metric: "normalized_profit", definition: "simple FY2022-FY2025 parent-profit average", unit: "RMBm", scope: "derived cycle cross-check", formula_or_boundary: "(246.060+401.855+457.972+486.264)/4=398.038", source_id: "F01" },
]);

const methodologyRefs = [
  { id: "berkshire_owner_manual", title: "Berkshire Hathaway Owner's Manual", url: "https://www.berkshirehathaway.com/ownman.pdf", use: "以每股长期内在价值、股东视角和理性资本配置组织结论。" },
  { id: "berkshire_1977_letter", title: "1977 Chairman's Letter", url: "https://www.berkshirehathaway.com/letters/1977.html", use: "用长期股东资本回报而非单期利润增速检验经营结果。" },
  { id: "berkshire_1986_letter", title: "1986 Chairman's Letter", url: "https://www.berkshirehathaway.com/letters/1986.html", use: "owner earnings 概念；本报告明确金融机构合并CFO不可机械套用。" },
  { id: "berkshire_1989_letter", title: "1989 Chairman's Letter", url: "https://www.berkshirehathaway.com/letters/1989.html", use: "区分会计利润、经济现实和制度性约束。" },
  { id: "berkshire_1996_letter", title: "1996 Chairman's Letter", url: "https://www.berkshirehathaway.com/letters/1996.html", use: "以能力圈和可预测性限制估值确信度。" },
  { id: "berkshire_2005_letter", title: "2005 Chairman's Letter", url: "https://www.berkshirehathaway.com/letters/2005ltr.pdf", use: "检验管理层资本配置和每股结果。" },
  { id: "berkshire_2007_letter", title: "2007 Chairman's Letter", url: "https://www.berkshirehathaway.com/letters/2007ltr.pdf", use: "把长期护城河机制与竞争位置变化分开。" },
  { id: "berkshire_2009_letter", title: "2009 Chairman's Letter", url: "https://www.berkshirehathaway.com/letters/2009ltr.pdf", use: "把流动性和生存能力置于收益追求之前。" },
  { id: "berkshire_2018_letter", title: "2018 Chairman's Letter", url: "https://www.berkshirehathaway.com/letters/2018ltr.pdf", use: "避免只看合并数字而忽略分部经济性。" },
  { id: "berkshire_2022_letter", title: "2022 Chairman's Letter", url: "https://www.berkshirehathaway.com/letters/2022ltr.pdf", use: "关注留存收益如何转化为长期每股价值。" },
];

const indicatorMap = {
  security_and_legal_subject: ["exact_security_issuer_share_class_and_rights", "dated_price_share_count_currency_and_listing_status"],
  control_and_beneficial_ownership: ["controller_voting_pledges_and_cross_holdings", "value_transfers_nci_and_related_party_exposure"],
  business_model: ["payer_value_proposition_revenue_and_cash_mechanism", "capital_needs_and_business_failure_variables"],
  revenue_structure: ["segment_product_and_geography_reconciliation", "volume_price_mix_acquisition_and_scope_bridge"],
  industry_chain_position: ["upstream_process_customer_payer_and_substitute_map", "profit_pool_and_inventory_credit_technology_risk"],
  product_and_unit_economics: ["price_volume_mix_and_incremental_economics", "industry_denominator_scope_and_comparability"],
  customers: ["customer_channel_end_user_and_payer_separation", "concentration_retention_receivables_inventory_and_external_evidence"],
  suppliers: ["critical_inputs_concentration_related_parties_and_substitution", "terms_prepayments_availability_and_cost_pass_through"],
  competition_structure: ["entry_exit_capacity_price_and_substitution", "competitor_customer_and_regulator_corroboration"],
  durable_moat: ["mechanism_economic_result_durability_and_direction", "strongest_falsifying_evidence"],
  revenue_quality: ["revenue_receivables_contract_assets_returns_and_cash", "acquisition_period_end_channel_and_recognition_distortion"],
  earnings_quality: ["reported_to_normalized_parent_earnings_bridge", "tax_attribution_scope_and_adjustment_disagreement"],
  cash_conversion: ["profit_operating_cash_and_distributable_cash_bridge", "factoring_payment_restricted_cash_and_sector_scope"],
  working_capital: ["receivables_inventory_payables_prepayments_and_contract_balances", "sustainable_financing_vs_temporary_cash_release"],
  capital_intensity: ["maintenance_vs_growth_investment_range", "capex_capacity_utilization_and_competitive_requirements"],
  returns_on_capital: ["multiperiod_roe_roic_and_incremental_returns", "leverage_buyback_cycle_and_accounting_decomposition"],
  balance_sheet_survival: ["debt_liquidity_covenants_guarantees_pledges_and_off_balance", "adverse_scenario_financing_need"],
  capital_allocation: ["reinvestment_ma_dividend_buyback_issuance_debt_and_cash_ledger", "diluted_per_share_outcomes_and_opportunity_cost"],
  management: ["dated_commitments_vs_outcomes", "incentives_compensation_succession_insider_actions_and_candor"],
  governance_and_related_parties: ["related_sales_purchases_loans_guarantees_and_asset_transfers", "pricing_minority_fairness_oversight_and_dissent"],
  accounting_and_audit: ["audit_kam_standard_policy_and_restatement", "statement_reproduction_and_conflict_preservation"],
  tax_and_legal: ["effective_deferred_and_uncertain_tax", "litigation_penalties_compliance_and_tail_exposure"],
  per_share_economics: ["basic_diluted_and_fully_diluted_share_reconciliation", "per_share_growth_distribution_issuance_and_repurchase_outcomes"],
  valuation: ["currency_consistent_value_range_assumptions_and_dates", "reverse_expectations_sensitivities_and_cross_check"],
  disconfirming_evidence: ["independent_strongest_counter_thesis", "observable_invalidation_next_evidence_and_review_date"],
};
const dimensionMeta = {
  security_and_legal_subject: ["applicable", ["F01", "F05", "F06", "P01"], "02691.HK与603093.SH为同一发行人的H/A普通股；研究价格HK$6.65，使用转增后预期股本。"],
  control_and_beneficial_ownership: ["applicable", ["F01", "F02", "G02"], "横店控股持股59.23%，最终控制人为东阳市横店社团经济企业联合会；Q1披露无质押。"],
  business_model: ["applicable", ["F01"], "收入来自期货经纪手续费、客户保证金利差、资管/基金管理、风险管理和境外金融服务；生存变量是监管资本、客户资产安全、交易活跃度和利率。"],
  revenue_structure: ["applicable", ["F01", "F02"], "2025净手续费43.64%、净利息41.25%、投资收益10.67%；境外金融服务贡献91.9%集团税前利润。"],
  industry_chain_position: ["applicable", ["F01", "F12", "F13", "U01", "U02"], "位于交易所/清算基础设施与企业、机构及个人客户之间；美国映射仅作主题对照。"],
  product_and_unit_economics: ["applicable", ["F01", "F12", "F13"], "经纪经济性由客户权益、成交量和费率共同决定；利息经济性由客户资金规模与利率共同决定。"],
  customers: ["unknown", [], "披露了客户权益总量，但未披露客户集中度、留存率、分层费率和净新增客户。"],
  suppliers: ["unknown", [], "交易所、清算银行、行情/技术系统是关键输入，但未见完整集中度和替代成本量化。"],
  competition_structure: ["unknown", [], "行业成交总量可核验，但公司份额、净费率和同口径跨境竞争数据不完整。"],
  durable_moat: ["unknown", [], "跨境牌照、清算席位和客户资产规模可能构成网络/合规优势，但缺少份额、留存、费率韧性的反事实验证。"],
  revenue_quality: ["applicable", ["F01", "F02"], "手续费和利息合计占2025经营收入约84.9%，但投资与公允价值波动会改变单季表现。"],
  earnings_quality: ["applicable", ["F01", "F02", "F03", "G04"], "Q1利润既有手续费/利息改善，也有投资收益和减值转回；会计估计变化的季度影响未单列。"],
  cash_conversion: ["unknown", [], "客户保证金流动使合并经营现金流无法代表可分配现金；缺少母公司法人口径上游现金与资本留存桥。"],
  working_capital: ["not_applicable", [], "工业企业营运资本框架不适用于客户资金隔离的期货金融机构，应改看客户资产匹配、流动性和监管资本。"],
  capital_intensity: ["applicable", ["F01", "F02"], "主要资本要求是监管净资本、清算结算资金、风险管理和境外业务资本，而非工业维护性资本开支。"],
  returns_on_capital: ["applicable", ["F01"], "ROE由2022年7.75%升至2024年11.71%，2025年11.30%；ROIC不适合直接跨金融与工业公司比较。"],
  balance_sheet_survival: ["applicable", ["F01", "F02", "F11"], "客户资金与公司资金隔离；Q1净资本/风险资本降至137%，仍高于100%最低值但缓冲显著收窄。"],
  capital_allocation: ["applicable", ["F04", "F05", "F06", "G03"], "同时存在转增、H股回购授权、拟A股可转债和条件性股利计划，必须用完全摊薄每股结果复核。"],
  management: ["unknown", [], "年报与业绩预告有经营归因，但未找到截至研究日可独立核验的近期CFO公开讲话与承诺兑现时间表。"],
  governance_and_related_parties: ["applicable", ["F01", "F11", "G01", "G02"], "关联采购上限上调绝对金额较小；内控警示、审计师变更和整改需要持续追踪。"],
  accounting_and_audit: ["applicable", ["F01", "G01", "G04"], "2025为标准无保留意见；2026信用减值估计前瞻变更且拟更换审计师。"],
  tax_and_legal: ["applicable", ["F01", "F11"], "税项随地域和业务变化；已识别监管警示但未把它误写成行政处罚或停牌。"],
  per_share_economics: ["applicable", ["F05", "F06", "F07"], "转增后预期1,038.145m股为基准；员工库存股和拟可转债转股分别列为摊薄情景。"],
  valuation: ["applicable", ["F01", "F02", "F03", "P01", "P02"], "研究日约12.3倍FY PE、9.9倍TTM PE、15.0倍简单周期正常化PE、1.07倍PB；估值只保留区间。"],
  disconfirming_evidence: ["applicable", ["F02", "F11", "G04", "P01"], "最强反证是监管资本压缩、利润集中、会计顺风与小盘流动性；下一证据是正式中报和资本恢复。"],
};
const dimensions = Object.entries(indicatorMap).map(([dimension, ids]) => {
  const [status, refs, summary] = dimensionMeta[dimension];
  const gaps = status === "unknown" ? [`${dimension}所需的分层主源数据未披露。`] : [];
  const notApplicable = status === "not_applicable";
  return {
    dimension,
    status,
    summary,
    source_refs: refs,
    positive_evidence: status === "applicable" ? [summary] : [],
    counter_evidence: status === "applicable" ? ["结论只在已披露范围内成立，未披露项不得外推。"] : [],
    source_gaps: gaps,
    ...(notApplicable ? { not_applicable_reason: summary } : {}),
    indicators: ids.map((id) => ({
      id,
      status: status === "unknown" ? "not_disclosed" : notApplicable ? "not_applicable" : "observed",
      summary,
      source_refs: status === "applicable" ? refs : [],
      source_gaps: gaps,
      ...(notApplicable ? { reason: summary } : {}),
    })),
  };
});

const peMatrix = [
  {
    label: "reported_fy", status: "calculated", currency: "HKD", price,
    price_as_of: researchDate, eps: round(486.264 / postCapShares / fx, 6),
    eps_period: "FY2025", eps_type: "reported parent profit on expected post-cap shares, converted to HKD",
    pe: round(price / (486.264 / postCapShares / fx), 6),
    formula: "HK$6.65 / ((RMB486.264m / 1,038.14454m shares) / 0.86601 CNY/HKD)",
    confidence: "medium; audited numerator, expected post-cap denominator",
  },
  {
    label: "reported_ttm", status: "calculated", currency: "HKD", price,
    price_as_of: researchDate, eps: round(605.289 / postCapShares / fx, 6),
    eps_period: "TTM through 2026Q1", eps_type: "FY2025 + 2026Q1 - 2025Q1, post-cap shares, HKD",
    pe: round(price / (605.289 / postCapShares / fx), 6),
    formula: "HK$6.65 / (((RMB486.264m + RMB204.763m - RMB85.738m) / 1,038.14454m shares) / 0.86601)",
    confidence: "medium; includes unaudited Q1 and volatile investment/impairment items",
  },
  {
    label: "normalized_cycle_average", status: "calculated", currency: "HKD", price,
    price_as_of: researchDate, eps: round(398.038 / postCapShares / fx, 6),
    eps_period: "FY2022-FY2025 average", eps_type: "simple reported parent-profit average, post-cap shares, HKD",
    pe: round(price / (398.038 / postCapShares / fx), 6),
    formula: "HK$6.65 / ((average FY2022-FY2025 parent profit / 1,038.14454m shares) / 0.86601)",
    confidence: "low-to-medium; simple cycle cross-check, not a forecast",
  },
];
const forward = [
  ["bear", 650], ["base", 740], ["upside", 820],
].map(([scenario, profit]) => {
  const eps = profit / postCapShares / fx;
  return {
    scenario, status: "calculated_pe", forecast_parent_profit_rmb_m: profit,
    forecast_eps: round(eps, 6), implied_pe_at_current_price: round(price / eps, 6),
    assumptions: "research sensitivity; no consensus claim; post-cap shares and 2026-07-27 FX",
  };
});
const intrinsic = [
  { scenario: "downside", sustainable_roe_pct: 8, terminal_growth_pct: 2, discount_rate_pct: 11, fair_pb: 0.6667, intrinsic_value_per_share: 4.1495 },
  { scenario: "base", sustainable_roe_pct: 10, terminal_growth_pct: 4, discount_rate_pct: 11, fair_pb: 0.8571, intrinsic_value_per_share: 5.3351 },
  { scenario: "upside", sustainable_roe_pct: 12, terminal_growth_pct: 6, discount_rate_pct: 11, fair_pb: 1.2, intrinsic_value_per_share: 7.4691 },
].map((row) => ({
  ...row, status: "calculated",
  formula: "fair P/B=(sustainable ROE-g)/(cost of equity-g); HKD/share=fair P/B×FY2025 RMB BVPS/0.86601",
  limitations: "金融机构P/B-ROE敏感性，不是现金流折现，也不是公司指引。",
}));

const combined = {
  schema_version: "seed.stock-fundamentals-valuation.v2",
  artifact_type: "stock_fundamentals_valuation",
  artifact_role: "public_company_research_upgrade",
  status: "needs_human_review",
  generated_at: generatedAt,
  security: {
    security_id: "XHKG:02691", company_name: "Nanhua Futures Co., Ltd.", company_name_zh: "南华期货股份有限公司",
    ticker: "02691", exchange: "HKEX", listing_type: "H ordinary share of A/H same issuer",
    currency: "HKD", fiscal_year_end: "12-31", reporting_standard: "HKFRS",
    same_company_listing: { security_id: "XSHG:603093", relationship: "same_company_listing" },
  },
  as_of: { research_date: researchDate, price, price_date: researchDate, price_source_ref: "P01", fx_cny_per_hkd: fx },
  methodology_refs: methodologyRefs,
  source_refs: sources,
  source_boundaries: {
    primary: "HKEX filings, SSE/SZSE Stock Connect lists and rules, CSRC, CFA and SEC filings.",
    secondary: "Tencent frozen daily-price response only for market prices and event windows.",
    management_claims: "Company explanations and competitive-advantage language remain labeled as management claims.",
    unknowns: "No formal 2026 interim report date, actual H-share repurchase trade, final convertible terms, complete customer retention/fee-rate data, or statutory distributable-cash bridge found by the cutoff.",
  },
  ownership_structure: {
    controller: "Hengdian Holdings, 59.23%",
    ultimate_controller: "Dongyang Hengdian Social Organization and Economic Enterprise Association",
    q1_pledge_status: "no pledge disclosed for the controller holding",
    ah_identity: "603093.SH and 02691.HK are ordinary shares of the same legal issuer.",
    source_refs: ["F01", "F02"],
  },
  financial_history: { currency: "RMB", unit: "million unless stated", periods: annual, source_refs: ["F01"] },
  segment_data: {
    currency: "RMB", unit: "million", periods: ["FY2024", "FY2025"], rows: segments,
    key_observation: "FY2025 overseas financial services PBT RMB501.010m was about 91.9% of group PBT RMB545.309m.",
    source_refs: ["F01"],
  },
  research_dimensions: dimensions,
  earnings_quality_bridge: {
    period: "2026Q1 vs 2025Q1", currency: "RMB", unit: "million", rows: q1Bridge,
    conclusion: "Growth combined core fee/interest gains with investment gains and a favorable impairment swing; fair-value and FX movements offset part of it.",
    source_refs: ["F02", "G04"],
  },
  owner_earnings: {
    status: "unavailable", currency: "HKD", range: [],
    reason: "For a futures financial institution, consolidated operating cash flow is dominated by segregated client-margin movements. Statutory parent and regulated-subsidiary distributable cash after required capital retention was not disclosed in a complete bridge.",
    limitations: [
      "Do not use consolidated CFO minus capex as owner earnings.",
      "The separate regulatory-retention table is only a sensitivity and is not company guidance or owner earnings.",
      "Upstreamability across regulated PRC and overseas subsidiaries is not fully disclosed.",
    ],
    source_refs: ["F01", "F02", "G03"],
  },
  financial_institution_distributable_earnings_sensitivity: {
    status: "research_sensitivity_not_owner_earnings", currency: "RMB", unit: "million",
    rows: ownerSensitivity, source_refs: ["F01", "G03"],
  },
  capital_allocation: {
    post_capitalisation_expected_shares_m: postCapShares,
    h_share_repurchase: "HK$130m funding cap and up to 10% H shares; approved, no execution evidence found by cutoff.",
    dividend_policy: "2026-2028 conditional cash dividend floor of 10% of distributable profit, subject to profit and regulatory capital.",
    convertible_bond: "Proposed A-share convertible bond up to RMB1.2bn; not issued and final conversion terms unknown.",
    fully_diluted_scenarios: shareBridge,
    source_refs: ["F04", "F05", "F06", "F07", "G03"],
  },
  balance_sheet_quality: {
    financial_institution_branch: true,
    client_fund_segregation: "Amounts payable to clients and corresponding client assets are not ordinary corporate leverage.",
    regulatory_capital: riskCapital,
    key_risk: "Net capital/risk capital compressed from 240% at FY2025 to 137% at 2026Q1, versus 100% minimum.",
    source_refs: ["F01", "F02"],
  },
  pe_matrix: peMatrix,
  forward_scenarios: {
    currency: "HKD", price_anchor: price, price_date: researchDate, scenarios: forward,
    limitations: "Research sensitivities, not consensus estimates or company guidance.",
  },
  intrinsic_value_scenarios: {
    currency: "HKD", method: "financial institution P/B-ROE sensitivity", book_value_basis: "FY2025 parent equity on expected post-cap shares",
    scenarios: intrinsic, limitations: "Range-only cross-check; results are highly sensitive to sustainable ROE and regulatory-capital retention.",
  },
  moat_evidence: {
    positive_evidence: [
      "Cross-border operating footprint, exchange memberships and clearing seats create a regulated-service network.",
      "Overseas client equity and FY2025 overseas PBT show meaningful scale outside Mainland China.",
    ],
    counter_evidence: [
      "Overseas PBT concentration is also a jurisdiction, rate and operating-risk concentration.",
      "No complete customer retention, pricing premium or market-share trend proves durable pricing power.",
    ],
    missing_tests: [
      "Same-scope multi-year brokerage market share and net fee rate.",
      "Client cohort retention and assets-per-client.",
      "Return on incremental regulatory capital by segment.",
    ],
  },
  red_team: [
    "Q1 headline growth may overstate repeatable economics because investment gains and impairment reversal were material.",
    "Regulatory-capital compression may constrain business expansion, dividends or repurchases.",
    "Short H-share history and low trading volume increase event and flow sensitivity.",
  ],
  gates: [
    { gate: "identity_and_source_integrity", result: "pass_with_scope", reason: "A/H legal identity, share class, current Southbound status and primary filings were checked; dynamic market data remains secondary." },
    { gate: "circle_of_competence", result: "inconclusive", reason: "Core income mechanisms are mapped, but customer/supplier/competition disclosures remain incomplete." },
    { gate: "business_economics", result: "inconclusive", reason: "Fee and interest economics are visible, but unit pricing, retention and market share are incomplete." },
    { gate: "durable_moat", result: "provisional", reason: "Licenses and cross-border network are moat candidates, not proven durable pricing power." },
    { gate: "management_and_capital_allocation", result: "mixed", reason: "Capital actions are transparent, while net-capital compression and absent CFO commitment ledger reduce confidence." },
    { gate: "owner_earnings", result: "range_only", reason: "Consolidated CFO is invalid for this branch; only regulatory-retention sensitivities are shown." },
    { gate: "survival_and_balance_sheet", result: "provisional", reason: "Ratios remain above minimums, but Q1 capital-buffer compression and control remediation require monitoring." },
    { gate: "intrinsic_value_and_margin_of_safety", result: "range_only", reason: "FY, TTM, normalized PE and P/B-ROE ranges disagree materially; no single-point conclusion is justified." },
    { gate: "decision_and_disconfirming_evidence", result: "inconclusive", reason: "Formal interim statements, capital recovery, recurring-earnings bridge and dilution terms remain unresolved." },
  ],
  source_gaps: [
    "Formal FY2026 interim results and exact publication date were not found by 2026-07-27.",
    "No actual H-share repurchase trade disclosure was found after authorization.",
    "Final A-share convertible bond approval, issue and conversion terms are unknown.",
    "Customer concentration, retention, pricing and same-scope market-share history are incomplete.",
    "No independent recent CFO speech or dated commitment ledger was found.",
    "Statutory distributable cash after regulatory-capital retention is not disclosed as a complete bridge.",
    "Current major index membership beyond Stock Connect was not independently confirmed.",
  ],
  invalidation_tests: [
    "If formal H1 profit falls outside RMB375m-RMB405m or contains a larger one-off component than indicated, reassess normalization.",
    "If net capital/risk capital approaches the regulatory minimum or needs external capital merely to sustain current business, survival and capital-allocation gates weaken.",
    "If overseas PBT falls without offsetting domestic fee economics, the cross-border advantage thesis weakens.",
    "If customer assets rise but fee and net-interest monetization both deteriorate, unit economics weaken.",
    "If Stock Connect current lists cease to include 02691, revise liquidity and flow assumptions without treating removal itself as a fundamental verdict.",
  ],
  historical_valuation: {
    status: "limited_by_short_h_share_history",
    listing_date: "2025-12-22", current_price_hkd: price,
    fy_pe_x: valuation[0].pe_x, ttm_pe_x: valuation[1].pe_x, normalized_pe_x: valuation[2].pe_x, pb_x: valuation[0].pb_x,
    limitation: "Less than one year of H-share trading is insufficient for a robust historical percentile.",
    source_refs: ["F01", "F02", "P01", "P02"],
  },
  price_move_attribution: {
    status: "descriptive_not_causal", event_windows: eventWindows,
    conclusion: "Inclusion, strong Q1 growth and repurchase authorization did not produce a uniform five-day direction. Small-cap liquidity, capital structure and concurrent information matter.",
    capitalisation_adjustment: "2026-06-17 theoretical adjusted reference=(HK$9.23-HK$0.07934)/1.45=HK$6.3108; close HK$6.42 (+1.73%); T+5 close HK$6.17.",
    source_refs: ["F03", "F04", "F05", "F09", "F11", "P01"],
  },
  review: {
    human_review_required: true, reviewed_for_publication: false, human_reviewer: null,
    machine_validation: "run after generation; see validator-results.json",
    status_reason: "Public package is production-shaped but not human-approved.",
  },
  disclaimer: "Research artifact for evidence review only; this is not investment advice. Unknowns and scenario values are not forecasts or assurances.",
};

writeJson("combined-artifact.v2.json", combined);
const combinedText = fs.readFileSync(path.join(root, "combined-artifact.v2.json"));
const combinedSha = sha(combinedText);

const evidenceSeed = [
  ["NH-CRIT-001", "ah_same_issuer", "F01", 8, "The annual report defines A shares and H shares as ordinary share capital of the Company, each with RMB1 nominal value, listed as 603093.SH and 2691.HK.", "FY2025", "shares", "RMB", "legal issuer and share classes", "audited", null],
  ["NH-CRIT-002", "fy2025_profit", "F01", 29, "FY2025 profit attributable to equity shareholders of the parent was RMB486.264 million.", "FY2025", "million", "RMB", "consolidated parent attribution", "audited", null],
  ["NH-CRIT-003", "fy2025_income_mix", "F01", 48, "Net fee and commission income was RMB605.560 million and net interest income was RMB572.343 million.", "FY2025", "million", "RMB", "consolidated operating income", "audited", null],
  ["NH-CRIT-004", "overseas_pbt_concentration", "F01", 200, "Overseas financial services segment profit before tax was RMB501.010 million.", "FY2025", "million", "RMB", "reportable segment", "audited", "501.010 / 545.309 = 91.9% of group PBT"],
  ["NH-CRIT-005", "client_equity", "F01", 4, "Domestic client equity was RMB38.982 billion and overseas client net equity was HKD23.306 billion.", "FY2025", "billion", "mixed", "client assets by geography", "audited", null],
  ["NH-CRIT-006", "fy2025_regulatory_capital", "F01", 30, "Net capital was RMB2,744.257 million and net capital/risk capital was 240%.", "FY2025", "million and percent", "RMB", "parent regulatory capital", "audited", null],
  ["NH-CRIT-007", "q1_profit_growth", "F02", 2, "2026Q1 operating revenue was RMB433.131 million and parent profit was RMB204.763 million.", "2026Q1", "million", "RMB", "consolidated", "unaudited", null],
  ["NH-CRIT-008", "q1_earnings_sources", "F02", 11, "Q1 net fee income, net interest income and investment gains were RMB187.355m, RMB193.121m and RMB107.406m; fair-value change was negative RMB44.740m.", "2026Q1", "million", "RMB", "consolidated income statement", "unaudited", null],
  ["NH-CRIT-009", "q1_cfo_client_funds", "F02", 14, "Operating cash flow was RMB5,317.832 million and was affected by client-equity movements.", "2026Q1", "million", "RMB", "consolidated cash flow", "unaudited", "Not treated as owner earnings"],
  ["NH-CRIT-010", "q1_capital_buffer", "F02", 3, "Net capital/risk capital was 137% at 2026Q1 versus 240% at FY2025.", "2026Q1", "percent", "RMB", "parent regulatory capital", "unaudited", "137%-100%=37 percentage-point buffer over minimum"],
  ["NH-CRIT-011", "h1_profit_range", "F03", 1, "2026H1 parent profit was preliminarily estimated at RMB375 million to RMB405 million.", "2026H1", "million", "RMB", "parent attribution", "unaudited", null],
  ["NH-CRIT-012", "implied_q2_profit", "F03", 1, "The H1 profit range and disclosed Q1 result imply 2026Q2 parent profit of RMB170.237m to RMB200.237m.", "2026Q2", "million", "RMB", "research derivation", "unaudited", "H1 range 375-405 minus Q1 204.763"],
  ["NH-CRIT-013", "post_cap_shares", "F06", 10, "Expected post-capitalisation issued shares are 1,038.144540 million, comprising A and H shares.", "2026 capitalisation", "million shares", "not_applicable", "expected issued share capital", "not_applicable", "717.724893m issued + (717.724893m - 5.681234m treasury) × 4.5/10 = 1,038.144540m after rounding"],
  ["NH-CRIT-014", "convertible_dilution", "F06", 68, "The proposed A-share convertible bond is up to RMB1.2 billion; illustrative conversion assumes RMB15.81 per A share and is not a final term.", "2026 proposal", "RMB million and shares", "RMB", "proposed financing", "not_applicable", "RMB1,200m / RMB15.81 = 75.901328m illustrative conversion shares"],
  ["NH-CRIT-015", "accounting_estimate", "G04", 2, "The expected-credit-loss estimate change applies prospectively from 2026-01-01 and was expected to increase FY2026 PBT by no more than RMB40 million.", "FY2026", "million", "RMB", "accounting estimate", "not_applicable", null],
  ["NH-CRIT-016", "auditor_change", "G01", 1, "The company proposed changing its domestic and international auditors to EY firms and stated there was no disagreement.", "FY2026", "not_applicable", "not_applicable", "audit governance", "not_applicable", null],
  ["NH-CRIT-017", "connected_procurement", "G02", 2, "The annual connected-procurement cap for 2026 and 2027 was revised from RMB1 million to RMB7 million.", "2026-2027", "million", "RMB", "controller-group procurement", "not_applicable", "7 / 1 = 7x cap increase"],
  ["NH-CRIT-018", "dividend_policy", "G03", 2, "The 2026-2028 plan conditions cash dividends on profit and regulatory capital, with at least 10% of distributable profit when conditions are met.", "2026-2028", "percent", "RMB", "parent distributable profit", "not_applicable", null],
  ["NH-CRIT-019", "regulatory_warning", "F11", null, "The Zhejiang CSRC warning identified ineffective procurement/internal controls and deficiencies in employee-conduct management and required written remediation.", "2026-04-01", "not_applicable", "not_applicable", "PRC regulated operations", "not_applicable", null],
  ["NH-CRIT-020", "stock_connect_current", "S01", null, "02691 was present in the frozen Shanghai Southbound eligible list on the research date.", "2026-07-27", "eligibility status", "not_applicable", "Shanghai Southbound", "not_applicable", "Cross-checked with S02 Shenzhen list"],
  ["NH-CRIT-021", "current_price", "P01", null, "HK02691 closed at HK$6.65 on 2026-07-27 with volume 372,500 shares.", "2026-07-27", "HKD per share and shares", "HKD", "secondary-market H share", "not_applicable", null],
  ["NH-CRIT-022", "industry_cycle", "F13", null, "PRC futures-market H1 2026 volume rose 25.23% and turnover rose 42.08% year on year.", "2026H1", "percent", "RMB", "PRC futures industry", "not_applicable", null],
];
const sourceById = Object.fromEntries(sources.map((source) => [source.id, source]));
const evidence = {
  schema_version: "seed.company-research-evidence-index.v1",
  generated_at: generatedAt,
  combined_artifact: { path: "combined-artifact.v2.json", sha256: combinedSha },
  anchors: evidenceSeed.map(([id, claim_id, source_id, page, source_text, period, unit, currency, scope, audit_status, formula]) => ({
    id, claim_id, source_id, document_sha256: sourceById[source_id].content_sha256, page,
    source_text, period, unit, currency, scope, audit_status, formula, critical: true,
    limitations: "See source-ledger boundary and report context.",
  })),
};
writeJson("evidence-index.json", evidence);

const locatorSpec = [
  ["NH-CRIT-001","Definitions — A Share(s) / H Share(s)",32,39,"b6c9aaa025c685a72e517c432c36bf22c9bb7cf0392565c561e695883b459dd6","f7ef65fcc37d4d4d04db194c7f313dada45fb3f2b1f199b5b5ec523c322e7938"],
  ["NH-CRIT-002","Financial Summary — Principal Accounting Indicators",12,16,"5cc3a8dc7fe29db545211b7d8612924d1f178fee93c43f904e35f137c5a1d8e8","a2a19427f9d8ccf029b71fb3fe8a22754e0474020b251cd7cb27c6ffccba6105"],
  ["NH-CRIT-004","Note 6 — Operating Segment Information",19,23,"d81018461f0a000a768c5e9b7c131cf2de50864f25dba7135ae999ad9a77d707","c8b24f9252e495ca89303831186e6f831944ac868858d2553e89262ff8cc83d7"],
  ["NH-CRIT-005","Chairman’s Statement — client equity",9,12,"9c1ceb9a2dde222caad3191ce29f05893eaa5d871ba4c0922fcd45b9ff4f74a1","69617c2f9dfa8d5e8bb3ee597a78340d8d24d607f0ef41f8ecb1350a52eeeadd"],
  ["NH-CRIT-006","Financial Summary — Net Capital and Risk Indicators",16,24,"7a9291ea3ad94631b0cf271295e2d9d4867f31b74cbeae6217e4df05bec6550d","94a44a764669bde3af44ad6156bd6cfacb14d19ff4fdeef00ff5696ae8a6602d"],
  ["NH-CRIT-007","2026Q1 — Key Financial Information",28,35,"b2719e3e8428d8b2240bd8955ddcb88ecb3661df53f7363c672712c22fa6c1ca","5d0f72d0fe48c7d1016261f900ac864d7a5c59b0309a7a19054e2c7233b7cfa6"],
  ["NH-CRIT-008","2026Q1 — Consolidated Income Statement",11,36,"c825d17a6bc2a967bacce33ec457d41e04991a7d5bf2359f344ba1f7e719edbf","aed4835b76d9c71e4d741950c026295ceb3d52096124f0e652c5ece0e9a12e63"],
  ["NH-CRIT-009","2026Q1 — Consolidated Cash Flow Statement",11,35,"95813a71853e3d708208c64b92182c41f83ff21aa961dd53b428759b41d1e0af","d159aa7387a4af8d22130ae868701a04f25ad5b367ccf5abe382074a7a8ec997"],
  ["NH-CRIT-010","2026Q1 — Net Capital and Risk Control Indicators",2,15,"2a2130b5c9c097d5b27f7568937b2283ba90774f973fd768af252a0dee276c1a","cd4ee151bba51356b070f0110c2c3208c4618ff03e72554e7f67aeb1cdd07d7f"],
  ["NH-CRIT-011","2026H1 Profit Alert — estimated range",23,30,"6564d46b74f0973cc5b0f3fd423dd6bbd1ea302517bc0042f28625526cc4c525","11f07d7462cfc3a81c91655e2846b08809ccf5716d204ebed8ac5024fb751d67"],
  ["NH-CRIT-012","2026H1 Profit Alert — inputs for implied Q2",23,30,"6564d46b74f0973cc5b0f3fd423dd6bbd1ea302517bc0042f28625526cc4c525","11f07d7462cfc3a81c91655e2846b08809ccf5716d204ebed8ac5024fb751d67"],
  ["NH-CRIT-013","AGM Circular — Capitalisation Issue",16,24,"f5c6fb0778ff282c9d3b141de433f166ce558c4d1b8929476d1979e1198f95b5","f354a3378d3a5f510990fb34f3267b928db6af3c2977d1eb72efea6b0402e60a"],
  ["NH-CRIT-014","AGM Circular — Convertible Bond Calculation Assumptions",1,13,"d0ba5dfc31db374015ece56be74596d63960984ce6bf197627e066d005c0740a","18a15e7f0bc7c33cc8ca64804a5afdccd938738f1a0ae69ebb34a5fb2eecf1ac"],
  ["NH-CRIT-015","Accounting Estimate Change — date and expected effect",20,34,"2061dcaac36d8edb640325836a186bb6952115ef7fea5158508c7fe6b4226e64","a9621655d58a90ac52b4f1bcb41d32d34058330aa1223d3bf5f59b9edcc4eaea"],
  ["NH-CRIT-016","Proposed Change of Auditors — appointment and no disagreement",23,33,"edb620b5d9a1555d1915bb68aa6d145ccce9770273ec6eeb6726bc6d8d74c16b","d2867536b7df98dfd96c3f827725104f4865a14dbf9f79f194f5c0152d80116e"],
  ["NH-CRIT-017","Connected Procurement — Revised Annual Cap",20,37,"6c3035dcb247017a6bc036bb3332601a19bb2852fb49b43a5f750b35ae9bb8a5","1b20cb50fd4a9facb6537df9b5f1e3fcf05c08cd3a70e0f370625e49caad3da5"],
  ["NH-CRIT-018","Dividend Return Plan — 2026-2028 cash conditions",19,30,"84e46c4a5350b0e2fbc01ccc292781a0cdb6d1236c61e2c32a10cd86653c0b79","891e3ae6bbaf6968ea63fc14b67dac706d492eded10fb93df35985de1b335152"],
];
const locatorById = Object.fromEntries(locatorSpec.map((row) => [row[0], row]));
const locatorAnchors = locatorSpec.map(([id, section_or_table, page_line_start, page_line_end, text_snapshot_sha256, page_text_sha256]) => {
  const anchor = evidence.anchors.find((row) => row.id === id);
  return {
    ...anchor,
    text_locator: { section_or_table, page_line_start, page_line_end, text_snapshot_sha256, page_text_sha256 },
    limitations: "Line numbers and hashes were generated from pypdf text extraction of the checksum-matched PDF; extraction order may differ from visual reading order.",
  };
});
writeJson("data/critical-evidence-anchors.json", {
  schema_version: "seed.company-research-critical-evidence-locators.v1",
  generated_at: generatedAt,
  extraction_method: "pypdf text extraction; stripped non-empty lines; page numbering is physical PDF page number",
  anchors: locatorAnchors,
});
const locatorHeaders = [
  "id","claim_id","source_id","document_sha256","page","section_or_table","page_line_start","page_line_end",
  "text_snapshot_sha256","page_text_sha256","period","unit","currency","scope","audit_status","source_text","formula","limitations",
];
writeCsv("critical-evidence-locators.csv", locatorHeaders, locatorAnchors.map((anchor) => ({
  id: anchor.id, claim_id: anchor.claim_id, source_id: anchor.source_id, document_sha256: anchor.document_sha256,
  page: anchor.page, section_or_table: anchor.text_locator.section_or_table,
  page_line_start: anchor.text_locator.page_line_start, page_line_end: anchor.text_locator.page_line_end,
  text_snapshot_sha256: anchor.text_locator.text_snapshot_sha256, page_text_sha256: anchor.text_locator.page_text_sha256,
  period: anchor.period, unit: anchor.unit, currency: anchor.currency, scope: anchor.scope,
  audit_status: anchor.audit_status, source_text: anchor.source_text, formula: anchor.formula, limitations: anchor.limitations,
})));

writeJson("source-ledger.json", {
  schema_version: "seed.company-research-source-ledger.v1",
  company: {
    name_zh: "南华期货股份有限公司", name_en: "Nanhua Futures Co., Ltd.", primary_ticker: "02691.HK",
    same_company_listings: [{ ticker: "603093.SH", relationship: "same_company_listing", note: "同一发行人A股。" }],
  },
  research_snapshot_at: generatedAt,
  market_data_cutoff: generatedAt,
  status: "needs_human_review",
  not_investment_advice: true,
  source_policy: {
    tier_A: "交易所、监管机构、公司公告、经审计报告和SEC主源。",
    tier_B: "仅将冻结的二级行情响应用于价格、成交量和事件窗口。",
    derived: "Q2、TTM、摊薄和估值均保留公式。",
    unknown: "未找到或未披露的数据保持unknown，不用近似叙述替代。",
  },
  sources: sources.map((source) => ({
    ...source,
    kind: source.source_type,
    publisher: source.url.includes("hkexnews") ? "HKEX / Nanhua Futures" :
      source.id.startsWith("S") || source.id === "F09" || source.id === "F10" ? "SSE/SZSE" :
      source.id === "P01" ? "Tencent market data" :
      source.id === "P02" ? "SAFE" :
      source.id.startsWith("U") ? "SEC / issuer" :
      source.id === "F11" ? "CSRC Zhejiang" :
      source.id === "F12" || source.id === "F13" ? "China Futures Association" : "Nanhua Futures / HKEX",
    retrieved_at: source.accessed_at,
    snapshot_sha256: source.content_sha256,
    used_for: source.covers,
    limitations: source.tier === "B" ? "Secondary market data; frozen response can change." : "Primary-source facts remain subject to stated scope and audit status.",
  })),
});

const redTeam = {
  schema_version: "seed.company-research-red-team.v1",
  artifact_type: "counter_thesis_review",
  security_id: "XHKG:02691",
  company_name: "Nanhua Futures Co., Ltd.",
  reviewer_or_agent: "Codex counter-thesis pass (machine, non-human)",
  reviewed_at: generatedAt,
  independence: "Separate counter-thesis pass; not a human approval.",
  counter_thesis: "Apparent growth may be a favorable trading-volume, investment-gain, impairment and client-fund cycle rather than a durable fee-rate moat. Capital compression, overseas concentration and small-cap liquidity can dominate near-term outcomes.",
  strongest_disconfirming_evidence: [
    "Q1 investment gains rose by RMB93.949m while fair value and FX moved adversely.",
    "A favorable credit-impairment swing contributed about RMB30.399m.",
    "Net capital/risk capital fell from 240% to 137%.",
    "FY2025 overseas PBT represented about 91.9% of group PBT.",
    "Stock Connect inclusion and strong Q1 growth did not produce uniform positive five-day windows.",
  ],
  failure_modes: [
    "Regulatory capital approaches minimums or capital raising is needed to maintain the current business.",
    "Overseas profitability reverses because of rates, regulation, customer assets or trading activity.",
    "Net fee rates fall despite higher industry volume.",
    "Accounting-estimate effects or investment gains dominate reported earnings.",
    "Proposed convertible financing causes greater per-share dilution than operating gains offset.",
  ],
  unresolved_issues: [
    "Formal H1 statements and regulatory-capital table.",
    "Customer concentration, retention, net fee rate and market share.",
    "Actual H-share repurchase execution.",
    "Final convertible bond terms.",
    "Statutory distributable-cash bridge.",
  ],
  invalidation_conditions: combined.invalidation_tests,
  next_review: "At formal 2026 interim results or earlier upon material regulatory-capital, auditor, repurchase, convertible or Stock Connect disclosure.",
  review_status: "needs_human_review",
  source_refs: ["F01", "F02", "F03", "F06", "F11", "G04", "P01"],
  disclaimer: "Machine counter-thesis for research review only; not investment advice.",
};
writeJson("red-team.json", redTeam);

const fmt = (v, digits = 1) => v === "" || v == null ? "—" : typeof v === "number" ? v.toLocaleString("zh-CN", { maximumFractionDigits: digits }) : v;
const table = (headers, rows, evidenceId = "") => `
  <div class="table-wrap"${evidenceId ? ` data-evidence-id="${evidenceId}"` : ""}><table>
    <thead><tr>${headers.map((h) => `<th>${h[1]}</th>`).join("")}</tr></thead>
    <tbody>${rows.map((row) => `<tr>${headers.map(([key]) => `<td>${fmt(row[key], 3)}</td>`).join("")}</tr>`).join("")}</tbody>
  </table></div>`;
const barChart = (title, labels, values, suffix = "", color = "#21c08b") => {
  const max = Math.max(...values.map((v) => Math.abs(v)), 1);
  return `<figure class="chart"><figcaption>${title}</figcaption><svg viewBox="0 0 720 ${80 + values.length * 45}" role="img" aria-label="${title}">
    ${values.map((v, i) => {
      const width = Math.abs(v) / max * 430;
      const y = 42 + i * 45;
      return `<text x="8" y="${y + 18}">${labels[i]}</text><rect x="190" y="${y}" width="${width}" height="25" rx="5" fill="${v < 0 ? "#e56b6f" : color}"/><text x="${200 + width}" y="${y + 18}">${fmt(v, 1)}${suffix}</text>`;
    }).join("")}
  </svg></figure>`;
};
const evidenceDrawers = evidence.anchors.map((e) => {
  const locator = locatorById[e.id];
  return `<details data-evidence-id="${e.id}"><summary>${e.id} · ${e.claim_id}</summary>
  <p>${e.source_text}</p><p class="meta">来源 ${e.source_id} · 页 ${e.page ?? "网页/动态表"}${locator ? ` · 抽取行 ${locator[2]}–${locator[3]} · 行快照SHA ${locator[4]} · 页文本SHA ${locator[5]}` : " · 网页/动态数据无稳定PDF页行，未伪造行号"} · 期间 ${e.period} · 单位 ${e.unit} · 币种 ${e.currency} · 范围 ${e.scope} · 审计 ${e.audit_status}${e.formula ? ` · 公式 ${e.formula}` : ""}</p>
</details>`;
}).join("");
const indicatorRows = dimensions.flatMap((dimension) => dimension.indicators.map((indicator, index) => ({
  dimension: dimension.dimension,
  dimension_status: dimension.status,
  indicator_no: index + 1,
  indicator: indicator.id,
  indicator_status: indicator.status,
  summary: indicator.summary,
  gap_or_reason: indicator.source_gaps.join("；") || indicator.reason || "—",
})));
const gateDisplay = combined.gates.map((gate) => {
  const extras = {
    identity_and_source_integrity: ["无硬阻断；二级行情仅限价格", "正式中报及最新股本/名单复核"],
    circle_of_competence: ["客户、供应商和竞争结构未完整披露", "客户分层、费率、份额、技术供应依赖"],
    business_economics: ["单客、净费率、留存率缺失", "正式中报手续费、客户权益与分部利润"],
    durable_moat: ["牌照/清算资格尚未证实持续定价权", "跨期份额、留存、费率韧性与增量资本回报"],
    management_and_capital_allocation: ["净资本压缩；CFO承诺账本缺失", "资本恢复、回购执行、可转债最终条款"],
    owner_earnings: ["法人口径可分配现金桥缺失", "监管资本留存、子公司上游现金和法定可分配利润"],
    survival_and_balance_sheet: ["137%资本比率接近需要高频监控的区间", "正式中报资本表和监管整改"],
    intrinsic_value_and_margin_of_safety: ["可持续ROE与资本需求不确定", "P/B-ROE反推、正常化利润和摊薄股本"],
    decision_and_disconfirming_evidence: ["多项unknown尚未关闭", "正式中报、资本恢复、重复性利润与流动性"],
  }[gate.gate];
  return { ...gate, blocking: extras[0], next_tests: extras[1] };
});

const html = `<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>南华期货 02691.HK｜基本面、估值与事件研究</title>
<style>
:root{--bg:#07111f;--card:#0e1d2f;--ink:#e9f3f8;--muted:#9db2c3;--line:#20384d;--green:#21c08b;--amber:#f4bf4f;--red:#e56b6f;--blue:#5ba7ff}
*{box-sizing:border-box}body{margin:0;background:linear-gradient(135deg,#06101d,#0a1727 55%,#0b2028);color:var(--ink);font:15px/1.62 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
a{color:#7bc1ff}main{max-width:1180px;margin:auto;padding:28px}.hero,.card{background:rgba(14,29,47,.94);border:1px solid var(--line);border-radius:18px;padding:24px;margin:18px 0;box-shadow:0 14px 38px #0004}
h1{font-size:34px;margin:.2em 0}h2{font-size:25px;margin:0 0 12px}h3{margin-top:22px}.sub,.meta{color:var(--muted)}.badge{display:inline-block;padding:5px 10px;border-radius:999px;background:#3d3012;color:#ffd77a;border:1px solid #745d25;margin-right:7px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px}.kpi{padding:15px;border-radius:13px;background:#0a1727;border:1px solid var(--line)}.kpi b{font-size:25px;display:block}
.nav{display:flex;gap:8px;flex-wrap:wrap}.nav a{padding:7px 11px;border:1px solid var(--line);border-radius:9px;text-decoration:none}.legend span{margin-right:15px}.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:5px}
.table-wrap{overflow:auto;border:1px solid var(--line);border-radius:12px;margin:13px 0}table{border-collapse:collapse;width:100%;min-width:720px}th,td{padding:9px 11px;border-bottom:1px solid var(--line);text-align:right}th:first-child,td:first-child{text-align:left}th{background:#10273b;position:sticky;top:0}.chart{background:#091725;border:1px solid var(--line);border-radius:13px;padding:12px;overflow:auto}.chart svg{min-width:650px;width:100%;height:auto}.chart text{fill:#dceaf2;font-size:13px}.callout{border-left:4px solid var(--amber);padding:10px 14px;background:#251f12;border-radius:8px}.risk{border-left-color:var(--red);background:#27161c}.ok{border-left-color:var(--green);background:#10261f}
details{border:1px solid var(--line);padding:9px 12px;border-radius:10px;margin:8px 0;background:#091725}summary{cursor:pointer;font-weight:700}.two{display:grid;grid-template-columns:1fr 1fr;gap:16px}@media(max-width:800px){.two{grid-template-columns:1fr}main{padding:14px}h1{font-size:27px}}
</style></head><body><main>
<header class="hero">
  <span class="badge">needs_human_review</span><span class="badge">研究日 2026-07-27</span>
  <h1>南华期货（02691.HK）</h1>
  <p class="sub">金融机构分支的长期底稿 + 小盘/港股通事件监控。A/H同一发行人已核验；美国公司仅作主题对照。</p>
  <div class="nav"><a href="#long-term">长期底稿</a><a href="#market-pricing">市场定价</a><a href="#event-monitor">近期监控</a><a href="#research-contract">25维度/50指标/9 Gate</a><a href="#evidence">证据抽屉</a></div>
  <div class="grid">
    <div class="kpi"><span>收盘价</span><b>HK$6.65</b><small>2026-07-27</small></div>
    <div class="kpi"><span>TTM PE</span><b>9.88×</b><small>含未经审计Q1</small></div>
    <div class="kpi"><span>正常化PE</span><b>15.02×</b><small>FY2022-25简单均值</small></div>
    <div class="kpi"><span>PB</span><b>1.07×</b><small>FY2025、转增后股本</small></div>
    <div class="kpi"><span>净资本/风险资本</span><b>137%</b><small>2026Q1；最低100%</small></div>
  </div>
  <p class="callout risk"><strong>结论先行：</strong>经营动量存在，但Q1不只是经纪增长；投资收益、减值转回和会计估计都影响利润质量。最大的中期验证点是正式中报中的监管资本恢复与利润重复性。估值只能保留区间，不能由单一TTM PE下结论。</p>
</header>

<section class="card legend"><h2>状态 / 程度图例与精确词汇</h2>
<p><span><i class="dot" style="background:var(--green)"></i>已观察 / 通过范围</span><span><i class="dot" style="background:var(--amber)"></i>临时 / 区间 / mixed</span><span><i class="dot" style="background:var(--red)"></i>阻断 / 反证</span><span><i class="dot" style="background:var(--muted)"></i>unknown / 未披露</span></p>
${table([["layer","层级"],["term","精确值"],["meaning","含义"]],[
  {layer:"artifact",term:"needs_human_review",meaning:"机器产物已成形，但没有人类审批；不能标为production_reviewed"},
  {layer:"dimension",term:"applicable",meaning:"维度适用且至少一项required indicator为observed"},
  {layer:"dimension",term:"not_applicable",meaning:"维度不适用；本报告仅用于工业营运资本框架"},
  {layer:"dimension",term:"unknown",meaning:"至少一项required indicator为not_disclosed，证据不足"},
  {layer:"dimension",term:"conflicting",meaning:"同一必要问题的可靠证据相互冲突；本报告当前没有该状态"},
  {layer:"indicator",term:"observed",meaning:"有可解析source_refs支持"},
  {layer:"indicator",term:"not_disclosed",meaning:"主源未披露，保留source gap"},
  {layer:"indicator",term:"not_applicable",meaning:"指标机制不适用于该金融机构分支"},
  {layer:"indicator",term:"conflicting",meaning:"指标证据冲突；本报告当前没有该状态"},
  {layer:"gate",term:"pass_with_scope",meaning:"在明确来源/范围边界内通过"},
  {layer:"gate",term:"provisional",meaning:"暂时成立，关键后续证据未关闭"},
  {layer:"gate",term:"range_only",meaning:"只支持区间或敏感性，不支持单点"},
  {layer:"gate",term:"mixed / inconclusive",meaning:"正反证并存或不足以定论"},
  {layer:"gate",term:"blocked / fail / outside_circle",meaning:"硬阻断；当前九道Gate没有使用，但若触发会阻止后续正向readiness"},
])}
</section>

<section id="long-term" class="card"><h2>长期底稿：业务、利润来源与护城河候选</h2>
<p>公司的主要收入不是单一“期货手续费”：2025年净手续费占43.64%、净利息占41.25%、投资收益占10.67%。期货经纪手续费又占净手续费82.62%。客户保证金利息随客户资金规模与利率共同变化；2025客户权益扩大但净利息收入下降16.05%，表明利率下行可以压过规模增长。</p>
${barChart("2025经营收入构成（RMBm）", ["净手续费", "净利息", "投资收益", "交易净额", "其他"], [605.56,572.343,148.07,1.347,60.191])}
<p class="callout">图的含义：手续费与利息合计约84.9%，是可跟踪的核心；投资与公允价值损益波动较大，不适合与经纪收入使用同一持续性假设。</p>
${table([["item","收入项目"],["fy2024_rmb_m","2024 RMBm"],["fy2025_rmb_m","2025 RMBm"],["yoy_pct","同比%"],["fy2025_mix_pct","2025占比%"]],income,"NH-CRIT-003")}

<h3>分部利润：优势候选也是集中风险</h3>
${table([["segment","分部"],["fy2024_income_rmb_m","2024收入"],["fy2025_income_rmb_m","2025收入"],["fy2024_pbt_rmb_m","2024 PBT"],["fy2025_pbt_rmb_m","2025 PBT"]],segments,"NH-CRIT-004")}
<p>境外金融服务2025年税前利润RMB501.010m，约占集团PBT 91.9%。跨境牌照、清算资格和客户资产规模是护城河候选；但同一事实也意味着美国、香港、新加坡等地的利率、监管和客户交易活动会集中影响利润。缺少客户留存、费率溢价和份额趋势，不能把牌照数量直接写成已证实的护城河。</p>

<h3>五年财务与ROE</h3>
${barChart("归母利润趋势（RMBm）", annual.map(r=>r.period), annual.map(r=>Number(r.parent_profit_rmb_m)||0), "", "#5ba7ff")}
<p class="callout">图的含义：2022后利润增长明显，但2021经营收入与HKFRS口径未完整重列，故只保留利润；2023-2025的增长仍需拆解利率、交易活跃度、投资波动和境外业务。</p>
${table([["period","期间"],["operating_income_rmb_m","经营收入RMBm"],["parent_profit_rmb_m","归母利润RMBm"],["parent_equity_rmb_m","归母权益RMBm"],["client_payables_rmb_m","客户应付款RMBm"],["roe_pct","ROE%"],["cfo_rmb_m","CFO RMBm"]],annual,"NH-CRIT-002")}

<h3>产品和客户指标</h3>
${table([["period","期间"],["metric","指标"],["value","值"],["unit","单位"],["scope_note","范围"]],[
  {period:"FY2025",metric:"境内客户权益",value:38.982,unit:"RMBbn",scope_note:"隔离客户资金"},
  {period:"FY2025",metric:"境外客户净权益",value:23.306,unit:"HKDbn",scope_note:"境外业务"},
  {period:"FY2025",metric:"境外AUM",value:4.812,unit:"HKDbn",scope_note:"资产管理"},
  {period:"FY2025",metric:"国内AUM",value:1.081,unit:"RMBbn",scope_note:"资产管理"},
  {period:"FY2025",metric:"公募基金规模",value:19.136,unit:"RMBbn",scope_note:"南华基金"},
  {period:"FY2025",metric:"场外衍生品新增名义本金",value:74.9,unit:"RMBbn",scope_note:"风险管理子公司"},
],"NH-CRIT-005")}
</section>

<section class="card"><h2>Q1与隐含Q2：增长从哪里来</h2>
${barChart("2026Q1相对2025Q1的利润来源变动（RMBm）", q1Bridge.map(r=>r.item), q1Bridge.map(r=>r.change_rmb_m), "", "#21c08b")}
<p class="callout">图的含义：手续费与利息的改善是核心顺风；投资收益增加RMB93.9m和信用减值费用转回带来约RMB30.4m有利变化，公允价值与汇兑则抵消。不能把+138.8%的归母利润同比全部视为经纪业务的重复性增长。</p>
${table([["item","项目"],["q1_2025_rmb_m","2025Q1"],["q1_2026_rmb_m","2026Q1"],["change_rmb_m","变动RMBm"],["interpretation","解释"]],q1Bridge,"NH-CRIT-008")}
${table([["metric","指标"],["q1_2025_rmb_m","2025Q1"],["q1_2026_rmb_m","2026Q1"],["yoy_pct","同比%"],["h1_2025_rmb_m","2025H1"],["h1_2026_rmb_m","2026H1预告"],["q2_2025_rmb_m","2025Q2"],["implied_q2_2026_rmb_m","2026Q2隐含"]],quarterly,"NH-CRIT-011")}
<p>H1归母利润预告RMB375m–405m，减去Q1后隐含Q2为RMB170.237m–200.237m；相对2025Q2约+17.0%至+37.6%，相对2026Q1约-16.9%至-2.2%。这说明Q2仍可能同比增长，但不等于Q1增速继续加速。正式中报尚未披露。</p>
</section>

<section class="card"><h2>金融机构 owner earnings：为什么不能用CFO减资本开支</h2>
<p data-evidence-id="NH-CRIT-009">Q1合并CFO为RMB5.318bn，主要由客户权益流动驱动。客户保证金由隔离资产对应，不是普通经营现金。因此本报告把owner earnings标为<strong>unavailable</strong>，不机械使用合并CFO-capex。</p>
${table([["case","敏感性"],["reported_parent_profit_rmb_m","2025归母利润"],["assumed_regulatory_retention_pct","假设资本留存%"],["candidate_distributable_rmb_m","候选可分配RMBm"],["status","状态"]],ownerSensitivity)}
<p class="callout risk">这张表只是“若监管资本留存为40%–70%”的研究敏感性，不是owner earnings、不是公司股利承诺。缺失的是母公司及受监管子公司的法定可分配现金、上游能力和资本留存桥。</p>
</section>

<section class="card"><h2>监管资本、客户资金隔离与生存能力</h2>
${barChart("净资本/风险资本（%）", ["FY2024","FY2025","2026Q1","最低要求"], [166,240,137,100], "%", "#f4bf4f")}
<p class="callout risk" data-evidence-id="NH-CRIT-010">图的含义：Q1从240%降到137%，仍高于100%最低值，但缓冲由140个百分点缩至37个百分点。该变量会影响扩张、股利、回购和融资选择，是正式中报最重要的核验项。</p>
${table([["period","期间"],["net_capital_rmb_m","净资本RMBm"],["net_capital_to_risk_pct","净资本/风险资本%"],["net_capital_to_net_assets_pct","净资本/净资产%"],["current_assets_to_current_liabilities_pct","流动资产/流动负债%"],["liabilities_to_net_assets_pct","负债/净资产%"],["clearing_settlement_rmb_m","结算准备金RMBm"]],riskCapital,"NH-CRIT-006")}
</section>

<section class="card"><h2>股本、回购、可转债与每股经济性</h2>
${table([["scenario","情景"],["shares_m","股份m"],["treatment","处理"],["included_in_base_valuation","基准估值"]],shareBridge,"NH-CRIT-013")}
<p>4.5送10的资本化发行改变每股分母和股价刻度，不创造企业价值。研究使用公司披露的转增后预期1,038.145m股。拟A股可转债上限RMB1.2bn仍未发行，示例75.901m转股仅作摊薄情景；它不是“股价低于某价自动还钱、高于某价自动转股”的简单二元结构，最终要看发行条款、转股期、转股价调整、赎回和回售条件。</p>
<p>H股回购授权上限HK$130m、股数上限10%，截至研究日未发现实际成交披露。授权与执行必须分开记录。</p>
</section>

<section class="card"><h2>治理、会计与CFO信息边界</h2>
${table([["date","日期"],["event","事件"],["fact","事实"],["interpretation","研究解释"],["source_id","来源"]],[
  {date:"2026-03-27",event:"会计估计变更",fact:"ECL低风险对手方组合调整；FY2026 PBT影响不超过RMB40m",interpretation:"Q1精确贡献未披露",source_id:"G04"},
  {date:"2026-03-27",event:"拟更换审计师",fact:"拟改聘安永；声明无分歧",interpretation:"持续监控，不自动等同舞弊",source_id:"G01"},
  {date:"2026-03-27",event:"关联采购上限",fact:"RMB1m上调至RMB7m",interpretation:"倍数大、绝对金额小，关注定价与监督",source_id:"G02"},
  {date:"2026-04-01",event:"监管警示",fact:"采购内控和员工行为管理缺陷",interpretation:"跟踪书面整改和后续监管",source_id:"F11"},
],"NH-CRIT-015")}
<p>年报显示财务负责人/主管会计工作负责人为李莉（此前以代行财务总监职责披露）。截至研究日未找到可独立核验的近期CFO公开讲话或完整承诺兑现记录，因此管理层维度保持unknown；不能用董事长致辞替代CFO证据。</p>
</section>

<section id="market-pricing" class="card"><h2>市场定价：真实PE、PB与正常化</h2>
${table([["label","口径"],["profit_basis_rmb_m","利润基础RMBm"],["eps_hkd","EPS HKD"],["price_hkd","价格HKD"],["pe_x","PE×"],["pb_x","PB×"],["status","状态"]],valuation,"NH-CRIT-021")}
<p class="callout">FY PE约12.3×，TTM PE约9.9×，FY2022-25简单正常化PE约15.0×。TTM最低，是因为Q1高增长中含投资与减值顺风；三种口径必须同时保留。</p>
${barChart("P/B-ROE敏感性（HKD/股）", ["下行情景","基准情景","上行情景","研究日价格"], [4.1495,5.3351,7.4691,6.65], "", "#5ba7ff")}
<p class="callout">图的含义：基于FY2025净资产、转增后股本及11%权益成本，ROE 8%/10%/12%分别对应约HK$4.15/HK$5.34/HK$7.47。研究日价格高于基准情景，仅上行情景形成正差；这只是P/B-ROE敏感性，不是单点估值结论。</p>
${table([["scenario","情景"],["sustainable_roe_pct","可持续ROE%"],["terminal_growth_pct","长期增长%"],["discount_rate_pct","权益成本%"],["fair_pb","合理PB"],["intrinsic_value_per_share","HKD/股"]],intrinsic)}
</section>

<section id="event-monitor" class="card"><h2>近期监控：小盘、港股通、事件窗口与行业周期</h2>
<h3>港股通与调出风险</h3>
<p data-evidence-id="NH-CRIT-020">截至2026-07-27，02691同时在沪、深南向官方冻结名单中，状态为<strong>eligible</strong>。A/H同一发行人身份与资格已分开核验。调出不是当前事实；如果A股进入风险警示/退市等规则条件，或H股上市状态变化，才需要按当时两份名单重新确认。</p>
<p>港股通可以改变南向资金可达性和流动性，但不保证方向。指数成分资格（港股通之外）截至研究日未完成独立核验，保持unknown。</p>

<h3>已发生大事件与真实5日窗口</h3>
${barChart("事件T0至T+5收益（%）", eventWindows.filter(r=>r.t0_to_t5_pct!=="").map(r=>r.event), eventWindows.filter(r=>r.t0_to_t5_pct!=="").map(r=>Number(r.t0_to_t5_pct)), "%", "#5ba7ff")}
<p class="callout">图的含义：调入港股通、Q1高增长和回购授权没有形成一致的五日方向；T0规则按公告后下一完整交易日处理。窗口只是描述，不做单一事件因果推断。</p>
${table([["event","事件"],["t_minus_1_date","T-1"],["t_minus_1_close","T-1收盘"],["t0_date","T0"],["t0_close","T0收盘"],["t_plus_5_date","T+5"],["t_plus_5_close","T+5收盘"],["t0_return_pct","T0%"],["t0_to_t5_pct","T0→T+5%"],["volume_ratio","量比"],["adjustment_note","说明"]],eventWindows)}

<h3>行业周期：近期强，但不是公司利润的充分条件</h3>
${table([["period","期间"],["market_volume_billion_lots","成交量bn手"],["volume_yoy_pct","量同比%"],["turnover_trillion_rmb","成交额RMBtn"],["turnover_yoy_pct","额同比%"]],industry,"NH-CRIT-022")}
<p>2026H1行业成交量同比+25.23%、成交额+42.08%，有利于经纪活动；但公司利润还取决于净费率、客户结构、客户权益利率、投资损益和监管资本，所以行业成交增长不能直接等同公司利润增速。</p>

<h3>美国映射：只作条件性主题对照</h3>
${table([["company","公司"],["ticker","代码"],["relationship","关系"],["comparable_mechanism","可比机制"],["non_comparable_boundary","不可比边界"]],usMapping)}
<p>CME代表交易所/清算基础设施，IBKR代表电子经纪与客户资产/净利息链；两者都不是南华的同一公司、同等经济敞口或可替代证券。对照价值在于观察交易活跃度、客户资产和利率敏感性，而不是照搬估值。</p>

<h3>小盘风险登记</h3>
${table([["risk","风险"],["likelihood","可能性"],["impact","影响"],["evidence","证据"],["monitor","后续核验"]],smallCap)}
<p class="callout risk">小盘特有的次级风险包括：流动性、股本事件的光学错觉、南向资金流、可转债摊薄、回购授权未执行、审计/会计变化与监管整改。近期监控应围绕“正式中报—监管资本—资本动作—南向资格—成交结构”的事件链，而不是只看固定20日价格形态。</p>
</section>

<section id="research-contract" class="card"><h2>25维度 × 50 required indicators × 9 Gate</h2>
<p>下表直接展开全部50个指标，不把状态只藏在JSON。每个维度恰有两项required indicator；维度状态、指标状态、摘要与缺口均可在移动端横向滚动。</p>
${table([["dimension","维度"],["dimension_status","维度状态"],["indicator_no","#"],["indicator","required indicator"],["indicator_status","指标状态"],["summary","摘要"],["gap_or_reason","gap / 原因"]],indicatorRows)}
<p>Gate不是分数：\`blocking\`列说明当前最强约束，\`next tests\`列说明下一批能改变结果的证据。</p>
${table([["gate","Gate"],["result","result"],["reason","reason"],["blocking","blocking"],["next_tests","next tests"]],gateDisplay)}
</section>

<section class="card"><h2>未来趋势与验证路径</h2>
<div class="two">
<div><h3>可能的正向机制</h3><ul><li>行业成交量和成交额维持增长，带动经纪手续费。</li><li>客户权益继续扩大且利率企稳，提高保证金利息变现。</li><li>跨境牌照与清算网络带来客户资产和产品扩张。</li><li>监管资本恢复后，资本配置约束减轻。</li></ul></div>
<div><h3>可能的反向机制</h3><ul><li>费率竞争抵消行业成交增长。</li><li>利率下行压缩客户保证金净利息。</li><li>境外业务监管、汇率或投资损益反转。</li><li>可转债与资本需求稀释每股结果。</li></ul></div>
</div>
<p>下一次重做的触发点不是任意20日波动，而是正式中报、净资本变化、H股回购实际成交、可转债最终条款、审计师正式任命/审计结论、监管整改结果和沪深两份港股通名单变化。</p>
</section>

<section id="evidence" class="card"><h2>关键证据抽屉</h2><p class="sub">每项包含来源、页码/定位、期间、单位、范围、审计状态和公式；原始链接见下方来源表。</p>${evidenceDrawers}</section>
<section class="card"><h2>来源与方法</h2>
${table([["id","ID"],["tier","层级"],["title","标题"],["period","期间"],["audit_status","审计"],["url","链接"]],sources.map(s=>({...s,url:`<a href="${s.url}">原始链接</a>`})))}
<p>方法：先核验证券/发行人/股本/币种；再拆收入与利润、现金与监管资本；随后完成正常化、完全摊薄、估值区间、反方证据和事件窗口。金融机构明确禁用工业CFO-capex模板。</p>
</section>
<footer class="meta">状态：needs_human_review。Research artifact for evidence review only; this is not investment advice. 研究截止：2026-07-27。</footer>
</main></body></html>`;
fs.writeFileSync(path.join(root, "report.html"), html);

const readme = `# 南华期货（02691.HK）公司研究公开包

状态：\`needs_human_review\`。研究日：2026-07-27。此目录是可公开审阅的 production-shaped 包，但没有人类审批，不得标为 \`production_reviewed\`。

## 入口

- [可读报告](./report.html)
- [25维度 / 50+指标 / 9 Gate 合并产物](./combined-artifact.v2.json)
- [来源账本](./source-ledger.json)
- [关键证据索引](./evidence-index.json)
- [机器反方审查](./red-team.json)
- [校验结果](./validator-results.json)

## 研究结论边界

- 02691.HK 与 603093.SH 是同一发行人的 H/A 普通股；截至研究日，沪深两份南向官方名单均显示 02691 eligible。
- 金融机构分支不使用“合并 CFO 减资本开支”作为 owner earnings。客户保证金流动、隔离资产和监管资本必须单独处理。
- 2026Q1 经营增长真实存在，但投资收益、减值转回、公允价值与汇兑共同影响利润质量。
- H1预告隐含Q2仍同比增长、但低于Q1；正式中报和净资本恢复是下一关键证据。
- FY、TTM、简单周期正常化 PE 与 P/B-ROE 情景同时保留；没有单点结论。
- 美国 CME / IBKR 只标为 \`thematic_peer\`，不是同公司或同等经济敞口。

## 数据表

\`data/\` 保留五年财务、季度/H1、收入与手续费、分部与地域、Q1盈利质量桥、监管资本、完全摊薄股本、PE/PB正常化、owner-earnings敏感性、行业周期、港股通、治理、事件时间轴、真实五日窗口、小盘风险及美国主题映射。

## 方法

按照 Buffett–Munger 公司研究合同：证券身份 → 能力圈 → 商业经济性 → 护城河 → 管理层与资本配置 → owner earnings → 生存能力 → 估值区间 → 反方证据。所有派生值保留期间、币种、范围与公式；找不到的资料保持 unknown。

This package is for evidence review and is not investment advice.
`;
fs.writeFileSync(path.join(root, "README.md"), readme);

console.log(JSON.stringify({
  combined_sha256: combinedSha,
  sources: sources.length,
  dimensions: dimensions.length,
  indicators: dimensions.reduce((n,d)=>n+d.indicators.length,0),
  evidence_anchors: evidence.anchors.length,
  data_files: fs.readdirSync(dataDir).length,
}, null, 2));
