# Consolidated Review

## 输出语言

本审核的所有描述性内容使用中文撰写；Finding ID、严重等级、证据等级、置信度、决策状态、关系分类、冲突状态、合并决策、审核状态、审核结果等 UPPERCASE_WITH_UNDERSCORE 标识符与 YAML 索引的 key/枚举值保持英文；技术标识符与文件路径保持英文。

## Review Metadata

### Review ID

2026-08-04-review-001

### Review Type

CONSOLIDATED_REVIEW

### Design Spec

docs/superpowers/specs/2026-08-04-spec-review-slim-design.md

### Consolidation Date

2026-08-04

### Consolidator

yy-spec-review (main agent)

### Review Status

COMPLETED

---

## Consolidation Scope

This document consolidates the independent reviews produced by:

* `yy-product-reviewer`
* `yy-system-critic`
* `yy-test-designer`

The purpose of consolidation is to merge duplicate findings without losing evidence, preserve materially different findings, record conflicts, establish unified finding identities (CR-IDs), and prepare a single decision-ready document for the Spec owner.

This document is a consolidation artifact. It is not a replacement for the original reviewer reports.

---

## Source Reviews

| Reviewer            | Review Type    | Review ID            | Source File                                                              | Status   |
| ------------------- | -------------- | -------------------- | ------------------------------------------------------------------------ | -------- |
| yy-product-reviewer | PRODUCT_REVIEW | 2026-08-04-review-001 | docs/superpowers/reviews/spec-review-slim-design/2026-08-04-review-001/product-review.md  | AVAILABLE |
| yy-system-critic    | SYSTEM_REVIEW  | 2026-08-04-review-001 | docs/superpowers/reviews/spec-review-slim-design/2026-08-04-review-001/system-review.md    | AVAILABLE |
| yy-test-designer    | TEST_REVIEW    | 2026-08-04-review-001 | docs/superpowers/reviews/spec-review-slim-design/2026-08-04-review-001/test-review.md      | AVAILABLE |

---

## Consolidator Predispositions

> 以下为 Phase 1 主 agent 形成、可能影响合并的关键判断，供审计认知偏差。

### Predisposition 1

本 Design Spec 由本人（主 agent）撰写，可能在"共享化拆分的具体机制"上低估迁移风险——例如如何精确区分"共享定义"与"角色独有指令"而不丢失语义。此偏差可能使合并时对 CR-001/CR-006 的严重程度估计偏低。

### Predisposition 2

本人倾向于认为"删冗余而保留规则"是低风险操作，这可能弱化对运行时/加载层面微妙问题的敏感度——而三位评审员独立指出的 CR-001（common.md 未进入 subagent 上下文）恰恰落在该盲区。

### Predisposition 3

本人曾将"固定框架 tokens 降幅 ≥40%"视为充分的质量护栏；评审显示该指标在口径/基线/工具上均不可复现（CR-003），我可能高估了它的判定力。

---

# Consolidated Findings

## CR-001 — 共享定义 `references/common.md` 未纳入 subagent 加载契约，独立评审核心不变量面临静默失效

### Consolidated Severity

P0

### Consolidation Confidence

HIGH

### Finding Status

ACCEPTED

### Underlying Problem

设计把严重度、证据等级、Finding 必填字段格式、以及关键的「独立评审 / 上下文隔离」规则从角色/模板内联内容中抽离，集中到新增的 `references/common.md`，并要求角色改为"见 common.md"引用；但 §5 规定的 subagent 加载清单仍为 `roles/X.md + templates/X.md + spec`，**不包含 common.md**。结果：被抽离的判定标准在 subagent 运行上下文中悬空不可达，独立评审不变量（§4 第 6 条）可能被静默破坏，且失效不报错、不被现有验收发现。

### Evidence

#### Confirmed Evidence

* §3.1："各角色与模板以『见 `references/common.md`』引用，不再各自重述。"
* §3.2：删除严重度、证据等级、Finding 格式、独立评审规则等共享块，替换为对 common.md 的引用。
* §5："subagent 提示词仍指示『读 roles/X.md + templates/X.md + spec 路径』"——未提及 common.md。
* §4 第 6 条：独立评审硬约束，角色间互不参考、subagent 提示词不含主 agent 分析。

#### Inferred Evidence

* subagent 运行于隔离上下文，无法从主 agent 上下文继承 common.md 内容；若加载清单不含 common.md，则该定义不会进入 subagent 上下文。

#### Unknowns

* 现有 `review-orchestrator-protocol.md` 是否另有机制注入 common.md（设计未说明）。

### Trigger Scenario

1. 实施按 §3.1–3.2 将共享定义移入 common.md，角色文件仅保留引用。
2. 主 agent 按 §5 组装 subagent 提示词，加载清单仍为 `roles + templates + spec`。
3. subagent 在隔离上下文启动，读到指向 common.md 的引用但上下文无其内容。
4. 设计未定义此后行为，出现两条均未定义的分支：A) subagent 不读 common.md → 严重度/证据等级失去统一基准；B) subagent 读 common.md → 上下文总量与瘦身前相当，§5"每个 subagent 上下文更小"的受益结论不成立。

### Consequence

* Business Impact: 三份独立审核的口径不再基于同一判据，彼此不可比。
* Data Impact: Phase 3 合并的关系分类与完整性校验建立在口径不一致的输入上。
* Operational Impact: 失效静默，现有 §6 功能验收（正常产出 + 数量基本一致）无法检出。
* Verification Impact: 已消费的历史审核结论若基于失真口径，事后难以归因。

### Reviewer Perspectives

#### Product Perspective

**Source Findings:** PR-001

**Assessment:** 产品层工作流缺口——评审者获取判定标准的路径未定义，是核心工作流的必经环节缺失。

#### System Perspective

**Source Findings:** SC-001

**Assessment:** 架构层确认：外置共享定义使"独立评审/上下文隔离"指令在 subagent 上下文中不存在，核心不变量被静默破坏，属难以检测的静默回归。

#### Test Perspective

**Source Findings:** TD-002

**Assessment:** 验证层指出该失效无任何可观测判据——产出中仍会出现 P0/P1/P2 等枚举值（模型自行产生也会写出），因此"共享定义是否生效"不可证明，失效表现为静默降级。

### Relationship Classification

SAME_ROOT_CAUSE

#### Relationship Explanation

PR-001、SC-001、TD-002 从产品工作流、系统架构、验证可观测三个角度描述同一根因：common.md 被引用但未进入 subagent 加载契约。TD-002 补充的"静默降级不可观测"是同一根因的必然后果，故三者合并为一条 Consolidated Finding。

### Conflict Analysis

#### Conflict Status

NO_CONFLICT

#### Conflicting Positions

无。三位评审员结论一致收敛。

#### Conflict Evidence

不适用。

#### Resolution

无需裁决。

### Recommended Resolution

明确 subagent 的权威加载清单必须包含 `references/common.md`（与 roles/templates/spec 并列），或在 §5 显式声明其注入方式；并在 §6 功能验收中增加"独立性指令仍存在于 subagent 上下文"的校验点。此项必须在实施前以一行加载清单变更落地。

### Source References

#### Product Review

* PR-001

#### System Review

* SC-001

#### Test Review

* TD-002

#### Design Spec References

* §3.1 新增 references/common.md
* §3.2 瘦身角色文件
* §5 数据流向（行为不变）
* §4 第 6 条 质量不变量

### Consolidation Decision

MERGED

#### Decision Rationale

三源指向同一根因与同一必然后果，合并后保留各自视角证据，避免重复且不失真。

### Severity Change Rationale

No severity change from source findings.（PR-001 P0 / SC-001 P0 / TD-002 P0 均为 P0）

---

## CR-002 — 「不损失审核质量」缺少可判定验收判据，回滚触发条件不可执行

### Consolidated Severity

P0

### Consolidation Confidence

HIGH

### Finding Status

ACCEPTED

### Underlying Problem

设计将"不损失审核质量"作为首要前置约束，但 §6 唯一对应的验收判据是"Finding 数量与严重度分布基本一致"，该表述无可判定阈值、无判定责任人、无消除 LLM 运行波动的比较协议；因此"质量下降→git revert"的回滚规则没有可执行的触发条件，质量回归可能被当作正常波动放行，或正常波动被误判为回归。

### Evidence

#### Confirmed Evidence

* 目标陈述（第 5 行）："在不损失审核质量、不改变三角色并行独立审核架构的前提下……"
* §6 功能验收第 2 条："Finding 数量与严重度分布基本一致"，无阈值、无判定人。
* §6 回滚条："若功能验收质量下降，直接 git revert 到留底提交。"
* §1 自述："一次 Product Reviewer 真实抽样运行"——佐证产出由 LLM subagent 生成，存在运行间波动。

