# Product Review

## 输出语言

本审核的所有描述性内容使用中文撰写；Finding ID、严重度/证据等级/置信度等大写枚举、文件路径保持英文（遵循模板要求）。

## Review Metadata

### Review ID

2026-08-04-review-002

### Reviewer

yy-product-reviewer

### Review Type

PRODUCT_REVIEW

### Design Spec

/Users/yuezhenhua/yonyou/AI/skills/yy-spec-review/docs/superpowers/specs/2026-08-04-spec-review-slim-design.md

### Review Date

2026-08-04

### Review Status

COMPLETED

---

## Review Scope

本审核从产品正确性、业务规则完整性、用户/角色行为、工作流完整性、运营可操作性角度评估该 Design Spec。

本审核不评估：实现质量、源码质量、详细系统架构、技术选型、基础设施、性能优化、测试实现细节。

本审核目的：识别在"不损失审核质量、不改变三角色并行独立审核架构"这一既定目标下，规格中存在的模糊、不完整、矛盾、或定义不足、足以导致实现歧义的产品级问题。

---

## Completeness Checklist（完整性检查）

| 类别 | 状态 | 说明 |
| --- | --- | --- |
| 1. Problem Definition（问题定义） | PRESENT | §1 量化结论明确问题：固定框架开销高、重复陈述多、输出被撑大。 |
| 2. Desired Outcome（期望结果） | PRESENT | 开头目标段与 §6 验收定义结果与成功判据。 |
| 3. Business Rules（业务规则） | PARTIAL | §4 质量不变量、§3.1 枚举/字段契约定义较充分，但若干判定规则（质量护栏、删除纪律）本身未闭环。 |
| 4. Workflows（工作流） | PRESENT（高层） | §5 流水线"完全不变"，仅修订加载契约；但加载失败的异常路径未定义。 |
| 5. States and Transitions（状态与转换） | NOT_APPLICABLE | 本设计非状态型产品；决策协议状态枚举仅被引用、未变更。 |
| 6. Boundary Conditions（边界条件） | PARTIAL | §6 要求"1 个小 spec + 1 个大型/真实 spec"，但"小/大"未定义、通过条件未定义。 |
| 7. Data Lifecycle（数据生命周期） | NOT_APPLICABLE | 本设计为提示词/协议文件瘦身，无运行时数据生命周期议题。 |
| 8. Assumption Declarations（假设声明） | PARTIAL | §1 基线说明、§2 参考值说明声明了若干假设，但部分关键假设（如"4× spec 读取为固有成本"对总收益的影响）未展开。 |

---

## Findings

### PR-001 — 质量护栏的"基本一致"判据不可客观判定

#### Severity

P1

#### Evidence Class

MATERIAL_RISK

#### Confidence

HIGH

#### Location

Design Spec §6「质量护栏（可判定，落实 CR-002）」整段，尤其"建议 ≥80%"与"以 severity + 所指向问题 为标识"。

#### The Gap

规格声称本节落实 CR-002（质量可判定），但留下两处未定义，使质量护栏无法被客观判定：

1. 复现率阈值为"建议 ≥80%"，"建议"意味其非强制绑定值。规格未定义当复现率低于 80% 但高于某一未声明数值时的判定结果，也未定义绑定阈值由谁、以何种规则最终确定。
2. "P0/P1 所指向问题是否仍被覆盖"的判定依赖"以 severity + 所指向问题 为标识"进行跨轮次匹配，但规格未定义"所指向问题"的归一化/匹配算法（例如瘦身后的表述差异、同一问题被拆分为不同 severity、语义等价但字面不同如何判定为同一问题）。

由于回滚触发（git revert）直接依赖这一比对结果，护栏的 PASS/FAIL 实际落在一个未定义的比对启发式上，与"可判定"的既定目标相矛盾。

#### Trigger Scenario

1. 瘦身实施完成，对同一大型 spec 运行验收。
2. 验收人发现：P0/P1 关键问题在瘦身前后"集合"存在，但瘦身后有 1 条 P0 被降为 P1、2 条问题表述被改写。
3. 验收人尝试用"severity + 所指向问题"比对，因"问题"无归一化定义，无法客观判定这两条是否"仍被覆盖"。
4. 复现率落在 78%（低于建议值但非硬门槛），规格未给出绑定阈值与判定归属，验收人无法依规格得出确定结论。
5. 结果：是否触发 git revert 取决于个人主观判断，质量护栏失去可判定性。

