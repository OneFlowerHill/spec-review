# System Review

## Review Metadata

### Review ID

SR-SLIM-DESIGN-2026-08-04-SYS

### Reviewer

yy-system-critic

### Review Type

SYSTEM_REVIEW

### Design Spec

docs/superpowers/specs/2026-08-04-spec-review-slim-design.md

### Review Date

2026-08-04

### Review Status

COMPLETED

---

## Review Scope

本审核从系统可靠性、架构一致性、数据/契约完整性、安全边界（角色独立性与上下文隔离）、可运维性、可逆性与长期可维护性角度，独立评审该「瘦身设计」。

本设计表面是一次提示词/协议/角色/模板的剪枝，但其本质是一次**架构重构**：引入新的共享依赖 `references/common.md`，并将原本内联在各角色/模板中的定义改为跨文件引用。这种重构会改变每个 subagent 实际加载到的指令集合，因此必须按系统变更评审，而非按文案精简评审。

本审核不重写设计、不产出实现计划、不做最终接受/拒绝决策。

---

## Findings

### SC-001 — 共享文件 `references/common.md` 被角色/模板引用但不在 subagent 加载契约中

#### Severity

P0

#### Evidence Class

CONFIRMED_DEFECT

#### Confidence

HIGH

#### Location

Design Spec 第 3.1 / 3.2 节（角色删除共享块、改为引用 `references/common.md`）；第 5 节「数据流向」（subagent 提示词仍指示「读 roles/X.md + templates/X.md + spec 路径」）。

#### Risk

设计在 §3.1–3.2 明确要求角色文件「删除共享块 → 替换为对 `references/common.md` 的引用」，但在 §5 定义的实际行为（subagent 加载清单）中，subagent 仍只读取 `roles/X.md` + `templates/X.md` + `spec 路径`，**未将 `references/common.md` 加入 subagent 的加载契约**。

结果：被抽离并外置的定义（严重度、证据等级、Finding 格式、以及关键的「独立评审 / 上下文隔离」规则）在 subagent 运行上下文中**悬空不可达**。三个 subagent 将失去强制执行「互不参考、不得读其他评审、不得含主 agent 分析」的指令，核心架构不变量（§4 第 6 条「独立评审」）被静默破坏。

#### Trigger Condition

1. 实施按 §3.1–3.2 执行，角色文件删除共享块并改为 `见 references/common.md`。
2. 实施按 §5 保持 subagent 加载清单不变（仅 roles/X.md + templates/X.md + spec）。
3. 主 agent 启动 Phase 1–3 的三角色并行 subagent。
4. 每个 subagent 上下文不含 `references/common.md` 内容，却看到指向它的引用。
5. 原本由内联指令强制的「独立评审 / 上下文隔离」规则在该 subagent 上下文中不存在 → 风险暴露。

#### Consequence

- 正确性/质量影响：三份评审不再被机制保证独立；subagent 可能（无意或受提示）交叉参考，违反 §4 第 6 条质量不变量；合并阶段 Source Finding 独立性受损，可能放大重复/矛盾判定错误。
- 隐蔽性：这是**静默回归**——流水线仍「正常产出」三份审核，功能验收（§6）难以发现独立性已失效，属难检测缺陷。
- 一致性影响：`references/common.md` 即使后续被创建，只要加载契约不改，问题持续存在。

#### Likelihood

HIGH

该缺陷由设计文本的两条明确陈述直接组合而成（角色依赖 common.md + subagent 不加载 common.md），与 spec 大小/流量无关，每次运行必现。

#### Reversibility

REVERSIBLE

后果可通过在 subagent 加载契约中加入 `references/common.md` 并回归验证来修复；但静默质量回归一旦进入生产审核，已产出的历史审核结论不可自动纠正。

#### Recommendation

明确将 `references/common.md` 纳入每个 subagent 的加载契约（与 `roles/X.md`、`templates/X.md`、`spec` 并列），或在 §5 数据流向中显式声明其加载方式。否则「外置共享定义」这一重构无法在不破坏独立评审不变量的前提下落地。该约束必须在实施前以一行加载清单变更落地，并在 §6 功能验收里增加「独立性指令仍存在于 subagent 上下文」的校验点。

#### Evidence

