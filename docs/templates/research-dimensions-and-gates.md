# Buffett–Munger 公司研究 v2：25 维度与九道 Gate 可读 Crosswalk

版本：2026-07-27

用途：帮助研究员、reviewer 和报告读者理解现有 production contract

边界：本文件只解释既有规范，不新增 dimension、indicator、gate、result 或发布状态

## 1. 唯一规范与适用边界

本文件的唯一规范来源是：

1. `skills/research-buffett-munger-company/references/company-research-schema.md`
2. `skills/research-buffett-munger-company/references/company-research-master-checklist.md`
3. `skills/research-buffett-munger-company/references/methodology-implementation-crosswalk.json`
4. 可执行实现：`src/seed/company_research_validation.py`

正式 combined artifact 使用：

```text
seed.stock-fundamentals-valuation.v2
```

以下内容不是 contract：

- “公司底稿 / 事件监控”双入口；
- evidence drawer、搜索、筛选、CSV 下载；
- HTML 的图表、卡片和导航布局。

这些可以改善交付体验，但不能替代 v2 artifact、25 个固定维度、50 个固定 indicator family、九道 gate、red-team、validator 或具名人工复核。

## 2. 不得改写的状态与字段

### 2.1 Dimension row

25 个 dimension 必须按固定顺序出现。每行字段为：

```text
dimension
status
summary
indicators
source_refs
positive_evidence
counter_evidence
source_gaps
```

Dimension 的 exact `status` 只有：

```text
applicable
not_applicable
unknown
conflicting
```

规则：

- `applicable`：至少一个 indicator、明确 tier 的公司证据和正面证据；
- `not_applicable`：必须有 `not_applicable_reason`，不能用 0 代替；
- `unknown`：必须有 source gap；
- `conflicting`：必须保留冲突来源并有 reconciliation gap。

### 2.2 Indicator row

每个 dimension 必须包含两个固定 indicator family，共 50 个。Indicator 字段为：

```text
id
status
summary
source_refs
source_gaps
```

Indicator 的 exact `status` 只有：

```text
observed
not_disclosed
not_applicable
conflicting
```

传播规则：

- `observed` 必须绑定直接公司证据；methodology citation 不能替代 company fact；
- required indicator 为 `not_disclosed` 时，父 dimension 必须是 `unknown`；
- required indicator 为 `conflicting` 时，父 dimension 必须是 `conflicting`；
- 整个 dimension 为 `not_applicable` 时，两个 indicator 都必须为 `not_applicable`；
- generic catch-all indicator 不能替代任一固定 indicator family。

### 2.3 Evidence layer

证据层只有：

```text
facts
reported_claims
interpretations
assumptions
source_gaps
```

公司讲话进入 `reported_claims`；Seed 计算进入 `facts` 的确定性计算分支或 `interpretations`；情景输入进入 `assumptions`。缺失 CFO 讲话、客户留存或维护性资本开支时，保留 `source_gaps`，不能用其他发言人、同行数值或模型常识补齐。

## 3. 25 个 exact dimensions × 50 个 exact indicator IDs

`origin` 的含义：

- `primary_method`：研究问题直接实现经主源审计的方法原则；具体阈值仍是 Seed 工程化；
- `mixed`：主源方法决定问题，Seed 增加证据、会计或流程控制；
- `seed_operating_control`：Seed 为防止证据丢失或错误推断而增加，不能冒充 Buffett/Munger 原话。

`stage` 决定 deterministic pipeline 的唯一归属：`fact_pack` 16 项、`company_research` 7 项、`red_team` 1 项、`valuation` 1 项。