#### Inferred Evidence

* 三份独立审核由 LLM 生成，同一提示词重复运行本身产生不同 Finding 集合；单样本前后对比无法区分"瘦身导致的下降"与"固有波动"。

#### Unknowns

* 该波动的实际幅度未被设计测量。

### Trigger Scenario

1. 实施前用固定小 spec 跑一次基线（如 11 个 Finding：2×P0 / 6×P1 / 3×P2）。
2. 瘦身后再跑一次（如 9 个 Finding：1×P0 / 5×P1 / 3×P2），缺失的 P0 与基线非同一问题。
3. 对照 §6"数量与严重度分布基本一致"——设计无阈值，也无逐条语义比对要求。
4. 执行者可能判"基本一致"放行，也可能判"下降"回滚；两种相反结论在 §6 下都能自洽。

### Consequence

* Business Impact: 方案首要约束失去可证伪的验收，质量回归可能被静默发布。
* Operational Impact: 回滚决策依赖主观判断，可能误回滚（推翻整轮有效改造）或漏回滚。
* Verification Impact: §7 以"方案 A 验证有效"作为方案 B 前置，不可判定的验收会把后续决策一并置于主观判断上。

### Reviewer Perspectives

#### Product Perspective

**Source Findings:** PR-002

**Assessment:** 产品层指出回滚触发条件因判据缺失而无法执行，且验收样本固定为小 spec，代表性未被论证。

#### System Perspective

**Source Findings:** —

**Assessment:** 系统评审未单独提出此问题（SC-003 从验收样本错配角度相关，已并入 CR-004）。

#### Test Perspective

**Source Findings:** TD-001

**Assessment:** 验证层强调"单次前后对比无法区分质量回归与模型波动"，给出可计算通过条件的方向（关键 Finding 复现率为主判据）。

### Relationship Classification

SAME_ROOT_CAUSE

#### Relationship Explanation

PR-002 与 TD-001 均指向"质量约束不可判定 → 回滚不可执行"这一根因，合并。

### Conflict Analysis

#### Conflict Status

NO_CONFLICT

#### Conflicting Positions

无。

#### Conflict Evidence

不适用。

#### Resolution

无需裁决。

### Recommended Resolution

将质量约束转为可判定判据：定义基线波动测量方式（同一 spec 改动前后各运行 N≥2 次记录波动范围）；定义"基本一致"的量化口径（建议以 P0/P1 所指向问题是否仍被覆盖为准，而非仅比较数量）；明确判定责任人；要求验收样本至少包含一个大型 spec 或显式声明并接受小 spec 局限；回滚触发条件与上述判据一一对应。

### Source References

#### Product Review

* PR-002

#### System Review

* —

#### Test Review

* TD-001

#### Design Spec References

* 目标陈述（第 5 行）
* §1 量化结论（第 19–20 行）
* §6 回滚与验收（第 110–120 行）

### Consolidation Decision

MERGED

#### Decision Rationale

PR-002 与 TD-001 描述同一不可判定根因，合并保留产品与验证双视角。

### Severity Change Rationale

No severity change from source findings.（PR-002 P0 / TD-001 P0）

---

## CR-003 — 「固定框架 tokens 降幅 ≥40%」的基线、口径与测量工具不可复现，量化验收结论不唯一

### Consolidated Severity

P1

### Consolidation Confidence

HIGH

### Finding Status

ACCEPTED

### Underlying Problem

"降低 ≥40%"形式上是数值判据，但基线值未固定（§1 给的是 40–78K 区间且称"随 spec 大小变化"又"与 spec 内容无关"，口径自相矛盾）、统计对象未定义（common.md 是否计入、spec 4× 读取是否计入、按静态字数还是运行时实际加载量均未定义）、测量工具位于 `/tmp` 且允许"同类脚本"替换。三项任一不固定，降幅结论即不唯一，核心量化目标事实上未被验证。

### Evidence

#### Confirmed Evidence

* 目标陈述："固定框架开销降低 ≥40%……减少单次审核的 token 消耗与运行时间。"
* §1 表格："约 40–78K tokens（随 spec 大小变化，但与 spec 内容无关、且大量重复）"；"spec 4× 读取……是大型 spec 的主导成本，但……本轮不动。"
* §6 静态验收："重跑 token 分析器（`/tmp/yy_spec_token_analyzer.py` 同类脚本），固定框架 tokens 降幅 ≥40%。"
* §2 目标行数使用"~400""~700"近似值，未说明为硬上限还是参考值。

#### Inferred Evidence

* 不同 token 估算实现（尤其中文感知估算）会给出不同数值，使"同类脚本"比较失去意义。

#### Unknowns

* `/tmp/yy_spec_token_analyzer.py` 当前是否存在、其统计口径为何。

### Trigger Scenario

1. 瘦身完成，协议与角色文件压缩。
2. 执行 §6 静态验收，重跑分析脚本计算降幅。
3. 测试者 A 以 78K 为基线、口径含 SKILL.md/CLAUDE.md，得 45% 判达标；测试者 B 以 40K 为基线、口径仅 4 协议文件、换"同类"脚本，得 32% 判不达标。设计无法裁决。

### Consequence

* Verification Impact: 量化验收结果可被口径选择左右，实际未达标的改造可论证为达标（或相反）。
* Operational Impact: 前后测量不可比，方案 B 启动前的收益判断失去依据。
* Business Impact: 改造投入与回归成本可能无法回收。

### Reviewer Perspectives

#### Product Perspective

**Source Findings:** PR-003

**Assessment:** 产品层指出静态文件体积降幅 ≠ 运行时 token 消耗改善，且"运行时间"完全无验收项。

#### System Perspective

**Source Findings:** —

**Assessment:** —

#### Test Perspective

**Source Findings:** TD-004

**Assessment:** 验证层强调基线须为定值、工具须纳入仓库或写死估算规则、目标行数须明确硬/参考。

### Relationship Classification

SAME_ROOT_CAUSE

#### Relationship Explanation

PR-003 与 TD-004 均指向"≥40% 量化目标不可被唯一判定"的根因（基线/口径/工具三者不固定），合并。

### Conflict Analysis

#### Conflict Status

NO_CONFLICT

#### Conflicting Positions

无。

#### Conflict Evidence

不适用。

#### Resolution

无需裁决。

### Recommended Resolution

在验收前记录具体基线数值及测量条件（所用 spec、纳入文件清单、是否计入 spec 多次读取）；将分析脚本纳入仓库或明确写死估算规则，禁止"同类脚本"替换；明确 §2 行数目标为硬上限还是参考值；验收结果以"基线值/改动后值/降幅/测量条件"四元组留存可复算。

### Source References

#### Product Review

* PR-003

#### System Review

* —

#### Test Review

* TD-004

#### Design Spec References

* 目标陈述（第 5 行）
* §1 量化结论（第 14–20 行）
* §2 目标文件结构（第 37–40 行）
* §6 静态验收（第 118 行）

### Consolidation Decision

MERGED

#### Decision Rationale

两源描述同一不可复现根因，合并。

### Severity Change Rationale

No severity change from source findings.（PR-003 P1 / TD-004 P1）

---

## CR-004 — 验收设计无法检出静默退化：happy-path 与小 spec 覆盖不到负向路径与合并能力

### Consolidated Severity

P1

### Consolidation Confidence

HIGH

### Finding Status

ACCEPTED

### Underlying Problem

§6 功能验收为一次小 spec 的正常成功运行，只能证明"流水线还能跑通"，无法证明"审核质量未下降"。具体三类盲区：(a) 负向路径——MISSING/INCOMPLETE 与 Source Finding 完整性校验在 happy-path 下根本不触发，被压缩掉的失败分支可在四项验收全绿时发布；(b) 样本错配——§1 自承风险（跨文件引用失效、字段漂移）在上下文更大、并发更高的大规模场景更易暴露，而小 spec 系统性低估风险；(c) 合并能力退化——被压缩最重的 consolidation 关系分类（DUPLICATE/SAME_ROOT_CAUSE/CONTRADICTORY 等）在小 spec 少重叠时不会触发，退化只会在真实复杂审核中显现。

### Evidence

#### Confirmed Evidence

* §4 第 4、5 条：MISSING 硬规则、INCOMPLETE 触发条件、完整性校验公式列为不可改动不变量，且恰位于被压缩的 consolidation-protocol.md。
* §3.3：consolidation-protocol.md 1583→~700 行，保留关系分类与冲突记录、砍掉"冗长 rationale、重复示例"（判定依据恰在砍掉部分）。
* §6 功能验收："用同一个小 spec……改动前后各跑一次完整审核"。
* §1："spec 4× 读取……是大型 spec 的主导成本"——风险暴露场景与小 spec 样本错配。

