# 上市公司基本面 × 行业 × 事件研究方法

版本：2.6（2026-07-28）

适用对象：A 股、港股、美股及跨市场上市公司

研究边界：公开资料、研究辅助、非投资建议

## 1. 这套方法解决什么问题

一份个股报告不能只回答“公司好不好”，而应同时回答：

1. 证券身份和交易制度是否确认；
2. 公司真正靠什么收入和利润赚钱；
3. 增长是流量、价格、销量、产能、付费率还是一次性项目驱动；
4. 报表利润有多少能转成股东可支配现金；
5. 行业第一性原理是否仍成立；
6. 短期事件为什么会影响小盘股弹性；
7. 当前估值使用了哪一种盈利分母；
8. 下一份数据怎样升级或推翻当前结论。

最终输出必须把“事实”“管理层主张”“研究推断”“证据缺口”分开，不从股价变化倒推事实，也不输出买卖或仓位指令。

## 2. V2 研究产品：先分入口，再合并证据

V2 不把长期价值判断、短期事件波动和产品热度混成一个结论。每家公司共享同一份事实层，但提供两个独立阅读入口：

| 入口 | 解决的问题 | 默认时间 | 允许的结论 | 禁止的措辞 |
| --- | --- | --- | --- | --- |
| 长期公司底稿 `long_term_dossier` | 公司怎样赚钱、护城河是否存在、资本回报和每股价值能否持续 | 3—5 年历史、3—10 年判断 | 证据状态、质量、估值不确定性、长期证伪条件 | 买入、卖出、仓位、入场、错过上涨 |
| 短期事件监控 `near_term_monitor` | 下一份财报、政策、产品、指数或行业事件会验证什么 | 已发生事件及未来 4—12 周 | 情景、领先指标、验证点、市场结构风险 | 交易指令、目标仓位、确定性涨跌预测 |

两者不能各自维护一套互相冲突的财务事实。推荐的数据流是：

```text
primary sources
  -> source ledger
  -> fact-level evidence anchors
  -> seed.stock-fundamentals-valuation.v2 combined artifact
  -> long-term dossier + near-term monitor
  -> HTML / CSV / change log
```

### 2.1 状态机

研究状态不是装饰标签，而是 gate 的结果：

| 状态 | 含义 | 能否公开 | 能否标为已完成人工复核 |
| --- | --- | --- | --- |
| `pending_sources` / `source_partial` | 主源尚未到齐或证据包不完整 | 仅可展示来源缺口 | 否 |
| `research_in_progress` | 正在采集、建模或核对 | 否 | 否 |
| `research_ready_not_decision_ready` | 九道 gate 已形成，但价值区间或关键证据仍不够窄 | 可以，必须显著披露缺口 | 否 |
| `needs_red_team` | 主研究完成，独立反方尚未完成 | 可以作为待审快照 | 否 |
| `needs_human_review` | deterministic validator 已完成，但尚无具名人工复核 | 可以作为待审样例 | 否 |
| `production_reviewed` | validator、独立 red-team 与具名 reviewer 闭环完成 | 可以 | 是 |
| `blocked` / `failed` | 身份、证据、治理、生存或其他硬条件阻断 | 可以公开阻断结论 | 是，但不代表通过投资质量判断 |
| `stale` | 已越过复核日或出现重大新披露 | 只可作为历史快照 | 否 |

任何 HTML 都必须展示 combined artifact 的 `status`、`as_of`、`stale_after`、`critical_gaps`、`validator_status`、`human_review_status`。页脚的“非投资建议”不能抵消正文中的交易指令化语言。

### 2.2 关键事实的最小证据合同

source-level 链接只能说明“文件存在”；决策级底稿必须把关键数字和结论绑定到 fact-level evidence。每个关键事实至少记录：

```yaml
evidence_id:
claim_id:
source_id:
document_sha256:
page:
section_or_table:
text_snapshot_sha256:
page_text_sha256:
page_line_start:
page_line_end:
source_text:
period:
unit:
currency:
scope:
audit_status:
formula:
accessed_at:
limitations:
```

规则：

- `page` 使用 PDF 页码；网页或无页码公告写 `null` 并保留稳定锚点或标题；
- PDF 再写 `section_or_table`；若已生成 checksum-bound 抽取文本，则同时保存整份文本和页内文本
  SHA-256，以及页内 `page_line_start/page_line_end`；
- 抽取文本行号只对对应哈希有效，不是 PDF 视觉行号；动态网页没有冻结快照时不用临时 DOM 行号，
  改用稳定 URL、标题、HTML anchor/表格名和访问日期；
- CSV/JSON 使用稳定记录键、列名或 JSON Pointer；代码证据绑定 commit SHA 和行号；
- `source_text` 只保存支持该事实的最短必要原文，避免复制整页；
- `scope` 明确集团/母公司/分部、持续经营/全部业务、归母/含少数股东；
- `audit_status` 区分 audited、reviewed、unaudited、voluntary_update、derived、third_party_estimate；
- 推导数字必须在 `formula` 中列出输入 evidence id，不能只写自然语言；
- 公开报告任取 10 个关键数字，应在两次点击内看到页码、原文、口径和公式。

### 2.3 三个必须可复算的桥

估值前必须公开三张桥；缺任一张时，DCF 只能是探索性情景。

**Owner earnings bridge**

```text
持续经营归母
- 非经营/公允价值/处置收益
+ 可辩护的一次性损失
- 持续股权激励等真实经济成本
+ 归属普通股股东的可加回非现金费用
- 维护性资本开支 low/base/high
- 正常营运资本增量 low/base/high
= owner earnings low/base/high
```

每行记录金额、正负号、税前/税后、期间、来源、理由、争议和三情景值。增长性资本开支和维护性资本开支无法准确拆分时，应给区间而不是单点。

**Net cash bridge**

```text
现金及现金等价物
+ 可自由变现的短期投资
- 受限现金
- 有息借款
- 可转债/优先股/租赁等类债务
- 已承诺但未支付的资本用途
= valuation net cash
```

必须避免把可转债募集现金计入净现金、却不扣除对应债务。

**Fully diluted share bridge**

