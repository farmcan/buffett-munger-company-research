# 上市公司研究报告 v2 HTML 模板

本目录提供一个不绑定具体公司、无外部 JavaScript/CSS 依赖的公开研究报告骨架。

```text
templates/
├── README.md
├── report-v2-template.html
├── company-research-v2.example.json
├── company-research-v2-contract.md
└── research-dimensions-and-gates.md
```

模板把两种不同用户任务拆成独立入口：

1. `长期公司底稿`：证券身份、业务与单位经济、三表、owner earnings、净现金、完全摊薄股本、25 个研究维度、九道 gate、red-team、估值和发布审核；
2. `短期事件监控`：官方事件日历、行业与全球映射、公司传导、公开产品信号、小盘结构风险、历史事件反应、情景闸门和 change log。

它是阅读层模板，不替代 `seed.stock-fundamentals-valuation.v2`、source ledger、CSV、red-team、validator 或人工复核 artifact。

长期入口另有独立的“市场定价状态”区块。它只描述市场如何给公司定价，不得反向改变
25 维度中的公司质量事实或 gate 结果。

## 使用方法

复制模板到目标公司的公开目录，再替换占位符：

```text
docs/company-research/<company-slug>/report.html
```

所有待替换内容使用显眼的 `[[UPPER_SNAKE_CASE]]` 或 `[[中文说明]]`。发布前应运行：

```bash
rg -n '\[\[' docs/company-research/<company-slug>/report.html
```

若仍有占位符，报告不得进入 `production_reviewed`。允许在刻意表达缺失证据时把值替换成 `未披露`、`不适用`、`冲突` 或 `待确认`，但必须同时给出原因、source gap 和下一验证动作，不能保留含糊空白。

## 给下一位研究者的最短实现路径

这五个文件不是平行版本，而是一套分层交接包：

| 文件 | 作用 | 可以改什么 | 不可改什么 |
| --- | --- | --- | --- |
| `company-research-v2.example.json` | 可通过核心 validator 的虚构机读样例 | 公司事实、来源、金额、状态与判断 | schema、25 维度、50 indicator、九 gate 的 ID 和顺序 |
| `company-research-v2-contract.md` | combined artifact 与发布边界 | 可增加有来源的可选 reader-facing block | 不得让可选块覆盖核心 contract |
| `research-dimensions-and-gates.md` | 人读 crosswalk 与状态传播规则 | 行业解释和证据示例 | exact dimension/indicator/gate vocabulary |
| `report-v2-template.html` | 长期底稿和短期监控的静态阅读层 | 公司内容、图表、表格、证据抽屉 | 双入口、精确表格、审核状态和非投资建议边界 |
| `README.md` | 实施、QA 与发布说明 | 可补行业分支 | 证据优先、可复算和人工复核边界 |

从零实施时按下面顺序，不要先填漂亮 HTML：

1. 复制 `company-research-v2.example.json`，先替换证券身份、研究日、价格日和主源；
2. 逐行完成 25 个维度与 50 个 indicator；没有证据就写 `unknown/not_disclosed`；
3. 建立五年三表、最新中期、owner earnings、净现金和完全摊薄股本桥；
4. 生成 source ledger、fact-level evidence index、独立 red-team 和可重算 CSV；
5. 运行核心 validator，通过后再把同一事实映射到 `report-v2-template.html`；
6. 运行 publication validator；没有具名人工复核时保持 `needs_human_review`；
7. 新财报或重大事件出现后写 change log，并把旧快照标为 `stale`，不静默覆盖。

最小命令：

```bash
cp docs/company-research/templates/company-research-v2.example.json \
  docs/company-research/<company-slug>/combined-artifact.v2.json
cp docs/company-research/templates/report-v2-template.html \
  docs/company-research/<company-slug>/report.html

PYTHONPATH=src python3 \
  skills/research-buffett-munger-company/scripts/validate_company_research.py \
  docs/company-research/<company-slug>/combined-artifact.v2.json

PYTHONPATH=src python3 \
  skills/research-buffett-munger-company/scripts/validate_company_research_publication.py \
  docs/company-research/<company-slug> \
  --output docs/company-research/<company-slug>/validator-results.json
```

样例中的公司、金额和 URL 均为虚构占位数据；它证明结构可以执行，不证明任何真实公司结论。

## 不可改变的结构

### 双入口

- `#long-term` 和 `#event-monitor` 必须继续是独立可深链入口；
- 长期结论不能用短期价格事件证明；
- 事件监控只写情景、传导和验证，不写买卖、仓位、止盈止损或“错过上涨”；
- 首页只保留当前证据状态、关键 blocking gaps 和下一验证事件。

### 25 个研究维度

`data-dimension` 必须保持以下顺序，不能缺失、重复或改名：

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

每张维度卡已经写入
`skills/research-buffett-munger-company/references/methodology-implementation-crosswalk.json`
中的两个规范 indicator ID。不得修改 ID 或顺序，只替换其后的
`[[INDICATOR_STATUS]]`，使用 `observed`、`not_disclosed`、`not_applicable`
或 `conflicting`。卡片只是 50 个 indicator family 的阅读摘要；结构化 artifact
仍是权威状态。