#### Inferred Evidence

* 小 spec Finding 少、跨角色重叠少，合并运行很可能只产生 INDEPENDENT 关系，不触发 DUPLICATE/CONTRADICTORY 等分支。

#### Unknowns

* 验收样本 spec 实际能否稳定产生跨角色重叠——TD-005 置信度记为 MEDIUM。

### Trigger Scenario

1. 实施完成，仅用小 spec 通过功能验收（数量"基本一致"）。
2. 生产中对大型 spec 运行瘦身后流水线。
3. 大型 spec 下 common.md 未加载（CR-001）/字段漂移（CR-006）的隐蔽影响放大；某角色产出缺失时 MISSING 分支从未被测；合并关系分类退化未被覆盖。
4. 质量回归未被"基本一致"阈值捕获，问题在多轮后才察觉。

### Consequence

* Verification Impact: 主要失效模式均静默，现有验收全为 happy-path 与静态字符串检查。
* Data Impact: 合并阶段可能漏标 MISSING、静默丢弃 Finding、把 DUPLICATE 当独立问题。
* Operational Impact: 缺陷潜伏至真实异常输入出现时才显现，届时无基线可比。

### Reviewer Perspectives

#### Product Perspective

**Source Findings:** —

**Assessment:** 产品评审未单独提出（PR-002/PR-003 已并入 CR-002/CR-003）。

#### System Perspective

**Source Findings:** SC-003

**Assessment:** 系统层指出验收主观且仅小 spec，与风险暴露场景错配。

#### Test Perspective

**Source Findings:** TD-003, TD-005

**Assessment:** 验证层给出可判定的负向用例（缺失一份产出→MISSING；MISSING+校验失败→INCOMPLETE；故意遗漏一条 Source Finding→校验失败）与关系分类覆盖用例（DUPLICATE/SAME_ROOT_CAUSE/CONTRADICTORY 各定义唯一预期结果）。

### Relationship Classification

SAME_ROOT_CAUSE

#### Relationship Explanation

SC-003、TD-003、TD-005 均指向"验收设计无法检出静默退化"这一根因，虽从样本错配、负向路径、合并能力三个不同面切入，但解决方向一致（补充可判定负向/覆盖用例），合并为一条。

### Conflict Analysis

#### Conflict Status

NO_CONFLICT

#### Conflicting Positions

无。

#### Conflict Evidence

不适用。

#### Resolution

无需裁决。

### Recommended Resolution

在功能验收中补充：(a) 负向用例——缺少一份角色产出→标记 MISSING；MISSING 且完整性校验失败→INCOMPLETE；输入故意遗漏一条 Source Finding→校验失败并被显式记录；(b) 合并能力用例——至少一个能产生跨角色重叠与矛盾的输入，为 DUPLICATE/SAME_ROOT_CAUSE/CONTRADICTORY 各定义唯一可观测预期；(c) 至少增加一个大型/真实 spec 样本覆盖上下文紧张场景；(d) 将"INCOMPLETE 逻辑 intact"替换为上述可观测判据。

### Source References

#### Product Review

* —

#### System Review

* SC-003

#### Test Review

* TD-003, TD-005

#### Design Spec References

* §1 量化结论
* §3.3 瘦身协议文件（consolidation-protocol.md）
* §4 质量不变量（第 4、5 条）
* §6 回滚与验收 → 功能验收

### Consolidation Decision

MERGED

#### Decision Rationale

三源收敛于"验收无法检出静默退化"，合并保留系统与验证多视角。

### Severity Change Rationale

No severity change from source findings.（SC-003 P1 / TD-003 P1 / TD-005 P1）

---

## CR-005 — 证据等级取值域（含 CONFIRMED_GAP）与现有角色/模板/协议未对齐，共享定义权威优先级未定义

### Consolidated Severity

P1

### Consolidation Confidence

MEDIUM

### Finding Status

ACCEPTED

### Underlying Problem

§3.1 将共享"证据等级"定义为四值（CONFIRMED_DEFECT / MATERIAL_RISK / CONFIRMED_GAP / DESIGN_PREFERENCE），但现有 Product 角色/模板仅承认 CONFIRMED_DEFECT / MATERIAL_RISK（且要求不把 DESIGN_PREFERENCE 作输出），System 角色无 CONFIRMED_GAP；合并/决策协议围绕既有枚举运作且未提及 CONFIRMED_GAP。设计未定义：各角色允许使用的证据等级子集是否变化、common.md 与角色/模板/协议冲突时的权威优先级、以及"各角色 evidence_class 取值域保持不变"是否应加入 §4 质量不变量。

### Evidence

#### Confirmed Evidence

* §3.1 第 58 行：证据等级四值。
* `roles/product-reviewer.md`：仅 CONFIRMED_DEFECT / MATERIAL_RISK / DESIGN_PREFERENCE，并要求不把 DESIGN_PREFERENCE 作为 Finding 输出。
* `templates/product-review.md`：evidence_class 限定为 CONFIRMED_DEFECT | MATERIAL_RISK。
* `roles/system-critic.md`：仅 CONFIRMED_DEFECT / MATERIAL_RISK / DESIGN_PREFERENCE，无 CONFIRMED_GAP。
* §4：仅把 decision 状态枚举列为权威，未涉及证据等级取值域与共享定义优先级。

#### Inferred Evidence

* CONFIRMED_GAP 可能为某角色（如 Test）专用；集中后若各角色仍各自收敛不同取值域，Machine-Readable 索引可能超出模板枚举范围，破坏合并协议消费。

#### Unknowns

* CONFIRMED_GAP 当前是否为 Test Designer 专用；合并/决策协议是否已能处理 CONFIRMED_GAP。

### Trigger Scenario

1. 实施在 common.md 写入四值证据等级。
2. Product Reviewer 依 common.md 将某 Finding 标为 CONFIRMED_GAP。
3. 同一产出的 Machine-Readable 索引依 product-review 模板仅允许 CONFIRMED_DEFECT|MATERIAL_RISK。
4. 设计未定义以哪份为准，合并阶段遇超域 evidence_class 时无处理规则。

### Consequence

* Data Impact: Machine-Readable 索引 evidence_class 可能超域，破坏合并协议直接消费。
* Operational Impact: 同等强度证据在不同角色下被标为不同等级，合并去重/关系分类失真。

### Reviewer Perspectives

#### Product Perspective

**Source Findings:** PR-004

**Assessment:** 产品层指出取值域冲突且共享定义权威优先级缺失。

#### System Perspective

**Source Findings:** SC-004

**Assessment:** 系统层指出将 CONFIRMED_GAP 提升到共享层后，若协议未同步识别该枚举，合并/决策阶段可能解析异常或静默错分。

#### Test Perspective

**Source Findings:** —

**Assessment:** —

### Relationship Classification

SAME_ROOT_CAUSE

#### Relationship Explanation

PR-004 与 SC-004 指向"证据等级枚举集中后与现有角色/协议未对齐"同一根因，合并。

### Conflict Analysis

#### Conflict Status

NO_CONFLICT

#### Conflicting Positions

无（二源一致指出对齐缺失）。

#### Conflict Evidence

不适用。

#### Resolution

无需裁决。

### Recommended Resolution

定义证据等级全局取值域与各角色允许子集，说明集中后各角色取值域是否变化（若有变化须声明为有意行为）；定义 common.md 与角色/模板/协议冲突时的权威优先级；评估将"各角色 evidence_class 取值域保持不变"加入 §4 质量不变量；§6 一致性校验扩展为枚举一致性 grep。

### Source References

#### Product Review

* PR-004

#### System Review

* SC-004

#### Test Review

* —

#### Design Spec References

* §3.1 证据等级条目（第 58 行）
* §4 第 2 条 质量不变量
* roles/product-reviewer.md / roles/system-critic.md / templates/product-review.md

### Consolidation Decision

MERGED

#### Decision Rationale

两源描述同一枚举对齐缺失根因，合并。

### Severity Change Rationale

Source findings PR-004 (P1) 与 SC-004 (P2) 不同；合并为 P1，理由：PR-004 以 CONFIRMED_DEFECT 高置信指出 Machine-Readable 索引可能超域并破坏合并协议消费，属数据完整性风险，严重程度不低于 P1。

---

## CR-006 — 共享 Finding 字段格式与 system-critic 模板实际字段互相矛盾