#### Consequence

- 业务影响：决定"是否回滚"的核心判据不可复算，CR-002 的"质量可判定"目标未真正落地。
- 运营影响：不同验收人/不同次验收可能产生不一致结论，规格的"可判定"承诺失效。
- 工作流影响：回滚决策可能因人因偏差被推迟或误触发，使质量下降的版本被合入。

#### Evidence

§6 原文：
- "‘基本一致’量化口径：以 P0/P1 所指向问题是否仍被覆盖为主判据（关键 Finding 复现率 ≥ 阈值，建议 ≥80%）"
- "判定责任人：每次验收由 Spec 所有者（或受托主 agent）指定并留名。"
- "回滚触发条件：若关键 Finding 复现率低于阈值，或新出现未被覆盖的 P0/P1 问题 → 触发 git revert"

其中"建议 ≥80%"使阈值非绑定；"所指向问题"无匹配定义。

#### Assumptions

- CONFIRMED：规格 §6 标题明示"落实 CR-002（质量可判定）"，即把质量判据客观化是既定需求。
- INFERRED：验收将依该护栏做回滚决策（§6 末尾"直接 git revert"）。
- UNKNOWN：实际验收中"小/大 spec"样本与 N≥2 次基线的具体取值，规格未锁定。

#### Source References

* Design Spec §6 质量护栏
* Design Spec §6 回滚触发条件

---

### PR-002 — 删除纪律的安全网为"自报告 + 非穷举核对"，无法拦截未枚举规范性语句的静默删除

#### Severity

P1

#### Evidence Class

MATERIAL_RISK

#### Confidence

HIGH

#### Location

Design Spec §3.2「删除纪律（落实 CR-007）」、§4 第 9 条、§6 一致性校验「删除项清单」、§7 删除项清单。

#### The Gap

规格把"禁止静默删除规范性语句"作为核心质量不变量（§4 第 9 条），但其唯一可执行的安全机制存在两类缺陷：

1. 删除项清单由执行者（瘦身实施人）自行维护、随 PR 提交（§7）。这是自报告机制，无独立来源可交叉验证其完整性。
2. §6 一致性校验要求"逐条对照 §4 与角色规范性语句，确认无静默删除"。但 §4 第 9 条已明确声明 §4"非穷尽"，角色/协议中尚存"大量未被本条款覆盖却约束输出质量的规范性语句（数量上限、证据等级不得升格、禁止制造 Finding 等）"。因此该核对只能覆盖 §4 已枚举的语句，对未枚举的质量相关规范性语句无能为力。

后果：一条未被 §4 枚举、但确实约束输出质量的规范性语句被删除时，删除项清单可"不记录"，而 §6 核对因只对照 §4 也无法发现——这正是 §4 第 9 条想要防止的危害，却缺少可 detect 的机制。

#### Trigger Scenario

1. 执行者对 product-reviewer.md 瘦身，删除了"Do not present MATERIAL_RISK as CONFIRMED_DEFECT"这类约束证据等级升格的禁止句（属 §4 第 9 条所称"证据等级不得升格"类，但未在 §4 显式列举原文）。
2. 执行者未将该删除记入删除项清单（自报告，无强制）。
3. 提交瘦身 PR，附带删除项清单（仅含其愿意记录的几项）。
4. 验收人按 §6 做"逐条对照 §4 与角色规范性语句"核对：因该禁止句不在 §4 枚举内，核对通过。
5. 结果：质量相关规范性语句被静默删除且未被任何检查捕获，违反 §4 第 9 条初衷。

#### Consequence

- 业务影响：瘦身可能以"通过验收"的形式丢失约束输出质量的规范性语句，导致后续审核质量在无预警下退化。
- 运营影响：质量不变量 §4 第 9 条缺乏可验证的执行手段，形同软约束。
- 数据/工作流影响：历史 review 所依赖的判据在不知情下改变，跨轮次一致性受损。

#### Evidence

