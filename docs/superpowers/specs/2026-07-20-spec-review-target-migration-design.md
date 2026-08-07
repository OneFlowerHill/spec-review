# Design Spec: 审核对象从 plans/ 迁移到 specs/

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 proposal-review 技能的审核对象从 `docs/superpowers/plans/` 下的实施计划改为 `docs/superpowers/specs/` 下的设计规格，审核模式从"对比式"改为"独立评估式"。

**Architecture:** 三角色并行独立审核架构不变，核心变更是审核对象的路径和审核逻辑——Product Reviewer 从"对比 Specification 和 Solution Proposal 的差距"变为"独立评估 Design Spec 自身的产品质量"。移除对上游 Specification 的依赖，简化 Phase 1 的上下文获取流程。

**Tech Stack:** Markdown 协议文件，无代码依赖。

## Global Constraints

- CR-ID 是唯一的合并 Finding 标识，所有文件必须使用 CR-001 格式
- 决策状态必须使用 decision-protocol 枚举
- Test Designer Finding 必须包含 Finding Type
- MISSING 审核的硬性规则：仅当 subagent 审核输出缺失时触发 MISSING（CR-003 修正）
- 合并后必须执行完整性校验
- 不修改 Design Spec——审核只产出 Finding
- 不跨角色阅读——独立审核阶段，角色间互不参考
- 不静默丢弃 Finding
- 不将假设升级为事实
- 不在合并阶段做决策
- 模板末尾的 Machine-Readable YAML 索引必须与详细内容保持同步
- Subagent 提示词不得包含主代理的分析
- 合并后必须记录 Consolidator Predispositions
- 完整性校验失败时最终状态必须为 INCOMPLETE
- 严重度变更理由为强制字段
- INCOMPLETE 状态触发条件：MISSING 审核 + 完整性校验失败 + Design Spec 文件不可用（CR-003 修正）

---

## 变更背景

### 当前问题

在 superpowers 框架中，文件路径有明确的语义约定：

| 路径 | 含义 | 产出技能 |
|------|------|----------|
| `docs/superpowers/specs/` | 设计规格（Design Spec）— 描述"要做什么" | brainstorming 技能产出 |
| `docs/superpowers/plans/` | 实施计划（Implementation Plan）— 描述"怎么做" | writing-plans 技能产出 |

当前 SKILL.md 的设计：
1. 主输入路径写成了 `docs/superpowers/plans/<proposal>.md` — 审核的是"实施计划"
2. 关联输入路径写成了 `docs/superpowers/specs/<specification>.md` — 把 spec 当成了辅助参考
3. 概念模型写的是 `Specification → Solution Proposal`，但路径映射把 Solution Proposal 对应到了 plans/

**实际意图**：审核的对象应该是 `specs/` 下的设计规格文件，不需要关联参考文件。

### 审核模式变更

**当前逻辑**（对比式审核）：
- Product Reviewer 的核心问题是"Solution Proposal 是否解决了 Specification 定义的问题？"
- 审核员需要同时持有两个文档，找差距
- 没有 Specification 时审核状态为 INCOMPLETE

**新逻辑**（独立评估式审核）：
- 审核 Design Spec 本身的质量——需求完整性、业务规则完整性、工作流完整性、技术可行性、可验证性等
- 没有上游对比参照，审核员基于自身专业判断来评估
- 不再因缺少上游文档而标记 INCOMPLETE

---

## 变更范围

### 第一层：路径与术语（机械替换）

| 当前 | 变更为 |
|------|--------|
| 主输入：`docs/superpowers/plans/<proposal>.md` | 主输入：`docs/superpowers/specs/<spec>.md` |
| 关联输入：`docs/superpowers/specs/<specification>.md` | 移除（无关联参考） |
| 术语 `Solution Proposal` | `Design Spec` |
| 术语 `Specification`（指上游文档） | 移除 |
| 术语 `proposal-stem` | `spec-stem` |
| 术语 `proposal owner` | `spec owner` |
| 输出路径 `docs/superpowers/reviews/<proposal-stem>/` | `docs/superpowers/reviews/<spec-stem>/` |

### 第二层：审核逻辑（核心变更）

#### Product Reviewer

**当前核心问题**：
> Does this Solution Proposal define a sufficiently complete and coherent product behavior to solve the problem described in the Specification?

**新核心问题**：
> Does this Design Spec define a sufficiently complete and coherent product behavior — with clear requirements, defined business rules, complete workflows, and no material ambiguities?

**当前概念模型**：
```
Specification
    ↓
What problem must be solved?
What outcome is required?
What rules and boundaries are implied?
    ↓
Solution Proposal
    ↓
What behavior is actually proposed?
What rules are actually defined?
What assumptions are being made?
```