| # | Exact dimension ID | 中文 | Origin | Stage | Exact indicator ID 1 | Exact indicator ID 2 | Exact gate IDs |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | `security_and_legal_subject` | 证券与法律主体 | `mixed` | `fact_pack` | `exact_security_issuer_share_class_and_rights` | `dated_price_share_count_currency_and_listing_status` | `identity_and_source_integrity` |
| 2 | `control_and_beneficial_ownership` | 控制权与受益所有权 | `mixed` | `fact_pack` | `controller_voting_pledges_and_cross_holdings` | `value_transfers_nci_and_related_party_exposure` | `identity_and_source_integrity`; `management_and_capital_allocation` |
| 3 | `business_model` | 商业模式 | `mixed` | `company_research` | `payer_value_proposition_revenue_and_cash_mechanism` | `capital_needs_and_business_failure_variables` | `circle_of_competence`; `business_economics` |
| 4 | `revenue_structure` | 营收结构 | `seed_operating_control` | `fact_pack` | `segment_product_and_geography_reconciliation` | `volume_price_mix_acquisition_and_scope_bridge` | `business_economics` |
| 5 | `industry_chain_position` | 产业链位置 | `mixed` | `fact_pack` | `upstream_process_customer_payer_and_substitute_map` | `profit_pool_and_inventory_credit_technology_risk` | `business_economics`; `durable_moat` |
| 6 | `product_and_unit_economics` | 产品与单位经济 | `mixed` | `fact_pack` | `price_volume_mix_and_incremental_economics` | `industry_denominator_scope_and_comparability` | `circle_of_competence`; `business_economics` |
| 7 | `customers` | 客户 | `seed_operating_control` | `fact_pack` | `customer_channel_end_user_and_payer_separation` | `concentration_retention_receivables_inventory_and_external_evidence` | `circle_of_competence`; `business_economics`; `durable_moat` |
| 8 | `suppliers` | 供应商 | `seed_operating_control` | `fact_pack` | `critical_inputs_concentration_related_parties_and_substitution` | `terms_prepayments_availability_and_cost_pass_through` | `circle_of_competence`; `business_economics`; `survival_and_balance_sheet` |
| 9 | `competition_structure` | 竞争结构 | `mixed` | `company_research` | `entry_exit_capacity_price_and_substitution` | `competitor_customer_and_regulator_corroboration` | `business_economics`; `durable_moat` |
| 10 | `durable_moat` | 护城河及其方向 | `primary_method` | `company_research` | `mechanism_economic_result_durability_and_direction` | `strongest_falsifying_evidence` | `durable_moat`; `decision_and_disconfirming_evidence` |
| 11 | `revenue_quality` | 收入质量 | `seed_operating_control` | `fact_pack` | `revenue_receivables_contract_assets_returns_and_cash` | `acquisition_period_end_channel_and_recognition_distortion` | `business_economics`; `owner_earnings` |
| 12 | `earnings_quality` | 盈利质量 | `mixed` | `fact_pack` | `reported_to_normalized_parent_earnings_bridge` | `tax_attribution_scope_and_adjustment_disagreement` | `business_economics`; `owner_earnings` |
| 13 | `cash_conversion` | 现金转换 | `mixed` | `fact_pack` | `profit_operating_cash_and_distributable_cash_bridge` | `factoring_payment_restricted_cash_and_sector_scope` | `owner_earnings`; `survival_and_balance_sheet` |
| 14 | `working_capital` | 营运资本 | `mixed` | `fact_pack` | `receivables_inventory_payables_prepayments_and_contract_balances` | `sustainable_financing_vs_temporary_cash_release` | `business_economics`; `owner_earnings` |
| 15 | `capital_intensity` | 资本强度与再投资 | `primary_method` | `fact_pack` | `maintenance_vs_growth_investment_range` | `capex_capacity_utilization_and_competitive_requirements` | `business_economics`; `owner_earnings` |
| 16 | `returns_on_capital` | 资本回报与增量回报 | `primary_method` | `company_research` | `multiperiod_roe_roic_and_incremental_returns` | `leverage_buyback_cycle_and_accounting_decomposition` | `business_economics`; `management_and_capital_allocation` |
| 17 | `balance_sheet_survival` | 资产负债表与生存 | `primary_method` | `fact_pack` | `debt_liquidity_covenants_guarantees_pledges_and_off_balance` | `adverse_scenario_financing_need` | `survival_and_balance_sheet` |
| 18 | `capital_allocation` | 资本配置 | `primary_method` | `company_research` | `reinvestment_ma_dividend_buyback_issuance_debt_and_cash_ledger` | `diluted_per_share_outcomes_and_opportunity_cost` | `management_and_capital_allocation`; `intrinsic_value_and_margin_of_safety` |
| 19 | `management` | 管理层 | `mixed` | `company_research` | `dated_commitments_vs_outcomes` | `incentives_compensation_succession_insider_actions_and_candor` | `management_and_capital_allocation`; `decision_and_disconfirming_evidence` |
| 20 | `governance_and_related_parties` | 治理与关联交易 | `mixed` | `company_research` | `related_sales_purchases_loans_guarantees_and_asset_transfers` | `pricing_minority_fairness_oversight_and_dissent` | `identity_and_source_integrity`; `management_and_capital_allocation`; `survival_and_balance_sheet` |
| 21 | `accounting_and_audit` | 会计与审计 | `seed_operating_control` | `fact_pack` | `audit_kam_standard_policy_and_restatement` | `statement_reproduction_and_conflict_preservation` | `identity_and_source_integrity`; `owner_earnings`; `survival_and_balance_sheet` |
| 22 | `tax_and_legal` | 税务与法律 | `seed_operating_control` | `fact_pack` | `effective_deferred_and_uncertain_tax` | `litigation_penalties_compliance_and_tail_exposure` | `survival_and_balance_sheet` |
| 23 | `per_share_economics` | 每股经济 | `primary_method` | `fact_pack` | `basic_diluted_and_fully_diluted_share_reconciliation` | `per_share_growth_distribution_issuance_and_repurchase_outcomes` | `business_economics`; `management_and_capital_allocation`; `intrinsic_value_and_margin_of_safety` |
| 24 | `valuation` | 估值与安全边际 | `primary_method` | `valuation` | `currency_consistent_value_range_assumptions_and_dates` | `reverse_expectations_sensitivities_and_cross_check` | `intrinsic_value_and_margin_of_safety` |
| 25 | `disconfirming_evidence` | 反方证据与失效条件 | `mixed` | `red_team` | `independent_strongest_counter_thesis` | `observable_invalidation_next_evidence_and_review_date` | `decision_and_disconfirming_evidence` |