§4 第 9 条原文："本条列为审查重点但非穷尽；角色/协议中尚存大量未被本条款覆盖却约束输出质量的规范性语句（数量上限、证据等级不得升格、禁止制造 Finding 等）。删减任一此类规范性语句须逐条记录理由并入删除项清单（§7），禁止静默删除。"

§6 一致性校验原文："删除项清单：逐条对照 §4 与角色规范性语句，确认无静默删除（§7）。"

§7 原文："该清单随瘦身 PR 一并提交，供评审对照 §4 与角色规范性语句；任何标记为‘影响质量约束’的项须经决策……不得静默合入。"（清单由执行方维护，核对基准仅为 §4。）

#### Assumptions

- CONFIRMED：§4 第 9 条自承 §4 非穷举且存在大量未枚举的质量相关规范性语句。
- INFERRED：删除项清单的完整性依赖执行者自觉，规格未规定对原始文件做全量 diff 的强制独立校验。
- UNKNOWN：实际角色/协议文件中究竟有多少条"未枚举但约束质量"的规范性语句，规格未盘点。

#### Source References

* Design Spec §3.2 删除纪律
* Design Spec §4 第 9 条
* Design Spec §6 一致性校验
* Design Spec §7 删除项清单

---

### PR-003 — 规格的 headline 收益（减少 token 消耗与运行时间）从未被验收，仅验收了中间代理指标

#### Severity

P1

#### Evidence Class

MATERIAL_RISK

#### Confidence

MEDIUM

#### Location

Design Spec 开头目标段、§1 量化结论「spec 4× 读取」行、§6 静态验收与功能验收。

#### The Gap

规格开篇将目标定义为"减少单次审核的 token 消耗与运行时间"，但最终验收只测量两类代理指标：
(a) 框架文件（协议+角色+模板）token 降幅 ≥40%（§6 静态验收，且明确为"期望下限而非硬门槛"）；
(b) 审核质量不下降（§6 质量护栏）。

规格未定义任何对"端到端单次审核 token 总量 / 运行时间"的实测与验收。而 §1 自身指出：Design Spec 在（主 agent 1 次 + 3 subagent 各 1 次）共读 4 次，"是大型 spec 的主导成本，但属独立评审设计固有，本轮不动"。即真正主导大型 spec 总成本的是 4× spec 读取，本轮明确不触碰。

由此产生的产品级缺口：当 spec 较大时，框架文件可能只是总 token 的小头，40% 框架降幅折算到端到端可能微不足道；而规格没有任何判据去确认"减少单次审核 token 消耗与运行时间"这一原始目标是否被满足。代理指标达标 ≠ 原始目标达标，二者缺口未被任何验收覆盖。

#### Trigger Scenario

1. 对一个 50K tokens 的大型 spec 执行瘦身。
2. 框架文件（假设占端到端 15K）降低 40% → 省 6K；但 4× spec 读取（200K）未变。
3. 端到端单次审核总量仅下降约 6K / 215K ≈ 2.8%，运行时间几乎不变。
4. §6 静态验收：框架降幅 ≥40% 通过；质量护栏通过。
5. 结果：规格 headline 目标（显著减少 token 与耗时）未达成，但因验收只测代理指标，被判定为"通过"。

#### Consequence

- 业务影响：投入瘦身工程的收益可能无法兑现，却因验收口径错位而被误判为成功。
- 运营影响：后续是否启动方案 B（§7）依赖方案 A"验证有效"，而"有效"若仅按代理指标判定，可能基于错误结论推进/放弃方案 B。
- 需求完整性影响：规格自陈的目标未被任何验收条款绑定，属需求—验收脱节。

#### Evidence

开头目标段："将固定框架开销……降低约 ≥40%……减少单次审核的 token 消耗与运行时间。"

§1：「spec 4× 读取 | Design Spec 在（主 agent 1 次 + 3 subagent 各 1 次）共读 4 次，是大型 spec 的主导成本，但属独立评审设计固有，本轮不动」

§6 静态验收："真实降幅以四元组为准，≥40% 为期望下限而非硬门槛。"（仅针对框架，未提端到端）

#### Assumptions