维度状态只能是 `applicable`、`not_applicable`、`unknown` 或
`conflicting`。缺失或冲突必须向映射 gate 传播，不能用漂亮叙事隐藏未研究项。
模板中的 `[[STATUS]]` 必须替换为这四个精确值之一；不得改成
`pass / conditional / fail / NA` 或任何自定义评分。

### 九道 gate

`data-gate` 必须保持以下顺序：

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

不计算加权总分。未知/冲突维度会阻止其映射 gate 使用正向结果；前置 gate
为 `fail`、`outside_circle` 或 `blocked` 时，后续 gate 不能重新宣告通过或
research readiness。`research_ready` 和
`research_ready_not_decision_ready` 只允许出现在最后一道 gate，且所有维度均已解决。

每个 `[[GATE_RESULT]]` 只能替换为 schema 允许的精确结果：

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

## 三个必须完整复算的桥

### Owner earnings

模板采用区间而不是单点：

```text
持续经营归母
- 非经营收益
+ 可辩护一次性损失
- 持续 SBC
+ 归属普通股东的其他非现金费用
- 维护 capex low/base/high
- 必需营运资本增量 low/base/high
= owner earnings low/base/high
```

每项写金额、币种、单位、期间、税前/税后、来源、理由和争议。若无法辩护维护
capex 或营运资本，状态应为 `unavailable`，不得把 EBITDA、调整后利润或
`CFO-capex` 直接改名为 owner earnings。

金融、保险、地产、资源、公共事业及其他行业分支必须换成相应法定资本和现金
分配桥，不能机械套工业企业公式。

### 净现金 / 净债务

逐项说明：

- 哪些现金可分配，哪些是受限、客户资金或最低经营现金；
- 流动投资采用何种流动性、信用、税务和估值折扣；
- 有息债务、租赁、未转股可转债及表外义务如何处理；
- 净现金的日期、法律实体范围和与估值币种的汇率来源。

### 完全摊薄股本

至少并排给出：

- 当前基本股数与库存股处理；
- 未转换情景：保留债务/到期现金偿还，使用未转换股数；
- 全转换情景：移除对应债务，加入潜在转换股，并说明转股价调整；
- 已授予 RSU、期权、股份奖励和其他承诺发行；
- 尚未授予的计划容量只列为 overhang，不冒充已发行股份；
- 回购注销、库存股再发行和每股 owner earnings 的一致口径。

## 页码级 evidence drawer

每个关键数字、桥接项、gate 结论和重要事件至少链接到一个
`details.evidence-drawer`。长期财务证据应包含：

```text
source_id
document_sha256
page
section_or_table
text_snapshot_sha256
line_start / line_end
source_text 或受版权约束的 evidence_summary
period
unit
currency
scope
audit_status
formula
source URL
limitations / conflict / source_gap
```

定位规则：

- PDF 首选 `page + section_or_table`；若仓库保存了由同一 PDF 生成的抽取文本，再补
  `text_snapshot_sha256 + line_start + line_end`；
- 行号只对该 SHA-256 对应的文本快照有效，不是原 PDF 的视觉行号，也不能脱离哈希单独引用；
- 动态网页优先使用稳定 URL、页面标题、HTML anchor/表格名和访问日期；只有保存了快照时才引用
  快照行号；
- CSV/JSON 使用 `record_key`、列名或 JSON Pointer；代码使用 commit SHA 和行号；
- `source_text/evidence_summary` 仍需保留最短必要摘录，行号不能替代读者可见证据。

事件证据额外包含：

```text
completed / confirmed / TBA
source tier
published_at / accessed_at
first tradable date
causal confidence
company transmission
required confirmation
```

官方 PDF 或公告必须深链到原始 HTTPS URL。直播网页或可变页面若被研究实际消费，
还需在 source ledger 保存内容快照 SHA-256。不要把方法论引用当成公司事实来源。

## 表格与 SVG 的同步规则

- SVG 只帮助识别形状，旁边必须保留精确表格；
- 两者使用相同期间、单位、scope、审计状态和 derived 标记；
- 折线趋势尽量使用足够连续的同粒度期间；
- Q1、H1 和全年绝对值不得画成一条等距趋势；
- 普通柱状图从零开始，不用双轴制造相关性；
- 正负方向必须有文字或数值标签，不能只靠红绿颜色；
- 更新 CSV 后，同步更新表格、SVG、caption、source as-of 和 change log。

## 市场定价状态

这一节必须和“公司质量状态”并排，避免把低估值、大回撤或上升趋势写成好公司证明。

至少展示：

- 无前视偏差的历史 FY/TTM PE、P/B、EV/owner earnings 或行业适配指标分位；
- 当前价相对 bear/base/upside 内在价值的 gap，并保持同币种、同净现金和同股本情景；
- 同行相对溢价/折价，统一业务、会计口径、周期、增长和资本结构；
- 三至五年每股经营收益、净稀释/回购、股东分配和估值倍数的回报分解；
- 一年、三年、五年最大回撤、相对 200 日趋势、实现波动率和成交/换手。

