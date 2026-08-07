# Shared Definitions (references/common.md)

> 本文件是 spec-review skill 的**共享权威定义源**，由 SKILL.md / CLAUDE.md / 角色 / 模板 / 协议引用。
> 修改本文件须与所有引用方**同批变更**（单次提交或同一 PR），且不得引入悬空引用（见设计规格 §4 第 10、11 条）。
> 本文件被纳入 token 降幅验收（prompt_scope.json candidate 含本文件）。

## 1. 严重度（Severity）

- **P0**：阻断性缺陷——审核流程无法继续、核心契约被破坏、或遗漏将导致严重质量/安全隐患。必须修复后方可 APPROVED。
- **P1**：重要缺陷——显著影响审核质量或正确性，但不阻断流程；须在进入 APPROVED 前解决。
- **P2**：次要问题——可读性、一致性或低成本改进；可延后，但须记录。

## 2. 证据等级（Evidence Class）

全局取值域（四个固定字面量，必须原样拼写；合并/决策协议须识别全部四值）：

| 字面量 | 含义 | 主要产出角色 |
|---|---|---|
| `CONFIRMED_DEFECT` | 已确认的设计缺陷 | Product / System |
| `MATERIAL_RISK` | 重大风险（非已确认缺陷） | Product / System / Test |
| `CONFIRMED_GAP` | 已确认的验证/覆盖缺口 | Test |
| `DESIGN_PREFERENCE` | 设计偏好（仅作内部参考，**不得**作为 Finding 输出） | — |

各角色**可输出**子集（与 `roles/*.md` 实际字段一致，不得静默变更）：

- Product：`CONFIRMED_DEFECT` | `MATERIAL_RISK`
- System：`CONFIRMED_DEFECT` | `MATERIAL_RISK`
- Test：`CONFIRMED_GAP` | `MATERIAL_RISK`

> `DESIGN_PREFERENCE` 在三个角色中均"仅作内部参考，不得作为 Finding 输出"。

## 3. Finding 字段契约

**共享必填字段**（每个 Finding 必须包含）：

`Severity` / `Evidence Class` / `Confidence` / `Location` / `Consequence` / `Evidence` / `Recommendation`

**各角色差异字段**（字段名须与对应模板逐字一致，禁止重命名/缩写）：

- Product：`The Gap` / `Trigger Scenario`
- System：`Risk` / `Trigger Condition` / `Causal Chain` / `Likelihood` / `Reversibility`
- Test：`Verification Gap` / `Trigger Scenario` / `Finding Type`（必填）

> 落地产出的 Machine-Readable 索引须同时包含共享字段与各角色差异字段；字段缺失、重命名或缩写视为一致性缺陷（设计规格 §6 字段校验）。

### 3.1 Confidence 三档语义

每个 Finding 必须带置信度，且置信度须与证据强度匹配（**不得**用置信度自动降低严重度；低置信度的 P0 风险仍须显式调查）。三档定义如下：

- **HIGH**：证据直接、可独立验证，结论可靠性高（如代码/文档原文引用、可复现行为、确定性的规范条文）。
- **MEDIUM**：证据较强但含推理链条或外部假设，结论大概率成立，仍需一处确认方可采信。
- **LOW**：证据间接、推断性或样本不足，结论不确定，须进一步核实后方可采信。

## 4. 独立评审 / 上下文隔离规则

- 每个 subagent **只能读**：`references/common.md` + 自己的 `roles/X.md` + 自己的 `templates/X.md` + 被审 spec 路径。
- subagent 提示词**不得包含**主 agent 的分析、结论或其他角色的评审内容。
- 角色之间**互不参考**；合并阶段才汇总。
- 该隔离规则本身须存在于每个 subagent 的运行上下文中（由 orchestrator 加载契约保证，§6 校验）。

## 5. 三角色边界摘要

- **Product Reviewer**：从业务/需求完整性角度审查（需求完整性、业务规则、工作流、状态迁移、边界、数据生命周期、时间一致性、隐藏假设）。
- **System Critic**：从系统/架构/可靠性角度审查（数据完整性、故障恢复、并发、外部依赖、状态生命周期、可扩展性、安全边界、可观测性、部署兼容、不可逆决策、复杂度）。
- **Test Designer**：从可验证性角度审查（验收标准、可观测结果、状态迁移验证、边界验证、失败验证、数据完整性验证、时间验证、向后兼容、运维验证、生产盲点）。

## 6. 不可删质量不变量字面量清单（见设计规格 §4 第 11 条）

以下字面量在任何瘦身/重构后必须仍可 grep 命中（删除安全网）：

- 合并标识：`CR-ID`（禁止 `RV-` 前缀）
- 决策枚举：`PENDING_DECISION` / `ACCEPTED` / `REJECTED` / `DEFERRED` / `PARTIALLY_ACCEPTED` / `DUPLICATE` / `INVALIDATED`
- 证据等级：`CONFIRMED_DEFECT` / `MATERIAL_RISK` / `CONFIRMED_GAP` / `DESIGN_PREFERENCE`
- 关系分类：`DUPLICATE` / `SAME_ROOT_CAUSE` / `RELATED` / `INDEPENDENT` / `CONTRADICTORY` / `SUBSET` / `CONSEQUENCE`
- 状态硬规则：`INCOMPLETE` / `MISSING`
- 独立评审：`独立评审` / `subagent 不得读其他评审`
- 差异字段名：`Gap` / `Trigger Scenario` / `Risk` / `Trigger Condition` / `Causal Chain` / `Likelihood` / `Reversibility` / `Finding Type`