- CONFIRMED：规格自承 4× spec 读取为大型 spec 主导成本且本轮不动。
- INFERRED：框架降幅对大型 spec 端到端收益有限（数学推论，受 spec 相对体积影响）。
- UNKNOWN：框架文件在端到端总成本中的真实占比，规格未在不同 spec 规模下量化。

#### Source References

* Design Spec 开头目标段
* Design Spec §1 spec 4× 读取
* Design Spec §6 静态验收

---

### PR-004 — "固定框架开销"指标自相矛盾，且小/大样本双达标条件未定义

#### Severity

P2

#### Evidence Class

MATERIAL_RISK

#### Confidence

HIGH

#### Location

Design Spec §1 量化结论「固定框架开销」行与「基线说明」、§2 行数目标性质说明、§6 静态验收样本要求。

#### The Gap

§1 将 40–78K tokens 称为"固定框架开销"，并同时标注"（随 spec 大小变化，但与 spec 内容无关、且大量重复）"。该表述内部矛盾：
- 既称"固定"，又称"随 spec 大小变化"——若随 spec 大小变化，则并非固定，且事实上与 spec 相关（体积相关）。
- 这一矛盾使"框架开销降低 40%"的口径在不同 spec 规模下含义不一致：对小 spec 与对大 spec，同一套框架文件产生的 token 不同，降幅百分比因而漂移。

叠加 §6 静态验收要求"至少 1 个小 spec + 1 个大型/真实 spec"，但规格未定义两个样本的通过关系（两者都须 ≥40%？任一即可？取平均？），导致 headline 的"≥40%"目标在双样本下无确定判定规则。

#### Trigger Scenario

1. 验收对"小 spec"测得框架降幅 45%，对"大型/真实 spec"测得框架降幅 33%（因大 spec 下框架占比/体积关系不同，且 §1 承认框架"随 spec 大小变化"）。
2. 规格 §6 要求两个样本，但未定义双样本通过条件。
3. 验收人无法依规格判定本次瘦身是否"达标"——45% 与 33% 如何合并无规则。
4. 结果：headline 目标的可判定性依赖于未定义的合并规则。

#### Consequence

- 业务影响："固定框架开销"这一核心度量自身的语义矛盾，削弱所有基于它的结论（含 §1 方向性结论）的严谨性。
- 运营影响：静态验收的"达标"结论在不同样本组合下可能得出相反判断。
- 需求完整性影响：度量定义不自洽，导致验收判据基础不稳。

#### Evidence

§1 行："固定框架开销 | 4 协议 + 3 角色 + 3 模板 + SKILL.md 合计约 40–78K tokens（随 spec 大小变化，但与 spec 内容无关、且大量重复）"

§1 基线说明："上述 40–78K 为区间估计……本节区间仅用于说明方向，不得作为验收基线。"

§6 静态验收："样本要求：至少 1 个小 spec + 1 个大型/真实 spec"——但未定义双样本通过条件。

#### Assumptions

- CONFIRMED：规格明示框架"随 spec 大小变化"且为"固定框架开销"，二者并存于同一句。
- INFERRED：因框架随 spec 体积变化，降幅百分比在不同规模下会漂移。
- UNKNOWN："小 spec""大型/真实 spec"的划分阈值，规格未定义。

#### Source References

* Design Spec §1 量化结论
* Design Spec §2 行数目标性质
* Design Spec §6 静态验收

---

### PR-005 — 加载契约未定义 common.md 运行时加载失败的产物与回退行为

#### Severity

P2

#### Evidence Class

MATERIAL_RISK

#### Confidence

MEDIUM

#### Location

Design Spec §5「subagent 权威加载契约」、§4 第 6 条、§6 一致性校验「引用可解析」。

#### The Gap

§5 规定 subagent 加载契约为"读 references/common.md + roles/X.md + templates/X.md + spec 路径"四者并列且不得省略，并声称由此保证"隔离规则与共享判据实际可达"（§4 第 6 条、§3.1）。§6 仅以"引用可解析：所有对 common.md 的引用均可解析，无悬空引用"做静态校验。