**新概念模型**：
```
Design Spec
    ↓
What problem is being solved?
What outcome is required?
What rules and boundaries are defined?
What behavior is specified?
What assumptions are being made?
What is left undefined that the Design Spec's own goal statement implies should be defined?
```

**Design Spec 完整性要素清单**（CR-001 采纳：定义独立评估的锚定基准）：

Product Reviewer 应确认 Design Spec 包含以下要素类别。缺少某类别不自动构成 Finding，但如果该类别的缺失导致产品行为不可判定，则应记录为 Finding。

1. **问题定义** — 要解决什么问题，为谁解决
2. **目标成果** — 期望的成果和成功标准
3. **业务规则** — 关键业务规则和决策逻辑
4. **工作流** — 用户/系统工作流的完整路径（含异常和替代路径）
5. **状态与转换** — 关键实体的状态机和转换规则
6. **边界条件** — 重要边界和限制
7. **数据生命周期** — 数据的创建、更新、删除、归档行为
8. **假设声明** — 显式声明的关键假设

**Review Dimensions 调整**：

| 当前维度 | 变更 |
|----------|------|
| 1. Requirement Alignment — "Compare the Specification with the Solution Proposal" | 改为 "Requirement Completeness — 评估 Design Spec 是否定义了完整、一致、无歧义的需求" |
| 2-8 维度 | **维度名称和检查项保持不变，但认知方法从"对比 Specification 发现差距"调整为"独立评估 Design Spec 自身完整性"**，需为每个维度重新定义"完整"的判定标准（CR-002 采纳：修正"不变的部分"声明） |

**Review Inputs 调整**：
- 移除 "Source Specification"
- 只保留 "Design Spec"
- 支撑上下文保持不变

**Completion Criteria 调整**：
- 移除 "the complete Specification has been read"
- 改为 "the complete Design Spec has been read"
- 新增完成标准："审核员已评估 Design Spec 显式或隐式承诺的所有行为，且未将审核扩展到 Design Spec 未引用或暗示的行为。"（CR-002 采纳）

#### System Critic

**当前核心问题**：
> Does this Solution Proposal remain correct, reliable, secure, operable, and maintainable when its assumptions are violated?

**新核心问题**（基本不变，仅术语调整）：
> Does this Design Spec remain correct, reliable, secure, operable, and maintainable when its assumptions are violated?

**Review Inputs 调整**：
- 移除 "Source Specification"
- 只保留 "Design Spec"

**Completion Criteria 调整**：
- 移除 "the complete Specification has been read"
- 改为 "the complete Design Spec has been read"

#### Test Designer

**当前核心问题**：
> Can an independent tester objectively determine whether the Solution Proposal is correct?

**新核心问题**（基本不变，仅术语调整）：
> Can an independent tester objectively determine whether the Design Spec is correct?

**Review Inputs 调整**：
- 移除 "Source Specification"
- 只保留 "Design Spec"

**Completion Criteria 调整**：
- 移除 "the complete Specification has been read"
- 改为 "the complete Design Spec has been read"

### 第三层：协议与模板（适配调整）

#### review-orchestrator-protocol.md

**移除**：
- Section 1 中 "Specification Lookup" 和 "Hard Rule" 部分 — 不再需要从 spec stem 查找 specification，不再因缺少 specification 而标记 INCOMPLETE

**保留并迁移**（CR-005 采纳）：
- Section 1 中的 "Stem Extraction" 算法迁移到 SKILL.md 的 Output 章节（或 review-orchestrator-protocol.md 的新章节 "Output Path Determination"）

**新增/修改**：
- Phase 1 简化：直接读取用户指定的 Design Spec 路径，无需查找关联文件
- Design Spec 文件可用性检查：如果 Design Spec 不存在或无法读取，技能应报错终止（CR-003 采纳）
- Subagent Prompt 模板：移除 "Specification: <SPEC_PATH>" 行，只保留 "Design Spec: <SPEC_PATH>"
- MISSING 审核的硬性规则重新定义：仅当 subagent 审核输出缺失时触发（CR-003 采纳）
- 格式验证清单更新：将 "Specification path is present" 替换为 "Design Spec path is present"（CR-003 采纳）

#### SKILL.md

**Inputs 部分重写**：
```text
The primary input is:

docs/superpowers/specs/<spec>.md
```

**Conceptual Model 重写**：
```text
Design Spec
    ↓
Independent Multi-Perspective Review (3 subagents in parallel)
    ↓
Finding Consolidation (main agent)
    ↓
Decision (by spec owner via superpowers)
    ↓
Spec Revision (outside this skill's scope)
```

**Phase 1 简化**：
1. Read the Design Spec path from user input
2. If the Design Spec file does not exist or cannot be read, report error and stop
3. Read the complete Design Spec
4. Construct an internal model of the problem, desired outcome, boundaries, and assumptions
5. Record Consolidator Predispositions
6. Determine the output directory and review round number by reading the existing index.md (if any)
7. If a review round already exists for today's date, warn the user

