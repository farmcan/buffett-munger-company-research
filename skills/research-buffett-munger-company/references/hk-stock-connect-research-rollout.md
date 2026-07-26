# 港股通公司研究 rollout

本文件把单公司方法扩展到港股通全市场。它是一套可移植的研究顺序和状态机，不包含证券
名单采集器，也不声称任何一份历史名单在今天仍然有效。

## 1. 基本边界

- 每次运行先从上交所、深交所与港交所官方来源冻结当日名单。
- “港股通证券数”不等于“独立公司数”；同一发行人可能有多类证券或 A/H 两地上市。
- 港股通资格是带日期的市场属性，不是公司质量标签。
- 先做全部证券的 U0/U1，再只对有充分主源与研究价值的样本做 U2。
- 不按近期涨跌、热度或模型偏好决定深研顺序。
- 每个结论必须绑定冻结名单、研究日和证据校验和。

## 2. 冻结快照

一次可复现的 universe snapshot 至少保存：

```text
snapshot_id
as_of_date
market = hk-stock-connect
official_source_urls[]
retrieved_at
raw_content_sha256[]
security_count
unique_issuer_count
securities[]
```

每条证券至少保存：

```text
security_id
stock_code
exchange
board
security_name_zh
security_name_en
security_type
currency
connect_channel
eligibility_status
eligibility_source_ref
legal_issuer_id
issuer_resolution_status
listing_structure
industry_route
```

只有沪港通与深港通的当前官方查询都成功且均未命中时，才可写
`not_eligible_currently`；任一查询失败时保留 `unknown`。

## 3. 三层覆盖

### U0：证券身份

目标是回答“这是什么证券、代表什么权利”：

- 代码、交易所、股份类别、币种和上市状态；
- 法律发行人、控股结构、A/H、红筹、VIE、同股不同权或其他特殊权利；
- 当前港股通资格及来源日期；
- 同一发行人的证券去重关系。

U0 未通过时，禁止估值和公司质量结论。

### U1：确定性广筛

只使用可统一取得且能追溯的事实，形成：

- 报告期与审计状态；
- 报表覆盖和缺失；
- 行业路由；
- 经营历史长度；
- 是否存在生存、审计、上市状态或主体识别阻断；
- 进入 U2、等待来源、行业 provider 待建或排除的明确原因。

U1 是资料与适用性筛查，不是价值投资总分，也不是买入名单。

### U2：九 gate 深研

对进入队列的公司执行：

1. 身份与来源；
2. 能力圈；
3. 商业经济；
4. 护城河；
5. 管理层与资本配置；
6. owner earnings；
7. 生存与资产负债表；
8. 内在价值与安全边际；
9. 决策边界与反证。

必须同时完成 25 个研究维度、50 个 indicator families、独立 red-team 与人工复核。

## 4. 发行人优先的队列

推荐队列键：

```text
issuer_resolution
primary_source_completeness
industry_provider_readiness
reporting_history
structure_complexity
human_review_capacity
stable_tie_breaker
```

推荐顺序：

1. 发行人已解析、主源完整、行业 provider 已校准的代表样本；
2. 同行业反例与失败样本；
3. A/H 同主体对照样本；
4. 来源不足或结构复杂但具有较高方法校准价值的样本；
5. 其他公司。

队列顺序只表示研究可执行性，不表示公司质量或预期收益。

## 5. 行业校准

扩展到全市场前，至少覆盖：

- 银行、保险、券商；
- 互联网平台与软件；
- 消费与品牌；
- 制造业；
- 资源周期；
- 公用事业与基础设施；
- 地产；
- 医疗服务与医药；
- 控股平台。

每个行业至少保留：

- 一个资料充分的正向研究样本；
- 一个明确失败或高风险样本；
- 一个来源缺失或口径冲突样本；
- 一个随机 reject QA 样本。

一个 broad route 的通过不能证明全部 subtype 已校准。

## 6. 状态机

```text
universe_frozen
  -> issuer_resolution_pending
  -> source_collection_pending
  -> fact_pack_pending
  -> fact_pack_review_pending
  -> u1_screened
  -> u2_research_pending
  -> red_team_pending
  -> human_review_pending
  -> research_ready_not_decision_ready
```

常见旁路状态：

```text
identity_blocked
evidence_insufficient
outside_circle
specialized_provider_required
survival_or_governance_fail
economics_unattractive
valuation_inconclusive
```

缺失数据不是负面经营结论。它必须停留在 `pending`、`unknown` 或
`evidence_insufficient`。

## 7. 批量 QA

每批至少检查：

- 输入 universe checksum 与证券数是否固定；
- 发行人去重是否稳定；
- 每个排除原因是否可复现；
- 主源是否使用官方 HTTPS 地址并保存内容 SHA-256；
- 报表、价格与研究日期是否无前视；
- U1 是否误用了估值或主观 moat 判断；
- U2 是否完整执行 25 维、50 指标与九 gate；
- 行业不适用项是否标记 `not_applicable` 而非 0；
- 失败样本是否被保留；
- 人工复核是否绑定被审 artifact 的 checksum。

## 8. 停止条件

出现下列任一情况时停止扩批：

- 官方名单抓取不完整或无法重现；
- 证券与法律发行人误配；
- 文档未保存校验和或页级证据；
- 行业 provider 把不适用指标当通用标准；
- source gap 被转换成负面公司结论；
- validator 失败仍进入后续阶段；
- 人工复核容量不足；
- 输出出现买卖、仓位或收益承诺语言。

## 9. 当前建议

先用 10–20 家覆盖多个行业和失败形态的校准集验证来源、行业口径和人工复核成本，再扩大到
全部冻结证券。每次名单变化都新建快照；不得回写旧批次以制造“始终正确”的历史。