规格定义了"文件存在/路径可解析"的静态检查，但未定义以下运行时情形：
- 若 subagent 运行框架因故未实际将 common.md 注入上下文（路径可解析但内容未送达、或注入为空）；
- 此时 subagent 缺失的不仅是共享判据，更缺失"独立评审/上下文隔离规则本身"（§3.1 明确该规则须存在于 subagent 上下文）。

规格未规定：加载失败如何被检测、是否中止该 subagent、是否整轮重跑、缺失 common.md 的产出是否视为 INVALIDATED。静态"可解析"检查无法保证运行时内容真正到达上下文，核心不变量可能在无预警下被破坏。

#### Trigger Scenario

1. 某次评审，orchestrator 按 §5 契约列出 common.md，但运行框架因配置/长度截断未将其注入某个 subagent 提示词。
2. 该 subagent 仍正常产出一份审核文件（缺失共享判据与隔离规则指令）。
3. §6 静态"引用可解析"检查通过（文件存在、路径正确），无法发现运行时未注入。
4. 合并阶段将该不完整上下文下的产出并入最终审核，§4 第 6 条"隔离规则须实际存在于每个 subagent 运行上下文"被静默违反。
5. 结果：质量不变量被破坏且全程无检测、无回退。

#### Consequence

- 业务影响：独立评审的核心隔离保证可能在运行时失效而不被察觉，损害三视角独立性的产品质量承诺。
- 运营影响：故障模式隐蔽，难以在验收或日常运行中定位。
- 工作流影响：缺失 common.md 的产出可能被当作有效输入进入合并，污染最终审核。

#### Evidence

§5：「subagent 权威加载契约……common.md 与角色/模板/spec 四者并列纳入加载清单，不得省略。」

§4 第 6 条：「该隔离规则须实际存在于每个 subagent 的运行上下文（由 §5 加载契约保证，§6 校验）。」

§6 一致性校验：「引用可解析：所有对 common.md 的引用均可解析，无悬空引用（§4 第 10 条）。」——仅静态，无运行时校验/失败行为定义。

#### Assumptions

- CONFIRMED：§3.1 声明隔离规则本身须存在于 subagent 上下文，且 §4 第 6 条将其可达性托付给 §5/§6。
- INFERRED：静态"可解析"检查不保证运行时内容注入成功。
- UNKNOWN：subagent 运行框架是否具备加载失败的可观测信号，规格未说明。

#### Source References

* Design Spec §5 加载契约
* Design Spec §4 第 6 条
* Design Spec §6 一致性校验

---

## Finding Summary

| Finding ID | Severity | Evidence Class                 | Confidence      | Short Description |
| ---------- | -------- | ------------------------------ | --------------- | ----------------- |
| PR-001     | P1       | MATERIAL_RISK                  | HIGH            | 质量护栏"基本一致"阈值非绑定且问题匹配算法未定义，质量判据不可客观判定（与 CR-002 目标矛盾） |
| PR-002     | P1       | MATERIAL_RISK                  | HIGH            | 删除纪律安全网为自报告+仅对照非穷举§4，未枚举质量语句的静默删除不可检测 |
| PR-003     | P1       | MATERIAL_RISK                  | MEDIUM          | headline 收益（端到端 token/耗时）未被任何验收覆盖，仅验收中间代理指标；主导成本 4×spec 读取未动 |
| PR-004     | P2       | MATERIAL_RISK                  | HIGH            | "固定框架开销"指标自相矛盾（固定却随 spec 大小变化），双样本通过条件未定义 |
| PR-005     | P2       | MATERIAL_RISK                  | MEDIUM          | 加载契约缺运行时加载失败检测/回退，静态"可解析"不足以保证隔离规则与共享判据实际可达 |

---

## Product Risk Coverage

| Risk Dimension                | Status                    | Finding IDs |
| ----------------------------- | ------------------------- | ----------- |
| State Machine Vulnerabilities | NOT_APPLICABLE            | —           |
| Hard Boundaries and Limits    | REVIEWED                  | PR-004      |
| Data Lifecycle                | NOT_APPLICABLE            | —           |
| Backward Compatibility        | REVIEWED                  | PR-002, PR-005 |
| Implicit Assumptions          | REVIEWED                  | PR-003, PR-004 |
| Business Rule Conflicts       | REVIEWED                  | PR-001, PR-002 |
| Temporal Consistency          | NOT_APPLICABLE            | —           |
| User Workflow Integrity       | REVIEWED                  | PR-001, PR-005 |
| Administrative Operability    | REVIEWED                  | PR-002, PR-003, PR-005 |
| Abuse and Misuse Scenarios    | REVIEWED                  | PR-002      |