**Stem Extraction 算法迁移到此处**（CR-005 采纳）：
```text
Given a spec filename, extract the stem:

Input:  2026-07-19-customer-operation.md
Step 1: Remove .md extension → 2026-07-19-customer-operation
Step 2: Remove YYYY-MM-DD- prefix → customer-operation
Result: customer-operation
```

**移除**：
- "If no specification is found, the review proceeds but the final review state must be INCOMPLETE"
- "Locate the associated Specification using the stem extraction algorithm"

**INCOMPLETE 状态触发条件完整枚举**（CR-003 采纳）：
- 任一 subagent 审核输出 MISSING
- Source Finding Integrity Check 失败

#### 所有模板

**Review Metadata 调整**：
- 移除 `### Specification` 字段
- `### Solution Proposal` → `### Design Spec`

**Source References 调整**：
- 移除 `#### Specification References` 子节
- `#### Solution Proposal References` → `#### Design Spec References`

#### finding-protocol.md

- "explicit text in the Specification" → "explicit text in the Design Spec"
- "explicit text in the Solution Proposal" → "explicit text in the Design Spec"
- Location 描述中 "Specification or Solution Proposal" → "Design Spec"

#### consolidation-protocol.md

- Input Contract 移除 "Original Specification"
- 示例路径调整
- 术语统一
- 修复已有残留不一致：Section 4 的 "RV means Review Finding" → "CR means Consolidated Review Finding"（CR-004 采纳）

#### decision-protocol.md

- 术语统一：Solution Proposal → Design Spec，Specification owner → Spec owner

#### CLAUDE.md

- 概念模型更新
- 输入路径更新
- 移除"如果找不到 Specification 则 INCOMPLETE"的规则
- 更新已解决的不一致列表（新增本次变更）

---

## 不变的部分

- 三角色并行独立审核架构
- Finding 结构（ID 前缀 PR/SC/TD、严重度 P0/P1/P2、证据等级、置信度）
- 合并协议的核心逻辑（去重规则、关系分类、冲突处理）
- 决策协议的核心逻辑（状态枚举、决策结构、最终审核状态）
- 输出目录结构 `docs/superpowers/reviews/<spec-stem>/YYYY-MM-DD-review-NNN/`
- 轮次管理和 index.md 跨轮次追踪
- 完整性校验（Source Finding Integrity Check）
- Subagent 上下文隔离
- Consolidator Predispositions 记录
- 严重度变更理由为强制字段

注意：Dimensions 2-8 的维度名称和检查项不变，但认知方法从"对比 Specification 发现差距"调整为"独立评估 Design Spec 自身完整性"——这不是措辞变更，而是逻辑变更（CR-002 修正）。

---

## 实施顺序

1. SKILL.md — 核心入口文件，先改（含 Stem Extraction 算法迁移）
2. review-orchestrator-protocol.md — 编排协议（移除 Specification Lookup，保留 Stem Extraction 迁移后的引用）
3. roles/product-reviewer.md — Product Reviewer 逻辑变更最大（含完整性要素清单、范围边界、完成标准）
4. roles/system-critic.md — 术语调整
5. roles/test-designer.md — 术语调整
6. protocols/finding-protocol.md — 术语统一
7. protocols/consolidation-protocol.md — 术语统一 + 修复 "RV means Review Finding" 残留
8. protocols/decision-protocol.md — 术语统一
9. templates/product-review.md — 模板调整
10. templates/system-review.md — 模板调整
11. templates/test-review.md — 模板调整
12. templates/consolidated-review.md — 模板调整
13. templates/index.md — 模板调整
14. CLAUDE.md — 项目文档更新
15. 验证步骤（CR-004 采纳）：术语扫描 + 引用完整性检查 + YAML 索引一致性

---

## 审核报告决策记录

| CR-ID | 原始严重度 | 决策 | 理由 |
|-------|-----------|------|------|
| CR-001 | P0→P1 | 部分采纳 | "需要锚定基准"成立，采纳完整性清单方案；P0 不成立（对比模式同样不可重复），不采纳 Specification 降级方案 |
| CR-002 | P1 | 采纳 | "不变的部分"声明不准确 + 审核范围无边界 |
| CR-003 | P1 | 采纳 | MISSING/INCOMPLETE 语义矛盾真实存在 |
| CR-004 | P1 | 采纳 | 验证步骤缺失 + 已有残留不一致需修复 |
| CR-005 | P1 | 采纳 | Stem Extraction 算法需保留并迁移 |
| CR-006 | P1 | 不采纳 | 没有现有审核记录需要兼容 |
| CR-007 | P2 | 不采纳 | 自我参照风险是理论操作风险 |