### Consolidated Severity

P1

### Consolidation Confidence

HIGH

### Finding Status

ACCEPTED

### Underlying Problem

§3.1 规定 common.md 统一"Finding 必填字段格式"为 `Severity / Evidence Class / Confidence / Location / Gap / Trigger Scenario / Consequence / Evidence / Recommendation`，但 `templates/system-review.md` 的实际字段为 `Severity / Evidence Class / Confidence / Location / Risk / Trigger Condition / Causal Chain / Likelihood / Reversibility / Recommendation / Evidence` 等。两者字段名（Gap vs Risk、Trigger Scenario vs Trigger Condition）与字段集（缺少 Causal Chain/Likelihood/Reversibility）均不一致。落地时必有一方被覆盖：要么 system 模板丢失去系统评审必需的因果链与可逆性分析（损害质量），要么 common.md 的"统一格式"名不副实（各角色仍各写各的，去重失败）。

### Evidence

#### Confirmed Evidence

* §3.1："Finding 必填字段格式：Severity / Evidence Class / Confidence / Location / Gap / Trigger Scenario / Consequence / Evidence / Recommendation。"
* `templates/system-review.md`：字段含 Risk / Trigger Condition / Causal Chain / Likelihood / Reversibility 等。
* §3.4：模板瘦身保留"结构骨架与字段定义"。

#### Inferred Evidence

* 设计未说明"统一格式"如何与各角色模板字段共存，字段契约分散在 common.md 与三模板中，未来增删字段需跨 4 文件协调。

#### Unknowns

* common.md 终稿是否会修订以容纳差异字段。

### Trigger Scenario

1. 实施在 common.md 写入统一字段格式（含 Gap / Trigger Scenario）。
2. system 模板按 §3.4 瘦身，保留"结构骨架与字段定义"。
3. subagent 同时看到 common.md 统一格式与 system 模板字段定义。
4. 二者不一致 → 输出字段歧义或缺失；合并阶段解析 Finding 时 Causal Chain/Reversibility 可能缺位。

### Consequence

* Data Impact: 合并协议依赖统一字段契约解析 Source Finding；字段缺失/重命名导致解析失败或静默丢字段。
* Business Impact: system 评审的因果链与可逆性分析若被"统一格式"抹除，系统评审深度下降。
* Operational Impact: 若各角色保留差异字段，common.md 未真正消除重复，§1 目标落空。

### Reviewer Perspectives

#### Product Perspective

**Source Findings:** —

**Assessment:** —

#### System Perspective

**Source Findings:** SC-002

**Assessment:** 系统层明确指出字段契约矛盾，要求 common.md 定义字段权威来源并显式列出每角色允许的差异字段。

#### Test Perspective

**Source Findings:** —

**Assessment:** —

### Relationship Classification

INDEPENDENT

#### Relationship Explanation

仅 System 评审独立识别此字段契约矛盾，Product/Test 未涉及，且它与其他 CR 根因不同（字段对齐 vs 加载契约 vs 验收），故独立保留。

### Conflict Analysis

#### Conflict Status

NO_CONFLICT

#### Conflicting Positions

无。

#### Conflict Evidence

不适用。

#### Resolution

无需裁决。

### Recommended Resolution

在 common.md 定义字段契约的权威来源，并显式列出每个角色允许的差异字段（如 system 必须保留 Risk / Trigger Condition / Causal Chain / Likelihood / Reversibility），禁止用一套统一字段列表覆盖角色独有字段；§6 一致性校验 grep 验证 common.md 与三模板字段定义无冲突。

### Source References

#### Product Review

* —

#### System Review

* SC-002

#### Test Review

* —

#### Design Spec References

* §3.1 references/common.md 字段定义
* §3.4 瘦身模板
* templates/system-review.md

### Consolidation Decision

KEPT_SEPARATE

#### Decision Rationale

单一来源、根因独立，保留为独立 Consolidated Finding 以维持决策可追溯。

### Severity Change Rationale

No severity change from source findings.（SC-002 P1）

---

## CR-007 — 「可删除内容」判定标准主观，行数/降幅目标与质量不变量优先级未定义

### Consolidated Severity

P1

### Consolidation Confidence

MEDIUM

### Finding Status

ACCEPTED

### Underlying Problem

设计给出硬性削减目标（consolidation 1583→~700、decision 1557→~700、角色各砍 ~40–50%）与主观的"砍掉"标准（"冗长 rationale、重复示例""冗余 prose""重复陈述"），但：(a) 未定义判定人与判定标准——谁、依据什么判断某段是"冗长 rationale"而非有效约束；(b) §4 未声明其七条不变量是否穷尽，而角色/协议中存在大量未被 §4 覆盖却约束输出质量的语句（如"输出不超过 5 个 Finding""不得把 MATERIAL_RISK 升格为 CONFIRMED_DEFECT"）；(c) 当保留全部有效约束后行数仍高于目标时，未规定以行数/降幅为准还是以质量约束为准。

### Evidence

#### Confirmed Evidence

* §2 / §3.2 / §3.3：数值化削减目标与"砍掉"列主观描述。
* §4 第 91 行："以下规则一条不动"列七条，全文未声明是否穷尽。
* `roles/product-reviewer.md`：多条未被 §4 覆盖的规范性约束（数量上限、证据等级不得升格、禁止制造 Finding 等）。
* §6 一致性校验仅 grep CR-ID / decision 枚举 / Finding Type 三项，无"规范性语句是否完整保留"的检查。

#### Inferred Evidence

* 现有角色与协议中存在大量未被 §4 覆盖但对输出质量有实质约束的语句。

#### Unknowns

* 协议文件中"冗长 rationale"实际占比——完整保留约束前提下能否达成行数目标未测量。

### Trigger Scenario

1. 实施按 §2 改写 consolidation-protocol.md（1583→~700）。
2. 删到 ~850 行仍高于目标，剩余含既像"冗长 rationale"又承载判定约束的段落。
3. §4 未声明穷尽，设计无判定标准；执行者为达成行数目标删除该段。
4. §6 功能验收因 CR-002 所述原因无法发现质量变化，删除被固化。

### Consequence

* Operational Impact: 删除决策依赖执行者个人判断，而硬性行数指标反向驱动"多删"，唯一质量护栏 §4 覆盖面小于现有规范性语句总量。
* Maintenance Impact: 承载质量的约束被静默移除，且设计未要求记录删除项，后续维护者无法区分有意删除与误删，也无法定向回滚（§6 回滚为整体 git revert）。

### Reviewer Perspectives

#### Product Perspective

**Source Findings:** PR-005

**Assessment:** 产品层要求声明 §4 穷尽性、明确行数目标为参考值、要求附"删除项清单"。

#### System Perspective

**Source Findings:** —

**Assessment:** —

#### Test Perspective

**Source Findings:** —

**Assessment:** —

### Relationship Classification

INDEPENDENT

#### Relationship Explanation

仅 Product 评审独立识别此执行风险，根因独立（删除判定与优先级），保留为独立 CR。

### Conflict Analysis

#### Conflict Status

NO_CONFLICT

#### Conflicting Positions

无。

#### Conflict Evidence

不适用。

#### Resolution

无需裁决。

### Recommended Resolution

补充三条最小规则：(1) 声明 §4 是否穷尽；若不穷尽，要求"删除任一规范性语句（祈使句约束/禁止项/数量上限）需逐条记录理由"；(2) 明确行数目标与 ≥40% 降幅为参考值，与质量约束冲突时以保留约束优先，并规定处理方式（接受较小降幅或转入方案 B）；(3) 要求瘦身产出附"删除项清单"使删除可复核、可定向恢复。

### Source References

#### Product Review

* PR-005

#### System Review

* —

#### Test Review

* —

#### Design Spec References

* §2 目标文件结构（第 37–40 行）
* §3.2 / §3.3 砍掉列
* §4 质量不变量（第 89–98 行）
* §6 一致性校验（第 119 行）

### Consolidation Decision

KEPT_SEPARATE

#### Decision Rationale

单一来源、根因独立，保留独立以追溯执行风险。

### Severity Change Rationale

No severity change from source findings.（PR-005 P1）

---

## CR-008 — `references/common.md` 成为单点共享依赖，存在部分部署/版本错配风险

### Consolidated Severity

P2

### Consolidation Confidence

LOW

### Finding Status

ACCEPTED

### Underlying Problem