NOT_APPLICABLE 说明：
- State Machine Vulnerabilities / Data Lifecycle / Temporal Consistency：本设计为提示词/协议文件瘦身，无运行时状态机、无数据生命周期、无跨时一致性议题；决策协议状态枚举仅被引用未变更。

---

## Unresolved Product Questions

### Q-001 — "禁止同类脚本替换"中"同类脚本"的绑定定义是什么？

#### Question

§6 静态验收规定 token_analyzer.py"禁止‘同类脚本’替换"，但规格未定义何种替换构成被禁止的"同类脚本"、何种属于允许的修复/升级。

#### Why It Matters

静态验收的完整性依赖该脚本的口径固定（中文感知估算写死）。若"同类脚本"无绑定定义，实施方可用一个产出更优数字的不同脚本替换它，静态验收的防操纵控制将失效，且无人能依规格判定是否违规。

#### Required Clarification

定义"同类脚本"的可判定边界（例如：必须复用同一估算函数与同一文件清单白名单；仅允许 bug 修复，禁止改变估算口径），或改为对脚本计算逻辑做哈希/契约测试而非依赖"同类"措辞。

#### Status

OPEN

---

### Q-002 — 是否存在引用角色/协议文件的外部消费者（其他 skill 或流水线）？

#### Question

本设计将严重性、证据等级、Finding 字段等共享定义从 roles/、protocols/、templates/ 集中到 references/common.md，并仅声明"防止悬空引用"（§4 第 10 条、§6）。但该检查范围限于本 skill 内部引用。

#### Why It Matters

若有其他 skill（如 writing-skills、brainstorming）或外部流水线直接读取 product-reviewer.md / consolidation-protocol.md 并依赖其中原有章节（如严重度定义），集中到 common.md 后可能造成外部悬空引用，而本规格的"可解析"检查不会覆盖。

#### Required Clarification

确认本 skill 文件是否被外部消费；若是，定义跨 skill 的引用迁移与兼容性处理。

#### Status

OPEN

---

### Q-003 — 以 N≥2 次基线运行刻画 LLM 波动是否足以支撑回滚容差？

#### Question

§6 质量护栏以"改动前对同一固定小 spec 运行 N≥2 次"记录波动范围，并将"正常 LLM 波动（在基线波动范围内）"排除出回滚触发。N=2 的样本对刻画 LLM 输出方差统计上偏弱。

#### Why It Matters

若基线波动被低估，则瘦身实际引入的质量退化可能被误判为"正常波动"而不触发回滚；反之亦然。这直接影响 PR-001 所述的回滚决策可靠性。

#### Required Clarification

明确 N 的下限依据（或改为置信区间/多次抽样），或显式声明接受该统计弱点的残余风险。

#### Status

OPEN

---

## Review Limitations

- 本审核仅基于提供的 Design Spec 文本进行，未读取 yy-spec-review skill 当前的角色/协议/模板实际文件内容，因此无法独立验证"现有规范性语句"的真实数量与分布（影响 PR-002 对"未枚举语句"风险的量化，但不影响该结构性缺口的存在性）。
- 本审核未读取其他评审者（system/test/consolidated）的输出，亦未读取主 agent 分析，所有发现均独立形成。
- 关于端到端 token/耗时占比（PR-003）缺乏具体数值，系规格自身未在不同 spec 规模下量化所致，本审核仅作结构性推断。

---

## Reviewer Conclusion

### Critical Finding Count

* P0: 0
* P1: 3
* P2: 2

### Review Result

REQUIRES_REVIEW

本审核识别的产品级缺口须由 Consolidation 阶段考虑。核心结论：本规格在"保留架构与质量不变量"上表述严谨，但在"如何客观验证瘦身未损害质量与收益"这一最关键的产品行为上，存在三处 P1 级缺口——质量护栏判据不可客观判定（PR-001）、删除安全网无法拦截未枚举规范性语句的静默删除（PR-002）、headline 收益未被任何验收覆盖（PR-003）。另两处 P2 涉及度量自相矛盾（PR-004）与加载契约运行时失败行为缺失（PR-005）。

