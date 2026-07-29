# 巴菲特—芒格式公司研究

[English](README.md)

这是一套独立、非官方、主源优先的公司研究工作流。它把公开可归因的巴菲特—芒格原则，
工程化为可以逐家公司执行、校验、反证和复盘的研究 contract。

它不是选股机器人、语录库、人物模拟器或固定分数模型。通过 validator 只表示研究结构达到
约定标准，不表示公司值得买入，更不保证收益。

> 本项目与 Berkshire Hathaway、Warren Buffett、Charlie Munger、其遗产管理方及任何
> 被引用的出版者均无隶属、授权、背书或赞助关系。仅供研究辅助，不构成投资建议。

## 公开公司报告

[GitHub Pages 研究首页](https://farmcan.github.io/buffett-munger-company-research/)
现已公开地平线机器人、小鹏汽车、美图公司、南华期货、中芯国际与阜博集团六份可追溯报告。每份 HTML 都直接展示
25 个维度、50 个指标、九道 gate、来源账本、页码/行号证据定位、估值边界与失效条件。
六份报告统一使用 `company-research-publication-v1` 发布母版和共享视觉主题；行业差异只进入
KPI、会计桥、现金桥和估值插槽，不再各自发明页面结构。

每份公司报告都在自己的“大事件时间轴”栏目内嵌独立的
`事件 Surprise × 市场共振` 终端，展示该公司的 `NOW` 分界、T0/T+5/T+20、
未来空心节点和原始来源证据卡；读者不需要跳到跨公司汇总页。

## 为什么它不是普通的“价值投资提示词”

当前版本固定并自动校验：

- 17 个经过审计的方法来源：13 个 A 级、2 个 A- 级、2 个 B 级补充来源；
- 21 个方法 claim；
- 9 个有顺序的研究 gate；
- 25 个公司研究维度；
- 50 个最低 indicator families；
- 主源 URL、发布日期、访问日、范围、审计状态与内容 SHA-256；
- 价格日、研究日和财报期的前视偏差控制；
- owner earnings、PE、未来 EPS 与内在价值的可复算状态；
- 亏损、未盈利、数据缺失和来源冲突的显式表达；
- gate 阻断传播、独立 red-team 与具名人工复核；
- 0 个 GitHub 项目被当作巴菲特/芒格方法权威。

这套 contract 的重点不是“指标多”，而是禁止常见偷换：

- 低 PE 不自动等于便宜；
- 高毛利或高市占率不自动等于护城河；
- CFO-capex 不自动等于 owner earnings；
- 缺失数据不自动等于公司差；
- 模型常识不替代公司主源；
- GitHub 高星不替代原始方法来源；
- validator 通过不等于投资批准。

## 研究顺序

```text
官方来源
  -> 证券与法律主体
  -> 能力圈
  -> 商业模式、客户、供应商与产业链
  -> 多年经济性
  -> 护城河与反证
  -> 管理层与资本配置
  -> owner earnings
  -> 生存与资产负债表
  -> 内在价值区间与反向估值
  -> 独立 red-team
  -> 具名人工复核
```

## 主要内容

```text
skills/research-buffett-munger-company/
  SKILL.md                         Agent 执行入口
  references/methodology.md        “道”、来源和归因边界
  references/company-research-master-checklist.md
                                   “术”、25 维公司检查表
  references/company-research-schema.md
                                   artifact 与 QA contract
  references/methodology-source-ledger.json
                                   来源、claims、GitHub 审计与权利边界
  references/methodology-implementation-crosswalk.json
                                   方法到 25 维、50 指标、9 gate 的映射
  references/hk-stock-connect-research-rollout.md
                                   港股通 U0/U1/U2 批量路线
  scripts/                         零第三方运行依赖的 validator
examples/synthetic-company-research.json
                                   可通过校验的纯合成样例
```

## 快速使用

### 作为 Codex Skill

使用 Codex 自带的 Skill Installer 从公共仓库直接安装：

```bash
python3 \
  "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo farmcan/buffett-munger-company-research \
  --path skills/research-buffett-munger-company
```

下一轮对话即可使用。需要保留开发 checkout 时，也可以 clone 后建立软链接：

```bash
git clone https://github.com/farmcan/buffett-munger-company-research.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
ln -s "$PWD/buffett-munger-company-research/skills/research-buffett-munger-company" \
  "${CODEX_HOME:-$HOME/.codex}/skills/research-buffett-munger-company"
```

调用：

```text
Use $research-buffett-munger-company to research <公司名和证券代码>。
先冻结研究日和主源，完成九个 gate，并在下结论前生成可通过 validator 的 artifact。
```

### 校验样例

Python 3.11+ 即可，运行时无第三方依赖：
`seed.*` schema 标识为兼容原始私有实现而保留，不构成 Seed 运行时依赖。

```bash
python skills/research-buffett-munger-company/scripts/validate_company_research.py \
  examples/synthetic-company-research.json
```

校验方法来源和实现映射：

```bash
python skills/research-buffett-munger-company/scripts/validate_methodology_source_ledger.py \
  skills/research-buffett-munger-company/references/methodology-source-ledger.json

python \
  skills/research-buffett-munger-company/scripts/validate_methodology_implementation_crosswalk.py \
  skills/research-buffett-munger-company/references/methodology-implementation-crosswalk.json
```

运行测试：

```bash
python -m pip install -e ".[dev]"
pytest
ruff check .
```

## 真正研究一家公司

1. 阅读[方法与归因边界](skills/research-buffett-munger-company/references/methodology.md)。
2. 冻结精确证券、法律发行人、研究日、价格日、会计准则和资料集。
3. 执行[公司研究主检查表](skills/research-buffett-munger-company/references/company-research-master-checklist.md)。
4. 按[schema contract](skills/research-buffett-munger-company/references/company-research-schema.md)
   序列化研究结果。
5. 运行 validator、独立 red-team 和具名人工复核。

合成样例中的 `example.com` URL、公司名和数字都不是现实公司证据。真实研究必须对实际使用的
文件保存校验和，并在更细的事实层保留页码、原文、期间、单位、币种和会计范围。

## 港股通路线

港股通批量研究采用发行人优先的三层结构：

- U0：证券、股份权利和法律发行人；
- U1：确定性的资料完整性与适用性广筛；
- U2：25 维、50 指标、九 gate 的完整深研。

仓库不内置一份会过期的“当前港股通名单”。每次运行必须从沪深交易所和港交所官方来源重新
冻结带日期的 universe。完整顺序见
[港股通 rollout](skills/research-buffett-munger-company/references/hk-stock-connect-research-rollout.md)。

## 方法来源

核心来源优先使用 Berkshire 官方
[Owner's Manual](https://www.berkshirehathaway.com/ownman.pdf) 和
[股东信](https://www.berkshirehathaway.com/letters/letters.html)。年会、演讲转录和 GitHub
项目按不同来源等级处理。

GitHub 高星项目只用于借鉴 Skill 包装、provider 分层、数据审计、估值敏感性和 red-team
结构；没有复制第三方代码，也没有把开源作者的固定阈值、权重或交易语言写成巴菲特/芒格
规则。逐项记录见
[方法来源账本](skills/research-buffett-munger-company/references/methodology-source-ledger.json)。

## 明确不做

- 不输出买卖或仓位指令；
- 不模拟巴菲特或芒格人格；
- 不提供统一“巴菲特分数”；
- 不设全行业固定 ROE、负债、PE 或安全边际阈值；
- 不打包受版权保护的股东信、书籍、长转录、市场数据或真实公司私有资料；
- 不声称结构校验能证明经济事实；
- 不暗示任何个人或机构背书。

## 开源与责任边界

本仓库的原创代码和文档采用 [MIT License](LICENSE)。第三方来源文件和名称仍归各自权利人
所有，仓库只保留短摘要、链接和研究用途边界。使用前请阅读
[DISCLAIMER.md](DISCLAIMER.md)。从 v0.1 到 v1.0 的验收路线见
[ROADMAP.md](ROADMAP.md)，引用信息见 [CITATION.cff](CITATION.cff)。
