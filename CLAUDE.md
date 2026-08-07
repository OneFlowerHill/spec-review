# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个 **Claude Code Skill**（AI 审核技能），用于对 Design Spec（设计规格）进行结构化多视角独立审核。它不是可执行代码项目，而是一套由 Markdown 协议、角色定义和输出模板组成的方法论框架，供 Claude Code 的 skill 系统调用。

核心流程：Design Spec → 三角色 subagent 并行独立审核 → Finding 合并 → 决策（规格所有者） → 规格修订

## 目录结构与关键文件

```
SKILL.md                          # Skill 主定义（单一入口，4 Phase 流程，subagent 并行审核）
roles/
  product-reviewer.md             # 产品审核员角色（product-reviewer）
  system-critic.md                # 系统批评员角色（system-critic）
  test-designer.md                # 测试设计师角色（test-designer，TD-001 + Finding Type）
protocols/
  finding-protocol.md             # 发现协议——单个 Finding 的结构与质量标准
  consolidation-protocol.md       # 合并协议——跨审核员 Finding 的去重/关联/合并规则（CR-ID）
  decision-protocol.md            # 决策协议——Finding 的最终处置（权威状态枚举来源，CR-ID）
  review-orchestrator-protocol.md # 编排协议——主 agent 的调度、失败处理、完整性校验、交接
templates/
  product-review.md               # 产品审核输出模板（PR-001 格式）
  system-review.md                # 系统审核输出模板（SC-001 格式）
  test-review.md                  # 测试审核输出模板（TD-001 统一格式 + Finding Type）
  consolidated-review.md          # 合并审核输出模板（CR-001 格式 + Superpowers Instructions）
  index.md                        # 跨轮次汇总模板（Review Rounds + Finding Tracking + Trend）
references/
  common.md                      # 共享权威定义源（严重度/证据等级/Finding 字段/独立评审/三角色边界/不变量清单）
```

## 架构：三角色独立审核 + 合并 + 决策

### 审核流程（4 个 Phase）

1. **Context Acquisition** — 读取 Design Spec + 相关代码/测试/架构；记录 Consolidator Predispositions
2. **Independent Reviews** — 三个 subagent 并行审核，上下文隔离，互不阅读对方结论
3. **Finding Consolidation** — 合并三个审核的 Finding，去重/关联/识别冲突；执行 Source Finding 完整性校验
4. **Output + Handoff** — 写入审核文件 + 更新 index.md；生成 Superpowers Instructions，等待规格所有者做决策

### 角色边界（严格隔离）

- **Product Reviewer**：评估"需求是否完整一致"——需求完整性、业务规则、工作流完整性、滥用场景
- **System Critic**：评估"技术方案是否自洽可靠"——架构、数据完整性、故障恢复、安全边界、可观测性
- **Test Designer**：评估"行为是否可客观验证"——验收标准、可观测结果、验证缺口、生产盲点

每个角色最多输出 5 个 Finding，使用各自的本地 ID 前缀（PR-/SC-/TD-）。

三角色边界的完整契约（含审查维度清单）见 `references/common.md` §5。

### Finding 严重等级

权威定义（P0/P1/P2：阻断性缺陷 / 重要缺陷 / 次要问题）见 `references/common.md` §1。

### Finding 证据等级

四字面量与各角色可输出子集的权威定义见 `references/common.md` §2。

### 合并协议核心规则

- 不按关键词/组件/后果/严重度合并——只按"同一根本问题"合并
- 不压制少数派 Finding——单一审核员的发现不能因其他审核员未发现而丢弃
- 不在合并阶段做最终决策（接受/拒绝属于 Decision Protocol）
- 冲突必须显式记录，不能静默选择一方
- Finding 关系分类：DUPLICATE / SAME_ROOT_CAUSE / RELATED / INDEPENDENT / CONTRADICTORY / SUBSET / CONSEQUENCE