Product Reviewer 不决定上述 Finding 最终是否被采纳、拒绝、延期或其他处置；最终处置由 Decision Protocol 确定。

---

## Machine-Readable Finding Index

```yaml
review:
  review_id: "2026-08-04-review-002"
  reviewer: "yy-product-reviewer"
  review_type: "PRODUCT_REVIEW"
  status: "COMPLETED"

findings:
  - id: "PR-001"
    severity: "P1"
    evidence_class: "MATERIAL_RISK"
    confidence: "HIGH"
    title: "质量护栏的“基本一致”判据不可客观判定"
    location: "Design Spec §6 质量护栏（建议≥80% 与 severity+所指向问题 标识）"
    source_references:
      - "Design Spec §6 质量护栏"
      - "Design Spec §6 回滚触发条件"
    risk_dimensions:
      - "Business Rule Conflicts"
      - "User Workflow Integrity"
    status: "PENDING_DECISION"

  - id: "PR-002"
    severity: "P1"
    evidence_class: "MATERIAL_RISK"
    confidence: "HIGH"
    title: "删除纪律安全网自报告且仅对照非穷举§4，未枚举质量语句静默删除不可检测"
    location: "Design Spec §3.2 / §4 第9条 / §6 一致性校验 / §7 删除项清单"
    source_references:
      - "Design Spec §3.2 删除纪律"
      - "Design Spec §4 第9条"
      - "Design Spec §6 一致性校验"
      - "Design Spec §7 删除项清单"
    risk_dimensions:
      - "Backward Compatibility"
      - "Administrative Operability"
      - "Abuse and Misuse Scenarios"
    status: "PENDING_DECISION"

  - id: "PR-003"
    severity: "P1"
    evidence_class: "MATERIAL_RISK"
    confidence: "MEDIUM"
    title: "headline 收益（端到端 token/耗时）未被任何验收覆盖，仅验收中间代理指标"
    location: "Design Spec 开头目标段 / §1 spec 4×读取 / §6 静态验收"
    source_references:
      - "Design Spec 开头目标段"
      - "Design Spec §1 spec 4×读取"
      - "Design Spec §6 静态验收"
    risk_dimensions:
      - "Implicit Assumptions"
      - "Administrative Operability"
    status: "PENDING_DECISION"

  - id: "PR-004"
    severity: "P2"
    evidence_class: "MATERIAL_RISK"
    confidence: "HIGH"
    title: "“固定框架开销”指标自相矛盾且双样本通过条件未定义"
    location: "Design Spec §1 量化结论 / §2 行数目标性质 / §6 静态验收样本要求"
    source_references:
      - "Design Spec §1 量化结论"
      - "Design Spec §2 行数目标性质"
      - "Design Spec §6 静态验收"
    risk_dimensions:
      - "Hard Boundaries and Limits"
      - "Implicit Assumptions"
    status: "PENDING_DECISION"

  - id: "PR-005"
    severity: "P2"
    evidence_class: "MATERIAL_RISK"
    confidence: "MEDIUM"
    title: "加载契约缺运行时加载失败检测/回退，静态可解析不足以保证隔离规则实际可达"
    location: "Design Spec §5 加载契约 / §4 第6条 / §6 一致性校验"
    source_references:
      - "Design Spec §5 加载契约"
      - "Design Spec §4 第6条"
      - "Design Spec §6 一致性校验"
    risk_dimensions:
      - "Backward Compatibility"
      - "User Workflow Integrity"
      - "Administrative Operability"
    status: "PENDING_DECISION"

open_questions:
  - id: "Q-001"
    status: "OPEN"
    question: "“禁止同类脚本替换”中“同类脚本”的绑定定义是什么？"
  - id: "Q-002"
    status: "OPEN"
    question: "是否存在引用角色/协议文件的外部消费者（其他 skill 或流水线）？"
  - id: "Q-003"
    status: "OPEN"
    question: "以 N≥2 次基线运行刻画 LLM 波动是否足以支撑回滚容差？"
```