- §3.1：「各角色与模板以『见 `references/common.md`』引用，不再各自重述。」
- §3.2：「删除……共享块 → 替换为对 `references/common.md` 的引用。」
- §5：「subagent 提示词仍指示『读 roles/X.md + templates/X.md + spec 路径』」——未提及 `references/common.md`。
- 推论（INFERRED）：当前 subagent 加载清单原不包含 `references/common.md`（否则 §5 应同步更新）。

#### Assumptions

- CONFIRMED：§5 的加载清单即实施后的实际加载清单（设计称「仍指示」）。
- INFERRED：`references/common.md` 在 §5 的清单之外，不会自动被 subagent 读取。
- UNKNOWN：现有 `review-orchestrator-protocol.md` 是否另有机制注入 common.md（设计未说明）。

#### Reversibility Analysis

- 可回滚：修改加载契约即可恢复，git revert 到留底提交可整体回退。
- 不可回滚：因独立性失效而产出的历史审核结论，若已被消费/合并，无法自动修正。
- 手动干预：需对受影响批次的审核重跑方可恢复质量。

#### Operational Impact

静默质量回归难以被监控/告警发现；功能验收（§6）仅靠「正常产出 + 数量基本一致」无法检出，需新增独立性校验点（grep/结构检查 common.md 关键指令是否出现在 subagent 上下文）。

#### Security Impact

NO_MATERIAL_SECURITY_IMPACT_IDENTIFIED

（注：独立评审被破坏属于质量/正确性范畴，非传统安全边界突破；但若独立性用于防止提示注入跨角色传播，则该边界被削弱。）

#### Maintenance Impact

引入「跨文件引用 + 加载契约」双重约束后，未来任何 common.md 字段变更都必须同步校验加载契约与三角色引用，增加维护耦合与回归风险。

#### Source References

* §3.1 新增 references/common.md
* §3.2 瘦身角色文件
* §5 数据流向（行为不变）

---

### SC-002 — 共享「Finding 必填字段格式」与 system-critic 模板实际字段互相矛盾

#### Severity

P1

#### Evidence Class

CONFIRMED_DEFECT

#### Confidence

HIGH

#### Location

Design Spec 第 3.1 节（common.md 的「Finding 必填字段格式」）；`templates/system-review.md`（实际字段含 Risk / Trigger Condition / Causal Chain / Likelihood / Reversibility）。

#### Risk

§3.1 规定 common.md 统一「Finding 必填字段格式」为：`Severity / Evidence Class / Confidence / Location / Gap / Trigger Scenario / Consequence / Evidence / Recommendation`。

但当前 `templates/system-review.md`（本角色实际使用的模板）的 Finding 字段为：`Severity / Evidence Class / Confidence / Location / Risk / Trigger Condition / Causal Chain / Consequence / Likelihood / Reversibility / Recommendation / Evidence / Assumptions …`。

矛盾点：
- 共享格式使用 `Gap` 与 `Trigger Scenario`，而 system 模板使用 `Risk` 与 `Trigger Condition`（字段名与语义不同）；
- 共享格式**缺失** system 模板独有且系统评审必需的 `Causal Chain`、`Likelihood`、`Reversibility` 等字段。

设计声称将「Finding 格式」统一外置到 common.md，却未与角色模板字段对齐。落地时二者必有一方被覆盖：要么 system 模板被迫丢弃 `Causal Chain/Likelihood/Reversibility`（系统评审失去因果链与可逆性分析，损害质量），要么 common.md 的「统一格式」名不副实（各角色仍各写各的，去重失败）。

#### Trigger Condition

1. 实施按 §3.1 在 common.md 写入统一字段格式（含 Gap / Trigger Scenario）。
2. system 模板按 §3.4 瘦身，保留「结构骨架与字段定义」。
3. subagent 同时看到 common.md 的「统一格式」与 system 模板的「字段定义」。
4. 二者字段集合不一致 → subagent 输出字段歧义或缺失。
5. 合并阶段解析 Finding 时，`Causal Chain` / `Reversibility` 等关键字段可能缺位，或 `Gap`/`Risk` 语义混乱。

#### Consequence

- 数据完整性：合并协议依赖统一字段契约解析 Source Finding；字段缺失/重命名会导致解析失败或静默丢字段。
- 质量影响：system 评审的因果链（Causal Chain）与可逆性（Reversibility）是系统风险判定的核心，若被「统一格式」抹除，系统评审深度下降。
- 去重失败：若各角色仍保留差异字段，common.md 并未真正消除重复，§1 目标（降低 ≥40% 框架开销）落空。