`references/common.md` 首次引入，成为三角色 + 多模板共同依赖的单一共享定义源。设计以单次 git commit 原子落地为前提（§6 留底 + git revert），但未考虑非原子变更（部分文件提交、分支 cherry-pick、缓存的旧 subagent 提示词）会出现"角色引用 common.md 但 common.md 缺失/半写"的中间态，导致三个 subagent 同时失效，故障面从单角色扩大为全角色；新增 `references/` 目录若未被索引/加载逻辑同步，存在引用路径失效风险。

### Evidence

#### Confirmed Evidence

* §2：新增 references/common.md 为共享定义源。
* §3.1–3.2：角色/模板引用之。
* §6：回滚依赖 git revert，未提及部分部署防护。

#### Inferred Evidence

* skill 以 git 仓库方式分发，存在副本/缓存可能，旧提示词可能仍内联旧定义，与新 common.md 并存时引发双源冲突。

#### Unknowns

* 现有 orchestrator 是否已处理 references/ 路径加载。

### Trigger Scenario

1. 某次后续变更只提交部分角色/模板而未同步 common.md（或部分 revert）。
2. 运行的 subagent 加载到引用 common.md 的角色文件，但 common.md 缺失/半写。
3. 三个 subagent 因缺少共享定义同时行为异常或报错。
4. 故障面从单角色扩大为全角色。

### Consequence

* Availability Impact: 单点共享文件异常同时拖垮三角色并行审核，扩大故障爆炸半径。
* Operational Impact: 故障表现为"审核产出异常"而非"文件缺失报错"，诊断成本上升。
* Maintenance Impact: 新增单一共享源后，任何跨角色定义变更都需谨慎协调，长期耦合上升。

### Reviewer Perspectives

#### Product Perspective

**Source Findings:** —

**Assessment:** —

#### System Perspective

**Source Findings:** SC-005

**Assessment:** 系统层指出单点依赖放大故障面，建议"common.md 与引用它的角色/模板必须同批变更"作为硬约束，并在发布前校验引用可解析。

#### Test Perspective

**Source Findings:** —

**Assessment:** —

### Relationship Classification

INDEPENDENT

#### Relationship Explanation

仅 System 评审识别此结构性维护风险，根因独立（单点依赖的发布安全），与 CR-001（加载契约缺失）互补但可独立决策，保留为独立 P2 CR。

### Conflict Analysis

#### Conflict Status

NO_CONFLICT

#### Conflicting Positions

无。

#### Conflict Evidence

不适用。

#### Resolution

无需裁决。

### Recommended Resolution

将"common.md 与引用它的角色/模板必须同批变更"写入变更规范；在 SKILL.md/CLAUDE.md/orchestrator 显式登记 references/ 路径；§6 一致性校验增加"所有对 common.md 的引用均可解析"的检查，防止悬空引用。

### Source References

#### Product Review

* —

#### System Review

* SC-005

#### Test Review

* —

#### Design Spec References

* §2 目标文件结构
* §3.1 references/common.md
* §6 回滚

### Consolidation Decision

KEPT_SEPARATE

#### Decision Rationale

单一来源、根因独立（发布安全/耦合），保留独立 P2 CR。

### Severity Change Rationale

No severity change from source findings.（SC-005 P2）

---

# Unmerged Source Findings

无。全部 15 条源 Finding 均已并入上述 8 条 Consolidated Finding（MERGED 或 KEPT_SEPARATE），无独立保留的未合并项。

---

# Duplicate and Superseded Findings

无。源 Finding 均通过合并保留可追溯性，无标记为 DUPLICATE / REPRESENTED_ELSEWHERE 的项。

---

# Cross-Reviewer Conflicts

无跨评审员矛盾。三位评审员独立识别出互补的缺口，结论一致收敛，未出现相互排斥的立场。所有 Consolidated Finding 的 Conflict Status 均为 NO_CONFLICT。

---

# Coverage Gaps

No coverage gaps — all three source reviews are available.

---

# Coverage Matrix

| Consolidated Finding | Product | System | Test    | Primary Risk Area |
| -------------------- | ------- | ------ | ------- | ----------------- |
| CR-001               | PR-001  | SC-001 | TD-002  | 独立评审不变量 / 运行时加载 |
| CR-002               | PR-002  | —      | TD-001  | 验收可判定性 / 质量护栏 |
| CR-003               | PR-003  | —      | TD-004  | 量化目标可复现性 |
| CR-004               | —       | SC-003 | TD-003, TD-005 | 验收覆盖 / 静默退化 |
| CR-005               | PR-004  | SC-004 | —       | 枚举一致性 |
| CR-006               | —       | SC-002 | —       | 字段契约一致性 |
| CR-007               | PR-005  | —      | —       | 删除执行风险 |
| CR-008               | —       | SC-005 | —       | 单点依赖 / 发布安全 |

---

# Review Coverage Summary

| Review Dimension       | Product  | System   | Test     | Consolidated Findings |
| ---------------------- | -------- | -------- | -------- | --------------------- |
| Business Rules         | REVIEWED | REVIEWED | REVIEWED | CR-002, CR-005, CR-007 |
| User Workflow          | REVIEWED | REVIEWED | REVIEWED | CR-001 |
| State Transitions      | —        | REVIEWED | REVIEWED | CR-004 |
| Data Integrity         | REVIEWED | REVIEWED | REVIEWED | CR-005, CR-006, CR-004 |
| Security               | —        | REVIEWED | REVIEWED | CR-001 |
| Availability           | —        | REVIEWED | REVIEWED | CR-008, CR-004 |
| Failure Recovery       | REVIEWED | REVIEWED | REVIEWED | CR-004 |
| Backward Compatibility | REVIEWED | REVIEWED | REVIEWED | CR-005 |
| Operational Complexity | REVIEWED | REVIEWED | REVIEWED | CR-003, CR-007 |
| Testability            | REVIEWED | REVIEWED | REVIEWED | CR-002, CR-003, CR-004 |
| Observability          | REVIEWED | REVIEWED | REVIEWED | CR-001, CR-004 |

---

# Superpowers Instructions

## What to Read

- **Consolidated Review**: 本文档
- **Source Reviews**: 见 Source Reviews 表（product-review.md / system-review.md / test-review.md）

## What to Decide

For each Consolidated Finding in the Decision Queue below, set a decision:

| CR-ID | Title | Severity | Decision (choose one) |
|-------|-------|----------|----------------------|
| CR-001 | 共享定义 common.md 未纳入 subagent 加载契约 | P0 | ___ |
| CR-002 | 「不损失审核质量」缺少可判定验收判据 | P0 | ___ |
| CR-003 | ≥40% token 降幅基线/口径/工具不可复现 | P1 | ___ |
| CR-004 | 验收无法检出静默退化（负向路径/合并能力/样本错配） | P1 | ___ |
| CR-005 | 证据等级枚举与现有角色/协议未对齐 | P1 | ___ |
| CR-006 | 共享字段格式与 system 模板字段矛盾 | P1 | ___ |
| CR-007 | 可删除内容判定主观，行数目标与质量优先级未定义 | P1 | ___ |
| CR-008 | common.md 单点共享依赖的部分部署风险 | P2 | ___ |

**Decision options**: PENDING_DECISION, ACCEPTED, REJECTED, DEFERRED, PARTIALLY_ACCEPTED, DUPLICATE, INVALIDATED

## Decision Template

For each finding, copy and fill in the following in the Decision Records section below:

```markdown
## DR-<NNN> — CR-<NNN>

### Decision Status

ACCEPTED_DECISION / ACCEPTED / REJECTED / DEFERRED / PARTIALLY_ACCEPTED / DUPLICATE / INVALIDATED

### Decision Owner

<your name or role>

### Decision Rationale

<Why this decision was made — must address the finding's validity, materiality, and evidence>

### Required Action

<If ACCEPTED: what must change in the Design Spec>

### Decision Date

<YYYY-MM-DD>
```

## Hard Rules

1. A Finding with status PENDING_DECISION cannot have a final review state of APPROVED
2. All P0 findings must be resolved (not PENDING_DECISION) before the final review state can be anything other than BLOCKED
3. Every decision must have a Decision Owner, Rationale, and Date

## Final Review State

After all decisions are recorded, determine the final review state:

| Condition | State |
|-----------|-------|
| Any unresolved P0 finding | BLOCKED |
| Accepted P1/P2 changes outstanding | CHANGES_REQUIRED |
| No blocking finding, conditions remain | CONDITIONAL_APPROVAL |
| All required changes incorporated | APPROVED |
| Review records incomplete | INCOMPLETE |

Write the final review state at the bottom of the Consolidation Conclusion section.

---

# Decision Queue

## DQ-001 — CR-001

### Problem

共享定义 common.md 被角色/模板引用，但 subagent 加载清单不含它，独立评审不变量面临静默失效。