### 3.1 25 维度如何读

这不是“25 项都有数据才算好公司”的评分表，而是“25 项都必须被处理”的证据覆盖表：

- 未披露是有效研究结果，但必须写 `not_disclosed` → dimension `unknown` → 传播到 mapped gate；
- 不适用是行业分支判断，必须写理由，不能填 0；
- 来源冲突必须原样保留，不能挑一个更顺眼的数字；
- `primary_method`、`mixed` 和 `seed_operating_control` 都可成为 production 必查项，但只有前两类中被方法主源支持的部分才能归因给 Buffett/Munger；
- 表中 50 项只是最低问题覆盖，不能替代多年序列、客户/供应商双向验证和行业专用指标。

## 4. 九个 exact gates

Artifact 必须按以下固定顺序保存九道 gate：

| # | Exact gate ID | Gate 要回答的问题 | 直接映射的 exact dimensions | 最低证据焦点 |
| ---: | --- | --- | --- | --- |
| 1 | `identity_and_source_integrity` | 证券、发行人、控制、来源、会计与治理基础是否可信？ | `security_and_legal_subject`; `control_and_beneficial_ownership`; `governance_and_related_parties`; `accounting_and_audit` | exact security/issuer/share rights；价格、股本、币种和上市状态同日；控制权/NCI/关联方；审计、准则、重述、statement reproduction |
| 2 | `circle_of_competence` | 能否解释谁付钱、为何付钱、单位经济、客户/供应商和失败变量？ | `business_model`; `product_and_unit_economics`; `customers`; `suppliers` | customer-to-cash；资本需求；行业 denominator；客户/渠道/终端/付款方；关键投入与替代周期 |
| 3 | `business_economics` | 3—5 年及最新中期的收入、利润、现金、资本回报和驱动是否清楚？ | `business_model`; `revenue_structure`; `industry_chain_position`; `product_and_unit_economics`; `customers`; `suppliers`; `competition_structure`; `revenue_quality`; `earnings_quality`; `working_capital`; `capital_intensity`; `returns_on_capital`; `per_share_economics` | 分部/产品/地域桥；量价组合；产业链利润池；收入/盈利质量；营运资本；维护/增长投资；ROE/ROIC；每股结果 |
| 4 | `durable_moat` | 优势机制是否能阻止竞争拿走超额回报，方向是变宽还是变窄？ | `industry_chain_position`; `customers`; `competition_structure`; `durable_moat` | 客户行为；进入/退出、产能、价格和替代；竞争者/客户/监管旁证；最强 moat falsifier |
| 5 | `management_and_capital_allocation` | 管理层是否诚信理性，资本配置是否增加稀释后每股价值？ | `control_and_beneficial_ownership`; `returns_on_capital`; `capital_allocation`; `management`; `governance_and_related_parties`; `per_share_economics` | 承诺兑现；激励/薪酬/继任；再投资/M&A/分红/回购/增发/债务/现金 ledger；机会成本；少数股东公平性 |
| 6 | `owner_earnings` | 归母利润能否桥接为可辩护的 owner-earnings 区间？ | `revenue_quality`; `earnings_quality`; `cash_conversion`; `working_capital`; `capital_intensity`; `accounting_and_audit` | reported-to-normalized；税与 scope；利润—CFO—可分配现金；受限现金/保理；维护 capex；所需营运资本；行业专用分支 |
| 7 | `survival_and_balance_sheet` | 公司能否穿越合理负面情景而不发生永久资本损失或被迫融资？ | `suppliers`; `cash_conversion`; `balance_sheet_survival`; `governance_and_related_parties`; `accounting_and_audit`; `tax_and_legal` | 债务期限、流动性、契约、担保、质押和表外；关键供应可得性；法务税务尾部；负面情景融资需求 |
| 8 | `intrinsic_value_and_margin_of_safety` | 价值区间、反向预期与交叉检查是否同币种、同日期、可复算？ | `capital_allocation`; `per_share_economics`; `valuation` | 股本与稀释；资本配置机会成本；explicit assumptions/dates；reverse expectations；sensitivities；至少一种 cross-check |
| 9 | `decision_and_disconfirming_evidence` | 综合结论是否保留最强反方、失效条件、下一证据和复核日期？ | `durable_moat`; `management`; `disconfirming_evidence`，并受全部 unresolved dimension 的全局阻断 | 独立 counter-thesis；可观察 invalidation；next evidence/review date；source gaps；条件化结论 |