#### Likelihood

HIGH

字段清单矛盾直接写在设计文本中（§3.1 的字段列表 vs system 模板的实际字段），属设计内部不一致，必然在落地时暴露。

#### Reversibility

REVERSIBLE

字段契约可通过修订 common.md 与模板重新对齐；但已按错误契约产出的审核文件需重跑。

#### Recommendation

在 common.md 中定义**字段契约的权威来源**，并显式列出每个角色允许的差异字段（如 system 必须保留 `Risk / Trigger Condition / Causal Chain / Likelihood / Reversibility`）。禁止用一套「统一字段列表」覆盖角色独有字段。要求 §6 一致性校验 grep 验证 common.md 与三模板字段定义无冲突。

#### Evidence

- §3.1：`Finding 必填字段格式：Severity / Evidence Class / Confidence / Location / Gap / Trigger Scenario / Consequence / Evidence / Recommendation`。
- `templates/system-review.md`（已读）：Field 为 Severity / Evidence Class / Confidence / Location / Risk / Trigger Condition / Causal Chain / Consequence / Likelihood / Reversibility / Recommendation / Evidence 等。
- 推论：设计未说明「统一格式」如何与各角色模板字段共存。

#### Assumptions

- CONFIRMED：system 模板当前字段如本文件顶部所读。
- INFERRED：product / test 模板字段与 system 不同（设计未提供，但 §3.2 称各角色保留独有内容）。
- UNKNOWN：common.md 终稿是否会被修订以容纳差异字段。

#### Reversibility Analysis

- 可回滚：字段定义回退至内联。
- 不可回滚：按错误字段契约产出的审核数据需重跑。
- 依赖：依赖 §6 一致性校验是否能捕获字段冲突（当前校验仅针对 CR-ID / decision 枚举 / Finding Type，未含字段契约）。

#### Operational Impact

合并阶段解析失败需在验收中显式测试；建议在功能验收中加入「三份输出字段与 common.md 契约一致」的结构校验。

#### Security Impact

NO_MATERIAL_SECURITY_IMPACT_IDENTIFIED

#### Maintenance Impact

字段契约分散在 common.md 与三模板中，未来增删字段需跨 4 个文件协调，维护成本上升；若二者漂移将重复出现本缺陷。

#### Source References

* §3.1 references/common.md 字段定义
* §3.4 瘦身模板
* templates/system-review.md

---

### SC-003 — 验收标准主观且未在风险集中的大规模/并发场景下验证

#### Severity

P1

#### Evidence Class

MATERIAL_RISK

#### Confidence

MEDIUM

#### Location

Design Spec 第 6 节「回滚与验收」；第 1 节量化结论。

#### Risk

§6 功能验收以「同一个小 spec」在改动前后各跑一次，对比「Finding 数量与严重度分布**基本一致**」与「Source Finding 完整性校验通过」作为质量无损证据。

问题：
1. 「基本一致」无量化阈值（允许偏差多少？），无法客观判定质量回归。
2. 验收仅用**小 spec**；但 §1 自身指出 spec 4× 读取是大型 spec 的主导成本，且本设计风险（跨文件引用失效、字段契约漂移）恰恰在**上下文更大、并发更高**的真实场景中更易暴露——小 spec 验收会系统性低估风险。
3. §6 静态验收依赖 `/tmp/yy_spec_token_analyzer.py`「同类脚本」，该脚本是否真实存在/可复现未确认，≥40% 降幅的度量口径（是否计入 common.md 新增 token、是否计入 subagent 额外加载）未定义，存在口径漂移。

#### Trigger Condition

1. 实施完成，仅用小 spec 通过功能验收（数量「基本一致」）。
2. 生产中对大型 spec 运行瘦身后的流水线。
3. 大型 spec 下 subagent 上下文更紧绷，SC-001（common.md 未加载）/SC-002（字段漂移）的隐蔽影响放大。
4. 质量回归（独立性失效或字段缺失）未被「基本一致」阈值捕获。
5. 问题在多个大型 spec 审核后才被察觉。

#### Consequence