```text
期末已发行普通股
- 库存股/已注销未生效股份
+ 在价内期权、RSU、股份奖励
+ 可转债/可交换债情景股份
+ 已公告配售/供股
= fully diluted shares
```

每个估值情景都必须与资本结构一致：未转换情景保留债务并使用当前股数；全转换情景移除相应债务并加入转换股份。若情景价格高于转股价而仍用未摊薄股数，validator 应判失败。

### 2.3.1 流通盘稀缺度与新增供给：不能用总市值代替

总市值回答公司整体权益规模，不能回答某一交易线实际有多少股票可交易。小盘与跨市场公司必须
另做“法定股本 → 可观测流通代理 → 活跃成交容量 → 未来新增供给”四层桥：

```text
issued shares
- treasury shares
= non-treasury outstanding shares

non-treasury outstanding shares
- 已披露控制人/董事实际持股
- 已披露战略持股
- 明确仍在锁定或限售的股份
= observable tradable-float proxy
```

四个口径不能混写：

| 口径 | 含义 | 使用纪律 |
| --- | --- | --- |
| `non_treasury_outstanding` | 已发行减库存股，是每股分母的常见起点 | 不是交易所官方 public float，不能标作“流通股” |
| `regulatory_public_float` | 交易所规则下公众持股量/比例 | 只有交易所或发行人明确披露并可复核时才填写；否则 `unknown` |
| `observable_tradable_float_proxy` | 用公开控制/战略/锁定持股从非库存股本扣减的研究代理 | 是上限或近似值，不等于每天真实卖盘；逐项显示扣减和遗漏 |
| `active_supply` | 某窗口内真正参与交易的股份 | 从成交、换手、借券和持有人行为推断，不能从静态股东表直接得出 |

固定计算：

```text
float_adjusted_market_cap_proxy
= dated_price × observable_tradable_float_proxy

float_turnover_per_day
= 20d_ADTV_shares / observable_tradable_float_proxy

float_days_to_trade
= observable_tradable_float_proxy / 20d_ADTV_shares

unlock_shock
= newly_unlocked_shares / pre_event_observable_tradable_float_proxy

new_supply_days
= newly_unlocked_or_newly_listed_shares / 20d_ADTV_shares
```

`float_days_to_trade` 只是容量代理，不是保证退出天数；真实冲击还取决于成交额、价差、集中度、
持有人意愿和市场状态。低流通盘也不是护城河：它会同时放大上涨、下跌、跳空、逼空和融资折价。

供给事件必须区分三个状态：

1. `legal_unlock`：法律/合同上可以出售；
2. `registration_or_listing`：股份已经登记或上市；
3. `actual_disposal`：持有人真的减持或股份进入成交。

解禁只代表出售权限，不等于已经卖出。供给日历至少覆盖 IPO 前/基石/控股股东锁定到期、
A 股限售解禁、配售/供股上市、股份奖励归属、期权行权、可转债转换、库存股再发行或注销，
并同时列出事件日期、交易线、股份数、占解禁前流通代理比例和相当于多少个 20 日平均成交日。
指数或港股通调整是需求事件，不应伪装成流通股变化。

A/H、ADR 和多股类必须逐交易线计算。A 股新增或解禁不会直接增加 H 股可交易股数；可以记录
集团总股本稀释和跨市场情绪传导，但不得用 H 股价格乘全公司 A+H 股数来表示 H 股流通市值。

HKEX 公众持股规则、MSCI/S&P 的 free-float 调整方法和发行人披露优先于行情商的
`floatShares`。GitHub 项目只可作为数据工程实现参考，不能作为 free float 的方法权威。

### 2.3.2 客户、供应商与上下游：关系名称和占比必须同表

公司“卖给谁”和“向谁采购”不是背景材料，而是收入质量、议价权、现金转换和护城河的共同
分母。公开报告必须单列关系图和集中度账本，不能只把它埋在 25 维度状态卡中。

至少区分：

```text
关键资源 / 设备 / 模型 / 平台
  -> 供应商与渠道
  -> 公司核心工序
  -> 直接客户 / 合同相对方
  -> 付款方 / 终端用户
  -> 平台、监管者、替代品和客户自制
```

每条关系至少保存：

| 字段 | 要求 |
| --- | --- |
| 对手方 | 法定名称/常用名/ticker；未披露时保持“匿名客户 A”或 `not_disclosed` |
| 角色 | 直接客户、渠道、终端用户、付款方、供应商、平台/门卫、合作方或竞争者，不能混写 |
| 占比 | 最大/前五客户收入占比、应收占比；最大/前五供应商采购占比、成本占比 |
| 分母 | 集团收入、分部收入、原材料采购、总采购或应收；不同分母不得横比 |
| 期间与趋势 | 至少三年；公司更名、并购和匿名编号变化不得假装为同一对象 |
| 关联与条款 | 关联方、账期、预付、独家/单一来源、最低采购、取消权、价格传导 |
| 双向重要性 | 该客户占本公司多少，以及本公司占该客户采购多少；后一项未知时明示未知 |
| 证据 | 公司年报、对手方披露、合同/认证、监管或采购主源；合作新闻不等于收入 |

固定计算：

```text
customer_CR1 = 最大客户收入 / 同口径收入
customer_CR5 = 前五客户收入 / 同口径收入
supplier_CR1 = 最大供应商采购 / 同口径采购
supplier_CR5 = 前五供应商采购 / 同口径采购
receivable_CR1/CR5 = 最大/前五客户应收 / 同口径应收
HHI = Σ(单一对手方占比²)  # 仅在逐家占比完整时计算
```

集中度低不自动代表安全：关键设备、EDA、云、模型 API、应用商店或清算基础设施可能采购金额
不大，却具有很高的替代时间和停供影响。反过来，大客户占比高也不自动等于差生意，必须结合
续约、毛利、回款、合同期限、双供、客户自制和议价变化判断。

具名纪律：

- 年报只写“最大客户/供应商”而未命名时，不从传闻或行业常识猜名字；
- YouTube、Apple、Google、交易所等平台可能是渠道、门卫、合作方、供应商或竞争者，不因
  技术连接就自动写成客户；
- 合作公告必须标记合同阶段、已实现收入和占比；占比未披露就是 `unknown`；
- 客户与供应商必须用对手方主源交叉验证；没有双向证据时标 `company_disclosed_only`。