每道 gate 的 exact row contract 是：

```text
gate
result
reason
source_refs        # optional
blocking_gaps      # optional
next_tests         # optional
```

## 5. Exact allowed gate results

不得使用 `conditional`、`NA`、`complete`、`needs_more_evidence` 等自造 gate result。九道 gate 的 exact allowed result vocabulary 只有：

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

特殊限制：

- `outside_circle` 只能用于 `circle_of_competence`；
- `research_ready` 和 `research_ready_not_decision_ready` 只能用于 `decision_and_disconfirming_evidence`；
- gate 必须说明理由；不能把九道 gate 压成加权总分；
- 优秀的商业经济不能抵消治理、生存或来源失败。

### 5.1 结果如何选择

contract 没有为每个 gate 建立固定数值阈值。研究员必须依据证据解释结果，但受以下硬约束：

- 适用维度完整、无 unresolved dimension，且该 gate 的核心问题得到直接公司证据支持，才可能使用正面结果；
- 证据只支持有限范围时可用 `pass_with_scope`，但 mapped dimension 仍不能是 `unknown`/`conflicting`；
- 正反证据并存时使用 `mixed_positive` 或 `mixed`，但 `mixed_positive` 同样属于被 unresolved dimension 禁止的正面结果；
- 只有区间可辩护时使用 `range_only`；
- 证据不足以收窄结论时使用 `provisional` 或 `inconclusive`；
- 早期 gate 使后续无法可靠工作时使用 `blocked`；
- 证据明确不通过 gate 时使用 `fail`。

## 6. 阻断与传播规则

### 6.1 Dimension → mapped gates

当任一 mapped dimension 为 `unknown` 或 `conflicting` 时，对应 gate 禁止使用：

```text
pass
pass_with_scope
mixed_positive
research_ready
research_ready_not_decision_ready
```

该 gate 仍可使用：

```text
mixed
provisional
range_only
inconclusive
fail
blocked
```

若适用，`circle_of_competence` 还可使用 `outside_circle`。

### 6.2 Earlier gate → later gates

若任一 earlier gate 为：

```text
fail
outside_circle
blocked
```

后续 gate 不得使用正面或 readiness result。后续研究仍可保留：

```text
mixed
provisional
range_only
inconclusive
fail
blocked
```

后面的估值或漂亮叙事不能修复前面缺失的主源、身份或能力圈。