- 质量影响：静默质量回归进入生产审核，违反 §4 质量不变量。
- 可运维性：缺乏客观验收阈值，回滚决策（§6 git revert）依赖主观判断，可能「未达回滚线但实际已劣化」或「误回滚」。
- 度量风险：token 降幅口径不清，可能宣称达标但实则未达 ≥40%（如漏计 common.md 新增与 subagent 额外加载）。

#### Likelihood

MEDIUM

小样本 + 主观阈值在剪枝类变更中常见，历史概率中等；但其与「风险集中在大规模场景」错配，使漏检概率升高。

#### Reversibility

PARTIALLY_REVERSIBLE

git revert 可回退代码；但已按弱化质量产出的审核结论无法自动恢复，且口径不清的 token 度量不可回放。

#### Recommendation

将验收标准客观化：(a) 定义质量等价阈值（如 Finding 数量偏差 ≤ N%、严重度分布偏差 ≤ M%、关键字段完整率 = 100%）；(b) 至少增加一个**大型/真实 spec** 作为验收样本，覆盖上下文紧张场景；(c) 明确 token 度量口径（含 common.md 与 subagent 加载增量），并锁定分析脚本路径而非「同类脚本」。

#### Evidence

- §6：「Finding 数量与严重度分布基本一致」「重跑 token 分析器（/tmp/yy_spec_token_analyzer.py 同类脚本）」。
- §1：「spec 4× 读取……是大型 spec 的主导成本」。
- 推论：验收样本与风险暴露场景错配。

#### Assumptions

- INFERRED：生产主要处理不止小 spec。
- UNKNOWN：分析脚本 `/tmp/yy_spec_token_analyzer.py` 是否存在且口径一致。

#### Reversibility Analysis

- 可回滚：git revert。
- 不可回滚：已消费的历史审核结论、不可复现的 token 度量。
- 手动：需补跑大型 spec 验收以确认。

#### Operational Impact

验收门槛主观，CI/人工门禁难以固化；建议将客观阈值写入验收清单，避免回滚决策依赖个人判断。

#### Security Impact

NO_MATERIAL_SECURITY_IMPACT_IDENTIFIED

#### Maintenance Impact

口径不清的度量会鼓励后续「为达标而达标」的二次剪枝，累积技术债。

#### Source References

* §1 量化结论
* §6 回滚与验收

---

### SC-004 — 证据等级枚举引入 `CONFIRMED_GAP` 但未与现有角色/协议对齐

#### Severity

P2

#### Evidence Class

MATERIAL_RISK

#### Confidence

MEDIUM

#### Location

Design Spec 第 3.1 节（common.md 证据等级含 `CONFIRMED_GAP`）；质量不变量 §4 与合并/决策协议。

#### Risk

§3.1 将共享「证据等级」定义为 `CONFIRMED_DEFECT / MATERIAL_RISK / CONFIRMED_GAP / DESIGN_PREFERENCE`。但当前 `roles/system-critic.md` 仅定义 `CONFIRMED_DEFECT / MATERIAL_RISK / DESIGN_PREFERENCE`，**不存在 `CONFIRMED_GAP`**；而 §4 质量不变量与合并/决策协议围绕既有枚举运作，并未提及 `CONFIRMED_GAP`。

风险：将 `CONFIRMED_GAP` 从某角色（如 Product/Test）提升到「共享定义」后，
- 若 system 等角色未采用 `CONFIRMED_GAP`，则「共享定义」名不副实，去重失败；
- 若强行统一为含 `CONFIRMED_GAP`，则合并/决策/一致性协议须同步识别该枚举，否则 Source Finding 校验或状态流转会因未知枚举出错；
- `CONFIRMED_GAP` 与 `CONFIRMED_DEFECT` 的语义边界在共享层未定义，易在跨角色合并时误判根因关系。

#### Trigger Condition

1. common.md 写入含 `CONFIRMED_GAP` 的共享证据等级。
2. 部分角色（如 system）沿用原 `CONFIRMED_DEFECT`，部分角色使用 `CONFIRMED_GAP`。
3. 合并阶段按既有协议解析证据等级。
4. 协议未定义 `CONFIRMED_GAP` → 校验失败或 silently 归入默认分支。
5. 跨角色根因归类（DUPLICATE/SAME_ROOT_CAUSE）因语义边界不清而误判。

#### Consequence