### Severity

P0

### Evidence Summary

§3.1–3.2 要求角色删除共享块改引用 common.md；§5 加载清单仍为 roles+templates+spec，未含 common.md。三位评审员（产品/系统/验证）独立确认此为根因。

### Recommended Resolution

将 common.md 纳入 subagent 权威加载清单，并在 §6 增加独立性指令仍存在于 subagent 上下文的校验点。

### Decision Required

是否在实施前修改 subagent 加载清单以包含 references/common.md（或定义等效注入方式）？

### Decision Status

ACCEPTED

---

## DQ-002 — CR-002

### Problem

"不损失审核质量"无可用收验收阈值，回滚触发条件不可执行。

### Severity

P0

### Evidence Summary

§6 唯一质量判据为"Finding 数量与严重度分布基本一致"，无阈值、无判定人、无消除 LLM 波动的比较协议。

### Recommended Resolution

定义基线波动测量（N≥2 次）、量化"基本一致"口径、明确判定责任人、至少一大型 spec 样本、回滚触发条件与上述判据对应。

### Decision Required

是否接受将质量约束改为可判定验收（含波动基线与量化阈值）？

### Decision Status

ACCEPTED

---

## DQ-003 — CR-003

### Problem

≥40% token 降幅的基线、口径、测量工具均不固定，量化验收结论不唯一。

### Severity

P1

### Evidence Summary

§1 基线为 40–78K 区间且口径自相矛盾；§6 工具位于 /tmp 且允许"同类脚本"替换；§2 行数目标用近似值。

### Recommended Resolution

记录定值基线及测量条件；工具纳入仓库或写死估算规则；明确行数目标硬/参考。

### Decision Required

是否接受锁定测量口径与工具以保证降幅可复算？

### Decision Status

ACCEPTED

---

## DQ-004 — CR-004

### Problem

验收仅小 spec 正常跑通，无法检出负向路径与合并能力退化等静默失效。

### Severity

P1

### Evidence Summary

§6 happy-path 不触发 MISSING/INCOMPLETE/完整性校验；§3.3 压缩最重的合并关系分类在小 spec 不触发；§1 风险暴露场景与小 spec 样本错配。

### Recommended Resolution

补充负向用例（MISSING/INCOMPLETE/校验失败）、合并关系分类覆盖用例、至少一大型 spec 样本。

### Decision Required

是否接受扩充验收以覆盖负向路径与合并能力？

### Decision Status

ACCEPTED

---

## DQ-005 — CR-005

### Problem

证据等级枚举（含 CONFIRMED_GAP）与现有角色/模板/协议未对齐，共享定义权威优先级未定义。

### Severity

P1

### Evidence Summary

§3.1 四值证据等级；product 模板仅允许两值、system 角色无 CONFIRMED_GAP；§4 未将证据等级取值域列为权威。

### Recommended Resolution

定义全局取值域与每角色子集、冲突时权威优先级、评估将取值域加入 §4 不变量、扩展一致性校验为枚举 grep。

### Decision Required

是否接受对齐证据等级枚举并定义共享定义权威优先级？

### Decision Status

ACCEPTED

---

## DQ-006 — CR-006

### Problem

共享 Finding 字段格式（Gap/Trigger Scenario）与 system 模板实际字段（Risk/Trigger Condition/Causal Chain…）矛盾。

### Severity

P1

### Evidence Summary

§3.1 统一字段列表与 system-review 模板字段集不一致，落地时必有一方被覆盖。

### Recommended Resolution

common.md 定义字段权威来源并显式列出每角色允许差异字段；一致性校验 grep 字段冲突。

### Decision Required

是否接受在 common.md 定义字段契约权威源并保留角色差异字段？

### Decision Status

ACCEPTED

---

## DQ-007 — CR-007

### Problem

"可删除内容"判定主观，§4 穷尽性未声明，行数/降幅目标与质量不变量优先级未定义。

### Severity

P1

### Evidence Summary

§2/§3.2/§3.3 数值目标 + 主观"砍掉"标准；§4 未声明穷尽；大量未被 §4 覆盖的规范性语句约束输出质量；§6 校验仅 grep 三项。

### Recommended Resolution

声明 §4 穷尽性、行数目标为参考值优先保留质量约束、附删除项清单。

### Decision Required

是否接受明确删除判定标准与质量优先级？

### Decision Status

ACCEPTED

---

## DQ-008 — CR-008

### Problem

common.md 单点共享依赖，部分部署/版本错配会同时拖垮三角色。

### Severity

P2

### Evidence Summary

§2 新增单点共享源；§6 回滚依赖 git revert，未考虑非原子变更与缓存旧提示词。

### Recommended Resolution

common.md 与引用方同批变更硬约束；登记 references/ 路径；校验引用可解析。

### Decision Required

是否接受将同批变更与引用可解析检查纳入变更规范？

### Decision Status

ACCEPTED

---

# Decision Records

（以下记录由 Spec 所有者委托主 agent 逐条决议，全部 8 条 Consolidated Finding 均为 ACCEPTED，修订待落实。）

## DR-001 — CR-001

### Decision

ACCEPTED

### Decision Date

2026-08-04

### Decision Maker

yy-spec-review（主 agent，受 Spec 所有者委托决策）

### Decision Rationale

三份独立评审（PR-001 / SC-001 / TD-002）独立收敛于同一根因，证据确凿：§3.1–3.2 将严重度、证据等级、Finding 格式与独立评审规则抽离至 common.md 并要求角色引用，但 §5 的 subagent 加载清单只含 roles + templates + spec，不含 common.md。若不修复，独立评审/上下文隔离不变量在 subagent 隔离上下文中根本不存在，且失效静默、不被现有验收发现。实施前一行清单变更即可消除，成本低收益高，故接受。

### Action Taken

待实施：在 §5 将 `references/common.md` 加入 subagent 权威加载清单（与 roles/templates/spec 并列），并显式定义注入方式；§6 一致性校验增加“独立性指令仍存在于 subagent 上下文”的校验点。

### Final Resolution

待 spec 修订后确认。

### Verification

修订后重跑小 spec 审核，grep subagent 提示词是否含 common.md 路径。

### Related Changes

* <Spec revision>

### Processing Status

ACCEPTED

---

## DR-002 — CR-002

### Decision

ACCEPTED

### Decision Date

2026-08-04

### Decision Maker

yy-spec-review（主 agent，受 Spec 所有者委托决策）

### Decision Rationale

§6 唯一质量判据“Finding 数量与严重度分布基本一致”无可判定阈值、无判定责任人、无消除 LLM 运行波动的比较协议，导致“质量下降 → git revert”的回滚规则无可执行触发条件——质量回归可能被当作正常波动放行，或正常波动被误判为回归。作为方案首要约束，必须转为可判定判据。接受。

### Action Taken

待实施：定义基线波动测量（同一 spec 改动前后各运行 N≥2 次记录波动范围）；定义“基本一致”的量化口径（建议以 P0/P1 所指向问题是否仍被覆盖为准，而非仅比数量）；明确判定责任人；验收样本至少含一个大型 spec 或显式声明并接受小 spec 局限；回滚触发条件与上述判据一一对应。

### Final Resolution

待 spec 修订后确认。

### Verification

修订后以小 spec + 大型 spec 双样本跑通，记录关键 Finding 复现率。

### Related Changes

* <Spec revision>

### Processing Status

ACCEPTED

---

## DR-003 — CR-003

### Decision

ACCEPTED

### Decision Date

2026-08-04

### Decision Maker

yy-spec-review（主 agent，受 Spec 所有者委托决策）

### Decision Rationale

“≥40%” 形式数值但基线（§1 给 40–78K 且口径自相矛盾）、统计对象（common.md 是否计入 / spec 4× 是否计入 / 静态字数 vs 运行时）、测量工具（/tmp 脚本且允许“同类脚本”替换）三项均不固定，降幅结论不唯一，核心量化目标事实未被验证。接受，需锁定口径。

### Action Taken

待实施：记录定值基线及测量条件（所用 spec、纳入文件清单、是否计入 spec 多次读取）；分析脚本纳入仓库或写死估算规则，禁止“同类脚本”替换；明确 §2 行数目标为硬上限还是参考值；验收留存“基线值 / 改动后值 / 降幅 / 测量条件”四元组可复算。

### Final Resolution

待 spec 修订后确认。

### Verification

修订后重跑分析器，四元组可复算且降幅口径唯一。

### Related Changes

* <Spec revision>

### Processing Status

ACCEPTED

---

## DR-004 — CR-004

### Decision

ACCEPTED

### Decision Date

2026-08-04