### 6.3 Final decision 的全局阻断

`decision_and_disconfirming_evidence` 受到全部 25 个 dimension 的全局约束：

- 任一 dimension 仍为 `unknown` 或 `conflicting`，final gate 不能使用任何正面结果；
- 因此 `research_ready` 和 `research_ready_not_decision_ready` 均不可用；
- 即使 unresolved dimension 主要映射到 earlier gate，也不能绕过；
- 报告可以继续是有价值的 provisional 研究，但必须显式列 blocking gaps 和下一验证事件。

### 6.4 `production_reviewed` 不是 gate result

`production_reviewed` 是 review/publication state，只能在具名人工复核后使用。至少要求：

- 主源身份和期间已解决；
- 25 个 dimensions 按序存在，包含 applicability、两个 exact indicators、company evidence、counter-evidence 和 gaps；
- material calculations 可复算；
- 九道 gate 都有解释；
- owner earnings 与 valuation 保留不确定性；
- moat 包含 counter-evidence；
- 独立 red-team 和 invalidation tests 存在；
- unresolved critical gaps 明示；
- human review state 已存储；
- 不含 buy/sell、position-size、guaranteed-return 或 creator-endorsement 语言。

一个 validator 通过、pipeline 完成的 machine artifact 仍应保持：

```text
needs_human_review
```

直到具名人工 review 被记录。新财报、重大股本/融资、审计、监管或业务事实使研究过期时，状态应转为：

```text
stale
```

## 7. Existing review / failure states

以下是 schema 推荐的现有状态，不应与 gate result 混用：

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

主检查表还定义了研究结论的否决顺序：

```text
identity_blocked
evidence_insufficient
outside_circle
survival_or_governance_fail
economics_unattractive
quality_research_candidate
valuation_inconclusive
research_ready_not_decision_ready
value_investing_candidate_needs_human_review
```

这些 conclusion/review states 也不是九道 gate 的 result vocabulary。任何状态都必须附最强支持证据、最强反方证据、blocking gaps、失效条件、下一份应读文件和下一次复核日期。

## 8. 可读报告如何映射到 contract

### 8.1 双入口只是展示层

可把 HTML 拆成：

1. `company dossier`：25 维度、三表、owner earnings、资本配置、护城河、估值；
2. `event monitor`：近期财报、行业/指数/监管/产品事件、市场结构、下一验证点。

但两者必须引用同一份 checksummed source catalog、同一套 facts 和同一个 v2 combined artifact。事件入口不能产生一套更乐观的平行事实。

### 8.2 Evidence drawer 只是 fact 的读者界面

每个重要数字的 drawer 建议显示：

```text
source_id
content_sha256
page
source_text
period
unit
currency
scope
audit_status
formula
```

drawer 改善“两次点击回原文”的体验，但不能替代 source manifest/fact pack，也不能让 live citation 自动成为 production fact。

### 8.3 图表不能替代表格

- 图表用于识别形状，原表/CSV 用于复算；
- 推导值、预告、未经审计和正式实际值必须视觉区分；
- Q1、H1、FY 不在同一绝对值趋势线上混画；
- 普通柱图从零开始；
- 每张表和图保留期间、单位、币种、scope、来源和更新时间。

## 9. 独立“市场定价状态”层

“市场定价状态”是可读报告的旁证层，不是第 26 个 dimension，不进入 50 个 indicator family，也不新增 gate、gate result 或 publication state。它只消费既有：

```text
historical_valuation
price_move_attribution
valuation
per_share_economics
capital_allocation
disconfirming_evidence
```

其结论仍受 `intrinsic_value_and_margin_of_safety` 和 `decision_and_disconfirming_evidence` 两道 gate 约束。