- 一致性：共享定义与角色实际枚举漂移，去重目标（§1）受损。
- 数据完整性：合并/决策协议遇未知枚举可能解析异常或静默错分。
- 质量：证据等级语义歧义削弱合并判定的可解释性。

#### Likelihood

MEDIUM

取决于实施时是否同步修订协议；设计未要求同步，故漂移概率中等。

#### Reversibility

REVERSIBLE

枚举定义可回退/对齐；已产出的审核中错误枚举需重跑解析。

#### Recommendation

在 common.md 中明确每个证据等级的**适用角色范围**与语义边界，并同步修订合并/决策/一致性协议以识别全部被采用的枚举。禁止将单一角色特有枚举提升为「共享」而不做协议对齐。§6 一致性校验应扩展为枚举一致性 grep。

#### Evidence

- §3.1：证据等级含 `CONFIRMED_GAP`。
- `roles/system-critic.md`（已读）：仅 `CONFIRMED_DEFECT / MATERIAL_RISK / DESIGN_PREFERENCE`。
- §4 质量不变量未提及 `CONFIRMED_GAP`。

#### Assumptions

- CONFIRMED：system-critic 当前无 `CONFIRMED_GAP`。
- UNKNOWN：product/test 角色是否使用 `CONFIRMED_GAP`（设计未提供其全文）。

#### Reversibility Analysis

- 可回滚：枚举定义回退。
- 不可回滚：已按不一致枚举产出的合并结论。
- 手动：需补跑一致性校验。

#### Operational Impact

合并阶段需新增枚举一致性校验，否则故障隐蔽。

#### Security Impact

NO_MATERIAL_SECURITY_IMPACT_IDENTIFIED

#### Maintenance Impact

共享枚举若与协议长期漂移，每次合并都需人工核对，维护成本上升。

#### Source References

* §3.1 references/common.md
* §4 质量不变量
* roles/system-critic.md

---

### SC-005 — `references/common.md` 成为新的跨文件硬依赖，存在部分部署/版本错配风险

#### Severity

P2

#### Evidence Class

MATERIAL_RISK

#### Confidence

LOW

#### Location

Design Spec 第 2–3 节（新增 `references/common.md` 并被角色/模板引用）；第 6 节回滚。

#### Risk

`references/common.md` 首次引入，成为三个角色 + 多个模板共同依赖的**单一共享定义源**。设计以单次 git commit 原子落地为前提（§6 留底 + git revert），但未考虑：
- 若未来以非原子方式变更（部分文件提交、分支 cherry-pick、缓存的旧 subagent 提示词），会出现「角色引用 common.md 但 common.md 缺失/半写」的中间态，导致全部三个 subagent 同时失效（单点依赖放大故障面）；
- 旧版本 subagent 提示词（如已缓存/已分发的 skill 副本）仍内联旧定义，新 common.md 与内联定义并存时可能引发定义双源冲突；
- `references/` 目录为新增，现有索引/加载逻辑（SKILL.md、CLAUDE.md、orchestrator）若未同步，存在引用路径失效风险。

#### Trigger Condition

1. 某次后续变更只提交部分角色/模板而未同步 common.md（或部分 revert）。
2. 运行的 subagent 加载到引用 common.md 的角色文件，但 common.md 处于缺失/半写状态。
3. 三个 subagent 因缺少共享定义同时行为异常或报错。
4. 故障面从「单角色」扩大为「全角色」。

#### Consequence

- 可用性：单点共享文件异常会同时拖垮三角色并行审核，扩大故障爆炸半径。
- 兼容性：新目录/路径若未被索引同步加载，引用失效。
- 可运维性：故障表现为「审核产出异常」而非「文件缺失报错」，诊断成本上升。

#### Likelihood

LOW

当前以原子 git 提交与 git revert 为主，非原子部分部署概率低；但 skill 副本分发/缓存场景使其不可完全排除。

#### Reversibility

REVERSIBLE

git revert 可整体回退；单点故障通过补全 common.md 修复。

#### Recommendation

将「common.md 与引用它的角色/模板必须同批变更」作为硬约束写入变更规范；在 SKILL.md/CLAUDE.md/orchestrator 中显式登记 `references/` 路径；§6 一致性校验增加「所有对 common.md 的引用均可解析」的检查，防止悬空引用。

#### Evidence

- §2：新增 `references/common.md` 为共享定义源。
- §3.1–3.2：角色/模板引用之。
- §6：回滚依赖 git revert，未提及部分部署防护。
- 推论：单点依赖放大故障面属结构性风险。