### Decision Maker

yy-spec-review（主 agent，受 Spec 所有者委托决策）

### Decision Rationale

§6 仅小 spec happy-path，MISSING/INCOMPLETE 与 Source Finding 完整性校验在 happy-path 下不触发，被压缩最重的合并关系分类（DUPLICATE/SAME_ROOT_CAUSE/CONTRADICTORY 等）在小 spec 少重叠时不覆盖，而 §1 自承风险暴露于上下文更大、并发更高的大规模场景——样本与风险暴露场景错配。接受。

### Action Taken

待实施：补充负向用例（缺一份产出→MISSING；MISSING 且校验失败→INCOMPLETE；故意遗漏一条 Source Finding→校验失败并显式记录）；合并能力用例（DUPLICATE/SAME_ROOT_CAUSE/CONTRADICTORY 各定义唯一可观测预期）；至少增加一个大型/真实 spec 样本覆盖上下文紧张；以可观测判据替换“INCOMPLETE 逻辑 intact”。

### Final Resolution

待 spec 修订后确认。

### Verification

修订后注入负向与矛盾输入，确认校验与关系分类被正确触发。

### Related Changes

* <Spec revision>

### Processing Status

ACCEPTED

---

## DR-005 — CR-005

### Decision

ACCEPTED

### Decision Date

2026-08-04

### Decision Maker

yy-spec-review（主 agent，受 Spec 所有者委托决策）

### Decision Rationale

§3.1 四值证据等级（含 CONFIRMED_GAP）；product 模板仅允许 CONFIRMED_DEFECT|MATERIAL_RISK、system 角色无 CONFIRMED_GAP；§4 仅把 decision 状态枚举列为权威，未涉及证据等级取值域与共享定义优先级。合并/决策协议围绕既有枚举运作且未识别 CONFIRMED_GAP，可能超域解析异常或静默错分。接受。

### Action Taken

待实施：定义证据等级全局取值域与各角色允许子集，说明集中后各角色取值域是否变化（若有变化须声明为有意行为）；定义 common.md 与角色/模板/协议冲突时的权威优先级；评估将“各角色 evidence_class 取值域保持不变”加入 §4 质量不变量；§6 一致性校验扩展为枚举一致性 grep。

### Final Resolution

待 spec 修订后确认。

### Verification

修订后 grep 三模板 evidence_class 枚举，确认与 common.md 取值域一致。

### Related Changes

* <Spec revision>

### Processing Status

ACCEPTED

---

## DR-006 — CR-006

### Decision

ACCEPTED

### Decision Date

2026-08-04

### Decision Maker

yy-spec-review（主 agent，受 Spec 所有者委托决策）

### Decision Rationale

§3.1 统一字段格式（Gap/Trigger Scenario 等）与 system-review 模板实际字段（Risk/Trigger Condition/Causal Chain/Likelihood/Reversibility 等）矛盾。落地时必有一方被覆盖：要么 system 丢失去系统评审必需的因果链与可逆性分析（损质量），要么“统一格式”名不副实（去重失败）。接受。

### Action Taken

待实施：common.md 定义字段契约的权威来源，并显式列出每个角色允许的差异字段（如 system 必须保留 Risk/Trigger Condition/Causal Chain/Likelihood/Reversibility），禁止用一套统一字段列表覆盖角色独有字段；§6 一致性校验 grep 验证 common.md 与三模板字段定义无冲突。

### Final Resolution

待 spec 修订后确认。

### Verification

修订后 grep 校验 common.md 与三模板字段定义无冲突。

### Related Changes

* <Spec revision>

### Processing Status

ACCEPTED

---

## DR-007 — CR-007

### Decision

ACCEPTED

### Decision Date

2026-08-04

### Decision Maker

yy-spec-review（主 agent，受 Spec 所有者委托决策）

### Decision Rationale

硬性行数/降幅目标（consolidation 1583→~700 等）与主观“砍掉”标准并存，但：未定义判定人与判定标准；§4 未声明是否穷尽，角色/协议中存在大量未被 §4 覆盖却约束输出质量的语句；行数目标与质量约束冲突时优先级未定义。硬性行数指标反向驱动“多删”，唯一质量护栏 §4 覆盖面小于现状。接受。

### Action Taken

待实施：声明 §4 是否穷尽；若不穷尽，要求“删除任一规范性语句（祈使句约束/禁止项/数量上限）需逐条记录理由”；明确行数目标与 ≥40% 降幅为参考值，与质量约束冲突时以保留约束优先（接受较小降幅或转入方案 B）；要求瘦身产出附“删除项清单”使删除可复核、可定向恢复。

### Final Resolution

待 spec 修订后确认。

### Verification

实施时附删除项清单，逐条对照 §4 与角色规范性语句。

### Related Changes

* <Spec revision>

### Processing Status

ACCEPTED

---

## DR-008 — CR-008

### Decision

ACCEPTED

### Decision Date

2026-08-04

### Decision Maker

yy-spec-review（主 agent，受 Spec 所有者委托决策）

### Decision Rationale

common.md 首次引入为三角色 + 多模板的单点共享源；设计以单次原子 git commit 为前提，但未考虑非原子变更（部分提交、cherry-pick、缓存旧提示词）出现“角色引用 common.md 但 common.md 缺失/半写”的中间态，故障面从单角色扩大为全角色；references/ 路径若未被索引/加载逻辑同步则存在悬空引用风险。虽置信度 LOW 且存在未知（orchestrator 是否已处理 references/ 加载），但缓解措施（同批变更 + 引用可解析校验）成本低，且与 CR-001 修复互补，故接受。

### Action Taken

待实施：将“common.md 与引用它的角色/模板必须同批变更”写入变更规范；在 SKILL.md/CLAUDE.md/orchestrator 显式登记 references/ 路径；§6 一致性校验增加“所有对 common.md 的引用均可解析”的检查，防止悬空引用。

### Final Resolution

待 spec 修订后确认。

### Verification

修订后校验所有 common.md 引用均可解析。

### Related Changes

* <Spec revision>

### Processing Status

ACCEPTED

---

# Finding Lifecycle

The lifecycle of every consolidated finding is:

```text
PENDING_DECISION
  ↓
ACCEPTED / REJECTED / DEFERRED / PARTIALLY_ACCEPTED / DUPLICATE / INVALIDATED
```

A Finding must not disappear from the review merely because it was rejected, deferred, considered unnecessary, or fixed in a later revision. Its history must remain available for future analysis.

---

# Review Statistics

## Finding Counts

### By Source Review

* Product Findings: 5
* System Findings: 5
* Test Findings: 5

### After Consolidation

* Consolidated Findings: 8
* Unmerged Findings: 0
* Duplicate Findings: 0
* Superseded Findings: 0
* Cross-Reviewer Conflicts: 0

### By Severity

* P0: 2
* P1: 5
* P2: 1

### By Status

* PENDING_DECISION: 0
* ACCEPTED: 8
* REJECTED: 0
* DEFERRED: 0
* PARTIALLY_ACCEPTED: 0
* DUPLICATE: 0
* INVALIDATED: 0

---

# Consolidation Conclusion

### Consolidation Result

COMPLETED

### Decision Readiness

DECIDED

### Summary

三份独立审核（15 条源 Finding）已成功合并为 8 条 Consolidated Finding，无源 Finding 静默丢失，Source Finding 完整性校验通过（15 = 15 + 0 + 0）。全部 8 条 Consolidated Finding 已由 Spec 所有者委托主 agent 逐条决议，均为 ACCEPTED（含 2 条 P0：CR-001、CR-002）。决议确认设计在实施前须修订——尤其 CR-001（common.md 纳入 subagent 加载契约）与 CR-002（质量约束转为可判定验收）。无跨评审员矛盾。

### Final Review State

CHANGES_REQUIRED

（依据 Superpowers Instructions：所有 P0 已决议（ACCEPTED），无未解决 P0；存在已接受但未落实的 spec 修订项，故为 CHANGES_REQUIRED。）

---

# Machine-Readable Consolidation Index