### 2.3.2 增长变量：研究“变好”，而不是追逐最高增速

本节吸收用户转述的 UP「大白不bai说」观点。原始视频 URL、逐字稿和时间戳尚未取得，因此
归因状态为 `creator_methodology_candidate_needs_source_verification`；以下公式、gate 和
状态是本项目的研究工程实现，不是投资建议。

```text
P1 / P0 = (EPS1 / EPS0) × (PE1 / PE0)
growth_rate_t = metric_t / comparable_metric_t-1 - 1
growth_acceleration_t = growth_rate_t - growth_rate_t-1
expectation_gap_t = actual_or_current_guidance_t - prior_market_implied_path_t
```

真正要找的不是“增速最高”，而是核心变量由差变好、改善扩散到利润/现金/每股价值、实际路径
好于此前已计入路径，而且当前价格没有要求更强但缺证的增长。至少需要两个连续、同口径的增长率；
只有一个同比百分比时必须写 `insufficient_evidence`。

| 阶段 | ID | 含义 |
| --- | --- | --- |
| 证据不足 | `I0_insufficient` | 无两个可比期间或关键口径冲突 |
| 恶化 | `I1_deteriorating` | 核心指标下降且恶化扩大 |
| 恶化收窄 | `I2_deterioration_slowing` | 仍为负增长，但降幅收窄 |
| 早期拐点 | `I3_early_inflection` | 领先 KPI/收入改善，利润或现金未确认 |
| 确认加速 | `I4_confirmed_acceleration` | 至少两类经营/财务指标连续改善且质量通过 |
| 高增长延续 | `I5_high_growth` | 增长仍高但没有明确加速/减速 |
| 高位减速 | `I6_high_level_deceleration` | 仍增长，但多个核心指标增速回落 |

升级为 `confirmed_inflection_for_research` 前，必须依次通过：

1. `direction`：两个以上同口径期间显示加速度为正；
2. `breadth`：领先 KPI/收入、利润/EPS、现金/营运资本至少两层同向；
3. `quality`：排除低基数、并购、汇率、一次性、公允价值、减值转回、资本化和回购抬 EPS；
4. `expectations_and_valuation`：改善高于此前路径，反向估值不要求更强的未证实增长；
5. `next_verification`：有具体官方披露窗口、升级阈值和失效条件。

前四项任一未通过，只能写 `watch_early_signal`、`high_growth_not_inflecting`、
`decelerating_or_deteriorating` 或 `insufficient_evidence`。阶段、公司质量和估值状态必须
分栏；增速从高到低不是机械卖出规则，从低到高也不是机械买入规则。

全年同比与单季同比只能用于方向筛查，不能替代连续同季度或滚动口径。凡使用“全年 → Q1/Q4”
判断阶段，阶段标签必须标为 `provisional`，并由下一期同口径数据确认。

### 2.3.3 同行比较：先证明可比，再计算 PE

同行比较不是把同一行业标签下的股票排成 PE 表。研究对象、同行和行业映射必须先分成：

- `target`：目标证券；
- `same_issuer_other_share_class`：同一发行人的 A/H/ADR 或其他股类，只用于价格结构，不进入同行中位数；
- `direct_economic_peer`：主要产品、客户、利润池和资本需求相近的直接同行；
- `adjacent_operating_peer`：部分工作流或收入模式相邻，只用于经营旁证；
- `thematic_peer`：共享主题或需求驱动，但经济性不同；
- `platform_or_substitute`：客户、渠道、模型厂商或平台内部替代；
- `excluded`：分母无意义、结构差异过大或证据不足，必须保留排除理由。

每家公司必须逐项通过资格矩阵：

| 资格项 | 至少回答什么 | 不通过时怎样处理 |
| --- | --- | --- |
| 产品与利润池 | 产品、付款方、单位经济与价值链位置是否相近 | 降级为 adjacent/thematic |
| 地区与监管 | 地域、牌照、补贴、出口管制和税制是否可比 | 披露差异，必要时排除 |
| 会计与分母 | GAAP/IFRS、持续经营/集团、FY/TTM/forward、SBC 和一次性是否统一 | 禁止计算 relative premium |
| 周期与增长 | 处于扩产、复苏、成熟、衰退或高增长哪一段 | 倍数必须与增长/利润率并列 |
| 资本结构 | 净现金、租赁、NCI、可转债、稀释和同股不同权是否统一 | 优先 EV 或完成股本桥 |
| 资本强度与回报 | 维护投入、资本化研发、ROIC/ROE 和现金转换是否接近 | 换用行业分支指标 |
| 日期、币种与证券 | 价格日、EPS 可用日、汇率、股类和上市状态是否一致 | 只能描述散点，不能精算折价 |

公开同行表的最小字段为：公司/ticker、比较角色、`eligible/excluded`、价格及日期、币种、
盈利分母及期间、PE/PB/EV 指标、增长/利润率/ROIC 或 ROE、限制、原始来源 URL、冻结哈希。
行情商动态 PE 必须标记 `provider_dynamic_pe`；若 EPS 期间未知，不得改名为 reported TTM PE。
负盈利写 `N/M`，不能把负 PE 纳入正盈利中位数。

行业分支不能机械套同一个倍数：

- 一般盈利公司：reported/TTM/normalized PE、P/owner earnings、EV/经营收益；
- 金融公司：P/B—ROE/ROTE、正常化 PE、监管资本和利润波动；
- 晶圆代工/重资产：PE、P/B、EV/EBITDA 只作交叉检查，同时展示资本开支、利用率和增量 ROIC；
- 未稳定盈利的 SaaS/AI 应用：EV/收入、毛利、留存、SBC 后 FCF；不制造“调整后正 PE”；
- 周期资源：正常化利润、EV/产能、资产净值和周期位置。

只有至少 3 家 `eligible` 同行、相同价格日和相同分母时，才可展示中位数/四分位和：

```text
relative_premium = target_multiple / eligible_peer_median - 1
```