| 市场定价视角 | 最低做法 | 主要 contract 锚点 | 必须避免 |
| --- | --- | --- | --- |
| 历史无前视偏差估值分位 | 在每个历史价格日，只使用当时已公开的 FY/TTM/forward/normalized 分母；记录发布时间、可用日、股本、币种和公司行动，给出同口径历史分位 | `historical_valuation`; dimension `valuation`; indicator `currency_consistent_value_range_assumptions_and_dates` | 用今天才知道的 EPS、后来重述或未来指引回填过去 PE；把不同分母混成一条分位 |
| 当前价格与内在价值 gap | 同币种比较当前 price anchor 与 bear/base/upside 或 low/base/high 价值区间；展示区间 gap、假设和 sensitivity，而非单点目标价 | `valuation`; `per_share_economics`; gate `intrinsic_value_and_margin_of_safety` | 只挑 base/upside；价值区间不可辩护时仍输出 gap；把 gap 写成买入空间 |
| 同行估值溢价/折价 | 统一会计准则、周期位置、业务范围、增长、ROIC、杠杆、NCI、稀释和价格日期，再比较 PE/PB/EV/owner earnings 等适用指标 | `industry_chain_position`; `returns_on_capital`; `per_share_economics`; `valuation` | 只按行业标签选同行；把业务/周期/资本结构差异误写成错误定价 |
| 3—5 年股东回报分解 | 用复权价格和现金分配先算总股东回报，再把每股 owner earnings/EPS 增长、分红/回购净影响、估值倍数变化、FX 和稀释列成可复算 bridge | `capital_allocation`; `per_share_economics`; `historical_valuation` | 把公司收入增长当股东回报；忽略增发、可转债、库存股和汇率；把历史分解外推成保证回报 |
| 长周期回撤、趋势、波动与流动性 | 使用可复核复权序列，记录 3—5 年及更长周期最大回撤、滚动波动、相对基准、成交/价差和重大事件；与 `price_move_attribution` 对照 | `price_move_attribution`; `disconfirming_evidence`; gate `decision_and_disconfirming_evidence` | 用上涨证明护城河、用下跌证明基本面恶化；用技术趋势替代公司事实；忽略停牌、除权和低流动性 |

### 9.1 无前视偏差的最低检查

每个历史估值点至少绑定：

```text
price
price_as_of
price_source_ref
earnings_or_owner_earnings_value
earnings_period
earnings_type
earnings_publication_date
first_market_available_date
share_count_and_dilution
currency_and_fx_as_of
corporate_action_adjustment
formula
```

历史日只能使用 `first_market_available_date <= price_as_of` 的信息。若当时分母不可得，记录 unavailable，不得用后来披露补数。历史 forward 估值还必须保存当时可获得的 consensus snapshot；当前一致预期不能倒灌。

### 9.2 定价状态不能反向污染基本面

允许的表述：

- “当前倍数处于同口径历史区间的某个位置，但该位置只描述市场定价。”
- “价格与可辩护价值区间存在 gap；区间宽度反映 owner-earnings 和终值不确定性。”
- “回撤与成交结构提示市场压力，需要回到监管、融资、盈利或股本主源验证。”

禁止的推断：

```text
股价强 -> 护城河已证实
股价弱 -> 公司一定爆雷
低历史分位 -> 一定低估
同行溢价 -> 一定质量更高
过去 5 年回报 -> 未来 5 年预期回报
```

若市场定价旁证与基本面结论冲突，应进入 `price_move_attribution`、`counter_evidence` 或 `source_gaps`，不能修改主源 facts 来解释价格。

## 10. 最小机读示例

### 10.1 Dimension

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

### 10.2 Gate

```json
{
  "gate": "durable_moat",
  "result": "provisional",
  "reason": "The mechanism is plausible, but required customer-retention evidence is not disclosed.",
  "source_refs": ["annual-report-2025"],
  "blocking_gaps": ["No independent retention evidence."],
  "next_tests": ["Read the next annual filing and customer-side evidence."]
}
```

## 11. 执行与 QA

验证 canonical crosswalk：

```bash
python \
  skills/research-buffett-munger-company/scripts/validate_methodology_implementation_crosswalk.py \
  skills/research-buffett-munger-company/references/methodology-implementation-crosswalk.json
```

验证单公司 combined artifact：

```bash
python \
  skills/research-buffett-munger-company/scripts/validate_company_research.py \
  <artifact.json>
```

最终检查重点：

- 25 个 dimension ID 顺序完全一致；
- 每行两个 exact indicator IDs 顺序完全一致；
- gate IDs 和 dimension-to-gate map 与 executable contract 一致；
- 没有自造 dimension/gate/indicator status；
- 没有把 methodology source 当公司事实；
- 没有因报告展示完善而跳过 red-team、validator 或 human review；
- `production_reviewed` 只在具名人工复核后出现。