```yaml
review:
  review_id: "2026-08-04-review-001"
  review_type: "CONSOLIDATED_REVIEW"
  status: "COMPLETED"
  design_spec: "docs/superpowers/specs/2026-08-04-spec-review-slim-design.md"
  round: 1
  spec_stem: "spec-review-slim-design"
  final_review_state: "CHANGES_REQUIRED"

source_reviews:
  - reviewer: "yy-product-reviewer"
    review_type: "PRODUCT_REVIEW"
    review_id: "2026-08-04-review-001"
    source_file: "docs/superpowers/reviews/spec-review-slim-design/2026-08-04-review-001/product-review.md"
    status: "AVAILABLE"
  - reviewer: "yy-system-critic"
    review_type: "SYSTEM_REVIEW"
    review_id: "2026-08-04-review-001"
    source_file: "docs/superpowers/reviews/spec-review-slim-design/2026-08-04-review-001/system-review.md"
    status: "AVAILABLE"
  - reviewer: "yy-test-designer"
    review_type: "TEST_REVIEW"
    review_id: "2026-08-04-review-001"
    source_file: "docs/superpowers/reviews/spec-review-slim-design/2026-08-04-review-001/test-review.md"
    status: "AVAILABLE"

consolidated_findings:
  - id: "CR-001"
    title: "共享定义 references/common.md 未纳入 subagent 加载契约，独立评审核心不变量面临静默失效"
    severity: "P0"
    confidence: "HIGH"
    status: "ACCEPTED"
    source_findings:
      product: ["PR-001"]
      system: ["SC-001"]
      test: ["TD-002"]
    finding_type: "N/A"
    relationship_classification: "SAME_ROOT_CAUSE"
    conflict_status: "NO_CONFLICT"
    source_references: ["§3.1", "§3.2", "§5", "§4 第6条"]
    processing_status: "ACCEPTED"
    severity_escalation: false
    severity_change_rationale: null
  - id: "CR-002"
    title: "「不损失审核质量」缺少可判定验收判据，回滚触发条件不可执行"
    severity: "P0"
    confidence: "HIGH"
    status: "ACCEPTED"
    source_findings:
      product: ["PR-002"]
      system: []
      test: ["TD-001"]
    finding_type: "UNTESTABLE_REQUIREMENT"
    relationship_classification: "SAME_ROOT_CAUSE"
    conflict_status: "NO_CONFLICT"
    source_references: ["目标陈述", "§6 回滚与验收", "§1"]
    processing_status: "ACCEPTED"
    severity_escalation: false
    severity_change_rationale: null
  - id: "CR-003"
    title: "≥40% token 降幅的基线、口径与测量工具不可复现"
    severity: "P1"
    confidence: "HIGH"
    status: "ACCEPTED"
    source_findings:
      product: ["PR-003"]
      system: []
      test: ["TD-004"]
    finding_type: "UNTESTABLE_REQUIREMENT"
    relationship_classification: "SAME_ROOT_CAUSE"
    conflict_status: "NO_CONFLICT"
    source_references: ["目标陈述", "§1", "§2", "§6 静态验收"]
    processing_status: "ACCEPTED"
    severity_escalation: false
    severity_change_rationale: null
  - id: "CR-004"
    title: "验收设计无法检出静默退化：负向路径/合并能力/样本错配"
    severity: "P1"
    confidence: "HIGH"
    status: "ACCEPTED"
    source_findings:
      product: []
      system: ["SC-003"]
      test: ["TD-003", "TD-005"]
    finding_type: "ACCEPTANCE_TEST"
    relationship_classification: "SAME_ROOT_CAUSE"
    conflict_status: "NO_CONFLICT"
    source_references: ["§4 第4/5条", "§3.3", "§6 功能验收", "§1"]
    processing_status: "ACCEPTED"
    severity_escalation: false
    severity_change_rationale: null
  - id: "CR-005"
    title: "证据等级枚举（含 CONFIRMED_GAP）与现有角色/协议未对齐"
    severity: "P1"
    confidence: "MEDIUM"
    status: "ACCEPTED"
    source_findings:
      product: ["PR-004"]
      system: ["SC-004"]
      test: []
    finding_type: "N/A"
    relationship_classification: "SAME_ROOT_CAUSE"
    conflict_status: "NO_CONFLICT"
    source_references: ["§3.1 证据等级", "§4 第2条", "roles/*", "templates/*"]
    processing_status: "ACCEPTED"
    severity_escalation: true
    severity_change_rationale: "PR-004(P1) 与 SC-004(P2) 合并为 P1：PR-004 以高置信指出 Machine-Readable 索引可能超域并破坏合并协议消费，属数据完整性风险。"
  - id: "CR-006"
    title: "共享 Finding 字段格式与 system-critic 模板实际字段互相矛盾"
    severity: "P1"
    confidence: "HIGH"
    status: "ACCEPTED"
    source_findings:
      product: []
      system: ["SC-002"]
      test: []
    finding_type: "N/A"
    relationship_classification: "INDEPENDENT"
    conflict_status: "NO_CONFLICT"
    source_references: ["§3.1", "§3.4", "templates/system-review.md"]
    processing_status: "ACCEPTED"
    severity_escalation: false
    severity_change_rationale: null
  - id: "CR-007"
    title: "可删除内容判定主观，行数/降幅目标与质量不变量优先级未定义"
    severity: "P1"
    confidence: "MEDIUM"
    status: "ACCEPTED"
    source_findings:
      product: ["PR-005"]
      system: []
      test: []
    finding_type: "N/A"
    relationship_classification: "INDEPENDENT"
    conflict_status: "NO_CONFLICT"
    source_references: ["§2", "§3.2", "§3.3", "§4", "§6 一致性校验"]
    processing_status: "ACCEPTED"
    severity_escalation: false
    severity_change_rationale: null
  - id: "CR-008"
    title: "references/common.md 成为单点共享依赖，存在部分部署/版本错配风险"
    severity: "P2"
    confidence: "LOW"
    status: "ACCEPTED"
    source_findings:
      product: []
      system: ["SC-005"]
      test: []
    finding_type: "N/A"
    relationship_classification: "INDEPENDENT"
    conflict_status: "NO_CONFLICT"
    source_references: ["§2", "§3.1", "§6 回滚"]
    processing_status: "ACCEPTED"
    severity_escalation: false
    severity_change_rationale: null

unmerged_findings: []
duplicate_or_represented: []
conflicts: []
decision_queue:
  - id: "DQ-001"
    finding_id: "CR-001"
    severity: "P0"
    processing_status: "ACCEPTED"
  - id: "DQ-002"
    finding_id: "CR-002"
    severity: "P0"
    processing_status: "ACCEPTED"
  - id: "DQ-003"
    finding_id: "CR-003"
    severity: "P1"
    processing_status: "ACCEPTED"
  - id: "DQ-004"
    finding_id: "CR-004"
    severity: "P1"
    processing_status: "ACCEPTED"
  - id: "DQ-005"
    finding_id: "CR-005"
    severity: "P1"
    processing_status: "ACCEPTED"
  - id: "DQ-006"
    finding_id: "CR-006"
    severity: "P1"
    processing_status: "ACCEPTED"
  - id: "DQ-007"
    finding_id: "CR-007"
    severity: "P1"
    processing_status: "ACCEPTED"
  - id: "DQ-008"
    finding_id: "CR-008"
    severity: "P2"
    processing_status: "ACCEPTED"

decisions:
  - cr_id: "CR-001"
    decision: "ACCEPTED"
    decision_maker: "yy-spec-review (main agent, delegated by Spec owner)"
    decision_date: "2026-08-04"
  - cr_id: "CR-002"
    decision: "ACCEPTED"
    decision_maker: "yy-spec-review (main agent, delegated by Spec owner)"
    decision_date: "2026-08-04"
  - cr_id: "CR-003"
    decision: "ACCEPTED"
    decision_maker: "yy-spec-review (main agent, delegated by Spec owner)"
    decision_date: "2026-08-04"
  - cr_id: "CR-004"
    decision: "ACCEPTED"
    decision_maker: "yy-spec-review (main agent, delegated by Spec owner)"
    decision_date: "2026-08-04"
  - cr_id: "CR-005"
    decision: "ACCEPTED"
    decision_maker: "yy-spec-review (main agent, delegated by Spec owner)"
    decision_date: "2026-08-04"
  - cr_id: "CR-006"
    decision: "ACCEPTED"
    decision_maker: "yy-spec-review (main agent, delegated by Spec owner)"
    decision_date: "2026-08-04"
  - cr_id: "CR-007"
    decision: "ACCEPTED"
    decision_maker: "yy-spec-review (main agent, delegated by Spec owner)"
    decision_date: "2026-08-04"
  - cr_id: "CR-008"
    decision: "ACCEPTED"
    decision_maker: "yy-spec-review (main agent, delegated by Spec owner)"
    decision_date: "2026-08-04"
statistics:
  source_findings:
    product: 5
    system: 5
    test: 5
  consolidated_findings: 8
  unmerged_findings: 0
  duplicate_findings: 0
  represented_elsewhere_findings: 0
  conflicts: 0
  p0: 2
  p1: 5
  p2: 1
```