少于 3 家时状态写 `bounded_no_median`；没有合格同行时写 `not_determinable`。若只取得同一个
行情商字段，可以展示该字段的横截面中位数，但必须明确它不能与自行重算的目标公司 reported
TTM 机械除算。同行中位数永远不是内在价值，也不能因为目标公司 PE 更低就推导“低估”。

当前四份公开报告的实现边界：

| 公司 | 合格/有限同行 | 被排除但保留的相邻样本 | 可支持结论 |
| --- | --- | --- | --- |
| 美图 | Adobe（仅 1 家有限可比） | Figma、万兴科技、金山办公 | 无同行中位数；增长、SBC、现金质量必须与 PE 并列 |
| 南华期货 | 永安、瑞达、弘业期货（同一 provider 字段） | 南华 A 股为同发行人股类 | 可展示 provider 横截面，不与目标 reported TTM 精算折价 |
| 中芯国际 | GFS、UMC（仅 2 家有限可比） | TSMC 为行业领导者映射 | 无中位数；目标交易后 EPS 缺失，机械 PE 只作反向压力测试 |
| 阜博集团 | 无 ≥3 家纯同行 | Veritone、Getty、Shutterstock | “无可比中位数”本身是结论，优先看现金与资本结构 |

### 2.4 市场定价状态：把“高估/低估”拆成可复核坐标

公司质量和市场定价是两个问题。V2 可以使用带一点技术分析味道的长周期市场状态，但只能回答
“当前价格相对什么偏高或偏低”，不能单独产生交易动作。

| 坐标 | 推荐指标 | 能回答什么 | 主要护栏 |
| --- | --- | --- | --- |
| 公司自身历史 | 无前视偏差的滚动 FY/TTM/normalized PE、PB、EV/销售、EV/owner earnings 分位 | 当前倍数相对自身历史处于何处 | 历史日期只能使用当时已披露 EPS；业务结构变化要分 epoch |
| 内在价值区间 | 当前价相对保守/基准/上行情景的折价或溢价 | 当前价落在模型区间的哪里 | 三情景必须使用一致净现金和 fully diluted 股数 |
| 横向相对估值 | 同行业同口径 PE/PB/EV、增长、ROIC、毛利、SBC 后 FCF | 溢价是否有质量或增长支撑 | 同行必须同会计口径、周期和资本结构 |
| 资金机会成本 | owner-earnings yield、FCF yield、股息率与同币种国债/信用利差 | 估值回报是否补偿不确定性 | 不能把股票收益率当成无风险收益 |
| 长周期价格状态 | 1/3/5 年回撤、200 日/40 周趋势、实现波动率、换手与成交深度 | 市场是否处于拥挤、恐慌或趋势反转阶段 | 只作市场状态旁证，不证明价值 |

固定展示三个差值：

```text
historical_percentile = 当前同口径倍数在无前视偏差历史样本中的分位
intrinsic_value_gap = 当前价 / 情景内在价值 - 1
relative_premium = 当前倍数 / 同口径同行中位数 - 1
```

以及 3—5 年情景回报分解：

```text
terminal_price = terminal_EPS_or_owner_earnings_per_share × terminal_multiple
scenario_annualized_return =
  ((terminal_price + cumulative_cash_distributions) / current_price)^(1 / years) - 1

近似解释：
每股盈利增长 + 倍数变化 + 现金分配 - 净稀释
```

这不是目标价或保证收益。每个情景必须公开终值倍数、盈利路径、分红、回购、发行、可转债和
期限；负值照常保留。

估值状态建议使用条件化标签：

- `low_vs_range`：低于保守内在价值下界，但仍展示模型不确定性；
- `within_range`：落在可辩护价值区间内；
- `high_vs_range`：高于上行情景上界；
- `historically_low/high`：只描述同口径历史分位；
- `relative_discount/premium`：只描述相对同行；
- `not_determinable`：盈利为负、结构变化或证据不足。

只有多个坐标在可比口径下同向，才可写“相对当前证据偏低/偏高”；不得只因跌破均线、回撤大、
PE 低或股价低于历史高点就写“低估”。金融公司优先看 P/B—ROE/ROTE，周期公司优先看
normalized earnings、EV/产能或资产净值，SaaS/AI 应用在盈利不稳定时补 EV/收入、毛利、
SBC 后 FCF 与留存，不能机械套 PE。

### 2.5 25 维度、50 indicator family 与九道 gate

完整定义放在 [`templates/research-dimensions-and-gates.md`](templates/research-dimensions-and-gates.md)。基本原则：

- 25 个研究维度是覆盖清单，不是机械总分；
- 每个维度至少两个 indicator family，总计至少 50 个；
- 维度状态只能是 `applicable`、`not_applicable`、`unknown` 或 `conflicting`；
- indicator 状态只能是 `observed`、`not_disclosed`、`not_applicable` 或 `conflicting`；
- 九道 gate 才决定发布状态；维度多不代表证据通过；
- `not_applicable` 必须给出行业和会计理由，不能用来绕过阻断项。

公开 HTML 必须在首屏附近显示读者状态图例，不能只在 schema 中定义术语：

| 层级 | 状态 | 读者含义 |
| --- | --- | --- |
| dimension | `applicable` | 维度适用且已有足够证据形成摘要；不表示结论正面或 gate 通过 |
| dimension | `unknown` / `conflicting` / `not_applicable` | 分别表示证据不足、证据冲突、结构性不适用；不得用后两者掩盖缺证 |
| indicator | `observed` | 已观察到可引用证据；不表示数值好或趋势正面 |
| indicator | `not_disclosed` / `conflicting` / `not_applicable` | 分别表示未披露或不可重建、指标证据冲突、指标结构性不适用 |
| gate | `pass` / `pass_with_scope` | 充分通过，或只在明确范围内通过 |
| gate | `mixed_positive` / `mixed` | 正反证据并存，不能简写成 pass |
| gate | `provisional` | 暂定结论可保留，但关键验证尚未完成 |
| gate | `range_only` / `inconclusive` | 只能给可辩护区间，或当前无法得出方向结论 |
| gate | `research_ready` / `research_ready_not_decision_ready` | 只用于最后一道 gate，表示研究流程完成或可读但尚非决策级 |
| gate | `fail` / `outside_circle` / `blocked` | 已被证据击穿、超出能力圈或前置条件未满足 |
| publication | `source_partial` / `research_in_progress` / `needs_human_review` / `production_reviewed` | 描述整份报告的来源、制作和审核成熟度，不描述公司质量或股价方向 |