#### Assumptions

- INFERRED：skill 以 git 仓库方式分发，存在副本/缓存可能。
- UNKNOWN：现有 orchestrator 是否已处理 `references/` 路径加载。

#### Reversibility Analysis

- 可回滚：git revert 整体回退。
- 不可回滚：部分部署已产生的异常审核产出。
- 手动：需校验所有引用可解析。

#### Operational Impact

建议将「引用可解析」纳入发布前检查，降低静默故障概率。

#### Security Impact

NO_MATERIAL_SECURITY_IMPACT_IDENTIFIED

#### Maintenance Impact

新增单一共享源后，任何跨角色定义变更都需谨慎协调，长期耦合上升。

#### Source References

* §2 目标文件结构
* §3.1 references/common.md
* §6 回滚

---

## Finding Summary

| Finding ID | Severity | Evidence Class                 | Confidence      | Likelihood      | Reversibility                                        | Short Description |
| ---------- | -------- | ------------------------------ | --------------- | --------------- | ---------------------------------------------------- | ----------------- |
| SC-001     | P0       | CONFIRMED_DEFECT               | HIGH            | HIGH            | REVERSIBLE                                           | common.md 被引用但不在 subagent 加载契约，独立评审不变量静默失效 |
| SC-002     | P1       | CONFIRMED_DEFECT               | HIGH            | HIGH            | REVERSIBLE                                           | 共享 Finding 字段格式与 system 模板字段互相矛盾 |
| SC-003     | P1       | MATERIAL_RISK                  | MEDIUM          | MEDIUM          | PARTIALLY_REVERSIBLE                                 | 验收标准主观且仅小 spec 验证，风险场景错配 |
| SC-004     | P2       | MATERIAL_RISK                  | MEDIUM          | MEDIUM          | REVERSIBLE                                           | 证据等级枚举引入 CONFIRMED_GAP 未与协议对齐 |
| SC-005     | P2       | MATERIAL_RISK                  | LOW             | LOW             | REVERSIBLE                                           | common.md 单点共享依赖的部分部署/版本错配风险 |

---

## System Risk Coverage

| Risk Dimension                   | Status          | Finding IDs |
| -------------------------------- | --------------- | ----------- |
| Data Integrity and Consistency   | REVIEWED        | SC-002, SC-004 |
| Security Boundaries              | REVIEWED        | SC-001 |
| Authentication and Authorization | NOT_APPLICABLE  | — |
| Availability and Resilience      | REVIEWED        | SC-005 |
| Failure Recovery                 | REVIEWED        | SC-001, SC-003 |
| External Dependencies            | REVIEWED        | SC-001, SC-005 |
| Concurrency and Race Conditions  | NOT_APPLICABLE  | — |
| Data Lifecycle and Migration     | REVIEWED        | SC-003, SC-005 |
| Backward Compatibility           | REVIEWED        | SC-004, SC-005 |
| Operational Complexity           | REVIEWED        | SC-003, SC-005 |
| Maintenance Burden               | REVIEWED        | SC-001, SC-002, SC-004, SC-005 |
| Irreversible Decisions           | REVIEWED        | SC-005 |
| Over-Engineering                 | REVIEWED        | — |
| Observability and Diagnosis      | REVIEWED        | SC-001, SC-003 |

说明：
- Authentication and Authorization / Concurrency and Race Conditions 标记为 NOT_APPLICABLE：本设计是对 skill 提示词/协议的剪枝重构，不涉及身份鉴权与并发写竞争（subagent 间无共享可变状态）。
- Over-Engineering 标记为 REVIEWED 但无独立 Finding：本设计方向是「去重/瘦身」，与过度工程相反；仅 SC-005 涉及引入新共享依赖带来的耦合，已归属维护/可用性维度。

---

## Irreversible Decisions

### ID-001 — 引入 `references/common.md` 作为跨角色/模板的共享定义源

#### Decision

将原本内联在 3 角色 + 3 模板中的严重度、证据等级、Finding 格式、独立评审规则集中到新增的 `references/common.md`，各角色/模板改为引用。

#### Why It Is Difficult to Reverse