历史估值在每个历史时点只能使用当时已公开的盈利、净资产、股数和企业价值输入，不能把
后来公布的全年利润回填到此前价格。PE 对非正盈利使用 `not_meaningful`；缺输入使用
`unavailable`。内在价值结果沿用 `calculated`、`non_positive_equity_value` 或
`unavailable`。

三至五年回报分解是透明研究假设，不是概率、目标价或收益承诺。回撤、200 日趋势、波动率和
换手只作市场状态旁证，不得生成买卖、仓位、止损或时点建议；平均成交额也不能保证大仓位
可以按屏幕价格退出。

### 价格形成与空头定位

小盘股的“为什么卡在某个价格”不能只看均线，也不能只看一个卖空比例。建议增加可选
`data/price-short-positioning.csv`，把以下证据分开：

| 层 | 最低字段 | 允许判断 | 禁止混同 |
| --- | --- | --- | --- |
| 价格状态 | 完整交易日收盘、20/60/200 日均线、成交量、VWAP 代理、观察窗 | 当前价格相对短中长期成本处于何处 | 均线或整数位等于硬支撑/阻力 |
| 可申报净空仓 | 官方报告日、净空仓股数、固定股本分母、申报阈值和发布滞后 | 空头存量及其周度方向 | 可申报仓位等于全部市场空头 |
| 每日卖空成交 | 完整/半日状态、卖空成交额、全日成交额、加权区间 | 当日卖空流量强弱 | 卖空成交等于净空仓增加 |
| 借券条件 | 借券费率、可借库存、利用率、召回风险；缺失写 `unknown` | 做空边际成本和拥挤度 | 用成交量替代借券数据 |
| 公司与市场供求 | 回购/增持、配售、解禁、可转债、指数/互联互通、事件套牢区 | 哪些可观察力量可能互相抵消 | 把同时发生写成已证实因果 |

净空仓除以近期平均成交量只能标为“流动性覆盖代理”，不是标准 days-to-cover；分母需固定到同一
股本日期。半日卖空比例不得与完整交易日直接比较。只有净空仓、完整日卖空强度、价格/成交量和
借券条件中至少两到三层同向，才可写“边际空头增强/减弱”；否则保持 `mixed/unknown`。

建议 CSV 最小表头：

```text
record_type,date_or_period,close_or_last,metric,value,unit,reference_denominator,source_url,limitations
```

## 短期事件替换规则

每个事件固定写：

```text
date / window
status: completed | confirmed | TBA
event_type
source_tier
fact
global_mapping_relation
transmission_to_company
required_confirmation
market_reaction（仅历史事件）
next_check
invalidation / uncertainty
```

历史价格反应统一首次可交易日和 T-1、T0、T+1、T+5，必要时 T+20，同时给基准、
超额收益、成交量、重叠事件和因果置信度。硬件或上游代理的价格变化不能直接写成
应用公司因果；至少需要成本/价格机制、应用股广度和公司 KPI 的共同验证。

公开产品数据分三层：公司连续经营证据、累计沉淀证据、短期热度。App Store、
Google Play、网站访问和搜索热度至少观察连续三至六个期间，并写清地区、平台、
估算方法和限制；排名或访问量不能直接推导收入、留存或付费。

## 审核与发布

模板中的审核卡必须分别显示：

1. combined/split artifact 的 schema、状态和 SHA-256；
2. 独立 red-team artifact 状态；
3. 确定性 validator 的版本、错误和警告；
4. 具名 reviewer、`reviewed_at`、未解决 critical gaps 和最终 publication state。

机器产物完整不等于人工批准。没有真实 reviewer 时必须保持
`needs_human_review`。重要披露发生后，先把旧报告标为 `stale`，再在 change log
记录事实、判断、artifact checksum 和复核者变化，不静默覆盖。

## 发布前最小检查

- [ ] 页面不再含 `[[...]]` 占位符；
- [ ] 证券身份、价格日、研究日和币种一致；
- [ ] 任取关键数字可在两次点击内看到页码、原文/摘要和公式；
- [ ] 页码同时给出表名/章节；有校验文本快照时给出 SHA-256 与起止行号；
- [ ] 图表与精确表格使用同一数据；
- [ ] owner earnings、净现金和完全摊薄股本可逐项复算；
- [ ] 公司质量与市场定价状态已分开，历史估值不存在前视偏差；
- [ ] 三情景 gap、同行溢价和三至五年回报分解使用一致币种、股本和日期；
- [ ] 回撤、200 日趋势、波动率和换手只作旁证，没有产生交易指令；
- [ ] 可申报净空仓、每日卖空成交和借券条件没有混写；半日数据已标明；
- [ ] 25 维度、50 indicator、九 gate 顺序完整且状态传播一致；
- [ ] red-team、validator 和具名人工复核状态真实；
- [ ] 短期事件按 completed / confirmed / TBA 分层；
- [ ] 公开产品信号没有冒充财务事实；
- [ ] change log 和 stale 日期已更新；
- [ ] 没有投资指令、仓位建议或收益承诺；
- [ ] 公开内容不含私有仓位、本地绝对路径、凭证或未经审查材料。