九道 gate 的 ID、顺序和允许结果以
[`company-research-schema.md`](../skills/research-buffett-munger-company/references/company-research-schema.md)
及 `src/seed/company_research_validation.py` 为唯一可执行规范。报告模板不得另造
`pass/conditional/fail/NA` 等平行词表。

### 2.6 Red-team、validator 和人工复核必须分工

| 角色 | 最低职责 | 不得替代 |
| --- | --- | --- |
| 研究作者 | 构建事实、模型、结论与缺口 | 不能自称独立 red-team |
| Red-team | 写最强反方、检查反证、模型脆弱点和措辞越界 | 不能只重复风险章节 |
| Validator | 确定性检查 schema、公式、引用、状态、过期、资本结构一致性 | 不能判断商业模式好坏 |
| Human reviewer | 具名确认关键数字抽查、模型合理性、发布边界 | 不能被自动评分代替 |

`production_reviewed` 必须同时满足：

1. combined artifact 通过 schema；
2. 25 个维度、50 个 indicator family 和九道 gate 顺序完整，结果满足现有传播规则；
3. validator 无 error；
4. 独立 red-team 有作者、时间、反方结论和 unresolved issues；
5. human review 有 reviewer、reviewed_at、decision 与 critical gaps；
6. HTML 与 combined artifact 使用同一版本和 checksum。

`production_reviewed` 表示研究过程经过人工复核，不表示九道 gate 全为正面结果，更不表示公司
适合投资。`fail`、`outside_circle` 或 `blocked` 也可以是经过正式复核的研究结论；它们会按
可执行 contract 阻止后续 gate 被写成正面或 readiness 状态。

### 2.7 更新、过期与不可静默覆盖

每份报告必须记录：

```yaml
as_of:
next_expected_event:
stale_after:
supersedes:
change_log:
  - changed_at:
    trigger:
    prior_conclusion:
    new_evidence:
    new_conclusion:
```

- `stale_after` 默认不晚于下一次正式财报或已确认重大事件；
- 新财报发布后，旧 HTML 自动标 `stale`，但保留历史结论；
- 事实修正、模型更新和观点变化分开记录；
- 不得用新数据静默改写事前判断或事件预期。

### 2.8 统一母版也是发布 Gate

研究完整和读者可用是两道不同的门。结构化 artifact 通过 25 维度、50 indicator
family 与九道 gate，只证明研究合同可执行；如果 HTML 各自发明主题、阅读顺序或状态词表，
读者仍无法跨公司比较，因此不能发布。

统一母版固定三层：

| 层 | 固定内容 | 允许变化 |
| --- | --- | --- |
| Publication shell | 主题、首屏、发布状态、图例、导航、长期/事件双入口、方法、时间轴、证据入口 | 公司名、结论和更新日期 |
| Research spine | 业务/利润来源、五年财务、最新季度、现金/资本桥、估值、行业事件、25×50×9、失效条件 | 公司事实、状态与证据 |
| Industry slots | 行业 KPI、有效的现金桥、估值分支和监管/技术风险 | 金融、晶圆代工、软件/SaaS 等分支内容 |

行业差异不能成为独立主题、平行状态体系或删减研究主干的理由。金融机构可以用监管资本、
母公司现金和可分配利润替代工业 `CFO-capex`；晶圆厂必须补产能、利用率、折旧和维护/增长
资本开支；软件与 AI 应用必须补留存、单位经济、SBC/R&D、平台依赖和替代风险。它们仍使用
同一发布壳。

发布前必须同时通过：

1. combined artifact 与 publication validator；
2. `company-research-publication-v1` template-parity validator；
3. 桌面与 390px 渲染检查；
4. 导航锚点、表格局部滚动、图表可读性和证据抽屉人工抽查。

改版时保留所有精确表格、图表、证据 ID、来源和限制；只移动到统一主干，不以视觉简化为由
删除审计信息。完整契约见
[`public-report-template-contract.md`](../skills/research-buffett-munger-company/references/public-report-template-contract.md)。

## 3. 固定的九步研究链

### 第一步：固定证券身份

先记录：

- 法定公司名、常用名和是否存在同名公司；
- ticker、交易所、证券类型和交易币种；
- A/H/ADR、多股类、母子公司和实际控制关系；
- 财年结日、报告币种和股本口径；
- 港股通、沪股通、深股通、指数和卖空资格；
- 价格锚点及其日期。

证券身份未确认前，不进入估值或事件分析。互联互通资格必须使用交易所当前官方名单；预测、媒体和历史名单不能写成当前事实。

### 第二步：建立披露日历和数据粒度

把披露分为：

| 类型 | 证据强度 | 能回答什么 | 不能回答什么 |
| --- | --- | --- | --- |
| 经审计年报 | 高 | 全年三表、分部、股本、会计政策 | 最新季度变化 |
| 中报/正式季报 | 高 | 半年或季度经营变化 | 未披露月份 |
| 自愿经营更新 | 中高 | 公司主动披露的有限 KPI | 完整利润、现金流和审计结论 |
| 盈利预告/表现更新 | 中高 | 利润区间或重大变化 | 完整分部和现金质量 |
| 管理层访谈 | 中 | 战略、产品和未来判断 | 审计事实 |
| 第三方流量/排名 | 中低 | 领先热度与方向 | 公司收入、留存和利润 |

规则：

- 没有独立季度财报，就不制造季度利润；
- 可以用“全年减 H1”推导 H2，但必须标记 `derived`；
- 可以在口径一致时用“H1 减 Q1”反推 Q2，但需等 H1 正式披露；
- 同比、环比、半年环比和年化数据必须分开。

### 第三步：拆解业务、收入与利润来源

先回答“客户为什么付钱”，再看总收入。

至少保留最近 3—5 年：

- 集团收入、毛利、经营利润、归母利润；
- 分部收入、分部利润和利润率；
- 经营现金流、资本开支、自由现金流；
- 净现金/净债务、少数股东损益；
- 已终止经营、收购、处置和重分类。