### 决策状态

每个 Consolidated Finding 最终必须进入以下状态之一：PENDING_DECISION / ACCEPTED / REJECTED / DEFERRED / PARTIALLY_ACCEPTED / DUPLICATE / INVALIDATED

最终审核状态：BLOCKED / CHANGES_REQUIRED / CONDITIONAL_APPROVAL / APPROVED / INCOMPLETE

## 已解决的不一致（v2 已修复）

1. ~~Finding ID 前缀冲突~~ → 统一为 CR-001，所有协议文件 RV→CR 已替换
2. ~~决策状态枚举冲突~~ → 统一为 decision-protocol.md 枚举，废弃 OPEN/READY_FOR_DECISION/RESOLVED/SUPERSEDED
3. ~~Test Designer 输出格式~~ → 统一为 TD-001 + Finding Type 字段，与 PR/SC 格式兼容
4. ~~SKILL.md 缺少 YAML frontmatter~~ → 已添加 name: spec-review
5. ~~Consolidator 角色文件缺失~~ → 主 agent 执行合并 + review-orchestrator-protocol.md 定义编排规则
6. ~~review-orchestrator 协议缺失~~ → 已创建 protocols/review-orchestrator-protocol.md
7. ~~审核对象路径偏差~~ → 主输入从 plans/ 迁移到 specs/，审核模式从对比式改为独立评估式
8. ~~consolidation-protocol.md RV 残留~~ → "RV means Review Finding" 已修复为 "CR means Consolidated Review Finding"

## 当前约束（修改时注意）

1. **CR-ID 是唯一的合并 Finding 标识** — 所有文件必须使用 CR-001 格式，不得使用 RV-001
2. **决策状态必须使用 decision-protocol 枚举** — PENDING_DECISION/ACCEPTED/REJECTED/DEFERRED/PARTIALLY_ACCEPTED/DUPLICATE/INVALIDATED
3. **Test Designer Finding 必须包含 Finding Type** — ACCEPTANCE_TEST/UNTESTABLE_REQUIREMENT/BLIND_SPOT
4. **MISSING 审核的硬性规则** — 仅当 subagent 审核输出缺失时触发 MISSING；Design Spec 文件缺失时报错终止
5. **合并后必须执行完整性校验** — Source Finding 总数 = 合并引用 + 未合并 + 重复/取代记录
6. **INCOMPLETE 状态触发条件** — MISSING 审核 + 完整性校验失败

## 审核输出路径

每次审核创建新的 Review Round，不覆盖之前的轮次：

```
docs/superpowers/reviews/<spec-stem>/
├── index.md                          # 跨轮次汇总（累积更新）
└── YYYY-MM-DD-review-NNN/
    ├── product-review.md
    ├── system-review.md
    ├── test-review.md
    └── consolidated-review.md
```

`<spec-stem>` 从规格文件名提取：移除 `YYYY-MM-DD-` 前缀和 `.md` 后缀。

输入来自：`docs/superpowers/specs/<spec>.md`

## 修改原则

- **不修改 Design Spec**——审核只产出 Finding，不直接改规格
- **不跨角色阅读**——独立审核阶段，角色间互不参考
- **不静默丢弃 Finding**——每个发现都必须有明确的处置记录
- **不将假设升级为事实**——证据等级必须严格区分
- **不在合并阶段做决策**——合并只组织问题，不做接受/拒绝判断
- **模板末尾的 Machine-Readable YAML 索引必须与详细内容保持同步**
- **Subagent 提示词不得包含主代理的分析**——只传递路径信息，禁止注入理解或假设
- **合并后必须记录 Consolidator Predispositions**——使认知偏差可审计
- **完整性校验失败时最终状态必须为 INCOMPLETE**——防止不完整审核被当作完整审核使用
- **严重度变更理由为强制字段**——必须引用具体源 Finding 证据，不得使用泛化推理
