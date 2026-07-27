# 中芯国际（00981.HK）公司研究包

研究截止：2026-07-27。公开状态：`needs_human_review`。

## 结论

中芯的产能利用率与收入周期向上，但这尚未证明是高股东回报生意。FY2025 利用率 93.5%、收入同比增长 16.2%，与此同时现金购置 PP&E 为 US$8.400bn、经营现金流仅 US$3.194bn；FY2021–FY2025 的 OCF-现金PP&E 代理连续为负。FY2023–FY2025 晶圆收入/8英寸等值出货 ASP 代理约从 US$988 降至 US$907。

2026Q1 收入同比 +11.5%，但毛利约 -0.4%、经营利润约 -20%；归母 +5% 还受 NCI 同比下降影响。2026Q2 收入 +14%～+16% QoQ、毛利 20%～22% 是管理层指引，不是实绩。

6 月 SMNC 交易后，股数增加与归母份额增加同时发生；公司尚未披露完整交易后 TTM 备考归母与同日稀释股数。因此本包不制造单一“当前真实 PE”。三个历史/机械交叉检查均在 100 倍以上，但每个都标注了分母限制。

## 目录

- `report.html`：适合 GitHub Pages 的可读报告，包含表格与内联 SVG 图。
- `combined-artifact.v2.json`：25 维度、50 指标、9 gates 的结构化研究。
- `source-ledger.json`：来源、时间、哈希与使用边界。
- `evidence-index.json`：18 条关键事实证据锚。
- `red-team.json`：独立反方审阅。
- `validator-results.json`：结构与公开发布校验结果。
- `data/critical-evidence-anchors.json`、`data/critical-evidence-locators.csv`：15 条 AR2025 关键事实的 PDF 页码、页内行号与页文本哈希；非分页网页或尚未冻结页文本的来源不伪造行号。
- `data/`：25 份可复算/可审计 CSV，加上上述 JSON locator 索引。

## 口径

- 同一发行人：年报第112页确认普通股分别在香港主板与上交所科创板上市，映射类型为 `same_company_listing`。
- 港股通：2026-07-27 冻结的沪深官方名单均显示 00981 eligible；资格会变化，实际公告优先。
- 价格：腾讯二级行情 2026-07-27 收盘 HK$70.65；不是交易所认证行情。
- 汇率：ECB 2026-07-24 EUR 交叉汇率，CNY/HKD=0.8635136、HKD/USD=7.842577。
- Owner earnings：因维护性capex、NCI现金流归属和交易后利润桥缺失，状态为 unavailable。集团 OCF-现金PP&E 只作诊断代理。
- 历史估值：未构造 look-ahead-safe 历史 PE；不会用事后利润回填历史日期。

## 下一次更新

以 2026Q2 正式结果、交易后首次完整归母/稀释股数披露或重大 BIS/EAR 更新中较早者为准。研究截止日未冻结官方 Q2 发布日期。

This is a research-support artifact, not investment advice.