建议用以下桥接：

```text
产品/分部数量 × 单价/ARPU/ASP
  -> 分部收入
  -> 毛利与经营费用
  -> 经营利润
  -> 利息、税、联营和少数股东
  -> 归母利润
  -> 经营现金流与资本开支
  -> 每股 owner earnings
```

### 第四步：重建盈利质量

不要只引用公司调整后利润。至少并列：

| 盈利口径 | 用途 | 常见问题 |
| --- | --- | --- |
| IFRS/GAAP 法定归母 | 与审计报表一致 | 可能含处置、公允价值、补助和减值 |
| 持续经营归母 | 排除退出业务 | 仍可能含非经营波动 |
| 公司 adjusted/core | 看管理层经营口径 | 可能把股权激励等真实成本加回 |
| 研究调整后盈利 | 统一可复核调整 | 判断具有主观性 |
| Owner earnings | 估计股东经济收益 | 维护资本开支和营运资本需区间化 |

现金质量至少检查：

- 经营现金流/净利润；
- 自由现金流/净利润；
- 应收、存货、合同负债和预付款；
- 股权激励、资本化研发、政府补助；
- 投资收益、公允价值、处置、减值；
- 回购、配股、期权和可转债造成的每股分母变化。

### 第五步：为行业建立 KPI 飞轮

指标不能机械复制，应按行业替换：

| 行业 | 领先指标 | 经营结果 | 证伪点 |
| --- | --- | --- | --- |
| AI 应用/SaaS | MAU、付费用户、付费率、ARPU、续费、credits、CAC | 收入、毛利、现金流、每股收益 | 留存下降、模型/渠道成本吞噬收入、平台直接打包 |
| 晶圆代工 | 产能、利用率、晶圆出货、ASP、节点/产品结构、资本开支 | 收入、毛利、折旧、现金流、ROIC | 利用率下滑、价格竞争、扩产快于需求、出口限制 |
| 期货/券商 | 客户权益、成交额、经纪份额、风险管理规模、资管 AUM、境外业务、净资本 | 手续费、利息、投资/做市收益、ROE | 市场活跃下降、信用/基差风险、资本约束、利润靠投资波动 |
| 消费/制造 | 销量、ASP、渠道库存、产能利用率、原料价格 | 收入、毛利、现金转换 | 库存积压、价格战、应收恶化 |

KPI 链必须走到利润和现金，不能停在下载量、订单、产能或生成量。

### 第六步：使用公开产品和流量信号

App Store、Google Play、网站访问和搜索热度的定位是“前置雷达”，不是财报替代品。

固定分三层：

1. **连续经营证据**：公司披露的 MAU、付费、收入、AUM、产能等；
2. **累计沉淀证据**：安装档位、累计评分、累计客户或商户；
3. **短期热度证据**：排名、月访问、搜索指数和发布活动。

至少观察连续 3—6 个期间，不用单月数据下长期结论。第三方估算必须标记来源、日期、地域和限制。

### 第七步：建立行业第一性原理和全球映射

把行业叙事写成可证伪链条：

```text
需求冲击
  -> 订单/付费/资本开支
  -> 供给与竞争
  -> 价格、销量和利用率
  -> 收入、毛利、现金流和 ROIC
  -> 估值与资金拥挤度
```

跨市场映射必须标明关系：

- `same_company_listing`
- `same_economic_exposure`
- `same_supply_chain`
- `thematic_peer`
- `no_direct_mapping`

美国、台湾、韩国、日本或欧洲同行只能提供领先信号，不能替代本地公司的财务验证。

### 第八步：单列事件和小盘结构风险

事件时间轴分为：

- `completed`：已经发生；
- `confirmed`：官方已确认日期；
- `TBA`：可能发生但未确认。

历史事件统一记录：

- 公告时间和首次可交易日；
- T-1、T0、T+1、T+5，必要时 T+20；
- 标的收益、基准收益和超额收益；
- 成交量变化；
- 同窗口其他事件；
- 因果置信度。

小盘/高弹性股票额外检查：

- 日均成交、买卖价差、停牌和无涨跌停机制；
- 非库存股本、监管公众持股、可观测流通代理、流通市值代理和 20 日成交容量；
- 可卖空、须申报空仓和衍生品；
- 回购、库存股、股权激励、配售、供股、可转债和逐交易线解禁日历；
- 大股东质押、减持、关联交易和披露控制；
- 指数、互联互通和被动资金事件；
- 审计意见、监管调查和诉讼。

创始人增持或公司回购只能证明利益信号，不能替代估值、现金机会成本和净股本变化。

“价格为何在某一整数位附近徘徊”应拆成价格状态、供求与空头三层，不用单一技术指标作因果：

| 层 | 必须保存 | 允许解释 | 主要限制 |
| --- | --- | --- | --- |
| 价格与成交 | 完整交易日收盘、20/60/200 日均线、成交量、VWAP 代理、观察窗 | 短中长期成本和供给区 | 整数位和均线不是已证实支撑/阻力 |
| 可申报净空仓 | 官方周度/规定频率仓位、固定股本分母、申报门槛、发布滞后 | 空头存量和边际方向 | 不等于全部市场空头，可能包含对冲 |
| 每日卖空流量 | 卖空成交额、总成交额、完整/半日状态、区间加权 | 当日做空交易强度 | 卖空成交不等于净空仓增加 |
| 借券条件 | 借券费率、可借库存、利用率、召回风险 | 做空拥挤和边际成本 | 缺失时保持 `unknown`，不用成交量替代 |
| 其他供求 | 回购/增持、配售/解禁、可转债、指数/互联互通、事件套牢区 | 多股力量为何可能互相抵消 | 同时发生不等于已证明因果 |

其中“配售/解禁”必须另算占解禁前可观测流通代理比例与 20 日平均成交量消化天数；低流通股
的相同绝对供给通常会形成更高冲击。监管 public float、指数 free float、行情商 float shares
和本报告研究代理必须分栏，不允许择一冒充官方精确值。