该文件成为所有角色与模板的单一依赖源：一旦下游 subagent 提示词、SKILL.md、CLAUDE.md、orchestrator 均围绕「外置共享定义」重构，回退需同步改回 4+ 个文件的内联内容，且需保证历史审核产出仍可解析。

#### Reversal Cost

MEDIUM

#### Risk

若共享定义与角色/模板/协议未对齐（见 SC-002/SC-004），质量不变量被静默破坏；且单点依赖放大故障面（见 SC-005）。

#### Recommendation

实施前明确：(a) common.md 必须纳入 subagent 加载契约（SC-001）；(b) 字段契约与各角色模板对齐（SC-002）；(c) 枚举与协议对齐（SC-004）；(d) 引用可解析性纳入发布校验（SC-005）。上述约束落地后，该决策方可安全提交。

#### Status

OPEN

---

## Over-Engineering and Complexity Risks

本设计方向为去重/瘦身，未识别出「过度工程」导致的独立系统风险。唯一相关的耦合上升属 SC-005（单点共享依赖），已作为不可逆决策与可用性风险记录，不另列复杂度 Finding。

---

## Unresolved System Questions

### Q-001 — subagent 的加载契约是否包含 `references/common.md`？

#### Question

§5 的 subagent 加载清单（roles/X.md + templates/X.md + spec）未列出 `references/common.md`；而 §3.1–3.2 要求角色改为引用它。二者是否矛盾？实施时是否会在加载清单中加入 common.md？

#### Why It Matters

直接决定 SC-001（独立评审不变量是否静默失效）。若为矛盾且未修正，则核心质量不变量被破坏。

#### Required Clarification

明确 subagent 实际加载文件清单，确认 `references/common.md` 被包含，或说明其如何注入 subagent 上下文。

#### Status

OPEN

### Q-002 — 各角色「独有内容」与 common.md 的边界契约是什么？

#### Question

§3.2 称各角色「保留独有内容」，但未定义哪些行属于 common.md、哪些必须留在角色文件。瘦身执行者如何避免将必要角色指令误判为「共享」而删除（或反之保留重复）？

#### Why It Matters

缺乏精确边界会导致瘦身结果不确定、易出错，可能引发 SC-002 类字段丢失或独立性指令丢失。

#### Required Clarification

提供每个角色文件的「保留清单」或机械校验规则（如必含字段/必含独立评审指令的断言）。

#### Status

OPEN

### Q-003 — 质量等价验收的客观阈值如何定义？

#### Question

§6 的「基本一致」「Source Finding 完整性校验通过」缺乏量化口径；是否定义 Finding 数量/严重度分布的可接受偏差，以及大型 spec 验收样本？

#### Why It Matters

决定 SC-003 风险是否可控，以及回滚决策是否客观。

#### Required Clarification

给出量化阈值与至少一例大型 spec 验收样本，并锁定 token 分析脚本与口径。

#### Status

OPEN

---

## Review Limitations

- 现有 `review-orchestrator-protocol.md` 全文未在本审核中提供，subagent 加载清单是否另有机制注入 `references/common.md` 无法确认（影响 SC-001 置信度）。
- product / test 角色文件与对应模板全文未提供，其字段与证据等级是否与 common.md 对齐仅能推断（影响 SC-002/SC-004）。
- token 分析脚本 `/tmp/yy_spec_token_analyzer.py` 未提供，≥40% 降幅的度量口径无法独立验证（影响 SC-003）。
- 本审核严格未读取其他评审者（product/test）输出，结论独立形成。

---

## Reviewer Conclusion

### Critical Finding Count

* P0: 1
* P1: 2
* P2: 2

### Risk Summary

* Security risks: 0（独立评审边界削弱归入质量/正确性，非传统安全突破）
* Data integrity risks: 2（SC-002, SC-004）
* Availability and resilience risks: 2（SC-001, SC-005）
* Operational risks: 3（SC-001, SC-003, SC-005）
* Maintenance risks: 4（SC-001, SC-002, SC-004, SC-005）
* Irreversible decisions: 1（ID-001）
* Over-engineering risks: 0

### Review Result

REQUIRES_REVIEW

本审核识别出系统级风险，须由 Consolidation 阶段纳入考量。System Critic 不判定各 Finding 最终接受/拒绝/延期。

最关键风险为 SC-001：设计将共享定义外置到 `references/common.md`，却未在 subagent 加载契约中加载该文件，导致「独立评审」核心不变量被静默破坏——该缺陷在「正常产出」表象下难以被 §6 功能验收发现，必须在实施前以一行加载清单变更修复。