净空仓除以近期平均成交量只能写“流动性覆盖代理”，不能冒充标准 days-to-cover。半日卖空比例
不能与完整交易日直接比较。只有官方净空仓、完整日卖空流量、价格/成交量和借券条件中至少
两至三层同向时，才可写“边际空头增强/减弱”；价格在空头下降后仍未改善，通常说明上方供给、
基本面等待或长线需求也在定价，不能继续把弱势全部归因于做空。

### 第九步：估值矩阵和验证闸门

至少并列：

- 最近财年 PE；
- TTM PE；
- 调整后 PE；
- Forward PE；
- Normalized PE；
- 周期或金融公司适用的 P/B、ROE、EV/EBITDA、SOTP 等。

每个倍数必须记录：

```text
price + price_as_of
EPS/profit + period + type
share_count + dilution
formula
source
limitations
```

结论不写“一个真实 PE”，而写分母矩阵。随后设三层闸门：

| 时间层 | 回答的问题 | 输出 |
| --- | --- | --- |
| 短期事件 | 行业/指数/财报催化是否可能影响弹性 | 事件日历、场景和风险 |
| 中期财报 | 收入能否转成利润、现金和每股价值 | 升级/观察/降级阈值 |
| 长期护城河 | 公司是否持续掌握客户、定价、成本和资本回报 | 证伪条件和长期跟踪项 |

## 4. 图表与表格必须并存

图表用于识别形状，表格用于精确审计。新增图表不得替换原表。

### 图表选择

| 问题 | 图形 | 规则 |
| --- | --- | --- |
| 连续趋势 | 折线图 | 尽量 8 个以上时间点；标记推导值 |
| 离散期间同比 | 分组柱状图 | 同一单位、零基线、直接标签 |
| 收入/利润构成 | 堆叠柱状图 | 分母和口径一致，类别不宜过多 |
| 盈利桥 | 瀑布图 | 调整项必须能相加到终值 |
| 事件反应 | 发散条形图 | 显示零线、正负标签和基准 |
| 估值情景 | 区间/敏感性表 | 不把预测画成已实现事实 |

### 禁止事项

- 不用双轴把不同单位强行拼成相关性；
- 不把 Q1、H1、全年放在同一绝对值趋势线上；
- 不截断普通柱状图零点；
- 不用绿色/红色颜色本身代替正负标签；
- 不删除表格中的精确值、来源和口径限制；
- 不用图形美观掩盖数据稀疏或定义冲突。

## 5. 证据层级

| 层级 | 来源 | 使用方式 |
| --- | --- | --- |
| A | 交易所、监管、审计财报、公司正式公告 | 核心事实 |
| A- | 公司 IR、官方产品文档、官方活动记录 | 经营与产品补充 |
| B | 有方法说明的数据商、指数公司、可信媒体 | 旁证与市场背景 |
| C | 券商转述、访谈转录、社交内容 | 管理层主张或待核验线索 |

所有重要结论保留 URL、发布日期、访问日期、用途和限制。二级来源不能覆盖相冲突的一手来源。

## 6. 标准交付目录

```text
<company-slug>/
├── README.md
├── report.html
├── source-ledger.json
├── combined-artifact.v2.json
├── evidence-index.json
├── validator-results.json
├── red-team.json
├── human-review.json
└── data/
    ├── financial-history.csv
    ├── financial-quarterly-or-half-year.csv
    ├── segment-economics.csv
    ├── operating-kpis.csv
    ├── valuation-matrix.csv
    ├── event-timeline.csv
    ├── event-price-reactions.csv
    ├── public-product-signals.csv
    ├── price-short-positioning.csv
    └── risk-register.csv
```

要求：

- README 先写结论、口径和持续跟踪项；
- HTML 先回答问题，再给证据、图表、表格和证伪条件；
- source ledger 记录来源层级和限制；
- evidence index 绑定 combined artifact checksum，并把关键事实连到文档 checksum、页码、最短必要原文和公式；
- CSV 保留可重算数据；
- 原始大型文件、私有仓位和未经公开审查的数据不进入公开仓库。

## 7. 从美图报告得到的可迁移经验

1. 公司多发一次 Q1 自愿更新，不代表已经建立季度披露制度；
2. 总流量慢增、付费快增时，价值来自货币化而不是流量故事；
3. 模型降价同时是成本利好和功能壁垒攻击，净结果看毛利、留存和 ARPU；
4. App 排名和网站访问适合预警，不适合直接推收入；
5. 回购和创始人增持是信号，不是“股票一定好”的结论；
6. 可转债在高股价时偏稀释、低股价时偏偿债压力，但转股不是自动触发；
7. 小盘事件应看 T0/T+5 和相对基准，同时记录重叠事件；
8. “真实 PE”必须是盈利分母矩阵，而非一个被挑选的倍数；
9. 空头研究必须分开净空仓、卖空成交与借券条件；“空头减少但价格不涨”也是供求信息；
10. 最终结论应写成下一财报可以验证或推翻的条件。

## 8. 行业适配示例

### AI 应用公司

重点补充产品矩阵、付费用户、付费率、ARPU、留存、credits、渠道费、模型/API 成本、App 与 Web 趋势、平台替代风险。

### 晶圆代工公司

重点补充晶圆出货、产能、利用率、ASP、成熟/先进节点、应用结构、客户地区、资本开支、折旧、补助、出口管制和全球同业周期。

### 期货公司

重点补充经纪、风险管理、资产管理、境外金融服务、客户权益、成交份额、净资本、保证金、信用/基差风险、投资收益和市场活跃度。

## 9. 交付前检查表

- [ ] 证券身份、交易所和互联互通资格来自当前官方名单；
- [ ] 年度、半年度、季度、自愿更新和推导值没有混用；
- [ ] 收入来源与利润来源分别解释；
- [ ] 法定、调整后和 owner earnings 已桥接；
- [ ] 同比、环比、季节性和单位明确；
- [ ] 每张图旁边仍有精确表格或数据文件；
- [ ] 管理层主张未冒充审计事实；
- [ ] 行业叙事有第一性原理和证伪条件；
- [ ] 事件反应有 T0 规则、基准和归因边界；
- [ ] 回购、增发、可转债、指数和互联互通风险已单列；
- [ ] 已发行、库存、非库存、监管公众持股、流通代理和活跃供给没有混写；
- [ ] 已按交易线计算流通市值代理、20 日换手/容量和未来解禁/转股/奖励供给天数；
- [ ] 解禁已区分可出售、登记/上市和实际减持，不把解禁公告写成卖出事实；
- [ ] PE/EPS 有同一日期、币种和股本口径；
- [ ] 下一验证点具体到报告窗口或官方日历；
- [ ] 长期公司底稿和短期事件监控是两个入口，共享同一事实层；
- [ ] owner earnings、净现金、fully diluted shares 可逐项复算；
- [ ] 任取 10 个关键数字可在两次点击内看到页码、原文、口径和公式；
- [ ] 25 维度、至少 50 个 indicator family 与九道 gate 已机读记录；
- [ ] 独立 red-team、validator 和具名 human review 状态已展示；
- [ ] `as_of`、`stale_after` 与 change log 已设置；
- [ ] 结论是条件化研究支持，不是买卖建议。

## 10. 方法论来源与工程参考

完整的 claim 映射、访问时间、用途、权利边界、Git commit 与采用/拒绝项记录在
[`methodology-source-ledger.json`](../skills/research-buffett-munger-company/references/methodology-source-ledger.json)；
下面保留公开复核所需的原始入口。巴菲特—芒格方法只以官方信件、Berkshire 授权档案或具日期
的演讲记录为依据；GitHub 项目只用于工作流设计，不是投资方法的权威来源。

### 10.1 巴菲特—芒格方法原始入口

- [Berkshire Hathaway Owner's Manual](https://www.berkshirehathaway.com/ownman.pdf)
- [1977 Chairman's Letter](https://www.berkshirehathaway.com/letters/1977.html)
- [1983 Chairman's Letter](https://www.berkshirehathaway.com/letters/1983.html)
- [1986 Chairman's Letter](https://www.berkshirehathaway.com/letters/1986.html)
- [1989 Chairman's Letter](https://www.berkshirehathaway.com/letters/1989.html)
- [1996 Chairman's Letter](https://www.berkshirehathaway.com/letters/1996.html)
- [2005 Chairman's Letter](https://www.berkshirehathaway.com/letters/2005ltr.pdf)
- [2007 Chairman's Letter](https://www.berkshirehathaway.com/letters/2007ltr.pdf)
- [2009 Chairman's Letter](https://www.berkshirehathaway.com/letters/2009ltr.pdf)
- [2018 Chairman's Letter](https://www.berkshirehathaway.com/letters/2018ltr.pdf)
- [2021 Chairman's Letter](https://www.berkshirehathaway.com/letters/2021ltr.pdf)
- [2022 Chairman's Letter](https://www.berkshirehathaway.com/letters/2022ltr.pdf)
- [2023 Chairman's Letter](https://www.berkshirehathaway.com/letters/2023ltr.pdf)

### 10.2 流通盘与供给口径原始入口

- [HKEX Rule 8.08：上市时公众持股要求](https://cn-rules.hkex.com.hk/%E8%A6%8F%E5%89%87%E6%89%8B%E5%86%8A/808)
- [HKEX Rule 13.32B：持续公众持股要求](https://en-rules.hkex.com.hk/entiresection/7010)
- [MSCI Global Investable Market Indexes Methodology](https://www.msci.com/downloads/web/msci-com/indexes/index-resources/market-classification/MSCI_GIMIMethodology_Mar2023.pdf)
- [S&P Dow Jones Indices: Index Mathematics Methodology](https://www.spglobal.com/spdji/en/methodology/article/index-mathematics-methodology/)
- [Field & Hanka: The Expiration of IPO Share Lockups](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=205011)（只作历史机制证据，不外推单一公司收益）
- [Berkshire Hathaway Annual Meetings archive](https://buffett.cnbc.com/annual-meetings/)
- [USC Gould 2007 Munger event record](https://gould.usc.edu/news/300-graduate-from-usc-law/)
- [Munger Archive: 1994 USC worldly-wisdom recording record](https://mungerarchive.com/recordings/usc-1994-worldly-wisdom/)
- [James Clear: Psychology of Human Misjudgment transcript record](https://jamesclear.com/great-speeches/the-psychology-of-human-misjudgment-by-charlie-munger)

后两项属于有日期的二级转录链，只用于搭建跨学科、激励与心理偏误问题，不作为公司事实或
巴菲特—芒格原话的唯一依据。

### 10.2 工程工作流快照

星标只是 2026-07-26 的可复核发现快照，不代表质量排序或背书，也不参与公司评分。

| 仓库 | 原始链接 | 快照星标 | 仅采用的工程启发 |
| --- | --- | ---: | --- |
| agentskills/agentskills | https://github.com/agentskills/agentskills | 23,503 | 可移植 skill 目录与渐进披露 |
| OpenBB-finance/OpenBB | https://github.com/OpenBB-finance/OpenBB | 71,029 | provider 抽象与取数/分析分离 |
| virattt/ai-hedge-fund | https://github.com/virattt/ai-hedge-fund | 62,421 | 角色分工与结构化中间产物 |
| xbtlin/ai-berkshire | https://github.com/xbtlin/ai-berkshire | 14,170 | 证据缺口、管理层兑现与 bear case |
| himself65/finance-skills | https://github.com/himself65/finance-skills | 3,071 | DCF、相对估值和 SOTP 路由 |
| tradermonty/claude-trading-skills | https://github.com/tradermonty/claude-trading-skills | 2,499 | 数据质量与缺失值检查 |
| yennanliu/InvestSkill | https://github.com/yennanliu/InvestSkill | 143 | filing item、bear case 与 result validator |
| OctagonAI/skills | https://github.com/OctagonAI/skills | 133 | 财报问题拆解和可组合财务模块 |
| kangarooking/buffett-letters-skill | https://github.com/kangarooking/buffett-letters-skill | 57 | 官方信件的原子主题索引 |
| kangarooking/poor-charlies-almanack-skill | https://github.com/kangarooking/poor-charlies-almanack-skill | 26 | 逆向、激励和偏误问题结构 |

固定阈值、综合打分、bullish/bearish 信号、买卖或加仓语言，以及无法回溯到一手材料的
“大师归因”均不采用。仓库许可证、commit SHA 和逐项拒绝理由以 source ledger 为准。