---

## Machine-Readable Finding Index

```yaml
review:
  review_id: "SR-SLIM-DESIGN-2026-08-04-SYS"
  reviewer: "yy-system-critic"
  review_type: "SYSTEM_REVIEW"
  status: "COMPLETED"

findings:
  - id: "SC-001"
    severity: "P0"
    evidence_class: "CONFIRMED_DEFECT"
    confidence: "HIGH"
    title: "共享文件 references/common.md 被角色/模板引用但不在 subagent 加载契约中"
    location: "Design Spec §3.1/§3.2 与 §5 数据流向"
    likelihood: "HIGH"
    reversibility: "REVERSIBLE"
    source_references:
      - "§3.1 新增 references/common.md"
      - "§3.2 瘦身角色文件"
      - "§5 数据流向（行为不变）"
    risk_dimensions:
      - "Security Boundaries"
      - "Failure Recovery"
      - "External Dependencies"
      - "Maintenance Burden"
    status: "PENDING_DECISION"

  - id: "SC-002"
    severity: "P1"
    evidence_class: "CONFIRMED_DEFECT"
    confidence: "HIGH"
    title: "共享 Finding 必填字段格式与 system-critic 模板实际字段互相矛盾"
    location: "Design Spec §3.1 与 templates/system-review.md"
    likelihood: "HIGH"
    reversibility: "REVERSIBLE"
    source_references:
      - "§3.1 references/common.md 字段定义"
      - "§3.4 瘦身模板"
      - "templates/system-review.md"
    risk_dimensions:
      - "Data Integrity and Consistency"
      - "Maintenance Burden"
    status: "PENDING_DECISION"

  - id: "SC-003"
    severity: "P1"
    evidence_class: "MATERIAL_RISK"
    confidence: "MEDIUM"
    title: "验收标准主观且仅小 spec 验证，风险场景错配"
    location: "Design Spec §1 与 §6 回滚与验收"
    likelihood: "MEDIUM"
    reversibility: "PARTIALLY_REVERSIBLE"
    source_references:
      - "§1 量化结论"
      - "§6 回滚与验收"
    risk_dimensions:
      - "Failure Recovery"
      - "Data Lifecycle and Migration"
      - "Operational Complexity"
      - "Observability and Diagnosis"
    status: "PENDING_DECISION"

  - id: "SC-004"
    severity: "P2"
    evidence_class: "MATERIAL_RISK"
    confidence: "MEDIUM"
    title: "证据等级枚举引入 CONFIRMED_GAP 未与现有角色/协议对齐"
    location: "Design Spec §3.1 与 §4 质量不变量"
    likelihood: "MEDIUM"
    reversibility: "REVERSIBLE"
    source_references:
      - "§3.1 references/common.md"
      - "§4 质量不变量"
      - "roles/system-critic.md"
    risk_dimensions:
      - "Data Integrity and Consistency"
      - "Backward Compatibility"
      - "Maintenance Burden"
    status: "PENDING_DECISION"

  - id: "SC-005"
    severity: "P2"
    evidence_class: "MATERIAL_RISK"
    confidence: "LOW"
    title: "references/common.md 单点共享依赖的部分部署/版本错配风险"
    location: "Design Spec §2/§3 与 §6 回滚"
    likelihood: "LOW"
    reversibility: "REVERSIBLE"
    source_references:
      - "§2 目标文件结构"
      - "§3.1 references/common.md"
      - "§6 回滚"
    risk_dimensions:
      - "Availability and Resilience"
      - "Data Lifecycle and Migration"
      - "Backward Compatibility"
      - "Maintenance Burden"
    status: "PENDING_DECISION"

irreversible_decisions:
  - id: "ID-001"
    status: "OPEN"
    title: "引入 references/common.md 作为跨角色/模板的共享定义源"

complexity_risks: []

open_questions:
  - id: "Q-001"
    status: "OPEN"
    question: "subagent 的加载契约是否包含 references/common.md？"
  - id: "Q-002"
    status: "OPEN"
    question: "各角色独有内容与 common.md 的边界契约是什么？"
  - id: "Q-003"
    status: "OPEN"
    question: "质量等价验收的客观阈值如何定义？"
```
